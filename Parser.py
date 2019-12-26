'''
定义parser
算符优先算法
递归下降算法
'''
from prettytable import PrettyTable
from Struct import *
import random
from OPGrammar import *
from LexAnalyzer import *




class OperatorPrecedenceParser():

    def __init__(self, grammar:OPGrammar, symbols:[Symbol], tokens:[Token]=None):
        self.grammar = grammar
        self.tokens = tokens
        self.symbols = symbols
        self.__tree_root = None
        self.__next_label = len(tokens)
        self.__tree_nodes = {}

    def get_tree_root(self):
        if self.__tree_root:
            return self.__tree_root
        raise RuntimeError('Error tree_root is None! Consider parser first!')

    def get_tree_nodes(self):
        if self.__tree_nodes:
            return self.__tree_nodes
        raise RuntimeError('Error tree_nodes dict is None! Consider parser first!')

    def __generate_next_node(self, name:str=None, action:int=None, token:Token=None):
        if token:
            temp = TreeNode(token=token)
            self.__tree_nodes[temp.label] = temp
        elif name and action:
            temp = TreeNode(name=name, label=self.__next_label, action=action)
            self.__next_label += 1
            self.__tree_nodes[temp.label] = temp
        else:
            raise RuntimeError('Error in generate_next_node, must give token or name!')
        return temp

    def __get_priority_table_index(self, name:str)->int:
        if self.__is_symbol(name)[0]:
            index = self.grammar.priority_table.terminal_index['i']
        elif name in self.grammar.terminals:
            index = self.grammar.priority_table.terminal_index[name]
        else:
            raise RuntimeError('Error could not get index of priority_table', name)
        # print('name, index', name, index)
        return index

    def __is_symbol(self, name:str)->(bool, int):
        for symbol in self.symbols:
            if symbol.name == name:
                return (True, symbol.code)
        return (False, None)

    def __is_token(self, name:str)->(bool, str):
        for token in self.tokens:
            if token.name == name:
                return (True, token.type)
        return (False, None)

    def __read_tokens(self):
        file = []
        for token in self.tokens:
            file.append(token.name)
        return file

    def __read_reduction_file(self, reduction_file_path = 'static/test-StateG.LLang'):
        print('Info 待算符优先文法归约格式化文件为', reduction_file_path)
        with open(reduction_file_path, 'r', encoding='utf-8') as file:
            temp = file.readlines()
        file = []
        for line in temp:
            line = line.strip('\n')
            line = line.strip('\r')
            line = line.strip('\t')
            line = line.strip(' ')
            line = line.split(' ')
            for word in line:
                if word not in self.grammar.terminals and word not in self.grammar.non_terminals and not self.__is_symbol(word)[0]:
                    raise RuntimeError('Error reduction file has unknown chars!', word)
                file.append(word)
        return file

    def __check_reduction(self, wait_reduct:[], wait_nodes:[TreeNode]):
        sentences:dict = self.grammar.sentences
        for key, line in sentences.items():
            left = line[0]
            candidate_right = [line[1]]
            for one in candidate_right:
                i = 0
                j = 0
                while i < len(one) and j < len(wait_reduct):
                    if one[i] in self.grammar.non_terminals:
                        if wait_reduct[j] in self.grammar.non_terminals:
                            i += 1
                            j += 1
                        else:
                            break
                    elif one[i] in self.grammar.terminals:
                        if wait_reduct[j] == one[i]:
                            i += 1
                            j += 1
                        elif one[i] == 'i':
                            judge = self.__is_symbol(wait_reduct[j])
                            if judge[0]: # a\b\c\... == i
                                if judge[1] == Code.TAG or judge[1] == Code.REAL or judge[1] == Code.INT:
                                # print(judge)
                                    i += 1
                                    j += 1
                            else:
                                break
                        else:
                            break
                    else:
                        break
                if i == len(one) and j == len(wait_reduct):
                    parent = self.__generate_next_node(name=left, action=key)
                    if left == self.grammar.start:
                        self.__tree_root = parent
                    for node in wait_nodes:
                        parent.set_child(node)
                        node.set_parent(parent)
                    return left, parent
        raise RuntimeError('Error could not find a appropriate product! Wait reduction phrase is', wait_reduct)

    def reduction(self, is_show=False, is_single_reduction=False, reduction_file_path=None):
        stack = []
        stack_tree_nodes = []
        if reduction_file_path:
            input_chars = self.__read_reduction_file(reduction_file_path)
        else:
            input_chars = self.__read_tokens()
        stack.append('#')
        stack_tree_nodes.append('#')
        input_chars.append('#')
        cursor = 0
        top = 0 # stack_top
        step = 0
        table = PrettyTable()
        table.title = 'Reduction Process'
        table.field_names = ['step', 'stack', 'input_chars']
        if is_single_reduction:
            print('Info 已开启 归约单非产生式')
            table.title += '(归约单非产生式, step*)'
        # while input_chars[cursor] != '#':
        # while (len(stack) != 2 or stack[1] not in self.grammar.non_terminals) or cursor < len(input_chars):
        while True:
            if input_chars[cursor] == '#' and len(stack) == 2 and stack[1] in self.grammar.non_terminals:
                break
            step += 1
            table.add_row([step, stack.copy(), input_chars[cursor:].copy()])
            if stack[top] not in self.grammar.terminals and not self.__is_symbol(stack[top])[0]:
                j = top - 1
            else:
                j = top
            while True:
                row = self.__get_priority_table_index(stack[j])
                col = self.__get_priority_table_index(input_chars[cursor])
                # print(row, col)
                # print(self.priority_table.value_table[row])
                # print(self.grammar.priority_table.value_table[row][col])
                if self.grammar.priority_table.value_table[row][col] == '<' or self.grammar.priority_table.value_table[row][col] == '=': # 移入
                    stack.append(input_chars[cursor])
                    stack_tree_nodes.append(self.__generate_next_node(token=self.tokens[cursor])) #增加TreeNode
                    top += 1
                    cursor += 1
                    break

                elif self.grammar.priority_table.value_table[row][col] == '>': # 归约
                    while j > 0: # find the head of the most left terminal
                        temp = j
                        if stack[j-1] not in self.grammar.terminals and not self.__is_symbol(stack[j-1])[0]:
                            j -= 2
                            if j < 0:
                                raise RuntimeError('Error in find the head of the most left terminal! index is', j)
                        else:
                            j -= 1
                        row = self.__get_priority_table_index(stack[j])
                        col = self.__get_priority_table_index(stack[temp])
                        if self.grammar.priority_table.value_table[row][col] == '<':
                            break
                    # reduct from stack[j+1] to stack[top]
                    wait_reduction = stack[j+1:]
                    wait_reduction_tree_nodes = stack_tree_nodes[j+1:]
                    reduct_ans, reduct_ans_node = self.__check_reduction(wait_reduction, wait_reduction_tree_nodes)
                    # print('ruduct ans', reduct_ans)
                    if reduct_ans and reduct_ans_node:
                        stack = stack[:j+1]
                        stack_tree_nodes = stack_tree_nodes[:j+1]
                        stack.append(reduct_ans)
                        stack_tree_nodes.append(reduct_ans_node)
                        top = j+1
                        break
                elif 'nil' in stack:
                    count = 0
                    stack.remove('nil')
                    for i in range(len(stack_tree_nodes)):
                        if stack_tree_nodes[i].name == 'nil':
                            stack_tree_nodes.pop(i)
                            count += 1
                    top -= count
                    break

                else: # 报错
                    step += 1
                    table.add_row([step, stack.copy(), input_chars[cursor:].copy()])
                    print(table)
                    # relation = self.grammar.priority_table.value_table[row][col]
                    # print(stack)
                    # print(input_chars[cursor:])
                    raise RuntimeError('Error invalid reduction! Could not find a precedence, stack, input_chars', stack, '\n\r', input_chars[cursor:])
        if stack[top] not in self.grammar.non_terminals or len(stack) != 2:
            raise RuntimeError('Error, input_chars is empty, but stack is invalid, stack is', stack)

        step += 1 # success
        table.add_row([step, stack, input_chars[cursor:]])
        if is_single_reduction:
            while stack[top] != self.grammar.start:
                step += 1
                reduct_ans = self.__check_reduction(stack[top])
                if reduct_ans:
                    stack = stack[:top]
                    stack.append(reduct_ans)
                    table.add_row([str(step)+'*', stack.copy(), input_chars[cursor:]])

        print('Info 归约完成，归约结果为', stack[top])
        # print(self.__tree_root)
        if is_show:
            print(table)




class RecursiveDescentParser():
    def __init__(self, grammar: OPGrammar, symbols: [Symbol], tokens: [Token] = None, reduction_file_path: str = None):
        self.grammar = grammar
        if reduction_file_path:
            self.reduction_file_path = reduction_file_path
        else:
            self.reduction_file_path = 'static/test-StateG.LLang'
        self.tokens = tokens
        self.symbols = symbols
        self.input_cursor = 0

    def L_begin(self, next_char:str):
        if next_char == 'S':
            pass


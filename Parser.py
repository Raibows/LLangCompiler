from prettytable import PrettyTable
from Struct import PriorityTable, Equ, Token, Symbol, Code
from Grammar import *
from LexAnalyzer import *




class OperatorPrecedenceParser():
    def __init__(self, grammar:Grammar, symbols:[Symbol], tokens:[Token]=None, reduction_file_path:str=None):
        self.grammar = grammar
        if reduction_file_path:
            self.reduction_file_path = reduction_file_path
        else:
            self.reduction_file_path = 'static/test.reduct'

        self.tokens = tokens
        self.symbols = symbols






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

    def __read_reduction_file(self):
        print('Info 待算符优先文法归约文件为', self.reduction_file_path)
        with open(self.reduction_file_path, 'r', encoding='utf-8') as file:
            temp = file.readlines()
        file = []
        for line in temp:
            line = line.strip('\n')
            line = line.strip('\r')
            line = line.strip('\t')
            line = line.strip(' ')
            line = line.split(' ')
            for word in line:
                if word not in self.grammar.terminals and word not in self.grammar.v_terminals and not self.__is_symbol(word)[0]:
                    raise RuntimeError('Error reduction file has unknown chars!', word)
                file.append(word)
        return file

    def __check_reduction(self, wait_reduct:[])->str:
        for line in self.grammar.sentences:
            left = line[0]
            candidate_right = line[1]
            for one in candidate_right:
                i = 0
                j = 0
                while i < len(one) and j < len(wait_reduct):
                    if one[i] in self.grammar.v_terminals:
                        if wait_reduct[j] in self.grammar.v_terminals:
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
                            if judge[0] and judge[1] == Code.TAG: # a\b\c\... == i
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
                    return left
        raise RuntimeError('Error could not find a appropriate product! Wait reduction phrase is', wait_reduct)

    def reduction(self, is_show=False):
        stack = []
        input_chars = self.__read_reduction_file()
        stack.append('#')
        input_chars.append('#')
        cursor = 0
        top = 0 # stack_top
        step = 0
        table = PrettyTable()
        table.title = 'Reduction Process'
        table.field_names = ['step', 'stack', 'input_chars']
        # while input_chars[cursor] != '#':
        while len(stack) != 2 or stack[1] not in self.grammar.v_terminals:
            step += 1
            table.add_row([step, stack.copy(), input_chars[cursor:]])
            if stack[top] not in self.grammar.terminals and not self.__is_symbol(stack[top])[0]:
                j = top - 1
            else:
                j = top
            while True:
                row = self.__get_priority_table_index(stack[j])
                col = self.__get_priority_table_index(input_chars[cursor])
                # print(row, col)
                # print(self.priority_table.value_table[row])
                # print(self.priority_table.value_table[row][col])
                if self.grammar.priority_table.value_table[row][col] == '<' or self.grammar.priority_table.value_table[row][col] == '=': # 移入
                    stack.append(input_chars[cursor])
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
                    reduct_ans = self.__check_reduction(wait_reduction)
                    # print('ruduct ans', reduct_ans)
                    if reduct_ans:
                        stack = stack[:j+1]
                        stack.append(reduct_ans)
                        top = j+1
                        break

                else: # 报错
                    relation = self.grammar.priority_table.value_table[row][col]
                    raise RuntimeError('Error invalid reduction! stack, input_chars, top, cursor, row, col, relation', stack, input_chars, top, cursor, row, col, relation)
        if stack[top] not in self.grammar.v_terminals or len(stack) != 2:
            raise RuntimeError('Error, input_chars is empty, but stack is invalid, stack is', stack)
        print('Info 归约完成，归约结果为', stack[top])
        table.add_row([step, stack, input_chars[cursor:]])
        if is_show:
            print(table)









class RecursiveDecline():
    def __init__(self):
        pass

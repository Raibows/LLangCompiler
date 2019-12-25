from prettytable import PrettyTable
from Struct import PriorityTable, Equ, Token, Symbol, Code








class OperatorPrecedenceParser():
    def __init__(self, grammar=None, terminals=None, v_terminals=None, reduction_file_path:str=None, tokens:[Token]=None, symbols:[Symbol]=None):
        if grammar:
            self.grammar = grammar
        else:
            self.grammar = [
                'A → # B #',
                'B → S ; S',
                'S → var D | nil',
                'D → L : K ; | L : K ; D',
                'L → i , L | i',
                'K → integer | bool | real',
            ]
        if terminals:
            self.terminals = terminals
        else:
            self.terminals = ['#', 'var', ':', ';', 'i', ',', 'integer', 'bool', 'real']
        if v_terminals:
            self.v_terminals = v_terminals
        else:
            self.v_terminals = ['A', 'S', 'D', 'L', 'K', 'B']

        if reduction_file_path:
            self.reduction_file_path = reduction_file_path
        else:
            self.reduction_file_path = './test.reduct'

        if tokens:
            self.tokens = tokens
        else:
            self.tokens = []

        if symbols:
            self.symbols = symbols
        else:
            self.symbols = []

        self.grammar_FIRSTVT = {}
        self.grammar_LASTVT = {}
        self.sentences = []
        self.priority_table = PriorityTable() # 2 dims
        '''
        sentences = [
                        ['S ', [' var D ', ' nil']],
                        ['D ', [' L : K ; ', ' L : K ; D']],
                        ['L ', [' i , L ', ' i']],
                        ['K ', [' integer ', ' bool ', ' real']],
                    ]
        '''


    def __get_priority_table_index(self, name:str)->int:
        if self.__is_symbol(name)[0]:
            index = self.priority_table.terminal_index['i']
        elif name in self.terminals:
            index = self.priority_table.terminal_index[name]
        else:
            raise RuntimeError('Error could not get index of priority_table', name)
        # print('name, index', name, index)
        return index


    def __set_sentences(self):
        for line in self.grammar:
            sentence = line.split('→')
            sentence[0] = sentence[0].strip()
            sentence[1] = sentence[1].split('|')
            for i in range(len(sentence[1])):
                sentence[1][i] = sentence[1][i].strip()
                sentence[1][i] = sentence[1][i].split(' ')
            self.sentences.append(sentence)
        # print(self.sentences)


    def __transfer(self, src:str, dst:str, flag='firstvt'):
        # print('transfer', flag, src, dst)
        change = False
        if flag == 'firstvt':
            for ch in self.grammar_FIRSTVT[src]:
                if ch not in self.grammar_FIRSTVT[dst]:
                    self.grammar_FIRSTVT[dst].append(ch)
                    change = True
        elif flag == 'lastvt':
            for ch in self.grammar_LASTVT[src]:
                if ch not in self.grammar_LASTVT[dst]:
                    self.grammar_LASTVT[dst].append(ch)
                    change = True
        else:
            raise RuntimeError('Grammar transfer flag is invalid !', flag)
        return change

    def set_grammar_FIRSTVT_LASTVT(self):
        if not self.sentences:
            self.__set_sentences()
        if (not self.grammar_FIRSTVT) or (not self.grammar_LASTVT):
            for v in self.v_terminals:
                self.grammar_FIRSTVT[v] = []
                self.grammar_LASTVT[v] = []
        while True:
            change_flag = False
            for line in self.sentences:
                for one in line[1]:
                    ch = one[0] #firstvt
                    if ch in self.terminals and ch not in self.grammar_FIRSTVT[line[0]]: # A -> a..
                        self.grammar_FIRSTVT[line[0]].append(ch)
                        change_flag = True
                    elif ch in self.v_terminals: # 'A -> Q...'
                        if len(one) > 1:  # A -> Qa..
                            if one[1] in self.terminals and one[1] not in self.grammar_FIRSTVT[line[0]]:
                                self.grammar_FIRSTVT[line[0]].append(one[1])
                                change_flag = True
                        change_flag = (change_flag or self.__transfer(ch, line[0], flag='firstvt')) # A -> Q..

                    ch = one[-1] #lastvt
                    if ch in self.terminals and ch not in self.grammar_LASTVT[line[0]]: # A -> ...a
                        self.grammar_LASTVT[line[0]].append(ch)
                        change_flag = True

                    elif ch in self.v_terminals: # A -> ...Q
                        if len(one) > 1: # A -> ...aQ
                            if one[-2] in self.terminals and one[-2] not in self.grammar_LASTVT[line[0]]:
                                self.grammar_LASTVT[line[0]].append(one[-2])
                                change_flag = True
                        change_flag = (change_flag or self.__transfer(ch, line[0], flag='lastvt')) # A -> ...Q

            if not change_flag:
                break

    def set_grammar_priority_table(self):
        if not (self.grammar_FIRSTVT and self.grammar_LASTVT):
            self.set_grammar_FIRSTVT_LASTVT()

        terminals_num = len(self.terminals)
        for i, t in enumerate(self.terminals): # init priority table
            self.priority_table.terminal_index[t] = i
            self.priority_table.value_table.append([' ' for _ in range(terminals_num)])

        for line in self.sentences:
            left = line[0]
            right = line[1]
            for one in right: # one=每一个候选式
                one_len = len(one)
                for i in range(one_len): # 遍历候选式中的每个符号
                    if one[i] in self.terminals: # one[i] is terminal
                        if i+1 < one_len and one[i+1] in self.terminals: # one[i] = one[i+1]
                            row = self.priority_table.terminal_index[one[i]]
                            col = self.priority_table.terminal_index[one[i+1]]
                            self.priority_table.value_table[row][col] = '='

                        if i+2 < one_len and one[i+1] in self.v_terminals and one[i+2] in self.terminals: # one[i] = one[i+2]
                            row = self.priority_table.terminal_index[one[i]]
                            col = self.priority_table.terminal_index[one[i+2]]
                            self.priority_table.value_table[row][col] = '='

                        if i+1 < one_len and one[i+1] in self.v_terminals: # ...aP... a < FIRSTVT(p)
                            row = self.priority_table.terminal_index[one[i]]
                            for first in self.grammar_FIRSTVT[one[i + 1]]:
                                col = self.priority_table.terminal_index[first]
                                self.priority_table.value_table[row][col] = '<'

                    elif one[i] in self.v_terminals: # one[i] is von terminals
                        if i+1 < one_len and one[i+1] in self.terminals: # ...pa.... LASTVT(P) > a
                            col = self.priority_table.terminal_index[one[i+1]]
                            for last in self.grammar_LASTVT[one[i]]:
                                row = self.priority_table.terminal_index[last]
                                self.priority_table.value_table[row][col] = '>'

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
        print('待算符优先文法归约文件为', self.reduction_file_path)
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
                if word not in self.terminals and word not in self.v_terminals and not self.__is_symbol(word)[0]:
                    raise RuntimeError('Error reduction file has unknown chars!')
                file.append(word)
        return file

    def __check_reduction(self, wait_reduct:[])->str:
        for line in self.sentences:
            left = line[0]
            candidate_right = line[1]
            for one in candidate_right:
                i = 0
                j = 0
                while i < len(one) and j < len(wait_reduct):
                    if one[i] in self.v_terminals:
                        if wait_reduct[j] in self.v_terminals:
                            i += 1
                            j += 1
                        else:
                            break
                    elif one[i] in self.terminals:
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
        table = PrettyTable(['step', 'stack', 'input_chars'])
        # while input_chars[cursor] != '#':
        while len(stack) != 2 or stack[1] not in self.v_terminals:
            step += 1
            table.add_row([step, stack.copy(), input_chars[cursor:]])
            if stack[top] not in self.terminals and not self.__is_symbol(stack[top])[0]:
                j = top - 1
            else:
                j = top
            while True:
                row = self.__get_priority_table_index(stack[j])
                col = self.__get_priority_table_index(input_chars[cursor])
                # print(row, col)
                # print(self.priority_table.value_table[row])
                # print(self.priority_table.value_table[row][col])
                if self.priority_table.value_table[row][col] == '<' or self.priority_table.value_table[row][col] == '=': # 移入
                    stack.append(input_chars[cursor])
                    top += 1
                    cursor += 1
                    break

                elif self.priority_table.value_table[row][col] == '>': # 归约
                    while j > 0: # find the head of the most left terminal
                        temp = j
                        if stack[j-1] not in self.terminals and not self.__is_symbol(stack[j-1])[0]:
                            j -= 2
                            if j < 0:
                                raise RuntimeError('Error in find the head of the most left terminal! index is', j)
                        else:
                            j -= 1
                        row = self.__get_priority_table_index(stack[j])
                        col = self.__get_priority_table_index(stack[temp])
                        if self.priority_table.value_table[row][col] == '<':
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
                    relation = self.priority_table.value_table[row][col]
                    raise RuntimeError('Error invalid reduction! stack, input_chars, top, cursor, row, col, relation', stack, input_chars, top, cursor, row, col, relation)
        if stack[top] not in self.v_terminals or len(stack) != 2:
            raise RuntimeError('Error, input_chars is empty, but stack is invalid, stack is', stack)
        print('归约完成，归约结果为', stack[top])
        table.add_row([step, stack, input_chars[cursor:]])
        if is_show:
            print(table)





    def show_FIRSTVT(self):
        print('grammar的FIRSTVT集合如下所示')
        if self.grammar_FIRSTVT:
            table = PrettyTable(['VT', 'FIRSTVT-SET'])
            for key in self.grammar_FIRSTVT.keys():
                table.add_row([key, self.grammar_FIRSTVT[key]])

            print(table)

    def show_LASTVT(self):
        print('grammar的LASTVT集合如下所示')
        if self.grammar_LASTVT:
            table = PrettyTable(['VT', 'LASTVT-SET'])
            for key in self.grammar_LASTVT.keys():
                table.add_row([key, self.grammar_LASTVT[key]])

            print(table)

    def show_priority_table(self):
        print('grammar的算符优先关系表如下')
        title = self.terminals.copy()
        title.insert(0, ' ')
        table = PrettyTable(title)
        for col, t in zip(self.priority_table.value_table, self.terminals):
            temp = col.copy()
            temp.insert(0, t)
            table.add_row(temp)
        print(table)

    def show_all(self):
        self.show_FIRSTVT()
        print()
        self.show_LASTVT()
        print()
        self.show_priority_table()
        print()



class RecursiveDecline():
    def __init__(self):
        pass

from Struct import *


class OPGrammar():
    def __init__(self, grammar):
        self.__grammar = grammar
        self.start = grammar.start
        self.grammar_name = grammar.name
        self.production = grammar.production
        self.terminals = grammar.terminals
        self.v_terminals = grammar.v_terminals
        self.sentences = []
        self.FIRSTVT = {}
        self.LASTVT = {}
        self.priority_table = PriorityTable()  # 2 dims
        '''
        EXAMPLE
        A -> a;B | c
        B -> d | e : f
        sentences = [
            [A, [a, ;, B], [c]],
            [B, [d], [e, :, f]],    
            ]
        '''
        self.__set_sentences()
        if self.__check_production():
            print('Info 检查完成！该文法可以使用算符优先算法', self.grammar_name)
            self.__set_FIRSTVT_LASTVT()
            self.__set_grammar_priority_table()
        else:
            raise RuntimeError('Error this production has like ...QR... format', self.grammar_name)

    def __check_production(self)->bool:  # 算符优先算法不能含有...QR...
        for line in self.sentences:
            right = line[1]
            for one in right:
                i = 0
                while i+1 < len(one):
                    if one[i] in self.v_terminals and one[i+1] in self.v_terminals:
                        return False
                    i += 1
        return True

    def __set_sentences(self):
        # first add A -> # S #
        self.production.insert(0, f'W -> # {self.start} #')
        self.terminals.insert(0, '#')
        self.v_terminals.insert(0, 'W')

        for line in self.production:
            sentence = line.split('->')
            sentence[0] = sentence[0].strip()
            sentence[1] = sentence[1].split('|')
            for i in range(len(sentence[1])):
                sentence[1][i] = sentence[1][i].strip()
                sentence[1][i] = sentence[1][i].split(' ')
                for j in range(len(sentence[1][i])):
                    sentence[1][i][j] = sentence[1][i][j].strip()
            self.sentences.append(sentence)

    def __transfer(self, src:str, dst:str, flag='firstvt'):
        # print('transfer', flag, src, dst)
        change = False
        if flag == 'firstvt':
            for ch in self.FIRSTVT[src]:
                if ch not in self.FIRSTVT[dst]:
                    self.FIRSTVT[dst].append(ch)
                    change = True
        elif flag == 'lastvt':
            for ch in self.LASTVT[src]:
                if ch not in self.LASTVT[dst]:
                    self.LASTVT[dst].append(ch)
                    change = True
        else:
            raise RuntimeError('Grammar transfer flag is invalid !', flag)
        return change

    def __set_FIRSTVT_LASTVT(self):
        if not self.sentences:
            self.__set_sentences()
        if (not self.FIRSTVT) or (not self.LASTVT):
            for v in self.v_terminals:
                self.FIRSTVT[v] = []
                self.LASTVT[v] = []
        while True:
            change_flag = False
            for line in self.sentences:
                for one in line[1]:
                    ch = one[0] #firstvt
                    if ch in self.terminals and ch not in self.FIRSTVT[line[0]]: # A -> a..
                        self.FIRSTVT[line[0]].append(ch)
                        change_flag = True
                    elif ch in self.v_terminals: # 'A -> Q...'
                        if len(one) > 1:  # A -> Qa..
                            if one[1] in self.terminals and one[1] not in self.FIRSTVT[line[0]]:
                                self.FIRSTVT[line[0]].append(one[1])
                                change_flag = True
                        change_flag = (change_flag or self.__transfer(ch, line[0], flag='firstvt')) # A -> Q..

                    ch = one[-1] #lastvt
                    if ch in self.terminals and ch not in self.LASTVT[line[0]]: # A -> ...a
                        self.LASTVT[line[0]].append(ch)
                        change_flag = True

                    elif ch in self.v_terminals: # A -> ...Q
                        if len(one) > 1: # A -> ...aQ
                            if one[-2] in self.terminals and one[-2] not in self.LASTVT[line[0]]:
                                self.LASTVT[line[0]].append(one[-2])
                                change_flag = True
                        change_flag = (change_flag or self.__transfer(ch, line[0], flag='lastvt')) # A -> ...Q

            if not change_flag:
                break

    def __set_grammar_priority_table(self):
        if not (self.FIRSTVT and self.LASTVT):
            self.__set_FIRSTVT_LASTVT()

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
                            for first in self.FIRSTVT[one[i + 1]]:
                                col = self.priority_table.terminal_index[first]
                                self.priority_table.value_table[row][col] = '<'

                    elif one[i] in self.v_terminals: # one[i] is von terminals
                        if i+1 < one_len and one[i+1] in self.terminals: # ...pa.... LASTVT(P) > a
                            col = self.priority_table.terminal_index[one[i+1]]
                            for last in self.LASTVT[one[i]]:
                                row = self.priority_table.terminal_index[last]
                                self.priority_table.value_table[row][col] = '>'

    def show_FIRSTVT(self):
        info = self.grammar_name + '的FIRSTVT集合如下所示'
        if self.FIRSTVT:
            table = PrettyTable()
            table.title = info
            table.field_names = ['VT', 'FIRSTVT-SET']
            for key in self.FIRSTVT.keys():
                table.add_row([key, self.FIRSTVT[key]])

            print(table)

    def show_LASTVT(self):
        info = self.grammar_name + '的LASTVT集合如下所示'
        if self.LASTVT:
            table = PrettyTable()
            table.title = info
            table.field_names = ['VT', 'LASTVT-SET']
            for key in self.LASTVT.keys():
                table.add_row([key, self.LASTVT[key]])

            print(table)

    def show_priority_table(self):
        info = self.grammar_name + '的算符优先关系表如下'
        table = PrettyTable()
        table.title = info
        field = self.terminals.copy()
        field.insert(0, ' ')
        table.field_names =  field
        for col, t in zip(self.priority_table.value_table, self.terminals):
            temp = col.copy()
            temp.insert(0, t)
            table.add_row(temp)
        print(table)

    def show_all(self):
        print()
        self.show_FIRSTVT()
        print()
        self.show_LASTVT()
        print()
        self.show_priority_table()
        print()



class StateGrammar():
    '''
    变量说明文法
    '''
    name = '变量说明文法 StateGrammar'
    start = 'S'
    production = [
        # 'S -> var D | nil',
        'S -> var D',
        'D -> L : K ; | L : K ; S',
        'L -> i , L | i',
        'K -> integer | bool | real',
    ]
    terminals = ['var', ':', ';', 'i', ',', 'integer', 'bool', 'real']
    v_terminals = ['S', 'D', 'L', 'K']



class ExpressionGrammar():
    '''
    算式表达式
    '''
    name = '算式表达式 ExpressionGrammar'
    start = 'E'
    production = [
        'E -> E + T | E - T | T | i',
        'T -> T * F | T / F | F',
        'F -> ( E ) | i'
    ]
    terminals = ['+', '-', 'i', '*', '/', '(', ')']
    v_terminals = ['E', 'T', 'F']



class BoolGrammar():
    '''
    布尔表达式
    '''
    name = '布尔表达式 BoolGrammar'
    start = 'B'
    production = [
        'B -> B or B | B and B | not B',
        'B -> ( B )',
        'B -> i',
        'B -> i < i | i <= i | i = i | i <> i | i > i | i >= i',
        'B -> true | false'
    ]
    terminals = ['or', 'and', 'not', '(', ')', 'i', '<', '<=', '=', '<>', '>', '>=', 'true', 'false']
    v_terminals = ['B']


"""
class BoolGrammar():
    name = 'BoolGrammar'
    start = 'B'
    production = [
        'B -> T | or T',
        'B -> F | and F',
        'F -> ( B ) | not F | C',
        'C -> true | false'
    ]
    terminals = ['or', 'and', '(', ')', 'not', 'true', 'false']
    v_terminals = ['B', 'T', 'F', 'C']
"""

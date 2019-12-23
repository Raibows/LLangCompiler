from prettytable import PrettyTable


define_false = (False, -2, 'unknown')
define_word_max_length = 10

class PriorityTable():
    def __init__(self):
        self.terminal_index = {}
        self.value_table = []

class Token():

    def __init__(self, label:int, name:str, code:int, addr:int, type:str):
        self.label = label
        self.name = name
        self.code = code
        self.addr = addr
        self.type = type


class Symbol():

    def __init__(self, number:int, name:str, code:int, type:str, token_label:int):
        self.number = number
        self.code = code
        self.name = name
        self.type = type
        self.token_labels = [token_label]


class Unrecognized():
    line = ''
    name = ''
    pos = -2
    un_index = -2

    def __init__(self, un_index:int ,line:str, name:str, pos:int):
        self.line = line
        self.name = name
        self.pos = pos
        self.un_index = un_index


class Code():
    # tag \ key \ int \ real \ operator
    key = {}
    key['and'] = 1
    key['begin'] = 2
    key['bool'] = 3
    key['do'] = 4
    key['else'] = 5
    key['end'] = 6
    key['false'] = 7
    key['if'] = 8
    key['integer'] = 9
    key['not'] = 10
    key['or'] = 11
    key['program'] = 12
    key['real'] = 13
    key['then'] = 14
    key['true'] = 15
    key['var'] = 16
    key['while'] = 17

    TAG = 18
    INT = 19
    REAL = 20

    bounder = {}
    bounder['('] = 21
    bounder[')'] = 22
    # bounder['.'] = 27
    bounder[','] = 28
    # bounder[':'] = 29
    bounder[';'] = 30



    operator = {}
    operator['+'] = 23
    operator['-'] = 24
    operator['*'] = 25
    operator['/'] = 26
    operator[':'] = 29
    operator[':='] = 31 # 赋值
    operator['='] = 32 # ==
    operator['<='] = 33
    operator['<'] = 34
    operator['<>'] = 35 # not equal
    operator['>'] = 36
    operator['>='] = 37


    def is_over_length(self, word)->bool:
        if len(word) > define_word_max_length:
            return True
        return False

    def is_TAG(self, word)->(bool, int, str):
        if word[0].isalpha() or word[0] == '_':
            if self.is_key(word)[0]:
                return define_false
            return (True, self.TAG, '标识符')
        else:
            return define_false

    def is_key(self, word:str)->(bool, int, str):
        temp = self.key.get(word)
        if temp:
            return (True, temp, '关键字')
        return define_false

    def is_bounder(self, word:str)->(bool, int, str):
        temp = self.bounder.get(word)
        if temp:
            return (True, temp, '定界符')
        return define_false

    def __is_digit(self, word)->bool: #先判断是不是数字
        tag = True
        try:
            temp = int(word)
        except:
            tag = False
        if tag:
            return True

        try:
            temp = float(word)
        except:
            return False

        return True


    def is_INT(self, word)->(bool, int, str):
        if self.__is_digit(word):
            try:
                word = int(word)
                if isinstance(word, int):
                    return (True, self.INT, '整 型')
            except: # float
                return define_false
        return define_false

    def is_REAL(self, word)->(bool, int, str):
        if self.__is_digit(word):
            if self.is_INT(word)[0]: #是整数
                return define_false
            else:
                return (True, self.REAL, '实 数')
        return define_false

    def is_operator(self, word)->(bool, int, str): # 必须传入已经分割好的word，对于<>，不应该只传入<
        temp = self.operator.get(word)
        if temp:
            return (True, temp, '运算符')
        return define_false



class Equ():
    def __init__(self, op_code:int, op_ip:int, src_name:str, src_ip:int, dst_name:str, dst_ip:int, result_ip:int):
        self.op_code = op_code
        self.op_ip = op_ip
        self.src_name = src_name
        self.src_ip = src_ip
        self.dst_name = dst_name
        self.dst_ip = dst_ip
        self.result_ip = result_ip


class Grammar():

    def __init__(self, state_grammar=None, terminals=None, v_terminals=None):
        if state_grammar:
            self.state_grammar = state_grammar
        else:
            self.state_grammar = [
                'A → # S #',
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
            self.v_terminals = ['A', 'S', 'D', 'L', 'K']


    state_grammar_FIRSTVT = {}
    state_grammar_LASTVT = {}
    sentences = []
    priority_table = PriorityTable() # 2 dims
    '''
    sentences = [
                    ['S ', [' var D ', ' nil']],
                    ['D ', [' L : K ; ', ' L : K ; D']],
                    ['L ', [' i , L ', ' i']],
                    ['K ', [' integer ', ' bool ', ' real']],
                ]
    '''

    def set_sentences(self):
        for line in self.state_grammar:
            sentence = line.split('→')
            sentence[0] = sentence[0].strip()
            sentence[1] = sentence[1].split('|')
            for i in range(len(sentence[1])):
                sentence[1][i] = sentence[1][i].strip()
                sentence[1][i] = sentence[1][i].split(' ')
            self.sentences.append(sentence)
        # print(self.sentences)


    def transfer(self, src:str, dst:str, flag='firstvt'):
        print('transfer', flag, src, dst)
        change = False
        if flag == 'firstvt':
            for ch in self.state_grammar_FIRSTVT[src]:
                if ch not in self.state_grammar_FIRSTVT[dst]:
                    self.state_grammar_FIRSTVT[dst].append(ch)
                    change = True
        elif flag == 'lastvt':
            for ch in self.state_grammar_LASTVT[src]:
                if ch not in self.state_grammar_LASTVT[dst]:
                    self.state_grammar_LASTVT[dst].append(ch)
                    change = True
        else:
            raise RuntimeError('Grammar transfer flag is invalid !', flag)
        return change


    def set_state_grammer_FIRSTVT_LASTVT(self):
        if not self.sentences:
            self.set_sentences()
        if (not self.state_grammar_FIRSTVT) or (not self.state_grammar_LASTVT):
            for v in self.v_terminals:
                self.state_grammar_FIRSTVT[v] = []
                self.state_grammar_LASTVT[v] = []
        while True:
            change_flag = False
            for line in self.sentences:
                for one in line[1]:
                    ch = one[0] #firstvt
                    if ch in self.terminals and ch not in self.state_grammar_FIRSTVT[line[0]]: # A -> a..
                        self.state_grammar_FIRSTVT[line[0]].append(ch)
                        change_flag = True
                    elif ch in self.v_terminals: # 'A -> Q...'
                        if len(one) > 1:  # A -> Qa..
                            if one[1] in self.terminals and one[1] not in self.state_grammar_FIRSTVT[line[0]]:
                                self.state_grammar_FIRSTVT[line[0]].append(one[1])
                                change_flag = True
                        change_flag = (change_flag or self.transfer(ch, line[0], flag='firstvt')) # A -> Q..

                    ch = one[-1] #lastvt
                    if ch in self.terminals and ch not in self.state_grammar_LASTVT[line[0]]: # A -> ...a
                        self.state_grammar_LASTVT[line[0]].append(ch)
                        change_flag = True

                    elif ch in self.v_terminals: # A -> ...Q
                        if len(one) > 1: # A -> ...aQ
                            if one[-2] in self.terminals and one[-2] not in self.state_grammar_LASTVT[line[0]]:
                                self.state_grammar_LASTVT[line[0]].append(one[-2])
                                change_flag = True
                        change_flag = (change_flag or self.transfer(ch, line[0], flag='lastvt')) # A -> ...Q

            if not change_flag:
                break

    def set_state_grammer_priority_table(self):
        if not (self.state_grammar_FIRSTVT and self.state_grammar_LASTVT):
            self.set_state_grammer_FIRSTVT_LASTVT()

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
                            for first in self.state_grammar_FIRSTVT[one[i+1]]:
                                col = self.priority_table.terminal_index[first]
                                self.priority_table.value_table[row][col] = '<'

                    elif one[i] in self.v_terminals: # one[i] is von terminals
                        if i+1 < one_len and one[i+1] in self.terminals: # ...pa.... LASTVT(P) > a
                            col = self.priority_table.terminal_index[one[i+1]]
                            for last in self.state_grammar_LASTVT[one[i]]:
                                row = self.priority_table.terminal_index[last]
                                self.priority_table.value_table[row][col] = '>'





    def show_FIRSTVT(self):
        print('state_grammer的FIRSTVT集合如下所示')
        if self.state_grammar_FIRSTVT:
            table = PrettyTable(['VT', 'FIRSTVT-SET'])
            for key in self.state_grammar_FIRSTVT.keys():
                table.add_row([key, self.state_grammar_FIRSTVT[key]])

            print(table)

    def show_LASTVT(self):
        print('state_grammer的LASTVT集合如下所示')
        if self.state_grammar_LASTVT:
            table = PrettyTable(['VT', 'LASTVT-SET'])
            for key in self.state_grammar_LASTVT.keys():
                table.add_row([key, self.state_grammar_LASTVT[key]])

            print(table)


    def show_priority_table(self):
        print('state_grammer的算符优先关系表如下')
        title = self.terminals.copy()
        title.insert(0, ' ')
        table = PrettyTable(title)
        for col, t in zip(self.priority_table.value_table, self.terminals):
            col.insert(0, t)
            table.add_row(col)
        print(table)


    def show_all(self):
        self.show_FIRSTVT()
        print()
        self.show_LASTVT()
        print()
        self.show_priority_table()
        print()















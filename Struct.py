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
        self.addr = addr # key is -1 other is Symbol's number
        self.type = type


class Symbol():

    def __init__(self, number:int, name:str, code:int, type:str):
        self.number = number
        self.code = code
        self.name = name
        self.type = type



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
    def __init__(self, op:str, op1:str, op2:str, result:str):
        self.op = op
        self.op1 = op1
        self.op2 = op2
        self.result = result





class TreeNode():
    def __init__(self, name):
        self.child = None
        self.sibling = None
        self.name = name
        self.data = None

    def set_child(self, child):
        if not isinstance(child, TreeNode):
            raise RuntimeError('Error in set child! child type must be TreeNode')
        self.child = child

    def set_sibling(self, sibling):
        if not isinstance(sibling, TreeNode):
            raise RuntimeError('Error in set sibling! sibling type must be TreeNode')
        self.sibling = sibling


















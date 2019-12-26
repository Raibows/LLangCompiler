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
    def __init__(self, op:int, op1:int, op2:int, result):
        '''
        注意op1、op2、result都是
        '''
        self.op = op
        self.op1 = op1
        self.op2 = op2
        self.result = result

    def __repr__(self):
        info = f'({self.op}, {self.op1}, {self.op2}, {self.result})'
        return info



class TreeNode():
    def __init__(self, name:str=None, token:Token=None, label:int=None, pos:int=0, action:int=None):
        if (token or (name and label)) == False:
            raise RuntimeError('Error must give token or label and name!')

        self.parent = None
        self.pos = pos
        if token: # terminal
            self.terminal_flag = True
            self.children = None
            self.name = token.name
            self.label = token.label
            self.action = None
        else: # non-terminal
            self.terminal_flag = False
            self.name = name
            self.label = label
            self.children:[TreeNode] = []
            if action:
                self.action = action # record semantic action
            else:
                self.action = False # temp node
            self.attr_t = '_' # true
            self.attr_f = '_' # false
            self.attr_q = '_' # quad
            self.attr_n = '_' # next



    def set_child(self, child):
        if self.terminal_flag:
            raise RuntimeError('Error terminal TreeNode could not set child!')
        if not isinstance(child, TreeNode):
            raise RuntimeError('Error in set child! child type must be TreeNode')
        self.children.append(child)
        child_pos = len(self.children)
        child.pos = child_pos - 1

    def set_parent(self, parent):
        if not isinstance(parent, TreeNode):
            raise RuntimeError('Error in set sibling! sibling type must be TreeNode')
        self.parent = parent

    def insert_sibling(self, sibling, right_offset:int):
        if not isinstance(sibling, TreeNode):
            raise RuntimeError('Error in set child! child type must be TreeNode')
        if self.parent == None:
            raise RuntimeError('Error do not has parent, so could not insert sibling of', self)
        p:TreeNode = self.parent
        self.pos = p.children.index(self) # 先定位自己
        p.children.insert(self.pos+right_offset, sibling)
        sibling.parent = p

    def get_sibling(self, right_offset:int):
        p:TreeNode = self.parent
        self.pos = p.children.index(self)
        sibling_pos = self.pos + right_offset
        if sibling_pos < len(p.children):
            return p.children[sibling_pos]
        else:
            return None

    def __repr__(self):
        return f'The TreeNode is {self.label}, {self.name}, {self.terminal_flag}, pos is {self.pos}, action is {self.action}, Children: {self.children}, Parent: {self.parent}'




def convertOP2Code(op:str):
    table = {}
    table[':='] = 51
    table['+'] = 43
    table['-'] = 45
    table['*'] = 41
    table['/'] = 48
    table['j<'] = 53
    table['j<='] = 54
    table['j>'] = 57
    table['j>='] = 58
    table['j='] = 56
    table['j'] = 52
    table['j<>'] = 55
    if table.get(op) == None:
        raise RuntimeError('Error in convertOP2Code invalid OP', op)
    return table[op]




if __name__ == '__main__':
    t1 = TreeNode('123', label=1)
    t2 = TreeNode('123', label=2)
    t3 = TreeNode('123', label=3)

    t1.set_child(t2)
    # t1.set_child(t3)
    t2.set_parent(t1)
    # t3.set_parent(t1)
    t2.insert_sibling(t3, 0)
    # print(t1)
    print(t1.children.index(t2), t1.children.index(t3))

    pass










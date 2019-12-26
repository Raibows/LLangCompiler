import pandas as pd
pd.set_option('display.max_columns', 100)
from prettytable import PrettyTable
import warnings
warnings.filterwarnings("ignore")

class LL1:
    def __init__(self):
        self.representation = []    # 表达式
        self.first_state = ''       # 初始状态

        self.VT = set()             # 终结符
        self.VN = set()             # 非终结符

        self.first = dict()         # first集
        self.follow = dict()        # follow集
        self.select = dict()        # select集
        self.table = dict()         # 预测分析表


    def get_representation(self):
        """
        从本地文件读取获取产生式，\n分隔
        根据读取文件第一个表达式左部，来确定初始状态
        :return:
        """
        # fo = open("./test1.txt", "r")
        # input = fo.read()
        # self.representation = input.split('\n')
        # self.representation = ['S -> A a | b', 'A -> A c | S d | ε']
        # self.representation=['E -> E + T | T', 'T -> T * F | F', 'F -> ( E ) | id']
        # self.representation=['P -> A a | i', 'A -> P b']
        # self.representation = [
        #     'B -> B or B | B and B | not B',
        #     'B -> ( B )',
        #     'B -> i',
        #     'B -> i < i | i <= i | i = i | i <> i | i > i | i >= i'
        # ]
        self.representation = [
            'P -> program i L',
            'L -> S ; L | S',
            'S -> if B then S',
            'S -> if B then L else S',
            'S -> while B do S',
            'S -> begin L end',
            'S -> var D',
            # 'S -> nil',
            'S -> A | A ;',
            # 'D -> i : K ; | i : K ',

            'D -> H : K ; | H : K ; S',
            'H -> i , H | i',

            'K -> integer | bool | real',
            'A -> i := E',
            'E -> E + T | E - T | T | - E | true | false',
            'E -> E and E | E or E | E and not E| E or not E',
            'B -> B or N | N | not B',
            'T -> T * F | T / F | F',
            'F -> ( E ) | i',
            'N -> N and M',
            'N -> M',
            'M -> ( B )',
            'M -> i < i | i > i | i <> i | i <= i | i >= i | i = i'
        ]
        print('产生式：', self.representation)

        self.first_state = self.representation[0].split(' -> ')[0]


    def get_VT_VN(self):
        """
        根据产生式，获取终结符，非终结符
        :return:
        """
        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')   # 前后消空格
            self.VN.add(left_representation)

        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')
            for r in right_representation.split(' '):
                if r not in self.VN | set(['|', 'ε']):
                    self.VT.add(r)


    def out_VT_VN(self):
        self.first = dict()
        self.follow = dict()
        self.VN = set()
        self.VT = set()

        self.get_VT_VN()
        print('非终结符：', self.VN)
        print('终结符：', self.VT)



    #直接间接左递归选择入口
    def is_recursion(self):
        """
        判断是否有间接左递归/直接左递归，确定消除左递归的入口
        :param self:
        :return:
        """
        is_indirect = False # 两个标志位，是否存在间接左递归，直接左递归
        is_direct = False

        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')
            right_representation_list = right_representation.split(' | ')

            for right in right_representation_list:
                right = right.split(' ')

                # 直接左递归判断
                if left_representation == right[0]:
                    is_direct = True
                # 间接左递归判断
                for isIndirect_representation in self.representation:
                    # 如果是自己，跳过
                    if isIndirect_representation == representation:
                        continue

                    isIndirect_left_representation, isIndirect_right_representation = isIndirect_representation.split(' -> ')
                    # 判断是否有递归关系
                    if isIndirect_left_representation != right[0]:
                        continue

                    # 存在递归，继续
                    isIndirect_right_representation_list = isIndirect_right_representation.split(' | ')
                    for isIndirect_right in isIndirect_right_representation_list:
                        isIndirect_right_list =  isIndirect_right.split(' ')
                        if left_representation == isIndirect_right_list[0]:
                            is_indirect = True

        if is_indirect:
            print('间接左递归')
            self.indirect2direct()
            self.de_direct_recursion()
        elif is_direct:
            print('直接左递归')
            self.de_direct_recursion()
        else:
            print('无左递归')





    def indirect2direct(self):
        """
        间接左递归变直接左递归
        :return:
        """
        self.get_VT_VN()
        message = []
        remove_list = []
        for i in self.representation:
            left, right = i.split(' -> ')
            for j in right.split(' '):
                if j in self.VN:
                    message.append(str(j + ' at right of ' +i))
                    message.append(j)
        for i in self.representation:
            left, right = i.split(' -> ')
            right_list = right.split(' | ')
            if left in right:
                if str(left + ' at right of ' +i) in message:
                    flag = 0
                    for j in right_list:
                        j = j.split(' ')
                        if j[0] in self.VN:
                            if j[0] is not left:
                                for k in self.representation:
                                    kleft, kright = k.split(' -> ')#注意这里的leftright是k循环内的新变量
                                    kright_list = kright.split(' | ')
                                    if kleft is j[0]:
                                        a = []
                                        a += [str(r) for r in kright_list]
                                        for c in a :
                                            a[a.index(c)] = a[a.index(c)] + right_list[right_list.index(' '.join(tmp for tmp in j))][1:]
                                        right_list.remove(' '.join(tmp for tmp in j))
                                        right_list.extend(a)
                                        remove_list.append(k)
                    self.representation += [left + ' -> ' + ' | '.join(right for right in right_list)]
                    remove_list.append(i)
                    pass
        for i in remove_list:
            self.representation.remove(i)
        print('间接左递归变直接左递归', self.representation)


    def de_direct_recursion(self):
        """
        消除直接左递归
        :return:
        """
        remove_list = []

        for i in self.representation:

            if '|' in i:
                ldirect_flag = False
                flag = False
                epsilion_flag = False
                left, right = i.split(' -> ')
                right_list = right.split(' | ')

                remove_list_ = []
                follow_left = []  # 在右部中出现在左部之后的表达式
                new_right = []

                for j in right_list:
                    temp = j.split(' ')
                    if temp[0] is left:
                        ldirect_flag = True
                        remove_list_.append(j)    # 当前元素加入删除列表
                        follow_left.extend(temp[1:])    # left的follow
                        new_right.append(' '.join(temp[1:]) + " " + left + "'") # 新的右部
                    elif temp[0] == 'ε':  # 第一个为空，表示为空
                        new_right.append('ε')  # 新的右部
                        epsilion_flag = True
                        remove_list_.append(j)
                    elif not ldirect_flag:
                        pass
                    elif temp[0] is not left:
                        flag = True
                        right_list[right_list.index(j)] = j + str(" " + left + "'") # 所有开头非左部表达四，都变成以他开头加左部'

                if epsilion_flag:
                    right_list.append(left + "'")  # 新的右部
                if flag:
                    new_right.append('ε')
                for re in remove_list_:
                    right_list.remove(re)
                remove_list.append(i)
                self.representation += [left + ' -> ' + str(right) for right in right_list]
                if flag:
                    self.representation += [left + "'" + ' -> ' + str(right) for right in new_right]
        for i in remove_list:
            self.representation.remove(i)

        print('消除左递归', self.representation)


    def get_first_VN(self,r):
        """
        获取first集的递归调用
        :param r: 右子表达式，左边第一个非终结符
        :return: first集(set)
        """
        add = set()
        for representation_ in self.representation:
            left_representation_, right_representation_ = representation_.split(' -> ')
            if left_representation_ == r:
                right_representation_list_ = right_representation_.split(' ')
                if right_representation_list_[0] in self.VT|set(['ε']):
                    add.add(right_representation_list_[0])
                elif right_representation_list_[0] in self.VN:
                    add|=(self.get_first_VN(right_representation_list_[0]))
        return add


    def get_first(self):
        """
        获取first集
        :return:
        """
        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')

            if left_representation not in self.first.keys():
                self.first[left_representation] = set()

            # 3种情况，第一个为非终结符/ε/终结符
            right_representation_list = right_representation.split(' ')
            if right_representation_list[0] in self.VT|set(['ε']):
                self.first[left_representation].add(right_representation_list[0])
            elif right_representation_list[0] in self.VN:
                self.first[left_representation]|=self.get_first_VN(right_representation_list[0])

        print('FIRST')
        for i in self.first.keys():
            print(i, self.first[i])


    def get_follow(self):
        """
        获取follow集合
        :return:
        """
        # 第一种情况，只计算没用用到其他follow集的follow集
        for i in self.VN:
            # 初始化
            if i not in self.follow.keys():
                self.follow[i] = set('$')

            for representation in self.representation:
                left_representation, right_representation = representation.split(' -> ')
                right_representation_list = right_representation.split(' ')

                if i in right_representation_list:
                    next = ''
                    # 第一种情况，后面没有
                    if len(right_representation_list) == right_representation_list.index(i)+1:    # 越界问题
                        # self.follow[i]|=self.follow[left_representation]    # 最后一位，后面没有的情况，follow加进来
                        pass
                    else:
                        next = right_representation_list[right_representation_list.index(i) + 1]

                    if next in self.VN:
                        # 第一种情况，后面指向空
                        if next + ' -> ε' in self.representation:
                            # self.follow[i] |= self.follow[left_representation]  # 最后一位，后面没有的情况，follow加进来
                            pass
                        self.follow[i]|=self.first[right_representation_list[right_representation_list.index(i) + 1]]
                        self.follow[i].remove('ε')

                    if next in self.VT:
                        self.follow[i].add(next)

        # 第二张，重新计算follow，计算包括其他follow集的follow集
        for i in range(2):
            for i in self.VN:
                for representation in self.representation:
                    left_representation, right_representation = representation.split(' -> ')
                    right_representation_list = right_representation.split(' ')

                    if i in right_representation_list:
                        next = ''
                        # 第一种情况，后面没有
                        if len(right_representation_list) == right_representation_list.index(i)+1:    # 越界问题
                            self.follow[i]|=self.follow[left_representation]    # 最后一位，后面没有的情况，follow加进来
                        else:
                            next = right_representation_list[right_representation_list.index(i) + 1]

                        if next in self.VN:
                            # 第一种情况，后面指向空
                            if next + ' -> ε' in self.representation:
                                self.follow[i] |= self.follow[left_representation]  # 最后一位，后面没有的情况，follow加进来
                            self.follow[i]|=self.first[right_representation_list[right_representation_list.index(i) + 1]]
                            self.follow[i].remove('ε')

                        if next in self.VT:
                            self.follow[i].add(next)


        print('FOLLOW')
        for i in self.follow.keys():
            print(i, self.follow[i])


    def get_select(self):
        """
        获取select集
        :return:
        """
        for representation in self.representation:
            left = representation.split(' -> ')[0]
            right_1st = representation.split(' -> ')[1].split(' ')[0]
            if right_1st in self.VN: # 非终结符
                self.select[representation] = self.first[left]
            elif right_1st in self.VT: # 终结符
                self.select[representation] = set()
                self.select[representation].add(right_1st)

            elif right_1st == 'ε':
                self.select[representation] = self.follow[left]
                pass
        # print(self.select)
        print('select')
        for i in self.select.keys():
            print(i, self.select[i])


    def is_ll1(self):
        """
        判断该文法是否为LL1文法
        :return:
        """
        _is_ll1 = False
        VN_selcet = dict()

        for i in self.select.keys():
            if i.split(' -> ')[0] not in VN_selcet.keys():
                VN_selcet[i.split(' -> ')[0]] = []
                VN_selcet[i.split(' -> ')[0]] += list(self.select[i])

        for i in VN_selcet.keys():
            if len(VN_selcet[i]) != len(set(VN_selcet[i])):
                pass
            else:
                _is_ll1 = True

        if _is_ll1:
            print('符合LL1文法')
        else:
            print('不符合LL1文法')
            exit()

        # print('VN_selcet')
        # for i in VN_selcet.keys():
        #     print(i, VN_selcet[i])


    def get_tabel(self):
        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')
            right_representation_list = right_representation.split(' ')

            # 一阶字典初始化
            if left_representation not in self.table.keys():
                self.table[left_representation] = dict()

            first = set('ε')
            if right_representation_list[0] in self.VN:
                first = self.first[right_representation_list[0]]
            elif right_representation_list[0] in self.VT:
                first = set()
                first.add(right_representation_list[0])

            if 'ε' in first:
                for i in first:
                    if i == 'ε':
                        continue
                    self.table[left_representation][i] = representation
                for i in self.follow[left_representation]:
                    self.table[left_representation][i] = representation
            else:
                for i in first:
                    self.table[left_representation][i] = representation

        # synch
        for i in self.VN:
            for j in self.follow[i]:
                if j not in self.table[i]:
                    self.table[i][j] = 'synch'

        print('TABLE')
        for i in self.table.keys():
            print(i, self.table[i])
        print('df_TABLE')
        df_table = pd.DataFrame(ll1.table).T.fillna('')
        # tmp.to_csv('./table.csv')
        print(df_table)


    def analyze(self, file_path=None):
        """
        对用户输入语句进行语法分析
        :return:
        """
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                with open(file_path, 'r', encoding='utf-8') as file:
                    temp = file.readlines()
                file = []
                for line in temp:
                    line = line.strip('\n')
                    line = line.strip('\r')
                    line = line.strip('\t')
                    line = line.strip(' ')
                    line = line.split(' ')
                    for word in line:
                        if word not in self.VT and word not in self.VN:
                            raise RuntimeError('Error reduction file has unknown chars!', word)
                        file.append(word)
            input_str = file
        else:
            input_str = input("请输入：")
            # input_str = '( ( id + id ) * id id'
            input_str += ' $'

            input_str = input_str.split(' ')

        # 判断是否输入正确
        for i in input_str:
            if i not in self.VT:
                if i != '$':
                    print('输入错误，请重新输入')
                    return 0


        stack = ['$']
        # 开始符号
        stack.append(self.first_state)

        table = PrettyTable(["栈", "输入", "动作"])
        table.padding_width = 1
        table.align = "l"

        i = 0  # 访问str

        table.add_row([stack.__str__(), input_str[i:], ''])

        c = stack.pop()  # 访问栈

        while c!='$':
            if c in self.VN:    # 非终结符
                if input_str[i] in self.table[c].keys():  # 如果有这个表达式，查表
                    representation = self.table[c][input_str[i]]

                    # 查表，弹栈顶
                    if representation == 'synch':
                        # 删除ε
                        error_list = []
                        for f in self.first[c]:
                            if f != 'ε':
                                error_list.append(f)
                        table.add_row([stack.__str__(), input_str[i:], 'error，位置：' + str(i) + '，字符：' + input_str[i]+'，缺少：' + str(error_list)])  # 先报错，再弹栈顶
                        c = stack.pop()
                        continue

                    left_representation, right_representation = representation.split(' -> ')
                    right_representation_list = right_representation.split(' ')

                    # 如果指向空，则替换为空，直接弹下一个
                    if right_representation == 'ε':
                        table.add_row([stack.__str__(), input_str[i:], representation])
                        c = stack.pop()
                        continue

                    # 正常情况反向进栈
                    stack+=[i for i in right_representation_list[::-1]]
                    table.add_row([stack.__str__(), input_str[i:], representation])
                    c = stack.pop()

                # 查表为空, 报错，忽略输入
                else:
                    # 删除ε
                    error_list = []
                    for f in self.first[c]:
                        if f != 'ε':
                            error_list.append(f)
                    table.add_row([stack.__str__(), input_str[i:], 'error，位置：' + str(i) + '，字符：' + input_str[i] + '，缺少：' + str(error_list)])
                    i = i + 1

            elif c in self.VT:  # 终结符
                if input_str[i] == c:   # 栈顶是否匹配输入
                    table.add_row([stack.__str__(), input_str[i+1:], '匹配' + input_str[i]])
                    i = i + 1
                    c = stack.pop()
                else:   # 不匹配，栈顶弹出
                    table.add_row([stack.__str__(), input_str[i:], 'error，位置：' + str(i) + '，字符：' + input_str[i] + '，缺少：' + c])
                    c = stack.pop()

        if input_str[i:][0] != '$':
            stack.append(c)

            while len(input_str[i:])!=0:
                if input_str[i:][0] != '$':
                    table.add_row([stack.__str__(), input_str[i:], 'error:输入栈未排空 ' + str(i) + input_str[i]])
                    i += 1
                else:
                    table.add_row([stack.__str__(), input_str[i:], '结束'])
                    i+=1

        print(table)


if __name__ == '__main__':
    pass
    # ll1 = LL1()
    # ll1.get_representation()
    #
    # ll1.is_recursion()
    #
    # ll1.out_VT_VN()
    #
    # ll1.get_first()
    # ll1.get_follow()
    # ll1.get_select()
    #
    # ll1.is_ll1()
    #
    # ll1.get_tabel()
    #
    # for i in range(1):
    #     ll1.analyze()
    pass
    def aaa():
        return 1, 2
    k, x = aaa()
    print(k, x)
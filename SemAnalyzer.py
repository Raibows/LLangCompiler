'''
语义分析器
'''

from Struct import *
from OPGrammar import OPGrammar



class Semantic():

    def __init__(self, tree_root:TreeNode, tree_nodes:dict, grammar:OPGrammar, tokens:[Token], symbols:[Symbol]):
        self.tokens:[Token] = tokens
        self.symbols:[Symbol] = symbols
        self.root = tree_root
        self.nodes:dict = tree_nodes
        self.grammar = grammar
        self.__next_label = len(tree_nodes)
        self.__optional_insert = ['while', 'do', 'then', 'else', 'or', 'and']
        self.__emit_list:[Equ] = []
        self.__next_quad = 0
        self.__new_temp_count = 0




    def analyzer_semantic(self, is_show_emit=True):
        print('Info 正在语义分析，产生四元式！')
        self.__dfs(self.root)
        if is_show_emit:
            print('Info 四元式结果如下')
            for emit in self.__emit_list:
                print(emit)



    def __get_node_symbol_addr(self, node:TreeNode):
        if node.terminal_flag:
            label = node.label
            return self.tokens[label].addr
        else:
            return -1
            raise RuntimeError('Error must be terminal!', node.name)


    def __get_new_temp(self)->str:
        name = 'T' + str(self.__new_temp_count)
        self.__new_temp_count += 1
        return name

    def __merge(self, *args):
        ans = []
        for one_list in args:
            if isinstance(one_list, int):
                ans.append(one_list)
            else:
                for x in one_list:
                    if isinstance(x, int):
                        ans.append(x)
        return ans


    def __action_later(self, node:TreeNode):
        if node.terminal_flag:
            raise RuntimeError('Error judge_action func needs a non_terminal_TreeNode, but you give a name as', node.name)
        action = node.action
        if True:
            if action == 0: # # p #
                node.attr_n = node.children[0].attr_n

            elif action == 1: # ['program', 'i', 'L']
                node.attr_n = node.children[2].attr_n

            elif action == 2: # ['L', ';', 'S']  L -> L ; M S
                pass
                # for x in node.children:
                #     print(x.name)
                self.__back_patch(node.children[0].attr_n, node.children[2].attr_q)
                node.attr_n = node.children[3].attr_n

            elif action == 3: # ['S']
                node.attr_n = node.children[0].attr_n

            elif action == 4: # if B then M S
                # print(node.children)
                # print(node.children[3].name)
                self.__back_patch(node.children[1].attr_t, node.children[3].attr_n)
                node.attr_n = self.__merge(node.children[1].attr_f, node.children[4].attr_n)

            elif action == 5: # if B then M L N else M S
                self.__back_patch(node.children[1].attr_t, node.children[3].attr_q)
                self.__back_patch(node.children[1].attr_f, node.children[7].attr_q)
                node.attr_n = self.__merge(node.children[4].attr_n, node.children[5].attr_n, node.children[8].attr_n)

            elif action == 6: # while M E do M S
                self.__back_patch(node.children[5].attr_n, node.children[1].attr_q)
                self.__back_patch(node.children[2].attr_t, node.children[4].attr_q)
                node.attr_n = node.children[2].attr_f
                self.__generate_emit('j', -1, -1, node.children[1].attr_q)

            elif action == 7: # S -> begin L end
                node.attr_n = node.children[1].attr_n

            elif action == 8: # var D
                pass
            elif action == 9: # S -> A
                pass
            elif action == 10:
                pass
            elif action == 11:
                pass
            elif action == 12:
                pass
            elif action == 13:
                pass
            elif action == 14:
                node.label = node.children[0].label
            elif action == 15:
                pass
            elif action == 16:
                pass
            elif action == 17:
                pass
            elif action == 18: # i := E
                op1 = self.__get_node_symbol_addr(node.children[0])
                self.__generate_emit(node.children[1].name, op1, -1, node.children[2].name)

            elif action == 19: # E + T
                temp_name = self.__get_new_temp()
                op1 = self.__get_node_symbol_addr(node.children[0])
                op2 = self.__get_node_symbol_addr(node.children[2])
                self.__generate_emit(node.children[1].name, op1, op2, temp_name)

            elif action == 20: # E - T
                temp_name = self.__get_new_temp()
                op1 = self.__get_node_symbol_addr(node.children[0])
                op2 = self.__get_node_symbol_addr(node.children[2])
                self.__generate_emit(node.children[1].name, op1, op2, temp_name)

            elif action == 21: # T
                node.attr_n = node.children[0].attr_n

            elif action == 22: # - E
                temp_name = self.__get_new_temp()
                op = node.children[0].name
                op1 = -1
                op2 = self.tokens[node.label].addr
                self.__generate_emit(op, op1, op2, temp_name)


            elif action == 23: # true
                pass
            elif action == 24: # false
                pass
            elif action == 25: # E1 and U E2
                self.__back_patch(node.children[0].attr_t, node.children[2].attr_q)
                node.attr_t = [node.children[3].attr_t]
                node.attr_f = self.__merge(node.children[0].attr_f, node.children[3].attr_f)

            elif action == 26: # E1 or U E2
                self.__back_patch(node.children[0].attr_f, node.children[2].attr_q)
                node.attr_t = self.__merge(node.children[0].attr_t, node.children[3].attr_t)
                node.attr_f = [node.children[3].attr_f]

            elif action == 27:
                pass
            elif action == 28:
                pass
            elif action == 29:
                pass
            elif action == 30:
                pass
            elif action == 31: # not E1
                node.attr_t, node.attr_f = node.children[1].attr_f, node.children[1].attr_t

            elif action == 32:
                pass
            elif action == 33:
                pass
            elif action == 34:
                pass
            elif action == 35: # ( E1 )
                node.attr_t, node.attr_f = node.children[1].attr_t, node.children[1].attr_f

            elif action == 36:
                pass
            elif action == 37:
                pass
            elif action == 38:
                pass
            elif action == 39:
                pass
            elif 40 <= action <= 45: # <    >   <>    <=    >=     =
                op = node.children[1].name
                op1 = self.__get_node_symbol_addr(node.children[0])
                op2 = self.__get_node_symbol_addr(node.children[2])
                node.attr_t = self.__get_next_quad()
                node.attr_f = self.__get_next_quad()
                self.__generate_emit(op, op1, op2, -1)
            else:
                raise RuntimeError('Error in finding ActionTable, invalid action index', action)



    def __generate_emit(self, op:str, op1:int, op2:int, result):
        '''
        emit 语句对应SymbolTable
        '''
        if op in ['<', '>', '<=', '>=', '=', '<>']:
            op = 'j' + op
        op = convertOP2Code(op)
        emit = Equ(op, op1, op2, result)
        self.__emit_list.append(emit)


    def __get_next_label(self):
        self.__next_label += 1
        return self.__next_label - 1

    def __get_next_quad(self):
        self.__next_quad += 1
        return self.__next_quad - 1

    def __back_patch(self, target:[int], quad:int):
        if isinstance(target, int):
            self.__emit_list[target].result = quad
        else:
            for t in target:
                if isinstance(t, int):
                    self.__emit_list[t].result = quad

    def __generate_temp_node(self, name='U'):
        label = self.__get_next_label()
        name += str(label)
        return TreeNode(name=name, label=label)





    def __dfs(self, node:TreeNode):
        if not node.terminal_flag: # non-terminal
            if len(node.children) > 0: # 有孩子,继续dfs
                for child in node.children:
                    self.__dfs(child)
                # 深度遍历后完成语义动作
                self.__action_later(node)
            else: # 无孩子，可能为空的情况对应 U结点，temp结点
                pass
        else: # terminal
            if node.name in self.__optional_insert: # 是候选项，需要在其右边插入姊妹临时结点U
                if node.name == 'then': # if e then else 需要在then后面插入一个，还需要在else前面插入一个
                    temp = node.get_sibling(2)
                    if temp and temp.name == 'else':
                        U1 = self.__generate_temp_node()
                        U2 = self.__generate_temp_node()
                        node.insert_sibling(U1, 1)
                        node.insert_sibling(U2, 3)
                    else:
                        U = self.__generate_temp_node()
                        node.insert_sibling(U, 1)
                else: # 其他情况插入一个结点即可
                    U = self.__generate_temp_node()
                    node.insert_sibling(U, 1)
            elif node.name == ';': # A ; S
                right = node.get_sibling(1)
                left = node.get_sibling(-1)
                if right and left and right.name in self.grammar.non_terminals and left.name in self.grammar.non_terminals:
                    U = self.__generate_temp_node()
                    node.insert_sibling(U, 1)
            else:
                return






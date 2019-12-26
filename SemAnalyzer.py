'''
语义分析器
'''

from Struct import *
from OPGrammar import OPGrammar


class Semantic():

    def __init__(self, tree_root:TreeNode, tree_nodes:dict, grammar:OPGrammar):
        self.root = tree_root
        self.nodes = tree_nodes
        self.grammar = grammar
        self.__next_label = len(tree_nodes)
        self.__optional_insert = ['while', 'do', 'if', 'then', 'else']



    def __generate_next_node(self, name:str=None, token:Token=None)->TreeNode:
        if token:
            temp = TreeNode(token=token)
            self.nodes[temp.label] = temp
        elif name:
            temp = TreeNode(name=name, label=self.__next_label)
            self.__next_label += 1
            self.nodes[temp.label] = temp
        else:
            raise RuntimeError('Error in generate_next_node, must give token or name!')
        return temp



    def analyzer_semantic(self):
        pass


    def __dfs(self, node:TreeNode):
        if not node.terminal_flag: # non-terminal
            if len(node.children) > 0: # 有孩子,继续dfs
                self.__dfs(node.children[0])
            else: # 无孩子，可能为空的情况对应 M结点，temp结点
                pass
        else: # terminal
            if node.name in self.__optional_insert: # 是候选项，需要在其右边插入姊妹临时结点M
                M = self.__generate_next_node(name='M')
                node.insert_sibling(M, 1)
            else:
                return






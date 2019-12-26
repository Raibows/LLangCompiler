from Struct import *
from prettytable import PrettyTable



class RDGrammar():
    pass



class MainGrammar():
    '''
    主表达式
    '''
    name = 'MainGrammar 主表达式'
    start = 'L'
    production = [
        'L -> S | S ; L',
        'S -> i := E',
        'S -> if B then S',
        'S -> if B then S else S',
        'S -> while B do S',
        'S -> begin L end'
    ]
    v_terminals = ['L', 'S', 'E', 'B']
    terminals = [';', ':=', 'if', 'then', 'else', 'while', 'do', 'begin', 'end', 'i']
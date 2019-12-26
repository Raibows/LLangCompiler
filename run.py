from LexAnalyzer import Lexer
from Parser import OperatorPrecedenceParser
from OPGrammar import *
from RDGrammar import *


class MixGrammar():
    name = 'MixGrammar'
    start = 'P'
    production = []
    terminals = []
    v_terminals = []

    def set_default(self):
        self.production = [
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
            'B -> B or N | N | not B',
            'T -> T * F | T / F | F',
            'F -> ( E ) | i',
            'N -> N and M',
            'N -> M',
            'M -> ( B )',
            'M -> i < i | i > i | i <> i | i <= i | i >= i | i = i'
        ]
        self.v_terminals = ['P', 'L', 'S', 'D', 'K', 'A', 'E', 'B', 'T', 'F', 'N', 'M', 'H']
        self.terminals = ['program', 'i', ';', 'if', 'then', 'else', 'while', 'do', 'begin', 'end', 'var', ':', ':=',
                          'integer', 'bool', 'real', '+', '-', '*', '/', 'or', 'and', 'not', '(', ')',
                          '<', '>', '<>', '=', '<=', '>=', ',', 'true', 'false']

    def mix_grammar(self, *args):
        p = []
        t = []
        vt = []
        for g in args:
            p += g.production
            t += g.terminals
            vt += g.v_terminals
        p = list(set(p))
        t = list(set(t))
        vt = list(set(vt))
        self.production = p
        self.terminals = t
        self.v_terminals = vt
        # print(p)
        # print(t)
        # print(vt)
        names = [ _.name for _ in args]
        print(names, '已经合并完毕')




if __name__ == '__main__':
    # reduct_test_file = r'static/test-ExpressionG.reduct'
    # reduct_test_file = r'static/test-stateG.reduct'
    # reduct_test_file = r'static/test-BoolG2.reduct'
    # reduct_test_file = r'static/test-MainG.reduct'
    # reduct_test_file = r'static/Lexformatted.reduct'


    m = MixGrammar()
    m.set_default()

    le = Lexer()
    le.scanner()
    # le.show_all()
    format_file_path = le.output_formatted_file()
    #
    g = OPGrammar(m)
    # g.show_all()
    o = OperatorPrecedenceParser(g, le.get_symbols(), reduction_file_path=format_file_path)
    o.reduction(is_show=True)




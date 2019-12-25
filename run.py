from LexAnalyzer import Lexer
from Parser import OperatorPrecedenceParser
from Grammar import *


if __name__ == '__main__':
    le = Lexer()
    le.scanner()
    le.show_all()
    le.output_formatted_file()
    g = Grammar(StateGrammar.production, StateGrammar.terminals, StateGrammar.v_terminals)
    o = OperatorPrecedenceParser(g, le.get_symbols())
    o.reduction(True)


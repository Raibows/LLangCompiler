from LexAnalyzer import Lexer
from Parser import OperatorPrecedenceParser


if __name__ == '__main__':
    le = Lexer()
    le.scanner()
    le.show_all()
    le.output_formatted_file()


    g = OperatorPrecedenceParser(symbols=le.get_symbols())
    g.set_grammar_FIRSTVT_LASTVT()
    g.set_grammar_priority_table()
    # g.show_all()
    g.reduction(is_show=True)


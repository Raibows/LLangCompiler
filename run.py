from LexAnalyzer import Lexer
from Parser import OperatorPrecedenceParser
from OPGrammar import *







if __name__ == '__main__':
    reduct_test_file = r'static/test-ExpressionG.reduct'
    reduct_test_file = r'static/test-stateG.reduct'
    reduct_test_file = r'static/test-BoolG.reduct'

    le = Lexer()
    le.scanner()
    # le.show_all()
    le.output_formatted_file()

    g = OPGrammar(BoolGrammar)
    g.show_all()
    o = OperatorPrecedenceParser(g, le.get_symbols(), reduction_file_path=reduct_test_file)
    o.reduction(is_show=True, is_single_reduction=False)




from LexAnalyzer import Lexer
from Parser import OperatorPrecedenceParser
from OPGrammar import *
from RDGrammar import *






if __name__ == '__main__':
    # reduct_test_file = r'static/test.LLang'
    # reduct_test_file = r'static/test-StateG.LLang'
    # reduct_test_file = r'static/test-BoolG2.LLang'
    reduct_test_file = r'static/test2.LLang'



    MixG = MixGrammar()
    MixG.set_default()

    OPG = OPGrammar(MixG)
    OPG.show_all()

    Lex = Lexer(is_output_formatted=True)
    Lex.scanner(LLang_path=reduct_test_file)
    Lex.show_all()


    o = OperatorPrecedenceParser(grammar=OPG, symbols=Lex.get_symbols(), tokens=Lex.get_tokens())
    o.reduction(is_show=True)




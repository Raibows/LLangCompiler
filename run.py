from LexAnalyzer import Lexer
from Parser import OperatorPrecedenceParser
from OPGrammar import *
from SemAnalyzer import Semantic






if __name__ == '__main__':
    reduct_test_file = r'static/test.LLang'
    # reduct_test_file = r'static/test-StateG.LLang'
    # reduct_test_file = r'static/test-BoolG2.LLang'
    # reduct_test_file = r'static/test2.LLang'


    # 初始化文法
    MixG = MixGrammar()
    MixG.set_default()

    # 自动求算符优先关系表
    OPG = OPGrammar(MixG)
    # OPG.show_all()

    # 词法分析器
    Lex = Lexer(is_output_formatted=True)
    Lex.scanner(LLang_path=reduct_test_file)
    Lex.show_all()

    # 语法分析器
    Parser = OperatorPrecedenceParser(grammar=OPG, symbols=Lex.get_symbols(), tokens=Lex.get_tokens())
    Parser.reduction(is_show=False)

    # 语义分析器
    Sem = Semantic(tree_root=Parser.get_tree_root(), tree_nodes=Parser.get_tree_nodes(),
                        grammar=OPG, tokens=Parser.tokens, symbols=Parser.symbols)
    Sem.analyzer_semantic(is_show_emit=True)










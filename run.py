from LexicalAnalyzer import LexicalAnalyzer
from Struct import Grammar


if __name__ == '__main__':
    # le = LexicalAnalyzer()
    # le.formatter()
    # le.scanner()
    # le.show_all()


    g = Grammar()
    g.set_state_grammer_FIRSTVT_LASTVT()
    g.set_state_grammer_priority_table()
    g.show_all()


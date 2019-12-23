from LexicalAnalyzer import LexicalAnalyzer
from Struct import Grammar


if __name__ == '__main__':
    # le = LexicalAnalyzer()
    # le.formatter()
    # le.scanner()
    # le.show_all()
    state_grammar = [
        'A → # S #',
        'S → D ( R )',
        'R → R ; P | P',
        'P → S | i',
        'D → i'
    ]
    terminals = ['#', '(', ')', ';', 'i']
    v_terminals = ['A', 'S', 'D', 'R', 'P']

    g = Grammar(state_grammar, terminals, v_terminals)
    g.set_state_grammer_FIRSTVT_LASTVT()
    g.set_state_grammer_priority_table()
    g.show_all()
    print(g.sentences)


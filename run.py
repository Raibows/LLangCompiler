from LexicalAnalyzer import LexicalAnalyzer
from Grammar import OperatorPrecedenceGrammar


if __name__ == '__main__':
    le = LexicalAnalyzer()
    le.formatter()
    le.scanner()
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

    g = OperatorPrecedenceGrammar()
    g.set_grammar_FIRSTVT_LASTVT()
    g.set_grammar_priority_table()
    g.show_all()
    g.reduction()


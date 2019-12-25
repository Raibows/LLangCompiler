from LexicalAnalyzer import LexicalAnalyzer
from Parser import OperatorPrecedenceGrammar


if __name__ == '__main__':
    le = LexicalAnalyzer()
    le.formatter()
    le.scanner()
    le.show_all()
    le.output_target_dir()
    state_grammar = [
        'L → S | S ; L',
        'S → i := E',
        'E → '
    ]
    terminals = ['#', '(', ')', ';', 'i']
    v_terminals = ['A', 'S', 'D', 'R', 'P']

    g = OperatorPrecedenceGrammar(symbols=le.get_symbols())
    g.set_grammar_FIRSTVT_LASTVT()
    g.set_grammar_priority_table()
    g.show_all()
    g.reduction()


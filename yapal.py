import argparse
import src.YAPAL_TOKENIZER as tokenizer
from src._yapal_seq import YapalSequencer as yapal_seq
from src.grammar import Grammar
from ygenerator import yalex


def main():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('yal_file', type=str,
                        help='File with the lexical analyzer specification (.yal)')
    parser.add_argument('yapl_file', type=str,
                        help='File with the syntax analyzer specification (.yapl)')
    parser.add_argument('input_file', type=str,
                        help='File with input strings for both generators')

    args = parser.parse_args()

    print('INPUT FILES')

    print(f"Lexical file: {args.yal_file}")
    print(f"Syntax file: {args.yapl_file}")
    print(f"Input file: {args.input_file}")

    print('*'*80)
    # Execute the command below to run the lexical analyzer
    dir_dfa = yalex(args.yal_file, '.', False, False, False)
    tokens = dir_dfa.returnDict.keys()

    print('*'*80)

    yapal_tokens = tokenizer.analyze(args.yapl_file, False)

    ypsq = yapal_seq(yapal_tokens)

    print("YAPAL SEQUENCER")

    print(f"Defined tokens: {ypsq.get_defined_tokens()}")
    print(f"Ignored tokens: {ypsq.get_ignored_tokens()}")
    print(f"Terminals: {ypsq.get_terminals()}")
    print(f"Non terminals: {ypsq.get_non_terminals()}")
    print(f"Productions:")

    print('-'*80)
    # Compare the YALEX Tokenizer with the YAPAL Tokenizer

    print("IMPORTANT!")
    if ypsq.compare_tokens(tokens):
        print("All the tokens used in YAPAL are defined in YALEX")

    else:
        print("Some tokens used in YAPAL are not defined in YALEX")
    print("IMPORTANT!")

    print('*'*80)

    grammar = Grammar(ypsq.get_defined_productions())
    print(grammar)

    print('*'*80)

    C, relations = grammar.items(ypsq.get_symbols())

    print("YAPAL")
    print("ITEMS")
    for i, item in enumerate(C):
        print(f"I{i}: {item}")

    print("RELATIONS")
    for i, relation in enumerate(relations):
        print(f"R{i}: {relation}")

    grammar.draw(C, relations, "LRAutomaton")


if __name__ == "__main__":
    main()

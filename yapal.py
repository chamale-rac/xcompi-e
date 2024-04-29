import argparse
import src.YAPAL_TOKENIZER as tokenizer
from src._yapal_seq import YapalSequencer as yapal_seq
from src.grammar import Grammar


def main():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('yal_file', type=str,
                        help='File with the lexical analyzer specification (.yal)')
    parser.add_argument('yapl_file', type=str,
                        help='File with the syntax analyzer specification (.yapl)')
    parser.add_argument('input_file', type=str,
                        help='File with input strings for both generators')

    args = parser.parse_args()

    print(f"Lexical file: {args.yal_file}")
    print(f"Syntax file: {args.yapl_file}")
    print(f"Input file: {args.input_file}")

    yapal_tokens = tokenizer.analyze(args.yapl_file, False)

    ypsq = yapal_seq(yapal_tokens)

    print(f"Defined tokens: {ypsq.get_defined_tokens()}")
    print(f"Ignored tokens: {ypsq.get_ignored_tokens()}")
    print(f"Terminals: {ypsq.get_terminals()}")
    print(f"Non terminals: {ypsq.get_non_terminals()}")
    print(f"Productions:")

    grammar = Grammar(ypsq.get_defined_productions())
    print(grammar)

    # Let's use an example set of items to compute its closure
    # Starting item with the dot at the beginning
    example_items = {("expression'", ('expression',), 0)}

    # Compute the closure of the example set of items
    kernel_items, non_kernel_items = grammar.closure(example_items)
    print(kernel_items)
    print(non_kernel_items)


if __name__ == "__main__":
    main()

import argparse
import src.YAPAL_TOKENIZER as tokenizer
from src._yapal_seq import YapalSequencer as yapal_seq


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
    for production in ypsq.get_defined_productions():
        print(f"  {production}")


if __name__ == "__main__":
    main()

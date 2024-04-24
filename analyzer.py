import argparse
from colorama import Fore, Style


from src.utils.tools import readFile, load_from_pickle
from src._dir_dfa import DirectDeterministicFiniteAutomaton as DFA
from src._tokenizer import Tokenizer


def analyze():
    symbolTable = []

    parser = argparse.ArgumentParser(description="Lexer Analyzer")
    parser.add_argument('read_file_path', type=str,
                        help='The .txt to tokenize')  # Read from file
    parser.add_argument('analyzer_file_path', type=str,
                        help='The .pkl file that has the analyzer')  # The analyzer file path

    args = parser.parse_args()

    read_file_path = args.read_file_path
    analyzer_file_path = args.analyzer_file_path

    fileContent = readFile(read_file_path)
    print(f'✔ File read successfully from {read_file_path}')

    # Check is not empty
    if len(fileContent) == 0:
        print('✖ File is empty!')
        return

    tokenized = Tokenizer(fileContent, useExtraSoftCodify=True)
    unCodified = tokenized.unCodified
    codified = tokenized.codified
    codified.append('#')

    # Load the structure from the pickle file
    structure: DFA = load_from_pickle(analyzer_file_path)
    print(f'✔ Analyzer loaded successfully from {analyzer_file_path}')

    print('-' * 10, 'ANALYSIS', '-' * 10)

    forward = 0
    while forward < len(fileContent):
        match, idx = structure.specialSimulate(
            codified[forward:]
        )
        if match is False:
            print(Fore.RED + '✖ No match found!' + Style.RESET_ALL)
            print(f'[{forward}:{forward+idx}]', 'No match')
            # Print skipping
            print(Fore.YELLOW + 'Skipping this token...' + Style.RESET_ALL)
            print(Fore.RED + '-'*31)
            print('-'*31 + Style.RESET_ALL)
            forward += 1
        else:
            print(Fore.GREEN + '✔ Match found!' + Style.RESET_ALL)
            print(f'[{forward}:{forward+idx}]', match,
                  '->', unCodified[forward:forward + idx])
            symbolTable.append((match, unCodified[forward:forward + idx]))
            print(Fore.YELLOW +
                  'Executing the attached python code...' + Style.RESET_ALL)
            # Remove first and last character
            code = structure.returnDict[match][1:-1]
            # Consider the code may have characters like \n so first we need not treat them as a character but as the special character
            code = code.encode().decode('unicode_escape')
            print(Fore.CYAN + 'Code to be executed:\n' + code + Style.RESET_ALL)
            try:
                exec(code)
            except Exception as e:
                print(Fore.RED + 'On running return, found error:',
                      e, Style.RESET_ALL)

            forward += idx
            print(Fore.RED + '-'*31)
            print('-'*31 + Style.RESET_ALL)
    print('Analysis finished!')
    return symbolTable


def main():
    analyze()


if __name__ == "__main__":
    main()
    print('Exiting...')
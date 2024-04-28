class YapalSequencer(object):
    """
    This class represents the YAPAL sequencer, which processes a list of tokens representing
    a grammar specification and extracts terminals, nonterminals, and productions.
    """

    def __init__(self, tokens) -> None:
        self.tokens = tokens

        self.sequence()

    def sequence(self):
        """
        This function processes the tokens and extracts terminals, nonterminals, and productions.
        """
        if self.splitBySpt():
            self.removeAnyCm()
            self.extractDefinitions()

    def splitBySpt(self):
        try:
            # Find the index of the split token
            split_index = self.tokens.index(('spt', '%%'))

            # Split the tokens into definitions and productions
            self.definitions = self.tokens[:split_index]
            self.productions = self.tokens[split_index+1:]

            return True
        except ValueError:
            # Split token not found
            return False

    def removeAnyCm(self):
        """
        This function removes any comments from the tokens.
        """
        self.tokens = [token for token in self.tokens if token[0] != 'cm']

    def extractDefinitions(self):
        """
        This function extracts the definitions from the tokens.
        """
        self.defined_tokens = set()
        self.ignore_tokens = set()

        flag_have_svd = False
        flag_have_ignore = False

        while self.definitions:
            # Extract the definition
            definition = self.definitions.pop(0)
            if definition[0] == 'nl':
                flag_have_svd = False
                flag_have_ignore = False
            elif definition[0] == 'svd':
                flag_have_svd = True
            elif flag_have_svd:
                if definition[0] == 'mayus':
                    self.defined_tokens.add(definition[1])
                    # TODO handle error minus here
            elif definition[0] == 'mayus' and definition[1] == 'IGNORE':
                flag_have_ignore = True
            elif flag_have_ignore:
                if definition[0] == 'mayus':
                    self.ignore_tokens.add(definition[1])

    def get_defined_tokens(self):
        """
        This function returns the defined tokens.
        """
        return self.defined_tokens

    def get_ignored_tokens(self):
        """
        This function returns the ignore tokens.
        """
        return self.ignore_tokens

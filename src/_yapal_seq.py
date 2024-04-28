from re import T


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
            self.extractProductions()

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

    def extractProductions(self):
        """
        This function extracts the productions from the tokens.
        """
        self.terminals = set()
        self.non_terminals = set()
        self.defined_productions = []

        name = None
        has_name = False
        this_production = []
        this_productions = []
        this_terminals = []

        while self.productions:
            # Extract the production
            production = self.productions.pop(0)

            if production[0] == 'minus' and has_name is not True:
                name = production[1]
            elif production[0] == 'stat':  # :
                has_name = True
            elif has_name and production[0] in ['mayus', 'minus']:
                this_production.append(production[1])
                this_terminals.append(production[1])
            elif has_name and production[0] == 'rpt':  # |
                this_productions.append(this_production)
                this_production = []
            elif has_name and production[0] == 'end':  # ;
                this_productions.append(this_production)
                has_name = False
                self.non_terminals.add(name)
                self.terminals.update(this_terminals)
                this_production = []

                for production in this_productions:
                    self.defined_productions.append((name, tuple(production)))

                this_productions = []

    def get_terminals(self):
        """
        This function returns the terminals.
        """
        return self.terminals

    def get_non_terminals(self):
        """
        This function returns the non-terminals.
        """
        return self.non_terminals

    def get_defined_productions(self):
        """
        This function returns the defined productions.
        """
        return self.defined_productions

class Grammar(object):
    def __init__(self, productions) -> None:
        self.productions = productions
        self.start_symbol = productions[0][0]
        self.nonterminals = {prod[0] for prod in productions}
        self.augment()

    def augment(self) -> None:
        new_start_symbol = f"{self.start_symbol}'"
        new_start_production = (new_start_symbol, (self.start_symbol,))
        self.productions.insert(0, new_start_production)
        self.nonterminals.add(new_start_symbol)
        self.start_symbol = new_start_symbol

    def closure(self, items) -> None:
        items = [
            (item[0], item[1], item[2]) for item in items
        ]

        closure_set = set(items)
        kernel_items = set()

        for item in items:
            kernel_items.add(item)

        while True:
            new_items = set()
            for (head, body, dot_position) in closure_set:
                # Only proceed if the dot is before a non-terminal and not at the end of the production
                if dot_position < len(body) and body[dot_position] in self.nonterminals:
                    B = body[dot_position]
                    for production in self.productions:
                        if production[0] == B:
                            # For each production B -> γ, add B -> .γ to the closure if not already present
                            new_item = (B, production[1], 0)
                            if new_item not in closure_set:
                                new_items.add(new_item)

                    if dot_position > 0:
                        kernel_items.add((head, body, dot_position))

            if not new_items:
                break

            closure_set.update(new_items)

        non_kernel_items = closure_set - kernel_items

        closure_set = set()

        # To all the non_kernel_items add the 4th parameter as False
        for item in non_kernel_items:
            head, body, dot_position = item
            closure_set.add((head, body, dot_position, False))

        # To all the kernel_items add the 4th parameter as True
        for item in kernel_items:
            head, body, dot_position = item
            closure_set.add((head, body, dot_position, True))

        return closure_set

    def goto(self, items, symbol) -> None:
        goto_items = set()

        for item in items:
            head, body, dot_position, is_kernel = item
            if dot_position < len(body) and body[dot_position] == symbol:
                new_item = (head, body, dot_position + 1, True)
                goto_items |= self.closure({new_item})

        return goto_items

    def items(self, terminals):
        C = [self.closure(
            {(self.start_symbol, self.productions[0][1], 0, True)})]
        relations = []

        symbols = list(self.nonterminals.union(set(terminals)))

        while True:
            new_sets_added = False
            for idx, I in enumerate(C):
                for X in symbols:
                    goto_set = self.goto(I, X)

                    if goto_set and goto_set not in C:
                        C.append(goto_set)
                        relations.append((idx, len(C) - 1, X))
                        new_sets_added = True
            if new_sets_added:
                break

        return C, relations

    def __str__(self) -> str:
        return "\n".join([str(production) for production in self.productions])

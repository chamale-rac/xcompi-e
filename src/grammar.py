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
        closure_set = set(items)
        kernel_items = set()

        kernel_items.update(items)

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

            # If no new items were added, we're done
            if not new_items:
                break

            # Add the new items to the closure set and repeat
            closure_set.update(new_items)

        non_kernel_items = closure_set - kernel_items

        return kernel_items, non_kernel_items

    def __str__(self) -> str:
        return "\n".join([str(production) for production in self.productions])

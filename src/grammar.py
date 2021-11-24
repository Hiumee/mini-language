# 1.a. recursive descendent

class Grammar:
    def __init__(self, filename):
        self.nonTerminals = []
        self.terminals = []
        self.productions = {}
        self.starting = ""
        self.read_from_file(filename)

    def read_from_file(self, filename):
        with open(filename) as f:
            data = f.read()

        data = data.split("\n")

        for nonTerminal in data[0].split(" "):
            self.nonTerminals.append(nonTerminal)

        self.starting = self.nonTerminals[0]

        for terminal in data[1].split(" "):
            self.terminals.append(terminal)

        for production in data[2:]:
            sides = production.split("=", 1)

            left = sides[0].strip()

            if len(left.split(" ")) > 1:
                raise Exception("Not a context free grammar")

            right = sides[1].strip()

            results = []

            for r in right.split("|"):
                results.append([x.strip() for x in r.strip().split(" ")])

            if left not in self.productions:
                self.productions[left] = []

            for r in results:
                self.productions[left].append((left, r))

    def get_products_from_nonterminal(self, nonterminal):
        if nonterminal not in self.productions:
            raise Exception("Given symbol is not a nonterminal")

        return self.productions[nonterminal]

    def is_terminal(self, symbol):
        return symbol in self.terminals


if __name__ == "__main__":
    g = Grammar("g1.txt")

    while True:
        print("x. Exit")
        print("1. Print productions")
        print("2. Print terminals")
        print("3. Print nonterminals")
        print("4. Products for a given nonterminal")

        x = input()
        if x == "x":
            break
        elif x == "1":
            print(g.productions)
        elif x == "2":
            print(g.terminals)
        elif x == "3":
            print(g.nonTerminals)
        elif x == "4":
            nont = input("Enter a nonterminal: ")
            print(g.get_products_from_nonterminal(nont))


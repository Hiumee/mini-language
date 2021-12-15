from grammar import Grammar
from enum import Enum

class StateMode(Enum):
    NORMAL = 1
    BACK = 2
    FINAL = 3
    ERROR = 4

class Parser:
    def __init__(self, grammar, debug = False):
        self.debug = debug
        self.grammar = grammar

    def parse(self, data):
        self.state = StateMode.NORMAL
        self.position = 0
        self.working_stack = []
        self.input_stack = [self.grammar.starting]

        while self.state != StateMode.FINAL and self.state != StateMode.ERROR:
            if self.debug:
                print(self.state, self.position)
                print(self.working_stack)
                print(self.input_stack)
                print()
            if self.state == StateMode.NORMAL:
                if self.position == len(data) and len(self.input_stack) == 0:
                    self.success()
                else:
                    if len(self.input_stack) > 0 and not self.grammar.is_terminal(self.input_stack[0]):
                        self.expand()
                    else:
                        if len(self.input_stack) > 0 and self.position < len(data) and self.input_stack[0] == data[self.position][0]:
                            self.advance()
                        else:
                            print("Not found")
                            print(data[self.position][0])
                            self.momentary_insuccess()
            else:
                if self.state == StateMode.BACK:
                    if len(self.working_stack[-1]) == 1:
                        self.back()
                    else:
                        self.another_try()

        if self.state == StateMode.ERROR:
            if self.debug:
                print("Error while parsing")
            return False
        else:
            if self.debug:
                print(self.working_stack)
                print()
                print("Parsing successful")
            return self.createTable()

    def createTable(self):
        table = {}
        pos = 1
        parent_stack = []
        parent_stack.append([0,1])

        for step in self.working_stack:
            parent = parent_stack[-1]
            parent_stack[-1][1] -= 1
            if parent_stack[-1][1] == 0:
                parent_stack = parent_stack[:-1]
            table[pos] = {"info": step[0], "parent": parent[0], "right": 0}
            if len(step) > 1:
                parent_stack.append([pos, len(step[1])])
            pos += 1

        for i in range(1, len(self.working_stack)+1):
            right = 0
            for j in range(len(self.working_stack),0,-1):
                if table[j]["parent"] == i:
                    table[j]["right"] = right
                    right = j

        return table

    def expand(self):
        if self.debug:
            print("expand")
        to_find = self.input_stack[0]
        print(to_find)
        production = self.grammar.get_products_from_nonterminal(to_find)[0]
        self.working_stack.append(production)
        self.input_stack = production[1] + self.input_stack[1:]

    def advance(self):
        if self.debug:
            print("advance")
        self.position += 1
        self.working_stack = self.working_stack + [(self.input_stack[0],)]
        self.input_stack = self.input_stack[1:]

    def momentary_insuccess(self):
        if self.debug:
            print("momentary_insuccess")
        self.state = StateMode.BACK

    def back(self):
        if self.debug:
            print("back")
        self.position -= 1
        self.input_stack.insert(0, self.working_stack[-1][0])
        self.working_stack = self.working_stack[:-1]

    def another_try(self):
        if self.debug:
            print("another_try")

        last_production = self.working_stack[-1]

        productions = self.grammar.get_products_from_nonterminal(last_production[0])
        i = 0
        while productions[i] != last_production:
            i += 1
        i += 1

        if i >= len(productions):
            if self.position == 0 and last_production[0] == self.grammar.starting:
                self.state = StateMode.ERROR
                return
            self.input_stack = [self.working_stack[-1][0]] + self.input_stack[len(productions[i-1][1]):]
            self.working_stack = self.working_stack[:-1]
        else:
            self.state = StateMode.NORMAL
            self.working_stack[-1] = productions[i]
            self.input_stack = productions[i][1] + self.input_stack[len(productions[i-1][1]):]

    def success(self):
        if self.debug:
            print("success")
        self.state = StateMode.FINAL

    def set_state(self, state, position, working_stack, input_stack):
        self.state = state
        self.position = position
        self.working_stack = working_stack
        self.input_stack = input_stack

    def assert_state(self, state, position, working_stack, input_stack):
        assert(state == self.state)
        assert(position == self.position)
        assert(working_stack == self.working_stack)
        assert(input_stack == self.input_stack)

def parsing_table_string(table):
    s = ""
    for k in table:
        v = table[k]
        s += f"{k},{v['info']},{v['parent']},{v['right']}\n"
    return s

# tests
def test_expand():
    parser = Parser(Grammar("testing.txt"))

    # (q,3, S1aS2b,A) |- (q,3,S1aS2bA1,bA) 
    parser.set_state(StateMode.NORMAL, 3, [('S', ['a', 'S']), ('a',), ('S', ['b', 'A']), ('b',)], ['A'])
    parser.expand()
    # Add the first production of the head of the input stack to the working stack and replace the head with the production result
    parser.assert_state(StateMode.NORMAL, 3, [('S', ['a', 'S']), ('a',), ('S', ['b', 'A']), ('b',), ('A', ['b', 'A'])], ['b', 'A'])

def test_advance():
    parser = Parser(Grammar("testing.txt"))

    # (q,3,S1aS2bA1,bA) |- (q,4,S1aS2bA1b,A)
    parser.set_state(StateMode.NORMAL, 3, [('S', ['a', 'S']), ('a',), ('S', ['b', 'A']), ('b',), ('A', ['b', 'A'])], ['b', 'A'])
    parser.advance()
    # Add terminal from input stack to working stack and increment position
    parser.assert_state(StateMode.NORMAL, 4, [('S', ['a', 'S']), ('a',), ('S', ['b', 'A']), ('b',), ('A', ['b', 'A']), ('b',)], ['A'])

def test_momentary_insuccess():
    parser = Parser(Grammar("testing.txt"))

    # (q,2,S1aS1,aS) |- (b,2,S1aS1,aS)
    parser.set_state(StateMode.NORMAL, 2, [('S', ['a', 'S']), ('a',), ('S', ['a', 'S'])], ['a', 'S'])
    parser.momentary_insuccess()
    # Sets the state to back
    parser.assert_state(StateMode.BACK, 2, [('S', ['a', 'S']), ('a',), ('S', ['a', 'S'])], ['a', 'S'])

def test_back():
    parser = Parser(Grammar("testing.txt"))

    # (b,4,S1aS2bA1b,A) |- (b,3,S1aS2bA1,bA)
    parser.set_state(StateMode.BACK, 4, [('S', ['a', 'S']), ('a',), ('S', ['b', 'A']), ('b',), ('A', ['b', 'A']), ('b',)], ['A'])
    parser.back()
    # Decrement the position, move the terminal head from the working stack to the input stack
    parser.assert_state(StateMode.BACK, 3, [('S', ['a', 'S']), ('a',), ('S', ['b', 'A']), ('b',), ('A', ['b', 'A'])], ['b', 'A'])

def test_another_try():
    parser = Parser(Grammar("testing.txt"))

    # (b,2,S1aS1,aS) |- (q,2,S1aS2,bA)
    parser.set_state(StateMode.BACK, 2, [('S', ['a', 'S']), ('a',), ('S', ['a', 'S'])], ['a', 'S'])
    parser.another_try()
    # Set the state to normal, decrement the position, move the terminal head from the working stack to the input stack
    parser.assert_state(StateMode.NORMAL, 2, [('S', ['a', 'S']), ('a',), ('S', ['b', 'A'])], ['b', 'A'])

def test_success():
    parser = Parser(Grammar("testing.txt"))

    # (q,0,[],[]) |- (f,0,[],[])
    parser.set_state(StateMode.NORMAL, 0, [], [])
    parser.success()
    # Sets the state to final
    parser.assert_state(StateMode.FINAL, 0, [], [])

def test_parser_success():
    parser = Parser(Grammar("testing.txt"))

    assert(parser.parse([(x,0) for x in "abbc"]) == True)

def test_parser_fail():
    parser = Parser(Grammar("testing.txt"))

    assert(parser.parse([(x,0) for x in "ca"]) == False)

def run_tests():
    print("Tests\n")
    test_expand()
    print("Expand test passed")
    test_advance()
    print("Advance test passed")
    test_momentary_insuccess()
    print("Momentary insuccess passed")
    test_back()
    print("Back passed")
    test_another_try()
    print("Another try passed")
    test_success()
    print("Success passed")
    test_parser_success()
    print("Parser correct passed")
    test_parser_fail()
    print("Parser incorrect passed\n\n")


if __name__ == "__main__":
    #run_tests()
    inp = "bcc"
    data = [(x,0) for x in inp]
    grammar = Grammar("g1.txt")

    parser = Parser(grammar, True)
    output_table = parser.parse(data)
    print(output_table)
    print(parsing_table_string(output_table))

    with open("parsing.out", "w") as f:
        f.write(parsing_table_string(output_table))

class FiniteAutomata:
    def __init__(self, fa_file):
        self.parse_file(fa_file)

    def parse_file(self, fa_file):
        with open(fa_file, "r") as f:
            data = f.read()

        components = data.split("\n") # 0 - states, 1 - alphabet, 2 - transitions, 3 - final states

        self.states = components[0].split(",")
        self.alphabet = components[1].split(",")
        self.transitions = [x.split(",") for x in components[2].split(";")]
        self.initial_state = components[3]
        self.final_states = components[4].split(",")

    def _check(self, sequence, current_state):
        if sequence == "":
            return current_state in self.final_states

        if sequence[0] not in self.alphabet:
            return False

        for transition in self.transitions:
            if transition[0] == current_state and transition[1] == sequence[0]:
                if self._check(sequence[1:], transition[2]):
                    return True

        return False

    def check_sequence(self, sequence):
        return self._check(sequence, self.initial_state)


if __name__ == "__main__":
    fa = FiniteAutomata("FA.in")

    while True:
        print("1. States")
        print("2. Alphabet")
        print("3. Transitions")
        print("4. Initial state")
        print("5. Final state")
        print("6. Check sequence")
        print("\nx. Exit")

        user_input = input()

        if user_input == '1':
            print("States:")
            print(fa.states)
        elif user_input == '2':
            print("Alphabet:")
            print(fa.alphabet)
        elif user_input == '3':
            print("Transitions:")
            for t in fa.transitions:
                print(f"{t[0]}, {t[1]} = {t[2]}")
        elif user_input == '4':
            print("Initial state:")
            print(fa.initial_state)
        elif user_input == '5':
            print('Final states:')
            print(fa.final_states)
        elif user_input == '6':
            print("Enter a sequence to check:")
            if fa.check_sequence(input()):
                print("The sequence is good")
            else:
                print("The sequence is bad")
        elif user_input == 'x':
            print("Exiting")
            break
        else:
            print("Invalid command")
        print("\n\n\n")


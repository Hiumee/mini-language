from symbol_table import SymbolTable

def main():
    st = SymbolTable()

    print(f"{st.add_token('a')=}")
    print(f"{st.add_token('d')=}")
    print(f"{st.add_token('b')=}")
    print(f"{st.add_token('c')=}")
    print(f"{st.add_token('23')=}")
    print(f"{st.add_token('c')=}")
    print(f"{st.add_token('a')=}")
    print(f"{st.add_token('23')=}")

    print()

    print(f"{st.get_position('a')=}")
    print(f"{st.get_position('b')=}")
    print(f"{st.get_position('c')=}")
    print(f"{st.get_position('d')=}")
    print(f"{st.get_position('e')=}")
    print(f"{st.get_position('23')=}")

if __name__ == "__main__":
    main()
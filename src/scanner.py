import re
from symbol_table import SymbolTable

RESERVED_WORDS = ["bool","int","char","str","list","test","while","else","and","or","read","write"]
OPERATORS = ["+","-","*","/","=","<",">"]
MULTICHAR_OP = ["<=",">=","==","<>"]
SEPARATORS = ["(",")","[","]","{","}"," ","\n"]

def detect(token):
    # Output:
    #   "reserved"   - reserved word
    #   "operator"   - operator
    #   "separator"  - separator
    #   "constant"   - number
    #   "identifier" - identifier
    #   "unknown"    - not fitting anywhere

    if token in RESERVED_WORDS:
        return "reserved"
    if token in OPERATORS or token in MULTICHAR_OP:
        return "operator"
    if token in SEPARATORS:
        return "separator"

    if token == "T" or token == "false" or re.fullmatch(r"(0|(-?[1-9][0-9]*))", token):
        return "constant"

    if re.fullmatch(r"[a-zA-Z_][a-zA-Z_0-9]*", token):
        return "identifier"

    return "unknown"

def generate_pif(tokens):
    pif = []
    st = SymbolTable()
    sts = {}

    for token, line_number in tokens:
        token_type = detect(token)
        if token_type in ("reserved", "operator", "separator"):
            pif.append((token, 0))
        elif token_type in ("identifier", "constant"):
            index = st.add_token(token)
            sts[index] = token
            pif.append((token_type, index))
        else:
            raise Exception(f"LEXICAL ERROR:\n`{token}` at line {line_number}")

    return pif

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def process_program(file_name):
    raw_program = read_file(file_name)
    tokens = []
    line_number = 0
    for line in raw_program.split("\n"):
        line_number += 1
        if len(line.strip()) == 0 or (len(line.strip()) > 0 and line.strip()[0] == "#"):
            continue

        # Add tokens
        line = line.strip()

        matches = re.findall(r"([A-Za-z_0-9]+)|(<=|>=|==|<>|[+\-*/=<>()\[\]{} \n])",line)

        for match in matches:
            for token in match:
                if token != "":
                    tokens.append((token, line_number))

        tokens.append(("\n",line_number))

    return generate_pif(tokens)

def test_output_program(program):
    data = process_program(program)

    for token, idd in data:
        if token == "identifier":
            print(f"ID_{idd}", end="")
        elif token == "constant":
            print(f"ID_{idd}", end="")
        else:
            print(token, end="")
g = ""
def test_program(program):
    try:
        result = process_program(program)
        global g
        g = result
    except Exception as e:
        print(e)
    print("Lexically correct")

    to_write = ""
    for token, idd in result:
        to_write += f"{token}:{idd};"

    with open("pif.out", "w") as f:
        f.write(to_write)

    with open("doc.txt", "r") as f:
        text = f.read()
    with open("st.out", "w") as f:
        f.write(text)

def read_pif(pif_file):
    with open(pif_file, "r") as f:
        data = f.read()

    entries = data.split(";")

    read_data = []

    for entry in entries:
        if entry != "":
            split = entry.split(":")
            token = split[0]
            idd = int(split[1])
            read_data.append((token, idd))

    return read_data

test_program("p1.bad")
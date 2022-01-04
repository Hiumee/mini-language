from scanner import test_program, read_pif
from grammar import Grammar
from parser_class import Parser, parsing_table_string



# inp = "bcc"
# pif = [(x,0) for x in inp]
# grammar = Grammar("g1.txt")

test_program("p1.bad")
pif = read_pif("pif.out")[:-1]
grammar = Grammar("g2.txt")

parser = Parser(grammar, True)
output_table = parser.parse(pif)

table_text = parsing_table_string(output_table)
print(table_text)
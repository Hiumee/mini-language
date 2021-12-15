from scanner import test_program, read_pif
from grammar import Grammar
from parser_class import Parser

test_program("p1.bad")

pif = read_pif("pif.out")

grammar = Grammar("g2.txt")
print(pif)

parser = Parser(grammar, True)
output_table = parser.parse(pif)
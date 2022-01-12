.PHONY: yacc
yacc:
	lex specif2.lxi
	byacc -d program.y
	gcc lex.yy.c y.tab.c -o parse -lfl
	./parse test.in

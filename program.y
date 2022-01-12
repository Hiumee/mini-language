%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define YYDEBUG 1
%}


%token INT
%token BOOL
%token STRING
%token CHAR
%token LIST
%token TEST
%token ELSE
%token READ
%token WRITE
%token WHILE
%token CONSTANT
%token IDENTIFIER
%token AND
%token OR
%token SEPARATOR_LP
%token SEPARATOR_RP
%token PLUS
%token MINUS
%token MUL
%token DIV


%start program

%%

program : statement optional_A ;
A : statement optional_A ;
optional_A : | A ;
statement : declaration_stmt | assing_stmt | conditional_stmt | io_stmt ;
declaration_stmt : type id ;
id : IDENTIFIER ;
type : basic_type | LIST_type ;
basic_type : INT | BOOL | STRING | CHAR ;
LIST_type : LIST basic_type ;
assing_stmt : id EQ expression ;
conditional_stmt : if_stmt | WHILE_stmt ;
stmt_block : LEFT_SQ program RIGHT_SQ ;
if_stmt : TEST logic_exp stmt_block B ;
B : | ELSE stmt_block B ;
WHILE_stmt : WHILE logic_exp stmt_block ;
io_stmt : READ_stmt | WRITE_stmt ;
READ_stmt : READ id ;
WRITE_stmt : WRITE expression ;
expression : arithmetic_exp | logic_exp ;
arithmetic_exp : term | term sign term ;
sign : PLUS | MINUS ;
term : factor | factor sing2 factor ;
sing2 : MUL | DIV ;
factor :  id | CONSTANT | SEPARATOR_LP arithmetic_exp SEPARATOR_RP ;
logic_exp :  CONSTANT | numeric_relation ;
numeric_relation : SEPARATOR_LP arithmetic_exp arithmetic_operatOR arithmetic_exp SEPARATOR_RP ;
arithmetic_operatOR : GR | LT ;

%%

yyerror(char *s)
{
  printf("%s\n", s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
  if(argc>1) yyin = fopen(argv[1], "r");
  if((argc>2)&&(!strcmp(argv[2],"-d"))) yydebug = 1;
  if(!yyparse()) fprintf(stderr,"\tO.K.\n");
}


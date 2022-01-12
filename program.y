%{
#include <stdio.h>
#include <stdlib.h>
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


%start program

%%

program : statement optional_A ;
A : new_line statement optional_A ;
optional_A : | A ;
new_line : '\n' ;
statement : declaration_stmt | assing_stmt | conditional_stmt | io_stmt ;
declaration_stmt : type id ;
id : IDENTIFIER ;
type : basic_type | LIST_type ;
basic_type : INT | BOOL | STRING | CHAR ;
LIST_type : LIST basic_type ;
assing_stmt : id '=' expression ;
conditional_stmt : if_stmt | WHILE_stmt ;
stmt_block : '{' optional_new_line program optional_new_line '}' ;
optional_new_line : new_line |  | new_line optional_new_line ;
if_stmt : TEST logic_exp stmt_block B ;
B : | ELSE stmt_block B ;
WHILE_stmt : WHILE logic_exp stmt_block ;
io_stmt : READ_stmt | WRITE_stmt ;
READ_stmt : READ id ;
WRITE_stmt : WRITE expression ;
expression : arithmetic_exp | logic_exp ;
arithmetic_exp : term | term sign term ;
sign : '+' | '-' ;
term : factor | factor sing2 factor ;
sing2 : '*' | '/' ;
factor :  id | CONSTANT | '(' arithmetic_exp ')' ;
logic_exp :  CONSTANT | numeric_relation ;
numeric_relation : '(' arithmetic_exp arithmetic_operatOR arithmetic_exp ')' ;
arithmetic_operatOR : '>' | '<' ;

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


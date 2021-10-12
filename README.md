# mini-language

This is a language made for the FLCD course.

# Examples of programs

## Max of 3 numbers
Used: declaration, assignation, io operations, if-else statement
```
int number1
int number2
int number3

int max

read number1
read number2
read number3

test (number1 > number2) {
    max = number1
}
else {
    max = number2
}

test (number3 > max) {
    max = number3
}

write max
```

## Get n-th fibonacci number
Newly used: while loop, arithmetic and logic expression
```
int last_1
int last_2
int index

last_1 = 1
last_2 = 1

read index

while (index > 2) {
    int new
    new = last_1 + last_2
    last_2 = last_1
    last_1 = new
    index = index - 1
}

write last_1
```

## Get the average of numbers from input
Newly used: lists (declaration, element access)
```
int count
int sum
int i

list int numbers

sum = 0

read count
i = count

while (i > 0) {
    i = i - 1
    read numbers[i]
}

i = count

while (i > 0) {
    i = i - 1
    sum = sum + numbers[i]
}

write sum / count
```

# Specification
## Tokens
+ `=` - assinment operator
+ `+`, `-`, `*`, `/` - common mathematical operators
+ `<`, `<=`, `>`, `>=`, `==`, `<>` - common logical operators
+ `and`, `or` - logical operators
+ space, newline, `(`, `)`, `[`, `]`, `{`, `}` - separators
+ `int`, `bool`, `char`, `string` - data types
+ `test`, `while`, `else` - statement-specific keywords

## EBNF
```ebnf
letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" | "_"
non_zero_digit = "1" | "2" | ... | "9"
zero = "0"
digit = zero | non_zero_digit
character = letter | digit

identifier = letter {(letter|digit)}

BOOL_CONSTANT = "T" | "F"
INT_CONSTANT = zero | ["-"] non_zero_digit {digit}
CHAR_CONSTANT = "'" character "'"
STR_CONSTANT = """ {character} """
```

```ebnf
program = {statement new_line}

new_line = <new line>   \n

statement = declaration_stmt |
            assign_stmt      |
            conditional_stmt |
            io_stmt

declaration_stmt = type IDENTIFIER

id = IDENTIFIER | id "[" arithmetic_exp "]"

type = basic_type | list_type
basic_type = "int" | "bool" | "string" | "char"
list_type = "list" basic_type

assign_stmt = id "=" expression

conditional_stmt = if_stament | while_stmt

stmt_block = "{" program "}"

if_stmt = "test" logic_exp stmt_block ["else" stmt_block]
while_stmt = "while" logic_exp stmt_block

io_stmt = read_stmt | write_stmt

read_stmt = "read" id
write_stmt = "write" expression

expression = arithmetic_exp | logic_exp

arithmetic_exp = arithmetic_exp ("+" | "-") arithmetic_exp | term
term = term ("*" | "/") term | factor
factor = "(" arithmetic_exp ")" | id | INT_CONSTANT

logic_exp = "(" logic_exp ("and"|"or"|"=="|"<>") logic_exp ")" | BOOL_CONSTANT | numeric_relation

numeric_relation = "(" arithmetic_exp ("<"|"<="|"=="|"<>"|">="|">") arithmetic_exp ")"
```
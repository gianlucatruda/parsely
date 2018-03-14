# import system library
from sys import *

# import our lexer and parser
import g4_lexer as lexer
import g4_parser as parser

# takes user input for filename, else compiles default file
fname = "file.g4"
if len(argv) == 2: # user gave exactly one filename
	fname = argv[1]
else: # user gave no parameters or more than one
	print("No filename or invalid filename given, so using file.g4")

# generate a "token stream" from lexer
data = lexer.open_file(fname)
toks = lexer.lex(data)

# instantiate a parser
p = parser.ExpressionTreeBuilder()

# pass "token stream" in line by line to parser
for line in toks:
	print(p.parse(line))

# ASSIGNMENT = DONE!!!!

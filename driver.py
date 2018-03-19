# import system library to allow terminal arguments
from sys import *

# import our lexer and parser
import parsely_lexer as lexer
import parsely_parser as parser

# import tree visualiser (only if you have all dependencies)
visualise = False
try:
	import treevis as vis
	visualise = True
except ImportError:
	visualise = False

# takes user input for filename, else compiles default file
fname = "file.prsly"
if len(argv) == 2: # user gave exactly one filename
	fname = argv[1]
else: # user gave no parameters or more than one
	print("No filename or invalid filename given, so using file.prsly")

# generate a "token stream" from lexer
data = lexer.open_file(fname)
toks = lexer.lex(data)

# instantiate a parser
p = parser.ExpressionTreeBuilder()

# pass "token stream" in line by line to parser
for key, line in enumerate(toks):
	print(p.parse(line, key)) # prints the parsed code to terminal
	if visualise: # only if all dependencies are available
		# Generates a .png of syntax tree
		stm = vis.syntaxTreeMaker()
		stm.generate(p.parse(toks[key], key), key)
		# Generates a .png of parse tree
		ptm = vis.parseTreeMaker()
		ptm.generate(p.parse(toks[key], key), key)

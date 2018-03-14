import lexer
import parser

# TODO make this dynamic, but for now hardcode is fine
fname = "file.g4"

# generate a token stream from lexer
data = lexer.open_file(fname)
token_stream = lexer.lex(data)


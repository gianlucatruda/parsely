
RESERVED = 'RES'
INT = 'INT'
ID = 'ID'
OP = 'OP'
COMMENT = 'COMMENT'
WS = 'WS'
ENDL = 'ENDL'
token_exprs = [
	#whitespace
    (r'[ \n\t]+', None),
    #comments
    (r'#[^\n]*',  None),
    #list of reserved words
    (r'\(',  RESERVED),
    (r'\)',  RESERVED),
    (r';',   ENDL),
    (r'PLUS',  RESERVED),
    (r'MINUS',   RESERVED),
    (r'TIMES',  RESERVED),
    (r'DIVIDE',   RESERVED),
    (r'EQUALS',   RESERVED),
    (r'TALK_TO_THE_HAND', RESERVED),
    (r'\d+', INT),
    #id must start lowercase
    (r'[a-z][A-Za-z0-9_]*', ID),
]
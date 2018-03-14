
RESERVED = 'RES'
INT = 'INT'
STRING = 'STRING'
ID = 'ID'
OP = 'OP'
COMMENT = 'COMMENT'
WS = 'WS'
ENDL = 'ENDL'
MINUS = 'MINUS'
TIMES = 'TIMES'
PLUS = 'PLUS'
EQUALS = 'EQUALS'
DIVIDE = 'DIVIDE'
token_exprs = [
	#whitespace
    (r'[ \n\t]+', None),
    #comments
    (r'#[^\n]*',  None),
    #list of reserved words
    (r'\(',  RESERVED),
    (r'\)',  RESERVED),
    (r'(\'|")', RESERVED),
    (r'PLUS',  PLUS),
    (r'MINUS',   MINUS),
    (r'TIMES',  TIMES),
    (r'DIVIDE',   DIVIDE),
    (r'EQUALS',   RESERVED),
    (r'TALK_TO_THE_HAND', RESERVED),
    (r'\d+', INT),
    #id must start lowercase
    (r'[a-z][A-Za-z0-9_]*', ID),
    (r'[^"]*',STRING),
    (r"[^']*",STRING)
]
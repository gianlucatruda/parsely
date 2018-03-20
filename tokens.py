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
    #functions must start with an uppercase
    (r'[Pp][lL][uU][sS]',  PLUS),
    (r'[Mm][iI][nN][uU][sS]',   MINUS),
    (r'[Tt][iI][mM][eE][sS]',  TIMES),
    (r'[Dd][iI][vV][iI][dD][eE]',   DIVIDE),
    (r'[Ee][qQ][uU][aA][lL][sS]',   EQUALS),
    (r'\d+', INT),
    #id must start lowercase
    (r'[a-z][A-Za-z0-9_]*', ID),
    (r'[^"]*',STRING),
    (r"[^']*",STRING)
]

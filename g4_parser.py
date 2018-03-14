import re
import g4_tokens as tokens
import collections

# Defines the Token data type used by the lexer and parser
Token = collections.namedtuple('Token', ['type','value'])

'''
Implementation of a recursive descent parser. Each method
implements a single grammar rule. Use the ._accept() method
to test and accept the current lookahead token. Use the ._expect()
method to exactly match and discard the next token on on the input
(or raise a SyntaxError if it doesn't match).
'''
class ExpressionEvaluator:

	def parse(self, tokline):
		self.tokens = tokline
		self.tok = None # Last symbol consumed
		self.nexttok = None # Next symbol tokenized
		self._advance() # Load first lookahead token
		return self.expr()

	def _advance(self):
		'Advance one token ahead'
		self.tok = self.nexttok
		if len(self.tokens) > 0: # when there aren't any tokens left
			self.nexttok = self.tokens[0]
			self.tokens = self.tokens[1:]

	def _accept(self,toktype):
		'Test and consume the next token if it matches toktype'
		if self.nexttok.type == toktype:
			self._advance()
			return True
		else:
			return False

	def _expect(self,toktype):
		'Consume next token if it matches toktype or raise SyntaxError'
		if not self._accept(toktype):
			raise SyntaxError('Expected ' + toktype)

	def expr(self):
		"expression ::= term { ('plus'|'minus') term }*"
		exprval = self.term()
		while self._accept('PLUS') or self._accept('MINUS'):
			op = self.tok.type
			right = self.term()
			if op == 'PLUS':
				exprval += right
			elif op == 'MINUS':
				exprval -= right
		return exprval

	def term(self):
		"term ::= factor { ('times'|'divide') factor }*"
		termval = self.factor()
		while self._accept('TIMES') or self._accept('DIVIDE'):
			op = self.tok.type
			right = self.factor()
			if op == 'TIMES':
				termval *= right
			elif op == 'DIVIDE':
				termval /= right
		return termval

	def factor(self):
		"factor ::= INT | ( expr )"
		if self._accept('INT'):
			return int(self.tok.value)
		else:
			raise SyntaxError('Expected INT')

class ExpressionTreeBuilder(ExpressionEvaluator):

	def expr(self):
		"expression ::= term { ('plus'|'minus') term }"
		exprval = self.term()
		while self._accept('PLUS') or self._accept('MINUS'):
			op = self.tok.type
			right = self.term()
			if op == 'PLUS':
				exprval = ('plus', exprval, right)
			elif op == 'MINUS':
				exprval = ('minus', exprval, right)
		return exprval

	def term(self):
		"term ::= factor { ('times'|'divide') factor }"
		termval = self.factor()
		while self._accept('TIMES') or self._accept('DIVIDE'):
			op = self.tok.type
			right = self.factor()
			if op == 'TIMES':
				termval = ('times', termval, right)
			elif op == 'DIVIDE':
				termval = ('divide', termval, right)
		return termval

	def factor(self):
		'factor ::= INT | ( expr )'
		if self._accept('INT'):
			return int(self.tok.value)
		else:
			raise SyntaxError('Expected INT b')

# if parser is run directly, it will default to file.g4 and print output
if __name__ == '__main__':
	import g4_lexer as lexer
	e = ExpressionTreeBuilder()
	fname = "file.g4"
	data = lexer.open_file(fname)
	toks = lexer.lex(data)
	for line in toks:
		print(e.parse(line))


import re
import sys
import tokens
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

	def parse(self, tokline, line_num):
		self.line_num = line_num
		self.tokens = tokline
		self.tok = None # Last symbol consumed
		self.nexttok = None # Next symbol tokenized
		self._advance() # Load first lookahead token
		if self.nexttok.type != 'INT':
			print('Error on line', self.line_num,': Lines start with INT, but got', self.nexttok.type)
			sys.exit()
		return self.expr()

	def _advance(self):
		'Advance one token ahead'
		self.tok = self.nexttok
		if len(self.tokens) > 0: # when there are tokens left
			self.nexttok = self.tokens[0]
			self.tokens = self.tokens[1:]

	def _accept(self,toktype):
		'Test and consume the next token if it matches toktype'
		if self.nexttok.type == toktype:
			self._advance()
			return True
		else:
			return False

	# def _expect(self,toktype):
	# 	'Consume next token if it matches toktype or raise SyntaxError'
	# 	if not self._accept(toktype):
	# 		raise SyntaxError('Expected ' + toktype)

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
			print('Error on line', self.line_num,': After', self.tok.type ,'Expected an INT, but got', self.nexttok.type)
			sys.exit()

# if parser is run directly, it will default to file.prsly and print output
if __name__ == '__main__':
	import parsely_lexer as lexer
	e = ExpressionTreeBuilder()
	fname = "file.prsly"
	data = lexer.open_file(fname)
	toks = lexer.lex(data)
	for key, line in enumerate(toks):
		print(e.parse(line, key))


import re
import sys
import tokens
import collections

# Defines the Token data type used by the lexer and parser
Token = collections.namedtuple('Token', ['type','value'])

'''
Implementation of a recursive descent parser, inspired by chapter
2.19 of Python Cookbook (3rd Edition) by David Beazley and
Brian K. Jones, but modified to fit a newly defined grammar.
'''

class ExpressionTreeBuilder():

	def parse(self, tokline, line_num):
		'Called once to begin the parsing on given tokens.'
		self.line_num = line_num
		self.tokens = tokline
		self.tok = None # Last token
		self.nexttok = None # Next token
		self._advance() # Load next token
		# Below code checks that line begins with INT as expected
		if self.nexttok.type != 'INT':
			if not self.nexttok.type == 'ID':
				print('Error: Lines start with INT or ID, but got',
					self.nexttok.type)
				sys.exit()
			else:
				return self.assign()
		return self.expr()

	def _advance(self):
		'Advance the current and next tokens'
		self.tok = self.nexttok
		if len(self.tokens) > 0: # when there are tokens left
			self.nexttok = self.tokens[0]
			self.tokens = self.tokens[1:]
		else:
			self.nexttok = Token('None', 'null')

	def _accept(self,toktype):
		'Test (and consume) the next token if it matches token type'
		if self.nexttok:
			if self.nexttok.type == toktype:
				self._advance()
				return True
			else:
				return False
		else:
			return False

	def assign(self):
		'ASSIGN -> ID EQUALS EXP'
		val = self.nexttok.value

		if self._accept('ID'):
			if self._accept('EQUALS'):
				exp = self.expr()
				return ('equals', val, exp)
		else:
			print('Error after',
				self.tok.type ,': Expected an OPERATOR, but got',
				self.nexttok.type)
			sys.exit()

	def expr(self):
		'EXP -> EXP PLUS TERM | EXP MINUS TERM | TERM'
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
		'TERM -> TERM TIMES FACTOR | TERM DIVIDE FACTOR | FACTOR'
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
		'FACTOR -> EXP | INT | ID'
		if self._accept('INT') and not (self.nexttok.type == 'INT' or self.nexttok.type == 'ID'):
			return int(self.tok.value)
		elif self._accept('ID') and not (self.nexttok.type == 'INT' or self.nexttok.type == 'ID'):
			return self.tok.value
		elif (self.tok.type == 'INT' or self.tok.type == 'ID') and (self.nexttok.type == 'INT' or self.nexttok.type == 'ID'):
			print('Error after',
				self.tok.type ,': Expected an OPERATOR, but got',
				self.nexttok.type)
			sys.exit()
		else:
			print('Error after',
				self.tok.type ,': Expected an INT or ID, but got',
				self.nexttok.type)
			sys.exit()

'''
if parser is run directly, it will default to file.prsly
and print output to terminal.
'''
if __name__ == '__main__':
	import parsely_lexer as lexer
	e = ExpressionTreeBuilder()
	fname = "file.prsly"
	data = lexer.open_file(fname)
	toks = lexer.lex(data)
	for key, line in enumerate(toks):
		print(e.parse(line, key))


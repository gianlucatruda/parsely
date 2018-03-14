from sys import *
import re
import g4_tokens as tokens
import collections

# Defines the Token data type used by the lexer and parser
Token = collections.namedtuple('Token', ['type','value'])

def open_file(filename):
	data = open(filename, "r").read()
	return data

def lex(data):
	data = data.split('\n')
	tokenized = []

	for i in range(len(data)-1):
		tokenized.append(lexify(data[i], (i+1)))

	# The next few lines convert the token format for parser
	token_list = []
	for line in tokenized:
		if line != []:
			token_line = []
			for pair in line:
				token_line.append(Token(pair[1], pair[0]))
			token_list.append(token_line)

	return token_list


def lexify(data, line_num):
	pos = 0
	token_list = []
	str = ''
	#state = 1 means everything we're looking at is part of string
	state = 0

	while pos < len(data):
		match = None
		token_exprs = tokens.token_exprs
		for i in range(len(token_exprs)-2):
			pattern, tag = token_exprs[i]
			regex = re.compile(pattern)
			match = regex.match(data, pos)
			if match:
				str = match.group(0)
				#if its not a whitespace or comment
				if tag:
					if(tag == 'RES'):
						if(str == '"' or str == "'"):
							state = 0 if state == 1 else 1
							#we found a string
							if state == 1:
								pattern, tag = token_exprs[len(token_exprs)-2] if str == '"' else token_exprs[len(token_exprs)-1]
								regex = re.compile(pattern)
								match = regex.match(data, pos+1)
								str = match.group(0)
								token_list.append((str, tag))
								pos = match.end(0)
								break
							if state == 0:
								break
					if(tag == 'INT'):
						#we want to strip leading zeros except if its '0'
						if(len(str) > 1):
							str = str.lstrip('0')
					#create a token - text and tag tuple
					token = (str, tag)
					token_list.append(token)
				break
		if not match:
			print('Illegal character in line',line_num,'at position',pos,':\n'+ data,'\n'+ ' '*(pos-1), '^')
			sys.exit()
		else:
			pos = match.end(0)

	return token_list

# if lexer is run directly, prints out tokens for each line
if __name__ == '__main__':
	open_file(argv[1])
	data = open_file(argv[1])
	t_list = lex(data)
	for i in range(len(t_list)):
		print('line ', i, t_list[i])

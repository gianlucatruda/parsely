import sys
from sys import *
import re
import tokens
import collections

def open_file(filename):
	data = open(filename, "r").read()
	return data

def run():
	open_file(argv[1])
	data = open_file(argv[1])
	t_list = lex(data)
	for i in range (len(t_list)):
		print('line ', i+1, t_list[i])

def lex(data):
	pos = 0
	token_list = []
	str = ''
	#state = 1 means everything we're looking at is part of string
	state = 0
	sub_list = []
	while pos < len(data):
		match = None
		token_exprs = tokens.token_exprs
		for i in range(len(token_exprs)):
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
								sub_list.append((str, tag))
								pos = match.end(0)
								break
							if state == 0:
								break
					if(tag == 'INT'):
						#we want to strip leading zeros except if its '0'
						if(len(str) > 1):
							str = str.lstrip('0')
					if (tag == 'ENDL'):
						token_list.append(sub_list)
						sub_list = []
					#create a token - text and tag tuple
					else:
						token = (str, tag)
						sub_list.append(token)
				break
		if not match:
			print('Illegal character: %s' % data[pos], data[pos:])
			sys.exit()
		else:
				pos = match.end(0)

	# coverts token_list to parser format Token(type='NUM', value='2')
	Token = collections.namedtuple('Token', ['type','value'])
	new_tokens = []

	for i in token_list:
		for j in i:
			new_tokens.append(Token(j[1],j[0]))

	return new_tokens
	# return token_list



	print (str)
if __name__ == '__main__':
	run()

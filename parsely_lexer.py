import sys
import re
import tokens
import collections

# Defines the Token data type used by the lexer and parser
Token = collections.namedtuple('Token', ['type','value'])

def open_file(filename):
	#read the data from the file
	data = open(filename, "r").read()
	return data

def lex(data):
	#split on spaces
	data = data.split('\n')
	tokenized = []
	#loop through the list
	for i in range(len(data)-1):
		#then add to the list the tokenized line. (i+1) is used to get new line
		#since we skip comments it used to throw the lines out of sync
		tokenized.append(lexify(data[i], (i+1)))

	# The next few lines convert the token format for parser
	token_list = []
	for line in tokenized:
		#there was an error where the last line is [] and it crashed
		if line != []:
			#create an empty line
			token_line = []
			#each Token is a tuple so we call it pair
			for pair in line:
				#create a named token and append it to the line
				token_line.append(Token(pair[1], pair[0]))
			token_list.append(token_line)
	return token_list

def lexify(data, line_num):
	#set the pos to 0, which is the beginning of a line
	pos = 0
	#initialize empty list of tokens
	token_list = []
	#this is used for pattern matching but we just initialize it here
	str = ''
	#state = 1 means everything we're looking at is part of string, ie inside ' ' or " "
	#state = 0 means its everything else
	state = 0
	#import the list of token expressions
	token_exprs = tokens.token_exprs

	#while not at end of line
	while pos < len(data):
		#havent found a match yet
		match = None
		#loop through all RE to find the next expression that matches
		for i in range(len(token_exprs)-2):
			#token are presented as tuples (pattern, string)
			pattern, tag = token_exprs[i]
			#compile it using re module
			regex = re.compile(pattern)
			#then match the longest pattern in data starting from pos
			match = regex.match(data, pos)
			#if something is found
			if match:
				#store the longest matching pattern in str
				str = match.group(0)
				#if its not a whitespace or comment
				if tag:
					#if its a reserved symbol like '' or "" 
					if(tag == 'RES'):
						if(str == '"' or str == "'"):
							state = 0 if state == 1 else 1
							#we found a string
							if state == 1:
								if str == "":
									pattern, tag = token_exprs[len(token_exprs)-2]
								else:
									token_exprs[len(token_exprs)-1]
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
					#then add this to the list of tokens
					token_list.append(token)
				break
		#if the tokens aren't a match in any of the regex
		if not match:
			#print the error
			print('Illegal character in line',line_num,'at position',pos,
				':\n'+ data,'\n'+ ' '*(pos-1), '^')
			#exit program
			sys.exit()
		else:
			#if a match has been found and a token allocated, move the pos to the last character of the string
			pos = match.end(0)
	return token_list

'''
if lexer is run directly, it will default to file.prsly
and print output to terminal.
'''
if __name__ == '__main__':
	data = open_file('file.prsly')
	t_list = lex(data)
	for i in range(len(t_list)):
		print('line ', i, t_list[i])

# TOKENIZER AND PARSER FOR SPOT LANGUAGE

import ply.lex as lex #import ply library
from symbol import *
import global_config

#############################################################
# TOKENIZER
# Tokenizer Uses Ply library
#############################################################


# List of token names
token_names = [
	'PERIOD',
	'COMMA',
	'BANG',
	'INT',
	'STRING',
	'ADD_OP',
	'MIN_OP',
	'MUL_OP',
	'DIV_OP',
	'LPAREN',
	'RPAREN',
	'NAME'
]

reserved = {
	'this is' : 'THISIS',
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'or' : 'OR',
	'and' : 'AND',
	}

#All tokens
tokens = token_names + reserved.values()

# Token functions-----
t_INT = r'[0-9][0-9]*'
t_STRING = r'"[A-Za-z0-9_]*"'
t_NAME = r'[A-Za-z_][A-Za0-9_]*'

# operators
t_ADD_OP = r'\+'
t_MIN_OP = r'\-'
t_MUL_OP = r'\*'
t_DIV_OP = r'\/'

#delimiters
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Defines a rule for tracking line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
# A string containing ignored chars (spaces and tabs)
t_ignore = ' \t'

def t_error(t):
	print "Illegal character '%s' " % t.value[0]

# Build the lexer
spotlexer = lex.lex()

# Test data for the lexer
data = raw_input(">What would you like to parse? ")

# Lex the data
spotlexer.input(data)
#Lexer returns LexToken, with attributes: tok.type, tok.value, tok.lineno, tok.lexpos

#create lex_token list
lex_tokens = []
while True:
	tok = lex.token()
	if not tok: 
		break	
	lex_tokens.append(tok)

#token class definitions

class Token:
	def __init__(self, value=0):
		self.value = value
	def __repr__(self):
		return "<%s %r>" %(self.__class__.__name__, self.value)

class AddOpTok(Token):
	lbp = 20
	
	def nulld(self):
		return expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(20)
		return self

class EndTok(Token):
	lbp = 0
	def leftd(self):
		pass
	def nulld(self):
		pass

# create class token list
class_tokens = []
for lex_token in lex_tokens:
	if lex_token.type == 'INT':
		new_int_tok = Token(lex_token.value)
		class_tokens.append(new_int_tok)
	elif lex_token.type == 'ADD_OP':
		new_add_op_tok = AddOpTok()
		class_tokens.append(new_add_op_tok)
	new_end_tok = EndTok()
	class_tokens.append(new_end_tok)
print class_tokens

#####################################################################################################
# PARSER
# Top Down Precedence Parsing
###################################################################################################
		
def parse(program):
    global_config.next = tokenize(program).next
    global_config.token = global_config.next()
    return expression()

def statement():
	pass
def advance(id=None):
	if (id and global_config.token.id!=id):
		raise SyntaxError("Expected" + id + "but got " + global_config.token.id)
	global_config.token = lex_tokens.pop(0) 	

# Process:
# 5+5
# [(num, 5), (add, +), (num, 5)]
# create all the corresponding class instances
# parse those class instance tokens















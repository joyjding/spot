#TODOS
#generate class tokens in PLY Lexer (not very important)
#separate lexer file from tokenizer/parser (not very important)



# TOKENIZER AND PARSER FOR SPOT LANGUAGE

import ply.lex as lex #import ply library
from symbol import *
import global_config

####PLY Lexer. Takes in a string --> lextokens

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
	def nulld(self):
		return self
	def leftd(self):
		pass
	def __repr__(self):
		return "(%s, %r)" %(self.__class__.__name__, self.value)

class BinaryOpToken(Token):
	def __init__(self, value=0):
		Token.__init__(self)
		self.first = None
		self.second = None

class AddOpTok(BinaryOpToken):
	lbp = 20
	def nulld(self):
		return expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(20)
		return self
	def __repr__(self):
		#weird bug that has to do with representation...even though the result seems fine

		return "(%s, %r): self.first = %s, self.second = %s" %(self.__class__.__name__, self.value, self.first, self.second)
		#return "(%s, %r)" %(self.__class__.__name__, self.value) 

class SubOpTok(BinaryOpToken):
	lbp = 20

	def nulld(self):
		return -expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(20)
		return self

class MulOpTok(BinaryOpToken):
	lbp = 30

	def leftd(self, left):
		self.first = left
		self.second = expression(30)
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
	
	ltype = lex_token.type 
	lvalue = lex_token.value

	if ltype == 'INT':
		new_int_tok = Token(lvalue)
		class_tokens.append(new_int_tok)
	elif ltype == 'ADD_OP':
		new_add_op_tok = AddOpTok(lvalue)
		class_tokens.append(new_add_op_tok)
	elif ltype == 'SUB_OP':
		new_sub_op_tok = SubOpTok(lvalue)
	
new_end_tok = EndTok()
class_tokens.append(new_end_tok)
print class_tokens

#####################################################################################################
# PARSER
# Top Down Precedence Parsing
###################################################################################################
		

def statement():
	pass

def expression(rbp=0):
    t = global_config.token
    advance()
    left = t.nulld()
    while rbp < global_config.token.lbp:
        t = global_config.token
        advance()
        left = t.leftd(left) 
    return left

def advance(id=None):
	if (id and global_config.token.id!=id):
		raise SyntaxError("Expected" + id + "but got " + global_config.token.id) 
	global_config.token = class_tokens.pop(0)
	
	print "\n"
def parse():
    advance() #put something into global token
    print "parsing done"
    return expression()

    
# Process:
# 5+5
# [(num, 5), (add, +), (num, 5)]
# create all the corresponding class instances
# parse those class instance tokens















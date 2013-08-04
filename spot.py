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
	'NUMBER',
	'STRING',
	'OPERATOR',
	'NAME'
]

tokens = token_names

#-Token Functions----------------------------- 
t_NUMBER = r'[0-9][0-9]*'
t_STRING = r'"[A-Za-z0-9_]*"'
t_OPERATOR = r'[\+-/\*]'
t_NAME = r'[A-Za-z_][A-Za0-9_]*'

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

# Test data for lexer
data = raw_input(">What would you like to parse? ")
spotlexer.input(data)

#Lexer returns LexToken , with attributes: tok.type, tok.value, tok.lineno, tok.lexpos
lex_tokens = []
while True:
	tok = lex.token()
	if not tok: break
	tdict = {
			'id': tok.type, 
			'value' : tok.value,
			'token_num' : tok.lexpos
			}
	lex_tokens.append(tdict)
print lex_tokens
#####################################################################################################
# PARSER
# Top Down Precedence Parsing
###################################################################################################

symbol("(literal)")
symbol("(end)") 
infix("+", 10)
infix("-", 10)
infix("*", 20)
infix("/", 20)
prefix("+", 100)
prefix("-", 100)
symbol("(literal)").nud = lambda self: self

def tokenize(program):
    for lex_token in lex_tokens:
    	if (lex_token['id'] == 'NUMBER' or lex_token['id'] == 'STRING'):
    		symbol_class = symbol_dict["(literal)"]
    		new_symbol = symbol_class()
    		new_symbol.value = lex_token['value']
    		yield new_symbol
    	elif lex_token['id'] == 'OPERATOR':
    		symbol_class = symbol_dict.get(lex_token['value'])
    		if not symbol_class:
    			raise SyntaxError("Unknown operator")
    		yield symbol_class() #make a new instance of the operator prototype class. No need to set a value b/c operators don't have values.
    	elif lex_token['id'] == 'NAME':
    		scope.find(lex_token['value'])
		
    new_symbol = symbol_dict["(end)"]
    yield new_symbol()

def parse(program):
    global_config.next = tokenize(program).next
    global_config.token = global_config.next()
    return expression()

class Scope:
	scope_names = {}
	
	def define(self, name):
		exists = scope_names.get(name.value)
		if not exists:
			scope_names[name.value] = name
		name.nud = lambda self: self
		name.led = None
		name.lbp = 0
		#return name - doesn't seem necc right now
	def find(self, name):
		defined = scope_names.get(name)
		if not defined:
			raise SyntaxError("name not defined")
		return defined

global_config.scope = Scope()














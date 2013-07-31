#-----------------------------
# Tokenizer and Parser for spot language
# Tokenizer Uses Ply library
#-----------------------------

import ply.lex as lex #import ply library

# List of token names
token_names = [
	'INT',
	'ADD_OP',
	'SUB_OP',
]

tokens = token_names

#-Token Functions-------------- 
t_INT = r'[0-9][0-9]*'
t_ADD_OP = r'\+'
t_SUB_OP = r'-'

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
data = "1-1"
spotlexer.input(data)

#Lexer returns LexToken , with attributes: tok.type, tok.value, tok.lineno, tok.lexpos
while True:
	tok = lex.token()
	if not tok: break
	print tok

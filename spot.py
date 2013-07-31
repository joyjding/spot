# TOKENIZER AND PARSER FOR SPOT LANGUAGE
#-----------------------------
# TOKENIZER
# Tokenizer Uses Ply library
#-----------------------------

import ply.lex as lex #import ply library

# List of token names
token_names = [
	'INT',
	'ADD_OP',
	'SUB_OP',
	'MUL_OP',
	'DIV_OP',
]

tokens = token_names

#-Token Functions-------------- 
t_INT = r'[0-9][0-9]*'
t_ADD_OP = r'\+'
t_SUB_OP = r'-'
t_MUL_OP = r'\*'
t_DIV_OP = r'/'

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
data = "1-1*2 3/"
spotlexer.input(data)

#Lexer returns LexToken , with attributes: tok.type, tok.value, tok.lineno, tok.lexpos
lex_tokens = []
while True:
	tok = lex.token()
	if not tok: break
	tok = tok.type, tok.value
	lex_tokens.append(tok)

print lex_tokens
#-----------------------------
# PARSER
# Top Down Precedence Parsing
#-----------------------------

# Declare global token variable that contains the current token
global token















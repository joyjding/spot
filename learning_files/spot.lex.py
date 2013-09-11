#-----------------------------
# Tokenizer for spot language
# Uses Ply library
# Started 7/23/2013
#-----------------------------

import ply.lex as lex

#-Tokens----------------------
# List of token names
token_names = [
	'ID',
	'PERIOD',
	'COMMA',
	'BANG'
	]

# Dictionary of reserved keywords
reserved = {
	'this': 'THIS', #TODO: decide about capitalizations later
	'is': 'IS',
	'can': 'CAN'
	}

# All tokens
tokens = token_names + reserved.values()

#-Token Functions-------------- 

t_CAN = r'can'
t_IS   = r'is'
t_THIS = r'this'

t_PERIOD   = r'.'
t_COMMA = r','
t_BANG = r'!'



# Defines a regular expression that categorizes tokens as ID
def t_ID(t):
	#regex: 
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	# Check in reserved dictionary using get 
	t.type = reserved.get(t.value, 'ID') # Check for reserved words
	return t

# Defines a rule for tracking line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
# A string containing ignored chars (spaces and tabs)
t_ignore = ' \t'

def t_error(t):
	print "Illegal character '%s' " % t.value[0]

# Build the lexer
lexer = lex.lex()

# Give the lexer some input
data = "this is spot.,!can"
lexer.input(data)

#Lexer returns LexToken , with attributes: tok.type, tok.value, tok.lineno, tok.lexpos
while True:
	tok = lex.token()
	if not tok: break
	print tok

# TOKENIZER AND PARSER FOR SPOT LANGUAGE
#############################################################
# TOKENIZER
# Tokenizer Uses Ply library
#############################################################

import ply.lex as lex #import ply library

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
###############################################################################
# PARSER
# Top Down Precedence Parsing
################################################################################

def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)
    return left

class LiteralToken:
    def __init__(self, value):
        self.value = value
    def nud(self):
    	return self
    def __repr__(self):
    	return "(literal %s)" % self.value

class OperatorAddToken:
    lbp = 10
    def nud(self):
    	self.first = expression(100)
    	self.second = None
    	return self
    def led(self, left):
        self.first = left
        self.second = expression(10)
        return self
    def __repr__(self):
    	return "(add %s %s)" % (self.first, self.second)

class OperatorSubToken:
	lbp = 10
	def nud(self):
		self.first = expression(100) #should this be -?
		self.second = None
		return self
	def led(self, left):
		self.first = left
		self.second = expression(10) #should this be -?
		return self
	def __repr__(self):
		return "(sub %s %s)" % (self.first, self.second)

class OperatorMulToken:
	lbp = 20
	def led(self, left):
		self.first = left
		self.second = expression(20)
		return self
	def __repr__(self):
		return "(mul %s %s)" % (self.first, self.second)

class OperatorDivToken:
	lbp = 20
	def led(self, left):
		self.first = left
		self.second = expression(20)
		return self
	def __repr__(self):
		return "(div %s %s)" % (self.first, self.second)

class OperatorPowToken:
	lbp = 30
	def led(self, left):
		self.first = left
		self.second = expression(30-1)
		return self
	def __repr__(self):
		return "(pow %s %s)" % (self.first, self.second)

class EndToken:
    lbp = 0


class SymbolBase:
	id = None
	value = None
	first = None
	second = None
	third = None

	def nud(self):
		raise SyntaxError("no nud")
	def led(self, left):
		raise SyntaxError("no led")
	def __repr__(self):
		if self.id == "(name)" or self.id == "(literal)":
			return "(%s %s)" % (self.id[1:-1], self.value) #cuts parens off self.id
		out = [self.id, self.first, self.second, self.third]
		out = map(str, filter(None, out))
		return "(" + " ".join(out) + ")"

symbol_dict = {}

def symbol(id, bp=0):
	try: 
		s = symbol_dict[id]
	except KeyError:
		class s(SymbolBase):
			pass
		s.__name__ = "symbol:" + id #for debugging
		s.id = id
		s.lbp = bp
		symbol_dict[id] = s
	else: 
		s.lbp = max(bp, s.lbp)
	return s

symbol("(literal)")
symbol("+", 10); symbol("-", 10)
symbol("*", 20); symbol("/", 20)
symbol("(end)") 


def tokenize(program):
    for lex_token in lex_tokens:
    	if (lex_token['id'] == 'NUMBER' or lex_token['id'] == 'STRING'):
    		symbol_class = symbol_dict["(literal)"]
    		new_symbol = symbol_class()
    		new_symbol.value = lex_token['value']
    		yield new_symbol
    	elif lex_token['id'] == 'OPERATOR':
    		symbol_class = symbol_dict.get(lex_token['id'])
    		if not symbol_class:
    			raise SyntaxError("Unknown operator")
    		yield symbol_class() #make a new instance of the operator prototype class. No need to set a value b/c operators don't have values.
    	elif lex_token['id'] == 'NAME':
    		pass
    new_symbol = symbol_dict["(end)"]
    yield new_symbol()

def parse(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()











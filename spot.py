#--TODOS

#generate class tokens in PLY Lexer (not very important)
#separate lexer file from tokenizer/parser (not very important)
#how to tokenize multiple words? (fairly important)
#parse declaration and assignment separately (I'd like this, but it's not super necessary)

#--Qs
#if declaration and assignment are handled separately, how does it know how to attach the value to the variable?

# TOKENIZER AND PARSER FOR SPOT LANGUAGE

import ply.lex as lex #import ply library
token = None
####PLY Lexer. Takes in a string --> lextokens

# List of token names
token_names = [
	'NAME',
	'INT',
	'STRING',

	'ADD_OP',
	'SUB_OP',
	'MUL_OP',
	'DIV_OP',
	
	'COMMA',
	'PERIOD',
	'COLON',
	'SEMICOLON',
	'BANG',
	
	'POSS',
	
	'LPAREN',
	'RPAREN',	

]

reserved = {
	'this is' : 'THISIS',
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'or' : 'OR',
	'and' : 'AND',
	
	#create a new variable and assign it a value
	'create_new_variable' : 'CREATE_NEWVAR',
	'is' : 'IS',
	'value' : 'VALUE',
	}

#All tokens
tokens = token_names + list(reserved.values())

# Token functions-----
t_INT = r'[0-9][0-9]*'
t_STRING = r'"[A-Za-z0-9_]*"'

# math operators
t_ADD_OP = r'\+'
t_SUB_OP = r'\-'
t_MUL_OP = r'\*'
t_DIV_OP = r'\/'

#delimiters
t_COMMA = r','
t_PERIOD = r'\.'
t_COLON = r':'
t_SEMICOLON = r';'
t_BANG = r'!'

t_POSS = r"'s"

t_LPAREN = r'\('
t_RPAREN = r'\)'


# def t_NEWTOKEN(t):
# 	r'create new var'
# 	return CreateVarToken()
# 	# return ....

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
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

print "these are the lex tokens", lex_tokens
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

class NameTok(Token):
	pass
class IntTok(Token):
	pass
class StringTok(Token):
	pass


class CommaTok(Token):
	pass
class PeriodTok(Token):
	pass
class ColonTok (Token):
	pass
class SemiColonTok(Token):
	pass
class BangTok(Token):
	pass


class PossTok:
	pass #define later

#I might end up taking these 2 classes out, as I'm using () for comments
class LParenTok:
	pass #define later
class RParenTok:
	pass 

# Reserved words tokens

class ThisIsTok:
	pass
class IfTok:
	pass
class ElseTok:
	pass
class WhileTok:
	pass
class OrTok:
	pass
class AndTok:
	pass
class IsTok:
	pass
class ValueTok:
	pass

class BinaryOpToken(Token):
	def __init__(self, value=0):
		Token.__init__(self)
		self.first = None
		self.second = None
	def __repr__(self):
		return "(%s, %r): self.first = %s, self.second = %s" %(self.__class__.__name__, self.value, self.first, self.second)

class AddOpTok(BinaryOpToken):
	lbp = 20
	
	def nulld(self):
		return expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(20)
		return self
	
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

class DivOpTok(BinaryOpToken):
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



#Parsing classes
class Create_NewVarTok(Token):
	def __init__(self, value = 0):
		self.value = value
		self.varname = None
		self.varvalue = None

	def __repr__(self):
		return "(%s): self.varname = %s, self.varvalue = %s" %(self.__class__.__name__, self.varname, self.varvalue)


# create class token list
class_tokens = []

token_map = {
	"NAME" : NameTok,
	"INT" : IntTok,
	"STRING" : StringTok,

	"ADD_OP" : AddOpTok,
	"SUB_OP" : SubOpTok,
	"MUL_OP" : MulOpTok,
	"DIV_OP" : DivOpTok,

	"COMMA" : CommaTok,
	"PERIOD" : PeriodTok,
	"COLON" : ColonTok,
	"SEMICOLON" : SemiColonTok,
	"BANG" : BangTok,

	"POSS" : PossTok,

	"LPAREN" : LParenTok,
	"RPAREN" : RParentok,

# reserved words:
	"THISIS" : ThisIsTok,
	"IF" : IfTok,
	"ELSE" : ElseTok,
	"WHILE" : WhileTok,
	"OR" : OrTok,
	"AND" : AndTok,
	"IS" : IsTok,
	"VALUE" : ValueTok
}

for lex_token in lex_tokens:
	
	ltype = lex_token.type 
	lvalue = lex_token.value

	new_class_token = token_map[ltype](lvalue) #create an instance of the class, pass in lvalue
	class_tokens.append(new_class_token)

	# if ltype == 'INT':
	# 	new_int_tok = Token(lvalue)
	# 	class_tokens.append(new_int_tok)
	# elif ltype == 'ADD_OP':
	# 	new_add_op_tok = AddOpTok(lvalue)
	# 	class_tokens.append(new_add_op_tok)
	# elif ltype == 'SUB_OP':
	# 	new_sub_op_tok = SubOpTok(lvalue)
	# 	class_tokens.append(new_sub_op_token)
	# elif ltype == 'CREATE_NEWVAR':
	# 	new_create_nv_tok = Create_NewVarTok(lvalue)
	# 	class_tokens.append(new_create_nv_tok)
	# elif ltype == 'NAME':
	# 	new_name_tok = NameTok(lvalue)
	# 	class_tokens.append(new_name_tok)
	# elif ltype == 'COLON':
	# 	new_colon_tok = ColonTok(lvalue)
	# 	class_tokens.append(new_colon_tok)
	# elif ltype == 'PERIOD':
	# 	new_period_tok = PeriodTok(lvalue)
	# 	class_tokens.append(new_period_tok)
	
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
    t = token
    advance()
    left = t.nulld()
    while rbp < token.lbp:
        t = token
        advance()
        left = t.leftd(left) 
    return left

def advance(tok_class=None):
	global token
	token = class_tokens.pop(0) 
	if (tok_class and token.__class__.__name__!=tok_class):
		raise SyntaxError("Expected %s but got %s" % (tok_class, token.value)) 
	
	print "\n"
def parse():
    advance() #put something into global token
    print "parsing done"
    return expression()

def parse_create():
	advance('Create_NewVarTok')
	create_newvar_node = token #save create_newvar token 
	advance('ColonTok') #check for colon
	advance('NameTok') #move token to name token
	name_token = token #save name_token
	create_newvar_node.varname = name_token.value #save the value of the name token as the varname attribute of Create_NewVar
	advance('PeriodTok')
	return create_newvar_node

    
# Process:
# 5+5
# [(num, 5), (add, +), (num, 5)]
# create all the corresponding class instances
# parse those class instance tokens















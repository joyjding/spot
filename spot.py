#!/usr/bin/env python
#--TODOS

#generate class tokens in PLY Lexer (not very important)
#separate lexer file from tokenizer/parser (not very important)
#parse declaration and assignment separately (I'd like this, but it's not super necessary)


#Shiny bits:
# Verb conjugations
# Indents
# I'd love to make all the math operators words...

#Add program class
#Add evaluate while behavior to while token
# | While | Expression | Block |
# __doc__ returns the doc string
#__getattribute__(...)
#  x.__getattribute__('name') <==> x.name


#--Qs



#DONE
#How to tokenize multiple words? (fairly important) --->Regex
#Make "ATok" optional (would be pretty fun)
#if declaration and assignment are handled separately, how does it know how to attach the value to the variable?
# ---> That's only taken care of in the eval step
#Capitalization -->regex


# TOKENIZER AND PARSER FOR SPOT LANGUAGE


import sys
import ply.lex as lex #import ply library
token = None

#----------------NOW WE LEX -----------------------------------------------------------------------------
#PLY Lexer. Takes in a string --> lextokens
#--------------------------------------------------------------------------------------------------------

# List of token names
token_names = [
	'INT',
	'STRING',

	'ADD_OP',
	'SUB_OP',
	'MUL_OP',
	'DIV_OP',
	'GREATER_THAN_OP',
	'LESS_THAN_OP',
	
	'COMMA',
	'PERIOD',
	'COLON',
	'SEMICOLON',
	'BANG',
	'LCURLY',
	'RCURLY',
	
	'POSS',
	
	'NAME',
	'INDENT',
	'IF_THE_CONDITION',
	'CREATE_NEW_VARIABLE',
	'DEFINE_NEW_FUNCTION',
	'WHILE_THE_CONDITION',
	'FOLLOW_THESE_INSTRUCTIONS',
]

reserved = {
	'this is' : 'THISIS',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'or' : 'OR',
	'and' : 'AND',
	'is' : 'IS',
	'value' : 'VALUE',
	}

# All tokens
tokens = token_names + list(reserved.values())

# Token functions-----
t_INT = r'[0-9][0-9]*'
t_STRING = r'"[A-Za-z0-9_]*"'

# math operators
t_ADD_OP = r'\+'
t_SUB_OP = r'\-'
t_MUL_OP = r'\*'
t_DIV_OP = r'\/'

t_GREATER_THAN_OP = r'<'
t_LESS_THAN_OP = r'>'

#delimiters
t_COMMA = r','
t_PERIOD = r'\.'
t_COLON = r':'
t_SEMICOLON = r';'
t_BANG = r'!'
t_INDENT = r'\t'
t_LCURLY = r'{'
t_RCURLY = r'}'

# A string containing ignored chars
t_ignore = ' '

# more complex lexing functions
def t_POSS(t):
	r'\'(\'s)?'
	return t

def t_CREATE_NEW_VARIABLE(t):
	r'[Cc]reate\s(a\s)?new\svariable'
	return t

def t_IF_THE_CONDITION(t):
	r'[Ii]f\sthe\scondition'
	return t

def t_DEFINE_NEW_FUNCTION(t):
	r'[Dd]efine\s(a\s)?new\sfunction'
	return t
def t_WHILE_THE_CONDITION(t):
	r'[Ww]hile\sthe\scondition'
	return t

def t_FOLLOW_THESE_INSTRUCTIONS(t):
	r'[Ff]ollow\s(s\s)?these\sinstructions'
	return t

# No return value. Token discarded
def t_COMMENT(t): 
    r'\([^)]*\)' #\( to get '(', [^]* to get any no. of characters inside  
    pass

# Defines a rule that checks for reserved words  
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')
    return t

# Defines a rule for tracking line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print "Illegal character '%s' " % t.value[0]



#----------------NOW WE CREATE CLASS TOKENS!-------------------------------------------------------------
#PLY Lexer. Takes in a string --> lextokens
#--------------------------------------------------------------------------------------------------------


#Most basic token classes
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
	def __repr__(self):
		return "(%s, %r): self.first = %s, self.second = %s" %(self.__class__.__name__, self.value, self.first, self.second)


#Primitives
class IntTok(Token):
	pass
class StringTok(Token):
	pass

#Basic punctuation
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
class IndentTok(Token):
	pass
class PossTok:
	pass

#Syntax
class ThisIsTok:
	pass
class ValueTok:
	pass
class TheTok:
	pass
class ConditionTok:
	pass
class TakesTok(Token):
	pass
class OrTok(Token):
	pass
class AndTok(Token):
	pass

#Statement tokens

class ElseTok:
	pass

class IfTheConditionTok(Token):
	def stmtd():
		return "hello"

class IfTheConditionNode(Token):
	def __init__(self, value = 0):
		self.value = value
		self.expression = expression
		self.block = block

	def __repr__(self):
		return "(%s): self.expression = %s, self.block = %s" %(self.__class__.__name__, self.expression, self.block)
class WhileTheConditionTok(Token):
	def stmd():
		advance('COMMA')
		advance() #move on to the beginning of the expression
		condition = expression() #parse the expression
		self.condition = condition #set left fo
		advance('COMMA')
		advance('FollowTheseInstructionsTok')
		advance('COLON')
		advance('{')
		#parse block goes here
class Create_A_New_VarTok(Token):
	pass
class Create_NewVarNode(Token):
	def __init__(self, value = 0):
		self.value = value
		self.varname = None
		self.varvalue = None

	def __repr__(self):
		return "(%s): self.varname = %s, self.varvalue = %s" %(self.__class__.__name__, self.varname, self.varvalue)

class DefineNewFuncTok(Token):
	pass 

class FollowTheseInstructionsTok(Token):
	pass 

# Misc tokens

class IsTok(BinaryOpToken):
	#serves the same function as ==
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self
class NameTok(Token):
	pass

class EndTok(Token):
	lbp = 0
	def leftd(self):
		pass
	def nulld(self):
		pass

#parsing classes

class BlockTok:
	def __init__(self, statements):
		self.statements = statements
	def stmtd(self):
		self.statements = block()
		return self
class Program:
	def stmtd(self):
		self.children = statement_list()
		return self


# Basic Math classes
class AddOpTok(BinaryOpToken):
	lbp = 50
	
	def nulld(self):
		return expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(20)
		return self
	
class SubOpTok(BinaryOpToken):
	lbp = 50

	def nulld(self):
		return -expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(20)
		return self

class MulOpTok(BinaryOpToken):
	lbp = 60

	def leftd(self, left):
		self.first = left
		self.second = expression(30)
		return self

class DivOpTok(BinaryOpToken):
	lbp = 60
	def leftd(self, left):
		self.first = left
		self.second = expression(30)
		return self

class GreaterThanOpTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self

class LessThanOpTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self


# create class token list and token map dict ----------------------------------
class_tokens = []

token_map = {
	"NAME" : NameTok,
	"INT" : IntTok,
	"STRING" : StringTok,

#math
	"ADD_OP" : AddOpTok,
	"SUB_OP" : SubOpTok,
	"MUL_OP" : MulOpTok,
	"DIV_OP" : DivOpTok,

#comparitors
	"GREATER_THAN_OP" : GreaterThanOpTok,
	"LESS_THAN_OP" : LessThanOpTok,

#punctuation
	"COMMA" : CommaTok,
	"PERIOD" : PeriodTok,
	"COLON" : ColonTok,
	"SEMICOLON" : SemiColonTok,
	"BANG" : BangTok,
	"INDENT" : IndentTok,

	"POSS" : PossTok,

# reserved words:
	"THISIS" : ThisIsTok,
	"ELSE" : ElseTok,
	"OR" : OrTok,
	"AND" : AndTok,
	"IS" : IsTok,
	"VALUE" : ValueTok,
	"CREATE_NEW_VARIABLE" : Create_A_New_VarTok,
	"DEFINE_NEW_FUNCTION" : DefineNewFuncTok,
	"IF_THE_CONDITION" : IfTheConditionTok,
	"WHILE_THE_CONDITION" : WhileTheConditionTok,
	"FOLLOW_THESE_INSTRUCTIONS" : FollowTheseInstructionsTok,
}

#####################################################################################################
# PARSER
# Top Down Precedence Parsing
###################################################################################################		

def statement_list():
	statements = []

	while token.__class__.__name__ != 'EndTok':
		statements.append(statement())	
	return statements

# def statement():
# 	if token.__getattribute__('stmtd'):
# 		return token.stmtd()
# 	else: 
# 		return expression(0)

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
		raise SyntaxError("Expected %s but got %s" % (tok_class, token.__class__.__name__)) 
	
	print "\n"
def next():
	pass

def block():
	# stmts = []
	# while 
	pass

def parse_expression():
	#put something into global token
    return expression()

def parse_create(): 
	advance('Create_A_New_VarTok') #advance on create - taken out b/c already advancing once
	advance('ColonTok') #advance on colon
	advance('NameTok')
	name_token = token #save name token as name_token
	create_newvarnode = Create_NewVarNode() #create new create_new_variable node
	create_newvarnode.varname = name_token.value #save the value of the name token as the varname attribute of Create_NewVarTok 
	advance('PeriodTok')
	return create_newvarnode

def parse_function():
	"""Define a new function: numapples. Numapples takes 0 arguments. Instructions"""
	advance('DefineANewFuncTok')
	advance('ColonTok')
	advance('NameTok')
	advance('PeriodTok')
	#check that the name is the same
	advance('TakesTok')
	advance('IntTok')
	advance('FollowTheseInstructionsTok')
	advance('ColonTok')
	advance('BlockTok')

def parse_if():
	""" If the condition, expression: do this."""
	
	advance('IfTheConditionTok')
	new_node = IfTheConditionNode()
	advance('CommaTok')
	new_node.expression = parse_expression()
	advance('COLON')

	advance() #block???
	#parse_block()

def statement(): # parses one statement
	# if the token has a stmtd attribute, invoke it
	if hasattr(token, "stmtd"):
		return token.stmtd()
	# otherwise, eval as an expression
	result = expression()
	print result
	return result

def parse():	
	advance() #to put the first token in
	p = Program()
	p.stmtd()	
	return p

def make_class_tokens(source):
	
	#-------turn a string into lextokens

	# build the lexer
	spotlexer = lex.lex()
	
	# Lex the data
	spotlexer.input(source)
	#Lexer returns LexToken, with attributes: tok.type, tok.value, tok.lineno, tok.lexpos
	
	# create lex_tokens list
	lex_tokens = []
	while True:
		tok = lex.token()
		if not tok:
			break	
		lex_tokens.append(tok)

	print "these are the lex tokens", lex_tokens

	#------convert lextokens to class tokens
	
	for lex_token in lex_tokens:
		
		ltype = lex_token.type 
		lvalue = lex_token.value

		new_class_token = token_map[ltype](lvalue) #create an instance of the class, pass in lvalue
		class_tokens.append(new_class_token)
	new_end_tok = EndTok()
	class_tokens.append(new_end_tok)

	print "these are the class tokens", class_tokens
	return class_tokens

def main():
	filename = sys.argv[1] if len(sys.argv) > 1 else None

	if filename:
		source = open(filename).read()
	else:
		source = raw_input(">What would you like to parse? ")
	
	class_tokens = make_class_tokens(source)
	parse()


if __name__ == "__main__":
	main()






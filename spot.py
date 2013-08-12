#!/usr/bin/env python
#--TODOS
# - convert integer strings to actual integers


#generate class tokens in PLY Lexer (not very important)
#separate lexer file from tokenizer/parser (not very important)
#parse declaration and assignment separately (I'd like this, but it's not super necessary)

#create two classes for is versus equal to DO THIS IT IS IMPORTANT
#add nud to true/false

#anything that parses as part of an expression needs an lbp

#Shiny bits:
# Verb conjugations
# Indents
# I'd love to make all the math operators words...

#Add program class
#Add evaluate while behavior to while token
# __doc__ returns the doc string
#__getattribute__(...)
#  x.__getattribute__('name') <==> x.name


#--Qs
# line 264: why do i have to advance again so that periodtok doesn't end up in self?
# scope? 


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
	'ELSE',
	'IS_EQUAL_TO',
	'WHICH_TAKES',
	'IF_THE_CONDITION',
	'CREATE_NEW_VARIABLE',
	'DEFINE_NEW_FUNCTION',
	'WHILE_THE_CONDITION',
	'FOLLOW_THESE_INSTRUCTIONS',
	'IF_NONE_CONDITION',
]

reserved = {
	'this is' : 'THISIS',
	'while' : 'WHILE',
	'or' : 'OR',
	'and' : 'AND',
	'is' : 'IS',
	'value' : 'VALUE',
	'true' : 'TRUE',
	'false' : 'FALSE',
	'arguments': 'ARGS',
	'Instructions' : 'INSTRUCTIONS',
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

t_GREATER_THAN_OP = r'>'
t_LESS_THAN_OP = r'<'

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
def t_IF_NONE_CONDITION(t):
	r'[Ii]f\snone\sof\sthe\sprevious\sconditions\sare\strue'
	return t
def t_ELSE(t):
	r'[Ee]lse'
	return t

def t_POSS(t):
	r'\'(\'s)?'
	return t

def t_WHICH_TAKES(t):
	r'which\stakes'
	return t

def t_IS_EQUAL_TO(t):
	r'is\sequal\sto'
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
# with nulld(), leftd(), statementd() when necessary, to make parsing happen
#--------------------------------------------------------------------------------------------------------


#Most basic token classes
class Token:
	def __init__(self, value = 0):
		self.value = value
	def nulld(self):
		print self 
		raise SyntaxError("This should not have a nulld")
	def leftd(self, left):
		pass
	def __repr__(self):
		return "(%s, %r)" %(self.__class__.__name__, self.value)

class LiteralToken(Token):
	lbp = 10
	def nulld(self):
		return self

class BinaryOpToken(Token):
	def __init__(self, value = 0):
		Token.__init__(self)
		self.first = None
		self.second = None
	
	def nulld(self):
		pass
	def __repr__(self):
		return "(%s, %r): self.first = %s, self.second = %s" %(self.__class__.__name__, self.value, self.first, self.second)


# Primitives
class IntTok(LiteralToken):
	pass
class StringTok(LiteralToken):
	pass

# Booleans
class TrueTok(LiteralToken):
	lbp = 0

class FalseTok(LiteralToken):
	lbp = 0

#Basic punctuation
class CommaTok(Token):
	lbp = 0
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
class PossTok(Token):
	pass
class LCurlyTok(Token):
	pass
class RCurlyTok(Token):
	lbp = 0
	pass

#Syntax Words and Phrases
class ThisIsTok:
	pass
class ValueTok:
	pass
class TakesTok(Token):
	pass
class OrTok(Token):
	pass
class AndTok(Token):
	pass
class ElseTok(Token):
	pass
class FollowTheseInstructionsTok(Token):
	pass
class WhichTakesTok(Token):
	pass
class ArgumentsTok(Token):
	pass
class InstructionsTok(Token):
	pass


#Statement tokens
class Create_A_New_VarTok(Token):
	"""Create a new variable: x."""

	def __init__(self, value = 0):
		self.value = value
		self.varname = None

	def statementd(self):
		advance('Create_A_New_VarTok')
		advance('ColonTok')
		name = advance('NameTok') 
		self.varname = name.value
		advance('PeriodTok')
		return self

	def __repr__(self):
		return "(%s): self.varname = %s" %(self.__class__.__name__, self.varname)

class DefineNewFuncTok(Token):
	"""Define a new function: numapples. Numapples takes 0 arguments and follows these instructions: {Block}"""
	def __init__(self, value = 0):
		self.value = value
		self.function_name = [] #a list so there can be multi-word names
		self.num_args = 0
		self.args = []
		self.block = None

	def statementd(self):
		advance("DefineNewFuncTok")
		#save multiple word names
		while isinstance(token, NameTok):
			self.function_name.append(token)
			advance()
		#for saving arguments, if there are any
		if isinstance(token, CommaTok):
			advance('CommaTok')
			advance('WhichTakesTok')
			self.num_args = advance('IntTok')
			advance('ArgumentsTok')
			advance('ColonTok')	
			#for saving multiple arguments
			while isinstance(token, NameTok):
				name = advance('NameTok')
				self.args.append(name)
				if isinstance(token, PeriodTok):
					break #break breaks most recent loop
				advance('CommaTok')	
			advance('PeriodTok')
		#instructions
		advance('InstructionsTok')
		advance('ColonTok')
		advance('LCurlyTok')
		new_block = parse_block()
		self.block = new_block
		advance('RCurlyTok')
		return self

	def __repr__(self):
		return "(%s): .function_name = %s | .num_args = %s | .args = %s" %(self.__class__.__name__, self.function_name, self.num_args, self.args) 


class IfTheConditionTok(Token):
	"""If the condition x>4 is equal to true, follow these instructions:"""
	def __init__(self, value = 0):
		self.value = value
		self.condition = None
		self.true_block = None
		self.else_block = None 

	def statementd(self):
		advance('IfTheConditionTok')
		new_condition = statement()
		self.condition = new_condition
		advance('CommaTok')
		advance('FollowTheseInstructionsTok')
		advance('ColonTok')
		advance('LCurlyTok')
		new_block = parse_block()
		self.true_block = new_block
		advance('RCurlyTok')
		while (token.__class__.__name__ != 'IndentTok' and token.__class__.__name__ != 'EndTok'):
			if token.__class__.__name__ == 'ElseTok':
				advance()
				if token.__class__.__name__ == 'IfTheConditionTok':
					new_if = token
					new_else_block =new_if.statementd()
					self.else_block = new_else_block
				elif token.__class__.__name__ == 'CommaTok':
					advance('CommaTok')
					advance('FollowTheseInstructionsTok')
					advance('ColonTok')
					advance('LCurlyTok')
					else_block = parse_block()
					self.else_block = else_block
					advance('RCurlyTok')				
		return self

	def __repr__(self):
		return "(%s): self.condition = %s, self.true_block = %s, self.else_block = %s " %(self.__class__.__name__, self.condition, self.true_block, self.else_block)

class WhileTheConditionTok(Token):
	"""While the condition x>4 is equal to true, follow these instructions: {block}"""
	
	def __init__(self, value = 0):
		self.value = value
		self.condition = None
		self.block = None

	def statementd(self):
		advance('WhileTheConditionTok')
		new_condition = statement()
		self.condition = new_condition
		advance('CommaTok')
		advance('FollowTheseInstructionsTok')
		advance('ColonTok')
		advance('LCurlyTok')
		new_block = parse_block()
		self.block = new_block
		advance('RCurlyTok')
		return self		
	
	def __repr__(self):
		return "(%s): self.condition = %s, self.block = %s" %(self.__class__.__name__, self.condition, self.block)


# Misc tokens
class IsTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self

class NameTok(LiteralToken):
	
	lbp = 10
	pass

class EndTok(Token):
	lbp = 0
	def leftd(self, left):
		pass
	def nulld(self):
		pass

#parsing classes
class Program:
	def statementd(self):
		self.children = statement_list()
		for selves in self.children:
			print selves
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
class IsEqualToTok(BinaryOpToken):
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
	"LCURLY" : LCurlyTok,
	"RCURLY" : RCurlyTok,

# reserved words:
	"TRUE" : TrueTok,
	"FALSE" : FalseTok,
	"THISIS" : ThisIsTok,
	"ELSE" : ElseTok,
	"OR" : OrTok,
	"AND" : AndTok,
	"IS" : IsTok,
	"VALUE" : ValueTok,
	"ARGS" : ArgumentsTok,
	"INSTRUCTIONS" : InstructionsTok,

	#reserved phrases:
	"IS_EQUAL_TO" : IsEqualToTok,
	"WHICH_TAKES" : WhichTakesTok,
	"CREATE_NEW_VARIABLE" : Create_A_New_VarTok,
	"DEFINE_NEW_FUNCTION" : DefineNewFuncTok,
	"IF_THE_CONDITION" : IfTheConditionTok,
	"WHILE_THE_CONDITION" : WhileTheConditionTok,
	"FOLLOW_THESE_INSTRUCTIONS" : FollowTheseInstructionsTok,
}

#----------------FUNCTIONS!-------------------------------------------------------------
# 
#--------------------------------------------------------------------------------------------------------	

def statement_list():
	statements = []

	while token.__class__.__name__ != 'EndTok':
		statements.append(statement())	
	return statements

def parse_block():
	block_statements = [] #initialize empty block statement list
	
	while token.__class__.__name__ != 'RCurlyTok': #while there is no rcurly
		new_statement = statement()
		block_statements.append(new_statement)
	return block_statements

def expression(rbp=0):	    
	    t = token
	    advance()
	    left = t.nulld()
	    while rbp < token.lbp:
	        t = token
	        advance()
	        left = t.leftd(left) 
	    return left

# def check_type(tok_class): #this function might not be necessary...
# 	if token.__class__.__name__==tok_class:
# 		return token
# 	else:
# 		raise SyntaxError("Expected %s but got %s" % (tok_class, token.__class__.__name__)) 

def advance(tok_class = None):
	global token
	#check if the current token is the one expected
	if (tok_class and token.__class__.__name__!=tok_class):
		raise SyntaxError("Expected %s but got %s" % (tok_class, token.__class__.__name__)) 
	
	current_token = token	

	#if so, move on to the next token
	token = class_tokens.pop(0)
	return current_token

def statement(): # parses one statement
	# if the token has a statementd attribute, invoke it
	if hasattr(token, "statementd"):
		return token.statementd()
	# otherwise, eval as an expression
	if hasattr(token, "nulld"):
		return expression(0)

def parse():	
	advance() #to put the first token in
	p = Program()
	p.statementd()	
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

	print "\n\nthese are the lex tokens", lex_tokens

	#------convert lextokens to class tokens
	
	for lex_token in lex_tokens:
		
		ltype = lex_token.type 
		lvalue = lex_token.value

		new_class_token = token_map[ltype](lvalue) #create an instance of the class, pass in lvalue
		class_tokens.append(new_class_token)
	new_end_tok = EndTok()
	class_tokens.append(new_end_tok)

	print "\n these are the class tokens", class_tokens
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






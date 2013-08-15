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
# scope



#########################################
# TOKENIZER AND PARSER FOR SPOT LANGUAGE


import sys
import ply.lex as lex #import ply library
token = None

#----------------NOW WE LEX -----------------------------------------------------------------------------
#PLY Lexer. Takes in a string --> lextokens
#--------------------------------------------------------------------------------------------------------

# List of token names
token_names = [
	
	#primitives
	'INT',
	'STRING',

	#math
	'ADD_OP',
	'SUB_OP',
	'MUL_OP',
	'DIV_OP',
	'GREATER_THAN_OP',
	'LESS_THAN_OP',
	
	#punctuation
	'COMMA',
	'PERIOD',
	'COLON',
	'SEMICOLON',
	'BANG',
	'LCURLY',
	'RCURLY',
	'SINGLEQ',
	'DOUBLEQ',
	
	'POSS',
	
	'NAME',
	'INDENT',
	'ELSE',
	'ELSE_IF_THE_CONDITION',
	'SET',
	'IS_EQUAL_TO',
	'WHICH_TAKES',
	'IF_THE_CONDITION',
	'CREATE_NEW_VARIABLE',
	'DEFINE_NEW_FUNCTION',
	'WHILE_THE_CONDITION',
	'FOLLOW_THESE_INSTRUCTIONS',
	'IF_NONE_CONDITION',
	'SET_VALUE_TO',
]

reserved = {
	'this is' : 'THISIS',
	'while' : 'WHILE',
	'or' : 'OR',
	'and' : 'AND',
	'is' : 'IS',
	'to' : 'TO',
	'value' : 'VALUE',
	'true' : 'TRUE',
	'false' : 'FALSE',
	'arguments': 'ARGS',
	'Instructions' : 'INSTRUCTIONS',

	#inbuilt methods
	'Screensay' : 'SCREENSAY',
	}

# All tokens
tokens = token_names + list(reserved.values())

# Token functions-----
t_STRING = r'".*"'

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
t_SINGLEQ = r'\''
t_DOUBLEQ = r'\"'

# A string containing ignored chars
t_ignore = ' '

# more complex lexing functions
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ELSE_IF_THE_CONDITION(t):
	r'[Ee]lse\sif\sthe\scondition'
	return t

def t_IF_NONE_CONDITION(t):
	r'[Ii]f\snone\sof\sthe\sprevious\sconditions\sare\strue'
	return t
def t_ELSE(t):
	r'[Ee]lse'
	return t

def t_POSS(t):
	r'\'(s)?'
	return t

def t_WHICH_TAKES(t):
	r'which\stakes'
	return t

def t_IS_EQUAL_TO(t):
	r'is\sequal\sto'
	return t

def t_SET(t):
	r'[Ss]et'
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
	lbp = 0

	def nulld(self):
		return self

	def eval(self):
		return self.value

class StringTok(LiteralToken):
	def eval(self):
		string = self.value[1:-1]
		print 2, string

		out_string = []

		while string:	
			start_brack = string.find("{")
			if start_brack == -1: #no string interpolation
				out_string.append(string)
				break
			else:
				out_string.append(string[:start_brack]) #add beg string to outstring
				end_brack = string.find("}")
				new_statement_string = string[start_brack+1:end_brack] #give me the contents of the brackets
				new_statement_lex = make_lex_tokens(new_statement_string)
				new_class_tok = make_class_tokens(new_statement_lex)
				advance()
				mini_e = expression()
				result = mini_e.eval()
				result_string = str(result)
				out_string.append(result_string)
				string = string[end_brack+1:]

		joined_string = "".join(out_string)
		return joined_string

# Booleans
class TrueTok(LiteralToken):
	lbp = 0

	def eval(self):
		return True

class FalseTok(LiteralToken):
	lbp = 0

	def eval(self):
		return False

#Basic punctuation
class CommaTok(Token):
	lbp = 0
	pass
class PeriodTok(Token):
	pass
class ColonTok (Token):
	lbp = 0
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
class SingleQTok(Token):
	pass
class DoubleQTok(Token):
	pass

#Syntax Words and Phrases
class ThisIsTok:
	pass
class ValueTok(Token):
	pass
class TakesTok(Token):
	pass
class OrTok(Token):
	pass
class AndTok(Token):
	pass
class ToTok(Token):
	pass
class ElseTok(Token):
	pass
class ElseIfTok(Token):
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
		advance(Create_A_New_VarTok)
		advance(ColonTok)
		name = advance(NameTok) 
		self.varname = name.value
		advance(PeriodTok)
		return self

	def eval(self):
		#create a new variable in the scope dictionary
		scope.dict[self.varname] = None
		print "added %r to scope.dict" %self.varname

	def __repr__(self):
		return "(%s): self.varname = %s" %(self.__class__.__name__, self.varname)

class SetTok(Token):
	def __init__(self, value = 0):
		self.value = value
		self.varname = []
		self.varvalue = None

	def statementd(self):
		advance(SetTok)
		#save multiple-word name 
		while isinstance(token, NameTok):
			self.varname.append(token.value)
			advance()
		advance(PossTok)
		advance(ValueTok)
		advance(ToTok)
		if not (isinstance(token, IntTok) or isinstance(token, StringTok) or isinstance(token, NameTok)):
			raise SyntaxError ("Expected a value for the variable %s, but got incompatible type") %self.varname
		new_varvalue = advance()
		self.varvalue = new_varvalue.value
		advance(PeriodTok)
		return self
	
	def eval(self):
		if scope.dict.has_key(self.varname) == False:
			raise SyntaxError("Variable %s doesn't exist" %self.varname)
		scope.define(self.varname, self.varvalue)
		print "set scope.dict[%r]: %r" %(self.varname, self.varvalue)
		
	def __repr__(self):
		return "(%s): .varname = %s | .varvalue = %s " %(self.__class__.__name__, self.varname, self.varvalue)

class DefineNewFuncTok(Token):
	"""Define a new function: numapples. Numapples takes 0 arguments and follows these instructions: {Block}"""
	def __init__(self, value = 0):
		self.value = value
		self.function_name = [] #a list so there can be multi-word names
		self.num_args = 0
		self.args = []
		self.block = None

	def statementd(self):
		advance(DefineNewFuncTok)
		#save multiple word names
		while isinstance(token, NameTok):
			self.function_name.append(token.value)
			advance()
		#for saving arguments, if there are any
		if isinstance(token, CommaTok):
			advance(CommaTok)
			advance(WhichTakesTok)
			self.num_args = advance(IntTok)
			advance(ArgumentsTok)
			advance(ColonTok)	
			#for saving multiple arguments
			while isinstance(token, NameTok):
				name = advance(NameTok)
				self.args.append(name)
				if isinstance(token, PeriodTok):
					break #break breaks most recent loop
				advance(CommaTok)	
			advance(PeriodTok)
		#instructions
		advance(InstructionsTok)
		advance(ColonTok)
		advance(LCurlyTok)
		new_block = parse_block()
		self.block = new_block
		advance(RCurlyTok)
		new_set = SetTok()
		new_set.varname = self.function_name
		new_set.varvalue = self
		return new_set  

	def eval(self):
		pass
		# f_name = self.function_name
		# if self.num_args == 0:
		# 	def f_name():
			#don't do this yet. go do eval for the other pieces of a function.	

		#create the function
		#put it in the scope dictionary??
	def __repr__(self):
		return "(%s): .function_name = %s | .num_args = %s | .args = %s" %(self.__class__.__name__, self.function_name, self.num_args, self.args) 



class IfTheConditionTok(Token):
	"""If the condition x>4 is equal to true, follow these instructions:{}. 
	Else if the condition x<4 is equal to true, follow these instructions:{}. 
	Else, follow these instructions: {}."""

	def __init__(self, value = 0):
		self.value = value
		self.condition = None
		self.true_block = None
		self.elseif_cond = None
		self.elseif_block = None
		self.else_block = None

	def statementd(self):
		advance(IfTheConditionTok)
		new_condition = statement()
		self.condition = new_condition
		advance(CommaTok)
		advance(FollowTheseInstructionsTok)
		advance(ColonTok)
		advance(LCurlyTok)
		new_block = parse_block()
		self.true_block = new_block
		advance(RCurlyTok)
		advance(PeriodTok)
		if isinstance(token, ElseIfTok):
			print 1, token
			advance(ElseIfTok)
			print 2, token
			new_condition = statement()
			self.elseif_cond = new_condition
			print 3, self.elseif_cond
			advance(CommaTok)
			advance(FollowTheseInstructionsTok)
			advance(ColonTok)
			advance(LCurlyTok)
			new_block = parse_block()
			self.elseif_block = new_block
			print 4, self.elseif_block
			advance(RCurlyTok)
			advance(PeriodTok)
		if isinstance(token, ElseTok):
			advance(ElseTok)
			advance(CommaTok)
			advance(FollowTheseInstructionsTok)
			advance(ColonTok)
			advance(LCurlyTok)
			else_block = parse_block()
			print 5,"else_block", else_block
			self.else_block = else_block
			advance(RCurlyTok)
			advance(PeriodTok)				
		return self

	def eval(self):	
		if self.condition.eval() == True:
			print "The if condition %s is true -->executing if block" % self.condition
			for statement in self.true_block:
				statement.eval()
		elif self.condition.eval() == False:
			print "The if condition %s is not true-->looking for else if or else" % self.condition
			if (self.elseif_cond == True and self.elseif_block != None):
				print "Else if condition %s is true-->executing else if block"
				for statement in self.elseif_block:
					statement.eval()
			if (self.elseif_cond == False and self.else_block != None):
				print "The else if condition %s is not true-->executing else block"
				for statement in self.else_block:
					statement.eval()
			if (self.elseif_block == None and self.else_block != None):
				print "Previous conditions were not true-->Executing the else condition"
				for statement in self.else_block:
					statement.eval()

	def __repr__(self):
		return "(%s): self.condition = %s, self.true_block = %s, self.else_block = %s " %(self.__class__.__name__, self.condition, self.true_block, self.else_block)

class WhileTheConditionTok(Token):
	"""While the condition x>4 is equal to true, follow these instructions: {block}"""
	
	def __init__(self, value = 0):
		self.value = value
		self.condition = None
		self.block = None

	def statementd(self):
		advance(WhileTheConditionTok)
		new_condition = statement()
		self.condition = new_condition
		advance(CommaTok)
		advance(FollowTheseInstructionsTok)
		advance(ColonTok)
		advance(LCurlyTok)
		new_block = parse_block()
		self.block = new_block
		advance(RCurlyTok)
		advance(PeriodTok)
		return self		
	
	def eval(self):
		while self.condition.eval() == True:
			for statement in self.block:
				statement.eval() 
	def __repr__(self):
		return "(%s): self.condition = %s, self.block = %s" %(self.__class__.__name__, self.condition, self.block)

#inbuilt methods
class ScreenSayTok(Token):
	def __init__(self, value = 0):
		self.value = value
		self.stringtok = None
		self.string = None
	def statementd(self):
		advance(ScreenSayTok)
		print 1, token
		advance(ColonTok)
		print 2, token
		new_stringtok = advance(StringTok)
		self.stringtok = new_stringtok
		return self
	def eval(self):
		string = self.stringtok.eval()
		print string

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
		return self
	def eval(self):
		for mini_selves in self.children:
			mini_selves.eval()

#eval classes
class Scope:
	def __init__(self):
		self.dict = {}
		self.parent = None
	def define(self, varkey, varvalue = None):
		if self.dict.get(varkey) != None:
			raise SyntaxError("The variable %s has already been defined, and its value is %s" %(self.varkey, self.dict[varkey]))
		else: 
			self.dict[varkey] = varvalue
	def find(self, varkey):
		while True:
			value = self.get(varkey)
			key = self.dict.has_key(varkey)
			if key: 
				if value!=None: #if value is not none, return value
					return value
				elif value == None:
					self = self.parent
					if self == None:
						print "The variable %s has been created but not defined" %varkey				
			self = self.parent #look in parent scope
			if self == None:
				print "The variable %s has not yet been created or defined"
	
	def pop(self):
		scope = self.parent

# Basic Math classes
class AddOpTok(BinaryOpToken):
	lbp = 50
	
	def nulld(self):
		return expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(50)
		return self
	def eval(self):
		print "Interpreter added %r and %r" % (self.first, self.second)
		return self.first.eval() + self.second.eval()
	
class SubOpTok(BinaryOpToken):
	lbp = 50

	def nulld(self):
		return -expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(50)
		return self
	def eval(self):
		print "Interpreter subtracted %r from %r" %(self.second, self.first)
		return self.first.eval() - self.second.eval()

class MulOpTok(BinaryOpToken):
	lbp = 70

	def leftd(self, left):
		self.first = left
		self.second = expression(70)
		return self
	def eval(self):
		print "Interpreter multipled %r and %r" % (self.first, self.second)
		return self.first.eval() * self.second.eval()


class DivOpTok(BinaryOpToken):
	lbp = 70
	def leftd(self, left):
		self.first = left
		self.second = expression(70)
		return self
	def eval(self):
		print "Interpreter divided %r by %r" %(self.first, self.second)
		return self.first.eval() / self.second.eval()

class GreaterThanOpTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self
	def eval(self):
		if self.first.eval() > self.second.eval():
			return True
		else:
			return False

class LessThanOpTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self
	def eval(self):
		if self.first.eval() < self.second.eval():
			return True
		else: 
			return False
class IsEqualToTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self
	def eval(self):
		if self.first.eval() == self.second.eval():
			return True
		else:
			return False

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
	"LCURLY" : LCurlyTok,
	"RCURLY" : RCurlyTok,
	"SINGLEQ" : SingleQTok,
	"DOUBLEQ" : DoubleQTok,

	"POSS" : PossTok,


# reserved words:
	"TRUE" : TrueTok,
	"FALSE" : FalseTok,
	"THISIS" : ThisIsTok,
	"ELSE" : ElseTok,
	"OR" : OrTok,
	"AND" : AndTok,
	"TO" : ToTok,
	"VALUE" : ValueTok,
	"ARGS" : ArgumentsTok,
	"INSTRUCTIONS" : InstructionsTok,


	#reserved phrases:
	"SET" : SetTok,
	"IS_EQUAL_TO" : IsEqualToTok,
	"WHICH_TAKES" : WhichTakesTok,
	"CREATE_NEW_VARIABLE" : Create_A_New_VarTok,
	"DEFINE_NEW_FUNCTION" : DefineNewFuncTok,
	"IF_THE_CONDITION" : IfTheConditionTok,
	"ELSE_IF_THE_CONDITION" : ElseIfTok,
	"WHILE_THE_CONDITION" : WhileTheConditionTok,
	"FOLLOW_THESE_INSTRUCTIONS" : FollowTheseInstructionsTok,

	#native methods:
	"SCREENSAY" : ScreenSayTok,
}

#----------------FUNCTIONS!-------------------------------------------------------------
# 
#--------------------------------------------------------------------------------------------------------	

def statement_list():
	statements = []

	while not isinstance(token, EndTok):
		statements.append(statement())	
	return statements

def parse_block():
	block_statements = [] #initialize empty block statement list
	
	while not isinstance(token, RCurlyTok): #while there is no rcurly
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

def advance(tok_class = None):
	global token
	#check if the current token is the one expected
	if (tok_class and not isinstance(token, tok_class)):
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
	global scope
	#create a new global scope -->later use nested scopes
	scope = Scope()
	advance() #to put the first token in
	p = Program()
	p.statementd()	
	return p

def make_lex_tokens(source):
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

	# print "\n\n\nLEXING"
	# print "-----Here are the lex tokens you ordered!"
	# print lex_tokens
	return lex_tokens

def make_class_tokens(lex_token_list):
	
	#------convert lextokens to class tokens
	
	for lex_token in lex_token_list:
		
		ltype = lex_token.type 
		lvalue = lex_token.value

		new_class_token = token_map[ltype](lvalue) #create an instance of the class, pass in lvalue
		class_tokens.append(new_class_token)
	new_end_tok = EndTok()
	class_tokens.append(new_end_tok)

	# print "\nTOKENIZING"
	# print"-----These class tokens are steaming hot!"
	# print class_tokens
	return class_tokens

def main():
	filename = sys.argv[1] if len(sys.argv) > 1 else None

	if filename:
		source = open(filename).read()
	else:
		source = raw_input(">What would you like to parse? ")
	
	lex_tokens = make_lex_tokens(source)
	print "\n\n\nMAIN LEXING"
	# print "-----Here are the lex tokens you ordered!"
	print lex_tokens
	
	class_tokens = make_class_tokens(lex_tokens)
	print "\nMAIN CLASS TOKENIZING"
	# print"-----These class tokens are steaming hot!"
	print class_tokens
	
	#parse the program
	print "\nMAIN PARSING" 
	# print "-----Woo! Nothing's broken yet. About to parse now!"
	program = parse()
	print "\n\nON TO EVALUATION, mateys-------------->"
	
	#eval the program
	print "\n-----Here are the results of your eval!"
	print "Program eval:", program.eval()
	

if __name__ == "__main__":
	main()






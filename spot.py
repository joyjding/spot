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

#imports#
import sys
import ply.lex as lex #import ply library

#globals#
token = None
globalenv = {}
if_count = 0
loop_count = 0
literal_list = []

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

	'A_AN',
	#'INDENT',
	'ELSE',
	'ELSE_IF_THE_CONDITION',
	'SET',
	'RETURN',
	'IS_EQUAL_TO',
	'WHICH_TAKES',
	'ARGUMENTS',
	'IF_THE_CONDITION',
	'CREATE_NEW_VARIABLE',
	'DEFINE_NEW_FUNCTION',
	'WHEN_CALLED',
	'WHILE_THE_CONDITION',
	'FOLLOW_THESE_INSTRUCTIONS',
	'IF_NONE_CONDITION',
	'SET_VALUE_TO',
	'RUN_THE_FUNCTION',
	'WITH_THE_ARGS',
	'PASSING_IN_THE_ARGS',
]

reserved = {
	'this is' : 'THISIS',
	'by' : 'BY',
	'while' : 'WHILE',
	'or' : 'OR',
	'and' : 'AND',
	'is' : 'IS',
	'it' : 'IT',
	'to' : 'TO',
	'value' : 'VALUE',
	'true' : 'TRUE',
	'false' : 'FALSE',
	'Instructions' : 'INSTRUCTIONS',
	'integer' : 'INTEGER',
	'Increase' : 'INCREASE',
	'modulus' : 'MODULUS',

	#inbuilt methods
	'Screensay' : 'SCREENSAY',
	}

# All tokens
tokens = token_names + list(reserved.values())

# Token functions-----
t_STRING = r'"[^"]*"'

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
# t_INDENT = r'\t' #v2 feature
t_LCURLY = r'{'
t_RCURLY = r'}'
t_SINGLEQ = r'\''
t_DOUBLEQ = r'\"'

# A string containing ignored chars
t_ignore = ' \t'

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
def t_A_AN(t):
	r'[Aa]n'
	return t
def t_POSS(t):
	r'\'(s)?'
	return t

def t_WHICH_TAKES(t):
	r'which\stakes'
	return t

def t_ARGUMENTS(t):
	r'argument(s)?'
	return t

def t_IS_EQUAL_TO(t):
	r'is\sequal\sto'
	return t

def t_SET(t):
	r'[Ss]et'
	return t

def t_RETURN(t):
	r'[Rr]eturn'
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

def t_WHEN_CALLED(t):
	r'[Ww]hen\scalled'
	return t

def t_FOLLOW_THESE_INSTRUCTIONS(t):
	r'[Ff]ollow(s)?\sthese\sinstructions'
	return t
def t_RUN_THE_FUNCTION(t):
	r'[Rr]un\sthe\sfunction'
	return t
def t_WITH_THE_ARGS(t):
	r'with\sthe\sarguments'
	return t
def t_PASSING_IN_THE_ARGS(t):
	r'passing\sin\s(the)?\sargument(s)?'
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
		raise SyntaxError("This should not have a nulld")
	def leftd(self, left):
		pass
	def __repr__(self):
		return "(%s, %r)" %(self.__class__.__name__, self.value)

class LiteralToken(Token):
	lbp = 10
	def nulld(self):
		return self
	def eval(self, env):
		return self.value

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

	def codegen(self):
		return self.value

class StringTok(LiteralToken):
	def __init__(self, value = 0):
		self.value = value
		self.len = len(self.value[1:-1])
		self.label = None

	def eval(self, env):
		string = self.value[1:-1]

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
				mini_e = statement() #something needs to change here
				# print "statement", mini_e
				result = mini_e.eval(env)
				# print "env", env
				# print "mini_e.eval", result
				result_string = str(result)
				out_string.append(result_string)
				string = string[end_brack+1:]

		joined_string = "".join(out_string)
		return joined_string

	def codegen(self):
		global literal_list
		new_label = self.value.replace(" ", "_")[1:-1]
		self.label = new_label

		data = ["%s db %s" %(self.label, self.value)]
		literal_list.extend(data)

# Booleans
class TrueTok(LiteralToken):
	lbp = 0

	def eval(self, env):
		return True

class FalseTok(LiteralToken):
	lbp = 0

	def eval(self, env):
		return False

class NameTok(LiteralToken): 
	lbp = 10

	def eval(self, env):
		namekey = self.value
		namevalue = env['%s' %namekey]
		#print ">>>Returning %s, the value of %s" % (namevalue, namekey)
		return namevalue

	def codegen(self):
		return "[%s]" %self.value #this is the issue

#Basic punctuation
class CommaTok(Token):
	lbp = 0
	pass
class PeriodTok(Token):
	lbp = 0
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
class AnTok(Token):
	pass
class ByTok(Token):
	pass
class OrTok(Token):
	pass
class AndTok(Token):
	pass
class ToTok(Token):
	pass
class ItTok(Token):
	pass
class ElseTok(Token):
	pass
class ElseIfTok(Token):
	pass
class WhenCalledTok(Token):
	pass
class FollowTheseInstructionsTok(Token):
	pass
class WhichTakesTok(Token):
	pass
class ArgumentsTok(Token):
	pass
class InstructionsTok(Token):
	pass
class WithTheArgsTok(Token):
	pass
class PassingInTheArgsTok(Token):
	pass

class IntegerTypeTok(Token):
	def codegen():
		return self.value
	

#Statement tokens
class ReturnTok(Token):
	def __init__(self, value = 0):
		self.value = value
		self.expr = None
	def statementd(self):
		advance(ReturnTok)
		new_return = statement()
		print new_return
		self.expr = new_return
		print self.expr
		advance(PeriodTok)
		return self
	def eval(self, env):
		result = self.expr.eval(env)
		print ">Returning to you: %s" %result
		return result
	def __repr__(self):
		return "(%s): .expr = %s" %(self.__class__.__name__, self.expr)


class Create_A_New_VarTok(Token):
	"""Create a new variable x, an integer."""

	def __init__(self, value = 0):
		self.value = value
		self.varname = None
		self.vartype = None

	def statementd(self):
		advance(Create_A_New_VarTok)
		varname_list = []
		while isinstance(token, NameTok):
			varname_list.append(token.value)
			advance()
		new_varname = " ".join(varname_list)
		self.varname = new_varname
		print 10, self.varname
		advance(CommaTok)
		advance(AnTok)
		if isinstance(token, IntegerTypeTok):
			advance(IntegerTypeTok)
			self.vartype = int
		elif isinstance(token, StringTypeTok):
			advance(IntegerTypeTok)
			self.vartype = str
		advance(PeriodTok)
		return self

	def codegen(self):
		#this goes in .data
		#if string --> add this code to literal_list
		if self.vartype == str:
			literal_list.extend(["%s db ?" %self.varname])
		#if int --> add this code to literal_list
		if self.vartype == int:
			literal_list.extend(["%s dd 0" %self.varname])
			#standard for integers to get 4 bytes
		return [] #so something is returned

	def eval(self, env):
		#create a new variable in the env dict		
		print "I'm here!"
		env[self.varname] = None
		print ">>Added %r to env dict. env: %s" %(self.varname, env)

	def __repr__(self):
		return "(%s): .varname = %s | .type = %s" %(self.__class__.__name__, self.varname, self.vartype)

class SetTok(Token):
	def __init__(self, value = 0):
		self.value = value
		self.varname = None
		self.varvalue = None
		self.vartype = None

	def statementd(self):
		advance(SetTok)
		#save multiple-word name 
		varname_list = []
		while isinstance(token, NameTok):
			varname_list.append(token.value)
			advance()
		new_varname = " ".join(varname_list)
		self.varname = new_varname
		advance(PossTok)
		advance(ValueTok)
		advance(ToTok)

		#cannot currently set value to another variable TO DO FOR LATER
		if isinstance(token, IntTok):
			self.vartype = int
		elif isinstance(token, StringTok):
			self.vartype = str
		else:
			raise SyntaxError ("Expected a value for the variable %s, but got incompatible type") %self.varname
		new_varvalue = statement()
		self.varvalue = new_varvalue
		advance(PeriodTok)
		return self

	def codegen(self):
		
		value = self.varvalue.codegen()

		commands = [
		"mov dword [%s], %s" %(self.varname, value)] 
		#set only works for integers right now
		return commands

	def eval(self, env):
		if env.has_key(self.varname) == False:
			raise SyntaxError("This variable has not been created yet")
		varvalue = self.varvalue.eval(env)
		env[self.varname] = varvalue
		print ">> Set env dict[%r]: %r. Env is now %r" %(self.varname, varvalue, env)
		
	def __repr__(self):
		return "(%s): .varname = %s | .varvalue = %s | .vartype = %s " %(self.__class__.__name__, self.varname, self.varvalue, self.vartype)

class DefineNewFuncTok(Token):
	"""Define a new function fizz buzz, which takes 1 argument: end number.
	When called, it follows these instructions: {}.

	Define a new function num apples, which takes 3 arguments: X, Y, and Z. 
	When called, it follows these instructions: {}."""	

	def __init__(self, value = 0):
		self.value = value
		self.function_name = None
		self.num_args = 0
		self.args = []
		self.block = None

	def statementd(self):
		advance(DefineNewFuncTok)
		#save multiple word names
		f_name_list = []
		while isinstance(token, NameTok):
			f_name_list.append(token.value)
			advance()
		new_function_name = " ".join(f_name_list)
		self.function_name = new_function_name	
		#for saving arguments, if there are any. Currently can only save one arg
		if isinstance(token, CommaTok):
			advance(CommaTok)
			advance(WhichTakesTok)
			new_num = advance(IntTok)
			self.num_args = new_num.value #number of arguments
			advance(IntegerTypeTok) #currently arguments can only be integers
			advance(ArgumentsTok)
			advance(ColonTok)
			new_var_bit = []
			while isinstance(token, NameTok): 
				print "new_var_bit", new_var_bit
				new_var_bit.append(token.value)
				advance()
			new_var = " ".join(new_var_bit)
			self.args.append(new_var)

			# put back in later, when I'll have multiple arguments
			# while not isinstance(token, AndTok):
			# 	new_arg = advance()
			# 	#easy hack to get values -->later, might need types
			# 	self.args.append(new_arg.value)
			# 	advance(CommaTok)
			# advance(AndTok)
			# last_arg = advance()
			# self.args.append(last_arg.value)
		advance(PeriodTok)
		advance(WhenCalledTok)
		advance(CommaTok)
		advance(ItTok)
		advance(FollowTheseInstructionsTok)
		advance(ColonTok)
		advance(LCurlyTok)
		new_block = parse_block()
		self.block = new_block
		advance(RCurlyTok)
		advance(PeriodTok)
		return self
		
	def eval(self, env):
		#look up variable in env
		env[self.function_name] = self	
		print ">> Put %r in the env dict" % self.function_name, env

	def __repr__(self):
		return "(%s): .function_name = %s | .num_args = %s | .args = %s" %(self.__class__.__name__, self.function_name, self.num_args, self.args) 

class RunTheFuncTok(Token):
	#changing it to only take one argument. v2 - multiple args
	"""Run the function numapples, passing in the arguments 4, 5, and 6."""
	def __init__(self, value = 0):
		self.value = value
		self.func_name = None
		self.args = []

	def statementd(self):
		advance(RunTheFuncTok)
		#capture the multi-word name
		f_name_list = []
		while isinstance(token, NameTok):
			f_name_list.append(token.value)
			advance()
		new_function_name = " ".join(f_name_list)
		self.func_name = new_function_name
		#for saving arguments, if there are any
		if isinstance(token, CommaTok):
			advance(CommaTok)
			advance(PassingInTheArgsTok)
			new_arg = advance(IntTok)
			self.args = new_arg
			
			#commenting out multiple args code
			# while not isinstance(token, AndTok):
			# 	new_arg = advance()
			# 	self.args.append(new_arg.value)
			# 	#hack to get just the values --> might need types later
			# 	advance(CommaTok)
			# advance(AndTok)
			# last_arg = advance()
			# self.args.append(last_arg.value)
		advance(PeriodTok)			
		return self
	def eval(self, env):
		#check if the fn has been defined
		if env.has_key(self.func_name) == False:
			raise SyntaxError("This function has not been defined yet.")
		#set fn to be the function object
		fn = env[self.func_name]
		args_passed_in = self.args.eval(env)
		
		#create a dictionary, with args and values together

		new_env = zip(fn.args, [args_passed_in])
		env = dict(new_env)
		
		print ">> Created a new environment:", env

		for statement in fn.block:
			statement.eval(env)
		
		#print "set env dict[%r]: %r. Env is now %r" %(self.varname, self.varvalue, env)
		
	def __repr__(self):
		return "(%s): .func_name = %s | .args = %s" %(self.__class__.__name__, self.func_name, self.args) 



	

class IfTheConditionTok(Token):
	"""If the condition x>4 is equal to true, follow these instructions:{}. 
	Else if the condition x<4 is equal to true, follow these instructions:{}. 
	Else, follow these instructions: {}."""

	def __init__(self, value = 0):
		self.value = value
		self.labelno = None
		self.condition = None
		self.true_block = None
		self.elseif_label = None
		self.elseif_cond = None
		self.elseif_block = None
		self.else_label = None
		self.else_block = None

	def statementd(self):
		global if_count
		advance(IfTheConditionTok)
		new_if_no = if_count
		self.labelno = "%d" %new_if_no
		if_count+=1
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
			advance(ElseIfTok) 
			self.elseif_label = "elseif_%d" % new_if_no
			new_condition = statement()
			self.elseif_cond = new_condition
			advance(CommaTok)
			advance(FollowTheseInstructionsTok)
			advance(ColonTok)
			advance(LCurlyTok)
			new_block = parse_block()
			self.elseif_block = new_block
			advance(RCurlyTok)
			advance(PeriodTok)
		if isinstance(token, ElseTok):
			advance(ElseTok)
			self.else_label = "else_%d" %new_if_no
			advance(CommaTok)
			advance(FollowTheseInstructionsTok)
			advance(ColonTok)
			advance(LCurlyTok)
			else_block = parse_block()
			self.else_block = else_block
			advance(RCurlyTok)
			advance(PeriodTok)				
		return self

	def eval(self, env):	
		if self.condition.eval(env) == True:
			print "\n>> The if condition %s is true -->executing if block" % self.condition
			for statement in self.true_block:
				statement.eval(env)
		elif self.condition.eval(env) == False:
			print "\n>> The if condition %s is not true-->looking for else if or else" % self.condition

			if (self.elseif_cond.eval(env) == True and self.elseif_block != None):
				print "\n>> Else if condition %s is true-->executing else if block"
				for statement in self.elseif_block:
					statement.eval(env)
			if (self.elseif_cond.eval(env) == False and self.else_block != None):
				print "\n>> The else if condition %s is not true-->executing else block"
				for statement in self.else_block:
					statement.eval(env)
			if (self.elseif_block == None and self.else_block != None):
				print "\n>> Previous conditions were not true-->Executing the else condition"
				for statement in self.else_block:
					statement.eval(env)

	def __repr__(self):
		return "(%s): self.condition = %s, self.true_block = %s, self.else_block = %s " %(self.__class__.__name__, self.condition, self.true_block, self.else_block)
	def codegen(self):
		
		# JG IF_TRUE_BLOCK1
		# MOV EAX, 7
		# MOV EBX, 6
		# CMP EAX, EBX
		# JL ELSE_IF_BLOCK1
		# JMP ELSE1

		# IF_TRUE_BLOCK1:
		# MOV ECX, 100
		# JMP END_IF1

		# ELSE_IF_BLOCK1:
		# MOV ECX, 200
		# JMP END_IF1

		# ELSE1:
		# MOV ECX, 300
		# END_IF1:
	
		commands = []

		# add if cond code
		if_cond_commands = self.condition.codegen()
		commands.extend(if_cond_commands)

		# add dif jump comparisons --> if block
		if isinstance(self.condition, GreaterThanOpTok):
			commands.extend(["JG if_%s" % self.labelno]) #jump to ifblocklabel
		elif isinstance(self.condition, LessThanOpTok):
			commands.extend(["JL if_%s" % self.labelno])
		elif isinstance(self.condition, IsEqualToTok):
			commands.extend (["JE if_%s" % self.labelno])
		

		#add elseif cond code
		if self.elseif_block != None:
			elseif_cond_commands = self.elseif_cond.codegen()
			commands.extend(elseif_cond_commands)

			#add dif jump comparisons --> else if block
			if isinstance(self.elseif_cond, GreaterThanOpTok):
				commands.extend(["JG %s" % self.elseif_label]) #jump to ifblocklabel
			elif isinstance(self.elseif_cond, LessThanOpTok):
				commands.extend(["JL %s" % self.elseif_label])
			elif isinstance(self.elseif_cond, IsEqualToTok):
				commands.extend (["JE %s" % self.elseif_label])

		#else block commands
		if self.else_block != None:
			#jump to else
			else_command = ["JMP %s" %self.else_label]
			commands.extend(else_command)

		#add true block code
		true_block = ["if_%s:" % self.labelno]
		for block in self.true_block:
			true_block.extend(block.codegen())
		true_block.extend(["JMP endif_%s" %self.labelno])
		commands.extend(true_block)

		#add else if true block
		if self.elseif_block!=None:
			else_if_block = ["%s:" %self.elseif_label]
			for block in self.elseif_block:
				else_if_block.extend(block.codegen())
			else_if_block.extend(["JMP endif_%s" %self.labelno])
			commands.extend(else_if_block)
		
		#add else true block
		if self.else_block!=None:
			else_block = ["%s:" %self.else_label]
			for block in self.else_block:
				else_block.extend(block.codegen())
			else_block.extend(["JMP endif_%s" %self.labelno])
			commands.extend(else_block)

		#end if
		commands.extend(["endif_%s:" %self.labelno])
		return commands

class WhileTheConditionTok(Token):
	"""While the condition x>4 is equal to true, follow these instructions: {block}"""
	
	def __init__(self, value = 0):
		self.value = value
		self.label = None
		self.condition = None
		self.block = None

	def statementd(self):
		global loop_count
		advance(WhileTheConditionTok)
		new_loop_no = loop_count
		self.label = "loop_%d" %new_loop_no
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
	
	def eval(self, env):
		while self.condition.eval(env) == True:
			print ">>> Yup, the condition is still true, continuing loop"
			for statement in self.block:
				statement.eval(env)
		print ">>> The while condition is now false, ending loop. Seeya!" 
	def __repr__(self):
		return "(%s): self.condition = %s, self.block = %s" %(self.__class__.__name__, self.condition, self.block)

	def codegen(self):
		
		# while_condition = self.condition.codegen()
		
		#look up the value of the variable
		# commands = [
		# "mov X, 0",
		# "cmp I, 100",
		# "jge WhileDone",
		# "inc I",
		# "jmp WhileLp"
		# ]


		# mov eax, 0
		# mov ebx, 0
		# cmp eax, ebx
		# je loop_0
		# jmp loop_0

		#return commands

		return []
#inbuilt methods
class ScreenSayTok(Token):
	def __init__(self, value = 0):
		self.value = value
		self.stringtok = None
		self.string = None
		self.string_label = None
		self.string_len = None
	def statementd(self):
		advance(ScreenSayTok)
		advance(ColonTok)
		new_stringtok = advance(StringTok)
		self.stringtok = new_stringtok
		self.string_label = self.stringtok.label
		advance(PeriodTok)
		return self
	def eval(self, env):
		string = self.stringtok.eval(env)
		#print ">>> Screensay printed to screen!"
		print string
	def __repr(self):
		return "(%s): .string = %s" %(self.__class__.__name__, self.string) 
	def codegen(self):
		self.stringtok.codegen()
		print literal_list
		# string = self.stringtok.codegen() #receive the string
		# return ["printf %s] % self.string_label
		commands = [
		"\n; prepare the arguments",
		"push dword %s 			; string length arg" %self.stringtok.len,
		"push dword %s          	; string to print arg" %self.stringtok.label,
		"push dword 1           		; file descriptor value",
		"\n",
		"; make the system call to write",
		"mov eax, 0x4 			; system call number for writescreen",
		"sub esp, 4 			; move the stack pointer for extra space",
		"int 0x80			; code to execute system call",
		"\n",
		"; clean up the stack",
		"add esp, 16 			; args * 4 bytes/arg + 4 bytes extra space"
		"\n"] 

		return commands

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
	def eval(self, env):
		for mini_selves in self.children:
			mini_selves.eval(env)
	def codegen(self):
		code = []

		for statement in self.children:
			code.extend(statement.codegen())
		return code

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
						print "Uh oh. The variable %s has been created but not defined" %varkey				
			self = self.parent #look in parent scope
			if self == None:
				print "Uh oh. The variable %s has not yet been created or defined"
	
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
	def eval(self, env):
		# print ">>> Added %r and %r" % (self.first, self.second)
		return self.first.eval(env) + self.second.eval(env)
	def codegen(self):
		code = [
		"mov eax %s" % self.first.value, #move self.first into eax
		"mov ebx %s" % self.second.value, #move self.second into ebx
		"add eax ebx" #add eax and ebx, store in eax
		]
		return code

class SubOpTok(BinaryOpToken):
	lbp = 50

	def nulld(self):
		return -expression(100)
	def leftd(self, left):
		self.first = left
		self.second = expression(50)
		return self
	def eval(self, env):
		print ">>> Subtracted %r from %r" %(self.second, self.first)
		return self.first.eval() - self.second.eval()
	def codegen(self):
		code = [
		"mov eax %s" % self.first.value, #move self.first into eax
		"mov ebx %s" % self.second.value, #move self.second into ebx
		"sub eax ebx" #add eax and ebx, store in eax
		]
		return code

class MulOpTok(BinaryOpToken):
	lbp = 70

	def leftd(self, left):
		self.first = left
		self.second = expression(70)
		return self
	def eval(self, env):
		print ">>> Multipled %r and %r" % (self.first, self.second)
		return self.first.eval() * self.second.eval()
	def codegen(self):
		pass


class DivOpTok(BinaryOpToken):
	lbp = 70
	def leftd(self, left):
		self.first = left
		self.second = expression(70)
		return self
	def eval(self, env):
		print ">>> Divided %r by %r" %(self.first, self.second)
		return self.first.eval() / self.second.eval()

class GreaterThanOpTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self
	def eval(self, env):
		if self.first.eval(env) > self.second.eval(env):
			print ">>> Yes, %s is greater than %s" % (self.first, self.second)
			return True
		else:
			print ">>> Nope, %s is not greater than %s" % (self.first, self.second)

	def codegen(self):

		commands = [
		"; greater than comparison of %s > %s" % (self.first.value, self.second.value),

		"MOV EAX, %s" % self.first.codegen(),
		"MOV EBX, %s" % self.second.codegen(),
		"CMP EAX, EBX"
		]
		#check to see if this works
		return commands

class LessThanOpTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self
	def eval(self, env):
		if self.first.eval(env) < self.second.eval(env):
			print ">>> Yes, %s is less than %s" % (self.first, self.second)
			return True
		else:
			print ">>> Nope, %s is not greater than %s" % (self.first, self.second)
			return False
	def codegen(self):
		commands = [
			"; less than comparison of %s < %s " % (self.first.value, self.second.value),
			"MOV EAX, %s" % self.first.value, #else
			"MOV EBX, %s" % self.second.value,
			"CMP EAX, EBX",
			]
		return commands

class IsEqualToTok(BinaryOpToken):
	lbp = 40
	def leftd(self, left):
		self.first = left
		self.second = expression(40)
		return self
	def eval(self, env):
		if self.first.eval(env) == self.second.eval(env):
			print ">>> Yes, %s is equal to %s" % (self.first, self.second)
			return True
		else:
			print ">>> Nope, %s is greater than %s" % (self.first, self.second)
			return False

	def codegen(self):
		#load self.first.codegen()
		#move self.first.codegen() into a register
		#self.second.codegen()
		#load self.second.codegen()
		#compare self.first and self.second
		pass

class ModulusTok(BinaryOpToken):
	lbp = 70
	def leftd(self, left):
		self.first = left
		self.second = expression(70)
		return self
	def eval(self, env):
		#print ">>> %r modulus %r" %(self.first, self.second)
		return self.first.eval(env) % self.second.eval(env)

class IncreaseTok(Token):
	def __init__(self, value = 0):
		Token.__init__(self)
		self.first = None
		self.second = None
	
	def statementd(self):
		advance(IncreaseTok)
		new_var = advance(NameTok)
		self.first = new_var
		advance(PossTok)
		advance(ValueTok)
		advance(ByTok)
		new_increment = advance(IntTok)
		self.second = new_increment
		advance(PeriodTok)
		return self

	def eval(self, env):

		variable = self.first.value
		prev_value = self.first.eval(env)
		
		if env.has_key(variable) == False:
			raise SyntaxError("This variable has not been created yet")
		
		if type(prev_value) != int:
			raise SyntaxError("Must be an integer to increment")

		env['%s' %variable] = prev_value + 1

	def __repr__(self):
		return "(%s, %r): self.first = %s, self.second = %s" %(self.__class__.__name__, self.value, self.first, self.second)

	def codegen(self):
		#we're only going to have increment go by 1
		# print "self.first.codegen", self.first.codegen()
		# print "self.second.codegen", self.second.codegen()
		if self.second.codegen() == 1: 
			commands = ["inc dword %s" % self.first.codegen()]
		
		return commands





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

#incrementer:
	"INCREASE" : IncreaseTok,

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
	"A_AN" : AnTok,
	"BY" : ByTok,
	"OR" : OrTok,
	"AND" : AndTok,
	"IT" : ItTok,
	"TO" : ToTok,
	"RETURN" : ReturnTok,
	"VALUE" : ValueTok,
	#"ARGUMENT" #wait a minute here checking on args
	"ARGUMENTS" : ArgumentsTok,
	"INSTRUCTIONS" : InstructionsTok,

	"INTEGER" : IntegerTypeTok,
	"INCREASE" : IncreaseTok,
	"MODULUS" : ModulusTok,


	#reserved phrases:
	"SET" : SetTok,
	"IS_EQUAL_TO" : IsEqualToTok,
	"WHICH_TAKES" : WhichTakesTok,
	"CREATE_NEW_VARIABLE" : Create_A_New_VarTok,
	"DEFINE_NEW_FUNCTION" : DefineNewFuncTok,
	"RUN_THE_FUNCTION" : RunTheFuncTok,
	"WITH_THE_ARGS" : WithTheArgsTok,
	"IF_THE_CONDITION" : IfTheConditionTok,
	"ELSE_IF_THE_CONDITION" : ElseIfTok,
	"WHILE_THE_CONDITION" : WhileTheConditionTok,
	"WHEN_CALLED" : WhenCalledTok,
	"FOLLOW_THESE_INSTRUCTIONS" : FollowTheseInstructionsTok,
	"PASSING_IN_THE_ARGS" : PassingInTheArgsTok,

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
	print "-----Here are the lex tokens you ordered!"
	print lex_tokens
	
	class_tokens = make_class_tokens(lex_tokens)
	print "\nMAIN CLASS TOKENIZING"
	print"-----These class tokens are steaming hot!"
	print class_tokens
	
	#parse the program
	#print "\nMAIN PARSING" 
	# print "-----Woo! Nothing's broken yet. About to parse now!"
	program = parse()
	#print "\n\nON TO EVALUATION, mateys-------------->"
	
	#eval the program
	#print "\n-----Here are the results of your eval!"
	print program.eval(globalenv)
	# header = [
	# 	"; < Woof! A Spot --> NASM file for your compiling pleasure /(^.^)\ >",
	# 	"\n; ----------------",
	# 	"section .text",
	# 	"global mystart ;make the main function externally visible",
	# 	"; ----------------",
	# 	";START OF PROGRAM\n",
	# 	"mystart:\n",
	# 	]

	# footer = [
	# 	"; --------------------------------------------",
	# 	"; EXIT THE PROGRAM\n",
	# 	"; prepare the argument for the sys call to exit",
	# 	"push dword 0 			; exit status returned to OS",
	# 	"\n",
	# 	"; make the call to sys call to exit",
	# 	"mov eax, 0x1 			; sys call no. for exit",
	# 	"sub esp, 4 			; give it some extra space",
	# 	"int 0x80 			; make the system call"
	# ]

	# code = header + program.codegen()
	# # code = program.codegen() #taking out headers and footers for now

	# base_file = filename.split(".")[0]
	# f = open("%s.asm"%base_file, "w")
	
	# for line in code:
	# 	f.write(line + "\n")

	# #data and footer section
	# data1 = [
	# ";----------\n",
	# "section .data\n"
	# ]

	# footer_data = footer + data1 + literal_list

	# for line in footer_data:
	# 	f.write(line + "\n")

	
	# #close the file
	# f.close();
	
	# #print out in the terminal
	# print "\n\n\n>>> Assembly Code------------------------------->\n"
	# for codelet in code:
	# 	print codelet
	# for data in footer_data:
	# 	print data
	# print "\n-----------------"
	# print ">>> Compilation complete\n\n"
	

if __name__ == "__main__":
	main()






#!/usr/bin/env python
#--TODOS

#generate class tokens in PLY Lexer (not very important)
#separate lexer file from tokenizer/parser (not very important)
#how to tokenize multiple words? (fairly important)
#parse declaration and assignment separately (I'd like this, but it's not super necessary)


#Shiny bits:
# Make "ATok" optional (would be pretty fun)
# Verb conjugations
# Indents

#--Qs
#if declaration and assignment are handled separately, how does it know how to attach the value to the variable?
# ---> That's only taken care of in the eval step
# TOKENIZER AND PARSER FOR SPOT LANGUAGE

import sys
import ply.lex as lex #import ply library
token = None
####PLY Lexer. Takes in a string --> lextokens

# List of token names
token_names = [
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
	
	'NAME',
]

reserved = {
	'this is' : 'THISIS',
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'or' : 'OR',
	'and' : 'AND',
	'create' : 'CREATE',
	'new' : 'NEW',
	'variable' : 'VARIABLE',
	'is' : 'IS',
	'value' : 'VALUE',
	'define' : 'DEFINE',
	'a' : 'A',
	'function' : 'FUNCTION',
	'the' : 'THE',
	'condition' : 'CONDITION',
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

def t_COMMENT(t):
    r'((...))'
    pass
    # No return value. Token discarded
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

#class token definitions
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
class TheTok:
	pass
class ConditionTok:
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

class CreateTok(Token):
	pass
class NewTok(Token):
	pass
class VariableTok(Token):
	pass

#Parsing classes
class Create_NewVarTok(Token):
	def __init__(self, value = 0):
		self.value = value
		self.varname = None
		self.varvalue = None

	def __repr__(self):
		return "(%s): self.varname = %s, self.varvalue = %s" %(self.__class__.__name__, self.varname, self.varvalue)

class DefineTok(Token):
	pass
class ATok(Token):
	pass
class FunctionTok(Token):
	pass
class InstructionsTok(Token):
	pass

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

# reserved words:
	"THISIS" : ThisIsTok,
	"IF" : IfTok,
	"ELSE" : ElseTok,
	"WHILE" : WhileTok,
	"OR" : OrTok,
	"AND" : AndTok,
	"IS" : IsTok,
	"VALUE" : ValueTok,
	"CREATE" : CreateTok,
	"NEW" : NewTok,
	"VARIABLE" : VariableTok,
	"DEFINE" : DefineTok,
	"A" : ATok,
	"FUNCTION" : FunctionTok,
	"INSTRUCTIONS" : InstructionsTok,
	"THE" : TheTok
}

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
		raise SyntaxError("Expected %s but got %s" % (tok_class, token.__class__.__name__)) 
	
	print "\n"
def parse():
	pass
def parse_expression():
    advance() #put something into global token
    print "parsing done"
    return expression()

def parse_create(): 
	#advance('CreateTok') #advance on create - taken out b/c already advancing once
	advance('ATok') 
	advance('NewTok') #advance on new
	advance('VariableTok') #advance on variable
	advance('ColonTok') #advance on colon
	advance('NameTok')
	name_token = token #save name token as name_token
	create_newvarnode = Create_NewVarTok() #create new create_new_variable node
	create_newvarnode.varname = name_token.value #save the value of the name token as the varname attribute of Create_NewVarTok 
	advance('PeriodTok')
	return create_newvarnode

def parse_function():
	#advance('DefineTok')
	advance('ATok')
	advance('NewTok')
	advance('FunctionTok')
	advance('ColonTok')
	advance('NameTok')
	advance('InstructionsTok')
	advance('BlockTok')

def parse_if():
	advance('IfTok')
	advance('TheTok')
	advance('ConditionTok')
	advance('CommaTok')
	#parse_expression()
	advance('COLON')
	#parse_block()

    
def main():
	filename = sys.argv[1] if len(sys.argv) > 1 else None

	if filename:
		source = open(filename).read()
	else:
		source = raw_input(">What would you like to parse? ")
	
#LEXING	
	# Build the lexer
	spotlexer = lex.lex()

	# Lex the data
	spotlexer.input(source)
	#Lexer returns LexToken, with attributes: tok.type, tok.value, tok.lineno, tok.lexpos

	#create lex_token list
	lex_tokens = []
	while True:
		tok = lex.token()
		if not tok:
			break	
		lex_tokens.append(tok)

	print "these are the lex tokens", lex_tokens

#convert lextokens to class tokens
	for lex_token in lex_tokens:
		
		ltype = lex_token.type 
		lvalue = lex_token.value

		new_class_token = token_map[ltype](lvalue) #create an instance of the class, pass in lvalue
		class_tokens.append(new_class_token)
	new_end_tok = EndTok()
	class_tokens.append(new_end_tok)

	print "these are the class tokens", class_tokens
	
#PARSING
	
	print "before the first advance, the token is", token
	advance() #first advance, to get a token into it
	print "after the first advance, now there should be a token", token
	while token.__class__.__name__ != 'EndTok':
		parse() #parsing goes here	
		print " after advance() now the current token is", token
	
	# advance()
	# while token.__class__.__name__ != 'EndTok':
	# 	# print token
		# print token.__class__.__name__
		
		#parse_expression()
#commented out to work on other parse functions
		# if token.__class__.__name__ == 'CreateTok': 
		# 	print "now running parse_create()"
		# 	parse_create_result = parse_create()
		# 	print parse_create_result
		# 	return parse_create_result
		# if token.__class__.__name__ == 'DefineTok':
		# 	print "now running parse_function()"

			#parse_create_result = parse_create()
			# print parse_create_result
			# return parse_create_result


if __name__ == "__main__":
	main()





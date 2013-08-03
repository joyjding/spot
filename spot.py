# TOKENIZER AND PARSER FOR SPOT LANGUAGE
#############################################################
# TOKENIZER
# Tokenizer Uses Ply library
#############################################################

# import ply.lex as lex #import ply library

# # List of token names
# token_names = [
# 	'INT',
# 	'ADD_OP',
# 	'SUB_OP',
# 	'MUL_OP',
# 	'DIV_OP',
# ]

# tokens = token_names

# #-Token Functions----------------------------- 
# t_INT = r'[0-9][0-9]*'
# t_ADD_OP = r'\+'
# t_SUB_OP = r'-'
# t_MUL_OP = r'\*'
# t_DIV_OP = r'/'

# # Defines a rule for tracking line numbers
# def t_newline(t):
# 	r'\n+'
# 	t.lexer.lineno += len(t.value)
# # A string containing ignored chars (spaces and tabs)
# t_ignore = ' \t'

# def t_error(t):
# 	print "Illegal character '%s' " % t.value[0]

# # Build the lexer
# spotlexer = lex.lex()

# # Test data for lexer
# data = "1-1*2 3/"
# spotlexer.input(data)

# #Lexer returns LexToken , with attributes: tok.type, tok.value, tok.lineno, tok.lexpos
# lex_tokens = []
# while True:
# 	tok = lex.token()
# 	if not tok: break
# 	tdict = {
# 			"id": tok.type, 
# 			"value" : tok.value,
# 			"token_num" : tok.lexpos
# 			}
# 	lex_tokens.append(tdict)
# print lex_tokens
###############################################################################
# PARSER
# Top Down Precedence Parsing
################################################################################



# #-the Symbol class and the make_symbol function----------------------------------

# # Every token will inherit from a symbol, all of which are held in the symbol_dict
# symbol_dict = {}

# # Now I'm going to create an original_symbol object, which is the prototype for all of the symbols
# class Symbol:
# 	""" In Crockford, he implements an original_symbol class, and then adds
# 	methods to it in a symbol function object but I think it might be more
# 	elegant to simply create one symbol class that already has id and lbp methods. """
# 	def __init__(self, id, bp):
# 		self.id = id
# 		self.lbp = bp
# 		self.value = id #-------I still don't really understand why id and value are both id. It's probably changed later
# 	def nud(self): 
# 		return None
# 	def led (self):
# 		return None

# # Now I'm going to write a function that makes symbols

# def make_symbol(id, bp=0):
# 	symbol = symbol_dict.get(id)
# 	if symbol: #if id does not exist in symbol_dict
# 		if bp>=symbol.lbp: #-------why would I want to update this?
# 			symbol.lbp = bp
# 	else:
# 		symbol = Symbol(id, bp) # make a new instance of Symbol
# 		symbol_dict[id] = symbol # put the new symbol into the dictionary
# 	return symbol # return the symbol object

# # Now to make a couple of popular separator and closer symbols

# make_symbol(",")
# make_symbol(".")
# make_symbol(":")
# make_symbol(";")
# make_symbol(")")
# make_symbol("]")
# make_symbol("}")
# # make_symbol("else") --- commented out b/c I don't really understand why it's here
# make_symbol("(end)")
# make_symbol("(name)")

# #-Tokens--------------------------------------------------------------------------------

# #Global variable token
# TOKEN = None

# #The advance function takes the next LexToken, transforms it, assigns it to the token variable
# def advance_token (id = None): #optional id argument
# 	if id and (TOKEN.id != id):
# 		print "Did not get expected token" # -----Later on, this will raise an error
# 	if TOKEN[token_num] > len(lex_tokens): #-----Do people usually destroy tokens?
# 		TOKEN = symbol_dict["(end)"]
	
# 	newtoken = lex_tokens[TOKEN[token_num]] #----Do I start it off with token_num = 0?
# 	token_num +=1 #----increment token_num
# 	value = newtoken[value]
# 	arity = newtoken[type]

# 	if arity == "name": #----change lextokens category
# 		#more code here
# 		print "this token is a name token"
# 	elif arity === "operator":
# 		#more code here
# 		print "this token is an operator"
# 	elif arity === "string" or arity === "number":
# 		arity = "literal"
# 		object_prototype = symbol_dict["(literal)"]
# 	else:
# 		print "Unexpected token."

# 	TOKEN = Symbol(object_prototype)
# 	TOKEN.value = value
# 	TOKEN.arity = arity

# 	return TOKEN

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
        self.value = int(value)
    def nud(self):
        return self.value

class OperatorAddToken:
    lbp = 10
    def led(self, left):
        right = expression(10)
        return left + right

class EndToken:
    lbp = 0

import re

token_pat = re.compile("\s*(?:(\d+)|(.))")

def tokenize(program):
    for number, operator in token_pat.findall(program):
        if number:
            yield LiteralToken(number)
        elif operator == "+":
            yield OperatorAddToken()
        else:
            raise SyntaxError("unknown operator")
    yield EndToken()

def parse(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()











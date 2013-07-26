# implementation of Pratt parser
# source: http://effbot.org/zone/simple-top-down-parsing.htm


import re # import regex


class symbol_base(object):
	id = None # node/token type name
	value = None # used by literal tokens
	first = None # first, second, and third are used by tree nodes
	second = None
	third = None  

	def nud(self):
		raise SyntaxError ("Syntax error: (%r)." %self.id)
	def led(self, left):
		raise SyntaxError("Unknown operator (%r)." %self.id)
	def __repr__(self):
		if self.id == "(name)" or self.id == "(literal)":
			return "(%s %s)" % (self.id[1:-1], self.value)
		out = [self.id, self.first, self.second, self.third]
		out = map(str, filter(None, out))
		return "(" + " ".join(out) + ")"

symbol_table = {}

def symbol(id, bp=0):
	try:
		s = symbol_table[id]
	except KeyError:
		class s(symbol_base):
			pass
		s.__name__ = "symbol-" + id # for debugging
		s.id = id
		s.lbp = bp
		symbol_table[id] = s
	else:
		s.lbp = max(bp, s.lbp)
	return s
# populating the symbol table
symbol("(literal)")
symbol("+", 10)
symbol("-", 10)
symbol("*", 20)
symbol("/", 20)
symbol("**", 30)
symbol("(end)")

# defining led methods for symbols that need additional behavior

def infix(id, bp):
	def led(self, left):
		self.first = left
		self.second = expression(bp)
		return self
	symbol(id, bp).led = led

infix ("+", 10)
infix ("-", 10)
infix ("*", 20)
infix("/", 20)

# providing helper functions for nud methods, and for operators with right associativity
def prefix(id, bp):
	def nud(self):
		self.first = expression(bp)
		self.second = None
		return self
	symbol(id).nud = nud

prefix ("+", 100)
prefix("-", 100)

def infix_r(id,bp):
	def led(self, left):
		self.first = left
		self.second = expression(bp-1)
		return self
	symbol(id, bp).led = led

symbol("(literal)").nud = lambda self:self #what happened here?



# Class Definitions - Commented out now that we can generate tokens		

# class literal_token:
# 	def __init__(self, value):
# 		self.value = int(value)
# 	def nud(self):
# 		return self
# 	def __repr__(self):
# 		return "(literal %s)" %self.value

# class operator_add_token:
# 	lbp = 10
# 	def nud(self):
# 		self.first = expression(100)
# 		self.second = None
# 		return self
# 	def led(self, left):
# 		self.first = left
# 		self.second = expression(10)
# 		return self
# 	def __repr__(self):
# 		return "(add %s %s)" % (self.first, self.second)
# class operator_sub_token:
# 	lbp = 10
# 	def nud(self):
# 		self.first = -expression(100)
# 		self.second = None
# 		return self
# 	def led(self, left):
# 		self.first = left
# 		self.second = expression(100) # should this be -expression?
# 	def __repr__(self):
# 		return "(sub %s %s)" % (self.first, self.second) 

# class operator_mul_token:
# 	lbp = 20
# 	def led(self, left):
# 		self.first = left
# 		self.second = expression(20)
# 		return self
# 	def __repr__(self):
# 		return "(mul %s %s)" % (self.first, self.second)
# class operator_div_token:
# 	lbp = 20
# 	def led(self, left):
# 		self.first = left
# 		self.second = expression(20)
# 		return self
# 	def __repr__(self):
# 		return "(div %s %s)" %(self.first, self.second) 

# class operator_pow_token:
# 	lbp = 30
# 	def led(self, left):
# 		self.first = left
# 		self.second = expression(30-1)
# 		return self
# 	def __repr__(self):
# 		return "(pow %s %s)" %(self.first, self.second)
# class end_token:
# 	lbp = 0

#Tokenizing
token_pat = re.compile("\s*(?:(\d+)|(\*\*|.))")

def tokenize(program):
	for number, operator in token_pat.findall(program):
		if number:
			symbol = symbol_table["(literal)"]
			s = symbol()
			s.value = number
			yield s
		else: 
			symbol = symbol_table.get(operator)
			if not symbol:
				raise SyntaxError("Unknown operator")
			yield symbol()
	symbol = symbol_table["(end)"]
	yield symbol
# Parsing
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

def parse(program):
	global token, next
	next = tokenize(program).next
	token = next()
	return expression()



	
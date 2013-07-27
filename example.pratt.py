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

#Tokenizing
token_pat = re.compile("\s*(?:(\d+)|(\*\*|.))")

#This first half of the tokenizer turns the source program into a stream of literals
#names and operators
def tokenize_python(program):
	import tokenize # for tokenizer
	from cStringIO import StringIO # for tokenizer

	type_map = {
	tokenize.NUMBER: "(literal)",
	tokenize.STRING: "(literal)",
	tokenize.OP: "(operator)",
	tokenize.NAME: "(name)",
				}

	for t in tokenize.generate_tokens(StringIO(program).next):
		try:
			yield type_map[t[0]], t[1]
		except KeyError:
			if t[0] == tokenize.ENDMARKER:
				break
			else:
				raise SyntaxError("Syntax error")
	yield "(end)", "(end)" #apparently it was a typo in this line that caused the bug. originally, I had "end", "(end)"

#This second half of the tokenizer turns those into token instances.
#It checks operators and names agains the symbol table
# Pseudo-symbol (name) is used for all other names
def tokenize(program):
	for id, value in tokenize_python(program):
		if id == "(literal)":
			symbol = symbol_table[id]
			s = symbol()
			s.value = value
		else: 
			#for name or operator
			symbol = symbol_table.get(value)
			if symbol:
				s = symbol()
			elif id == "(name)":
				symbol = symbol_table["(literal)"]
				s = symbol()
				s.value = value
			else:
				raise SyntaxError("Unknown operator (%r)" %id)
		yield s

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



	
# implementation of Pratt parser
# source: http://effbot.org/zone/simple-top-down-parsing.htm


import re # import regex

#Class Definitions
class literal_token:
	def __init__(self, value):
		self.value = int(value)
	def nud(self):
		return self.value

class operator_add_token:
	lbp = 10
	def led(self, left):
		right = expression(10)
		return left + right

class operator_sub_token:
	lbp = 10
	def led(self, left):
		return left - expression(10)

class operator_mul_token:
	lbp = 20
	def led(self, left):
		return left / expression(20)

class operator_div_token:
	lbp = 20
	def led(self, left):
		return left / expression(20)
class end_token:
	lbp = 0

#Tokenizing
token_pat = re.compile("\s*(?:(\d+)|(.))")

def tokenize(program):
	for number, operator in token_pat.findall(program):
		if number:
			yield literal_token(number)
		elif operator == "+":
			yield operator_add_token()
		elif operator == "-":
			yield operator_sub_token()
		elif operator == "/":
			yield operator_div_token()
		else:
			raise SyntaxError("unknown operator")
	yield end_token

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
# Function call



	
import global_config

def expression(rbp=0):
    t = global_config.token
    global_config.token = global_config.next()
    left = t.nud()
    while rbp < global_config.token.lbp:
        t = global_config.token
        global_config.token = global_config.next()
        left = t.led(left)
    return left

symbol_dict = {}

class SymbolBase:
	id = None
	value = None
	first = None
	second = None
	third = None

	def nud(self):
		raise SyntaxError("no nud")
	def led(self, left):
		raise SyntaxError("no led")
	def __repr__(self):
		if self.id == "(name)" or self.id == "(literal)":
			return "(%s %s)" % (self.id[1:-1], self.value) #cuts parens off self.id
		out = [self.id, self.first, self.second, self.third]
		out = map(str, filter(None, out))
		return "(" + " ".join(out) + ")"

def symbol(id, bp=0):
	try: 
		s = symbol_dict[id]
	except KeyError:
		class s(SymbolBase):
			pass
		s.__name__ = "symbol:" + id #for debugging
		s.id = id
		s.lbp = bp
		symbol_dict[id] = s
	else: 
		s.lbp = max(bp, s.lbp)
	return s

def infix(id, bp):
	def led(self,left):
		self.first = left
		self.second = expression(bp)
		return self
	symbol(id, bp).led = led

def prefix(id, bp):
	def nud(self):
		self.first = expression(bp)
		self.second = None
		return self
	symbol(id).nud = nud
//Implementation of Pratt parser in JS
//Source: http://javascript.crockford.com/tdop/tdop.html



//Every token, such as an operator or identifier, will inherit from a symbol.
//All symbols (which will determine the types of tokens) will be kept in a symbol_table object
var symbol_table = {}; //empty object?

//Original_symbol is the prototype object for all other symbol objects.
//Comes with a nud and led functions that will be usually be overriden.
var original_symbol =  
{
	nud: function() 
	{
		this.error("Undefined.");
	},
	led: function(left) 
	{
		this.error("Missing operator.");
	}
};

//Now, we define a function that makes symbol objects.
//It takes a symbol id, and an optional binding power that defaults to 0, and returns a symbol object.
//If the symbol already exists in the symbol_table, the function returns that symbol object.
//Otherwise, it makes a new symbol object that inherits from the original_symbol, stores it in the symbol table, and returns it. 
//A symbol object initially contains an id, a value, a left binding power, and the stuff inherited from original_symbol.
var symbol = function(id, bp) //
{
	var s = symbol_table[id] //Why doesn't this fail if there is no entry for id?
	bp = bp || 0; //attribute bp = bp from optional argument, otherwise 0 
	if (s) //if s is not None (does symbol_table[id] act like get in Python?)
	{
		if (bp >= s.lbp) //if lbp in symbol_table lookup is less than bp
		{
			s.lbp = bp; //set lbp to bp for this symbol object
		}
	} else //if s is None
	{
		s = Object.create(original_symbol) //create s, inheriting from original_symbol
		s.id = s.value = id; //set s.value to id argument, set s.id to id argument
		s.lbp = bp; //set s.lbp to bp argument
		symbol_table[id] = s; //create an entry in symbol table[id arg], set equal to s
	}
	return s; //return symbol object
};

//Now to add some symbols to our symbol table:
symbol(":"); //create a new symbol with id ":"
symbol(";");
symbol(",");
symbol(")");
symbol("]");
symbol("}");
symbol("else");
symbol("(end)"); //indicates end of token stream.
symbol("(name)"); //prototype for new names, such as variable names.























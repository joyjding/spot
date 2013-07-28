//Implementation of Pratt parser in JS
//Source: http://javascript.crockford.com/tdop/tdop.html


///////////////////SYMBOLS////////////////////

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

///////////////////TOKENS////////////////////

//Assuming that the source text has been transformed into an array of simple token objects(tokens),
//each containing a type member("name", "string", "number", or "operator")

//the token variable always contains the current token LOOK GLOBAL VARIABLE

var token;

//The advance function makes a new token object from the next simple token in the array,
//and assigns it to the token variable.
//It can take an optional id parameter which it can check against the id of the prev toke. WHY would it check?
//The new token's arity is "name", "literal", or "operator".
//Its arity may be changed later to "binary", "unary", or "statement" when we know more about its role in the program.

var advance = function (id) //set the variable name advance to the value of a function that optionally takes id
//Are all parameters optional? How does this function know that the param is optional?
{
	var a, o, t, v;
	//check that there is no id error
	if (id && token.id !== id) //If both id and token.id do not equal id WEIRD
	{
		token.error("Expected '" + id + "'.")
	}
	//check to see if token stream has ended
	if (token_nr >= tokens.length) //what is token_nr? I guess if num tokens>=length of tokens array
	{
		token = symbol_table["(end)"];
		return; //what is being returned here?
	}
	//now we get to the good part.
	t = tokens[token_nr]; //Set t = to the token at tokens[token_nr];
	token_nr +=1 //advance token_nr Why isn't token_nr declared earlier?
	v = t.value;
	a = t.type;
	if (a === "name") //makes sense to use === here
	{
		o = scope.find(v); //no idea what just happened. Set o to some object??
	}
	else if (a === "operator") //if token type is operator
	{
		o = symbol_table[v] // Use the token's value as the key to look in symbol_table; set o to be this object
		if (!o) 
		{
			t.error("Unknown operator."); //if the object with key [value] does not exist, raise error. Why is this t.error? 
		}
	}
	else if (a === "string" || a === "number") //previously a = t.type, now we're changing the type
	{
		a = "literal"; //save "literal" in a, later we set a bunch of things in the token
		o = symbol_table["(literal)"]; // set o to be the object saved in symbol_table["(literal)"]
	}
	else {
		t.error("Unexpected token."); //if the type of the token is neither a name, operator, string, or number, throw an error
	}
	token = Object.create(o); //create a new object from o. Set global token to that object. 
	//Whoa, is Object.create just an inherent js method?
	token.value = v;
	token.arity = a;
	return token;
};























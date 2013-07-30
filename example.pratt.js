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

///////////////////SCOPE////////////////////

//Most languages have some notation for defining new symbols (such as variable names)
//In a very simple language, when we encounter a new word, we might give it a definition and put it in the symbol table
//In a more sophisticated language, we would want to have scope
//Scope gives the programmer control over the lifespan and visibility of a variable
//So for instance, global means that a variable has visibility to everything

//A scope is a region of a program in which a variable is defined and accessible
//Scopes can be nested inside other scopes
//Variables defined in a scope are not visible outside of the scope

// the current scope object is kept in the scope variable
var scope; 

//original_scope is the prototype for all scope objects
//It contains a define method that is used to define new variables in the scope
//The define method transforms a name token into a variable token
//It produces an error if: the variable has already been defined in the scope, 
//or if the name has already been used as a reserved word

var itself = function() 
{
	return this; //what does this do?
};

var original_scope = 
{
	define: function(n) //Defines a function without a name that takes n. 	
	//I'm guessing n is a name token object
	{
		var t = this.def[n.value];
		//What does this refer to? I'm guessing:original_scope. 
		//How can this.def be used here when it is not declared until later? line
		//So this is saying set the value of t to be object n
		//why not just var t = n?
		
		//This if loop checks if name has already been used as a reserved word				
		if (typeof t === "object") //if t is an object, 
		{
			n.error(t.reserved ?
			//I really don't understand .error
			//is .error a method available on any object?
			//What does this ? do?
			//When did we define .reserved?
				"Already reserved." :
				"Already defined.");
		} 
		//Here's where we define all the default attributes of original_scope
		//If it were me, I think I'd put this stuff before the if loop
		//That way, I'd have the default attributes, and the if could override if necessary 
		this.def[n.value] = n;
		n.reserved = false;
		n.nud = itself;
		n.led = null;
		n.lbp = 0;
		n.scope = scope;
		return n;
	},

	//The find function is used to find the definition of a name
	//It starts with the current scope, and seeks
	//if necessary back through the chain of parent scopes, and ultimately to the symbol table
	//It returns symbol_table["name"] if it cannot find a definition

	//When it finds a value, it tests it to determine that it is neither undefined nor a function
	//undefined would mean an undeclared name, which I'm taking to mean that it has never been assigned a value
	//if it's a function, it would indicate a collision with an inherited method
	//I'm taking that collision to mean one name means multiple things within the same scope
	find: function(n) 
	{
		var e = this, o; //Is this equivalent to: 
								//var e = this
								//var e = o
		while (true) 
		{
			o = e.def[n]; //this seems convoluted. Set o to be the value of e.def[n]
			//okay based on the check below, it seems it's to save different bits to parts of o
			
			//if o exists, and type of o is not a function
			if (o && typeof o !== "function")
			{
				return e.def[n];
			}
			//set e to be e's parent
			e = e.parent;
			//if e (which is e.parent) does not exist...
			if (!e) 
			{
				o = symbol_table[n]; //how does this configuration work? 
				//set o equal to symbol_table[n]
				//if symbol_table[n] doesn't exist...does o become None?
				return o && typeof o !=='function' ?
						o : symbol_table["(name)"];
			} 
		}
	},

	//The pop method closes a scope, giving focus back to the parent.

	pop: function() 
	{
		scope = this.parent; //reassigns scope to being the parent scope
	},

	//The reserve method indicates that a name has been used as reserved word in the current scope
	reserve: function(n)
	{
		if (n.arity !== "name" || n.reserved) //if neither n's type is "name" nor n.reserved is true, move on
		{
			return; 
			//what does this return? 
			//I'm guessing it's one of those I need to return something in js so...here's a return things
		}
		var t = this.def[n.value]; //I really don't undersatnd this .def method
	//This is the handle both conditions (if n's type is name or if n.reserved is true)
		if (t) //if this.def[n.value] exists
		{
			if (t.reserved) //if t is reserved, which must be a boolean
			{
				return; //don't do anything
			}	

			if (t.arity === "name") //if the type of t is name
			{
				n.error("Already defined.");
			}
			this.def[n.value] = n;
			n.reserved = true;
		}
	};

	//We need a policy for reserved words. 
	//In some languages, words that are used structurally (like if) are reserved, and cannot be used as variable names.
	//The flexibility of this parser allows us to have a more useful policy (which I disagree with).
	//For example, we can say: in any function, any name may be used as a structure word or as a variable, but not both.
	//We will reserve words locally only after they are used as reserved words.
	//Crockford argues that this makes things better: 
	//for language designers, b/c adding new structure words to the language will not break existing programs
	//and for programmers, b/c they are not hampered by irrelevant restrictions on name usage
	//(I'm not sure if I agree with this. I probably don't.)
	//(I think that there are enough words for us to distinguish, rather than duplicate)
	//(Also when would I ever want a variable named if?)
	var new_scope = function() 
	{
		var s = scope;
		scope = Object.create(original_scope); //here we create an instance of a scope object!
		scope.def = {};
		scope.parent = s; //wait, how is scope its own parent????
		return scope
	};

///////////////////PRECEDENCE////////////////////

//Tokens are objects that have methods that allow them to:
//make precedence decisions, match other tokens, and build trees
//(and, in a more ambitious project, check types and optimize and generate code)

//The basic precedence problem: given an operand between 2 operators, is the operand bound to the left operator or the right?
	//d A e B f
//If A and B are operators, does e bind to A or B? 
	//(d A e) B f   or   d A (e B f)?
//Here, we develop a technique that uses token objects whose members include:
//binding powers (or precedence levels), and simple methods called nud(null denotation) and led (left denotation)
//A nud method does not care about the tokens to the left.
//A led method cares about tokens to the left.
//A nud method is used by values(such as variables and literals) and by prefix operators.
//A led method is used by infix operators and suffix operators. 
//A token may have both a nud method and a led method. 
//For example, - might be both a prefix operator (negation) and an infix operator (subtraction), so it woudld have both. 

//In our parser we will use these as binding powers:
	// 0 --- non-binding operators like ;
	//10 --- assignment operators like =
	//20 --- ?
	//30 --- || &&
	//40 --- relational operators like ===
	//50 --- + -
	//60 * /
	//70 --- unary operators like !
	//80 --- . [ (

///////////////////EXPRESSIONS////////////////////

//Here's where we get into the heart of Pratt's technique, the expression function.
//The expression function takes a right binding power as an argument that controls how aggressively the current token binds to tokens on its right.

//Expression calls the nud method of the token
//The nud is used to process literals, variables, and prefix operators
//As long as the right binding power is less than the left binding power of the next token, the led method is invoked on the following token
//The led is used to process infix and suffix operators
//This process can be recursive b/c the nud and led methods can call expression
//Okay, seems like we haven't defined these yet
var expression = function(rbp) //function expression takes rbp as its argument
{
	var left; //declare variable left -- seems redundant, why not just say var left = t.nud(); later?
	var t = token; //t = current token
	advance(); //In this implementation, advance actually saves the next token to token
	left = t.nud(); //I don't see this .nud as returning anything except in original_scope
					//Where di we set .nud?
	while (rbp<token.lbp) //while rbp is less than the lbp of the next token, keep going
	{
		t = token; //token (on the first pass, it's the next token)
		advance();//assign token to be the even next token
		left = t.led(left); //set left = t.led(left)
	}
	return left;
}	
























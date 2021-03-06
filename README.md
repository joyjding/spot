#Spot language


 Inspired by the simple language of See Spot Run, Spot is a language designed to expose the logic of programming to a beginning programmer using plain English syntax. Spot compiles to x86 assembly and its machinery from string to final compilation includes a PLY lexer, a Pratt recursive descent parser, and code generation functions that emit assembly.

###Quick Links:

- [Learn some Spot syntax](https://github.com/joyjding/spot#syntax-how-to-talk-to-your-computer-in-spot)

- [Code machinery](https://github.com/joyjding/spot#gears-gears-gears)



###Background

Hello there! So nice to meet you. Driven by an ever-present curiousity about how things really work, the thrill of a challenge, and a love of languages and language processing, I chose to design and implement a programming language for my Hackbright personal project. Spot was built in 3.5 weeks, and as such, is definitely a work in progress.  


###Getting Started: Setup, etc.

Go ahead and clone this repository to your computer.
    
    git clone https://github.com/joyjding/spot

Spot can run in compilation or interpretation mode. In compilation mode, Spot compiles to x86 assembly. In interpretation mode, Spot commands are interpreted in Python. 

To run Spot in compilation mode:

Run spot.py on your file of choice. This generates a filename.asm file.
    
    python spot.py <filename.spot>

Then, take the asm file and run it through a nasm assembler, which generates an object file that you can then run as an executable. Note: Not all features work in compilation. 


To run Spot in interpretation mode:
    
Run spot.py on your file of choice. 
    
    python spot.py <filename> -eval




###Syntax: How to Talk to Your Computer in Spot

1. Put comments to yourself or anyone else in parentheses
        
        (Hi! I just started writing in Spot!)
        (Oh, really?)
        (Yeah. Okay, maybe we should stick to Twitter for conversations from now on)

2. Creating and setting new variables

        Create a new variable cats, an integer.
        Set cats' value to 10000. 

3. Printing to the screen

        Screensay: "How'd this get on my screen?".
        Screensay: "Hey, stop that!".
        Screensay: "Printing to screen. You asked for it, right?".

4. If/ Else If /Else
        
        If the condition cats < 10000, follow these instructions: 
            {Screensay: "Time to head to the SPCA.".}

        Else if the condition cats is equal to 10000, follow these instructions: 
            {Screensay: "Goldilocks theorem satisfied. I have just the right amount of cats.".}

        Else, follow these instructions: 
            {Screensay: "Ahhhhhhhhhhhhhh!!!".}

5. While loops
        
        While the condition cats is equal to 1, follow these instructions: 
            {Screensay: "Spend all your time following your cat with your thumb hovering over Vine.".}

        (Notice, that if cats is initially set to 1, this while loop will never end. 
        Thank goodness cats is set to 10000, or we'd really be in trouble.)

6. Defining and running functions

        Define a new function running amok.

        When called, it follows these instructions: 
            {Screensay: "Running amok! Running amok! Running amok!"}.

        Run the function running amok. 


###An Example Program: Fizzbuzz.spot 


Here you see the code for fizzbuzz.spot :
    
    (FIZZBUZZ)

    Define a new function fizz buzz, which takes 1 integer argument: end.
    When called, it follows these instructions: {
        
        Create a new variable counter, an integer. 
        Set counter's value to 1.

        While the condition counter < end, follow these instructions: {
            If the condition counter modulus 5 is equal to 0, follow these instructions: {Screensay: "BUZZ".}.
            
            Else if the condition counter modulus 3 is equal to 0, follow these instructions: {Screensay: "FIZZ".}.

            Increase counter's value by 1. 
        }.
    }. 

    Run the function fizz buzz, passing in the argument 10.

### Reserved Key Words and Phrases

#### Reserved Words

    true
    false
    [Rr]eturn
    value
    takes
    a[n]
    by
    or
    and
    to
    it
    else
    if
    argument[s]
    set

#### Reserved Phrases
    
    Create [a] new variable
    Define [a] new function
    Run the function
    If the condition
    While the condition
    When called
    
    which takes
    is equal to
    passing in the arguments
    follow these instructions


### Gears, gears, gears

Spot is composed of several key parts: a PLY lexer, recursive descent parser, Python interpreter and x86 assembly code generator. 

In brief, a file is read in and broken up into tokens by the PLY lexer and mapped 1:1 to Python class objects. The parser checks if a token object possesses a statement method. If the token has a statement method, it is parsed as a statement; otherwise, it is parsed as an expression using Pratt-style expression parsing. Parsing generates an abstract-syntax tree, which can then either be interpreted in Python using the eval() method on each token, or written into an .asm file using the codegen() method on each token.


### Lexing 

Lexing is the process of converting an input stringinto a stream of significant tokens based on the grammar of a language. I used the [PLY](http://www.dabeaz.com/ply/) library to lex my tokens, such that an input string is broken into LexTokens, with the structure (tok.type, tok.value, tok.line, and tok.lexpos). 

So, given the string:
    
    Screensay: "Hello World.".

PLY generates:

    [LexToken(SCREENSAY,'Screensay',1,0), LexToken(COLON,':',1,9), LexToken(STRING,'"hello world."',1,11), LexToken(PERIOD,'.',1,25)]

Then, I took the LexTokens, and mapped them 1:1 to Python class token objects. This generates:

    [ScreensayTok, ColonTok, StringTok, PeriodTok, EndTok] 

### Parsing

_Note: For the purposes of explaining parsing, methods on class objects that are not related to parsing will be left out._ 


After the list of token objects is generated, `parse()` is called, and its results (an abstract syntax tree) will be saved to a program variable. 
    
```python
program = parse()   
```

The parse function kicks off the parsing. It creates a global scope, which is used to store created variables and their assignments. 

```python
def parse():    
    global scope
    scope = Scope()
    advance() #to put the first token in
    p = Program()
    p.statementd()  
    return p
```

Then it calls `advance()`, a function that pops the first item off the class token list, and puts it into a global variable named token. It creates a new instance of the Program class, and calls `statementd()` on that new Program, which calls `statement()`. `statement()` checks if the token has a `statementd()` method, which means the token is the beginning of a larger statement. Otherwise, the token is evaluated as an expression. Essentially, this allows the parser to parse exactly one statement at a time, and determine whether to parse it as a statement or an expression. And here's where things get interesting, and we get into Pratt-style parsing.    


### Pratt Parser

Although code generation is well-documented, both examples that I drew on for coding my parser were non-intuitive and difficult to understand. So here, I will attempt to describe Pratt, for anyone else writing a Pratt-style recursive descent parser.

#### Why Pratt?

Recursive-descent parsers are pretty efficient, so as long as the next action to take can most of the time be determined by what happens at the beginning of a statement. A recursive-descent parser checks the first token in a sequence, and then performs an appropriate action. 

This is all well and fine until we get to expressions, for instance:

    1+2*3

In the case of `1+2*3` , the parser cannot simply take an action based on what it sees first (`1`). It needs to be able to determine that `2*3` needs to be evaluated first, and then added to the `1`. Pratt-style recursive descent parsing makes it possible for expressions to be parsed efficiently. 

#### leftd(), nulld(), and lbp

Before we dive into Pratt's expression function, we're going to need to know a couple of things first. And to help us out, we'll take a look at these three object classes: the add operator token (AddOpTok), the multiply operator token (MulOpTok), and the integer token (IntTok).

```python
class AddOpTok(BinaryOpToken):
    lbp = 50
    
    def nulld(self):
        return expression(100)
    def leftd(self, left):
        self.first = left
        self.second = expression(50)
        return self

class MulOpTok(BinaryOpToken):
    lbp = 70

    def leftd(self, left):
        self.first = left
        self.second = expression(70)
        return self

class IntTok(LiteralToken):
    lbp = 0

    def nulld(self):
        return self
```

You'll notice that each of these tokens has a `lbp` attribute, and that the AddOptok has both a `nulld()` and `leftd()` method, while the MulOpTok only has a `leftd()` and the IntTok only has a `nulld().`

**nulld()** is the method that is called when the token appears at the beginning of an expression, and there is nothing (or null) before it. IntTok has a `nulld()` because you can start mathematical expressions, like `1+2` with an integer (in this case, `1`). Likewise, it makes sense that the add operator has a nulld(), because of expressions like `+4`. And yes, the subtract operator also has a nulld(), so negative numbers can be parsed correctly. 

**leftd()** is the method that is called when there are other tokens to the left of the token the parser is looking at. Both the MulOpTok and the AddOpTok have leftd() methods because they are binary operators. So for an expression like 5+2, when the parser is considering the `+`, the `5` is still to the left of it, so leftd() is called. 

**lbp** stands for left binding power. Left binding power is a number that represents how tightly a token "holds on" to the partial expression to the left of it. Accordingly, it makes sense that the AddOpTok (`lbp=50`) would have a smaller lbp than the MulOpTok (`lbp=70`), as multiplication comes before addition in order of operations. 

####Pratt's expression function

Okay, now we're ready to take a look at the heart of Pratt-style recursive descent parsing, the expression function. Implemented in Python, it looks something like this:

```python
def expression(rbp=0):      
        t = token
        advance()
        left = t.nulld()
        while rbp < token.lbp:
            t = token
            advance()
            left = t.leftd(left) 
        return left
```     

The advance function used looks like this:

```python
def advance(tok_class = None):
    global token
    #check if the current token is the one expected
    if (tok_class and not isinstance(token, tok_class)):
        raise SyntaxError("Expected %s but got %s" % (tok_class, token.__class__.__name__)) 
    
    current_token = token   

    #if so, move on to the next token
    token = class_tokens.pop(0)
    return current_token
```

Let's work through it with our previous example, `1+2*3`, using the two parsing diagrams below.

#####Diagram A

![Expression a](https://raw.github.com/joyjding/spot/master/images/expression_a.png)

At the beginning of parsing an expression, the expression function is called, with a rbp (right binding power) of `0` ( **Step 1** ). Rbp is set to `0`, because it is just a placeholder for when expression is later called with an lbp. For instance, the AddOpTok leftd() method calls expression(50). This also makes sense, because at this point, there is no partial expression to the right to bind to, as we are at the beginning of parsing an expression. 

Then, the global token variable is saved as `t`. In our case, the global token variable is `1`. Advance is called without an argument, which means it pops the next Python class token object off of the list and saves it in the global token variable. The `nulld()` method is called on the first token, and saved in the left variable. The while loop code executes because `0` is `<` the lbp of the add token. At the end of the while loop in **Step 1**, the `leftd()` method is called on t, which is currently `<+>`, which kicks off **Step 2**, the second calling of the expression function, this time passing in 50 for rbp. Then in **Step 3**, expression is called again, this time with the lbp of the `<*>`. But this time, when we get to the while loop, the condition of the while loop is false. `50` is not smaller than `0`, the lbp of EndTok ( **Step 4** ), so the while loop does not execute, bringing us to Diagram B, **Step 5**.

#####Diagram B
![Expression b](https://raw.github.com/joyjding/spot/master/images/expression_b.png)

In **Step 5**, left, the `<3>` token, is returned from `expression(70)`, and saved as the self.second attribute of `<+>` in `expression(50)`. So now, `left = t.leftd(left)` in `expression(50)` is complete, bringing us back to evaluate the while loop condition in `expression(50)`. And here's where the usage of the global token variable really shines. Because token is a global variable, now, when we evaluate `while rbp <token.lbp` we get `50 < EndTok.lbp`, which gives us '50 < 0'. This means that the while loop does not execute again, bringing us to **Step 7**. **Step 7** returns left, the `<*>` token with `<*>.first = <2>` and `<*>.second = <3>`. The entirety of the <*> token is then saved as the .second attribute of the `<+>` token in `expression(0)`. This brings us to **Step 8**, the evaluation of the while condition in `expression(0)`. Once again, `while rbp < token.lbp` gives us `while 0 < <EndTok>.lbp`, or `0 < 0`. As 0 is not less than 0, the while loop does not execute, and we go straight to **Step 9**, which returns left, the parse tree you see in **Step 10**. 

_Whew! That was a lot of words and diagrams. I hope that this explanation is helpful. Please feel free to ask questions or give feedback, so it can be even more clear._

### Interpretation

Spot is interpreted in Python, an intermediate step created mostly to make sure that parsing worked correctly, and to play with some features of interpreted languages like string interpolation. 

### Code gen

Code gen for Spot is accomplished with the `codegen()` method on each token. The codegen methods take attribute information that has been saved during parsing, and write sequential strings of assembly code to a couple of different lists that are then used to generate an .asm file. A list of assembly commands is returned as the result of `program.codegen()`. All created variables and their sizes are added to a list called `literal_list`, which will later be used to generate the .data section of the .asm file. Then, all of the lists are written to a .asm file in order: first a header, then the assembly commands code, followed by the .data section code, and finally a footer.  

####Thoughts on Code gen
The most difficult part of code gen was learning x86 assembly. I had known from the very beginning of the project that I wanted to delve into assembly, because it would be the closest that I could get to machine code.













--in progress--

















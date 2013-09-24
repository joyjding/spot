#Spot language

Hello there! So nice to meet you. 

Driven by an ever-present curiousity about how things really work, the thrill of a challenge, and a love of languages and language processing, for my final HB project I chose to design and implement a programming language. Inspired by the simple language of See Spot Run, Spot is a language designed to expose the logic of programming to a beginning programmer using plain English syntax. Spot compiles to x86 assembly and its machinery from string to final compilation includes a PLY lexer, a Pratt recursive descent parser, and code generation functions that emit assembly.

Spot was built in 3.5 weeks as my Hackbright personal project, and as such, is definitely a work in progress.  

Choose your own Spot adventure:

- [I'd like to learn some Spot syntax!](https://github.com/joyjding/spot#syntax-how-to-talk-to-your-computer-in-spot)

- [Show me the code gears!](https://github.com/joyjding/spot#gears-gears-gears)


###Getting Started: Setup, etc.

Go ahead and clone this repository to your computer.
	
	git clone https://github.com/joyjding/spot

Spot can run in compilation or interpretation mode. In compilation mode, Spot compiles to x86 assembly. In interpretation mode, Spot commands are interpreted in Python. 

To run Spot in compilation mode:

1. Run spot.py on your file of choice. This generates a filename.asm file.
	
		python spot.py <filename.spot>

2. Take the asm file and run it through codegen.sh, a shell script. Codegen.sh creates an object file and then executes it.

		./codegen.sh <filename>


To run Spot in interpretation mode:
	
1. Run spot.py on your file of choice. 
	
		python spot.py -eval <filename>

2. Results will show up in the terminal window. 


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


### Gears, gears, gears

Spot is composed of several key parts: a PLY lexer, recursive descent parser, Python interpreter and x86 assembly code generator. 

In brief, a file is read in and broken up into tokens by the PLY lexer and mapped 1:1 to Python class objects. The parser checks if a token object possesses a statement method. If the token has a statement method, it is parsed as a statement; otherwise, it is parsed as an expression using Pratt-style expression parsing. Parsing generates an abstract-syntax tree, which can then either be interpreted in Python using the eval() method on each token, or written into a .asm file using the codegen() method on each token.



















#spot

Hello there! So nice to meet you. 

Spot is an English syntax programming language that seeks to expose and teach a beginner programmer the logic foundations of programming without the overhead of learning what different symbols mean. Spot's machinery (parser/interpreter/compiler) is built on Python. Most of Spot compiles to x86 assembly.

So without further ado, let's get started!

###Getting Started (Boring, but necessary)

Go ahead and clone this repository to your computer. That gives you the requisite PLY library to run the lexer, a couple of sample Spot files to play with and spot.py, which is the engine that drives Spot. Then, you can start writing .spot files on your own!

##Syntax (Talking to your computer in Spot)

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

		(Notice, that if cats is initially set to 1, this while loop will never end. Thank goodness cats is set to 10000, or we'd really be in trouble.)



##All Together Now


Now let's see what an example program might look like. 

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

Testing syntax headers 

#One 
##Two
###Three
####Four
#####Five
######Six








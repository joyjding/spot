spot
====

Hello there! So nice to meet you. 

Spot is an English syntax programming language that seeks to expose and teach a beginner programmer the logic foundations of programming without the overhead of learning what different symbols mean. Spot's machinery (parser/interpreter/compiler) is built on Python. Most of Spot compiles to x86 assembly.

So without further ado, let's get started!

Setup (The boring, but necessary part)
===
Go ahead and clone this repository to your computer. That gives you the requisite PLY library to run the lexer, a couple of sample Spot files to play with and spot.py, which is the engine that drives Spot. Then, you can start writing .spot files on your own!

Syntax (How to talk to your computer in Spot)
===

Using fizzbuzz.spot as an example, let's take a walk through Spot syntax. 

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

1. Put comments to yourself or anyone else in parentheses
		
		(Hi! I just started writing in Spot!)
		(Oh, really?)
		(Yeah. Okay, maybe we should stick to Twitter for conversations from now on)



Creating and Setting Variables
----

	Create a new variable apples, an integer. 
	Set apples' value to 8. 

If/Else If/Else
----
	If the condition apples









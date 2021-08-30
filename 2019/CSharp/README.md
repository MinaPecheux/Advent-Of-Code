# [2019] CSharp (C#)

This subfolder contains my code solutions for challenges from the 2019 series, written in C# (5.0.7).

## Preliminary note: files organization
In these files, I try to always organize the code in the same way:

1. first, some imports if need be (usually C# built-in libs)

2. then, parsing functions to read and extract data from the provided input (that seems to always be a string of characters, or anyway lines in a text file)

3. then, the actual computation functions, separated in 3 bits:
  - util and common functions
  - functions for the Part I of the problem
  - functions for the Part II of the problem
  
4. a test function with a set of ``Debug.Assert``s to check that my computation functions seem to give an ok result (using the examples provided with the problem)

5. finally, the main part that solves the problem by running the computation functions on the actual inputs I was given (that depend on the user)

For data parsing and conversion, I will often rely on the [C# Linq utility](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) that allows you to quickly write very readable and optimized data pipelines :)

## Day 1: The Tyranny of the Rocket Equation

#### Answers
**Part I: 3345909 • Part II: 5015983**

This first challenge is a good opportunity to quickly discuss how we can use [C# Linq](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) to parse and convert our data to a more usable format. In our case, the puzzles are given as text files, i.e. multiple lines that are each a string, and you generally want to extract this info into a more easy-to-use data structure.

Here, we simply want to convert the strings to ints (checking if the line is not null). I do this in my ``ParseInput()`` function, at the top of the class, and I use ``Where()`` for filtering and ``Select()`` for re-mapping.

Other than that, this first puzzle is pretty straight-forward. The only notable thing is that Part II strongly indicates you should [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) to solve the problem. Given that you have a question of the form "compute a value for something, then compute the value for this new thing, and so on..." you want to create recursive function, i.e. a process where your top solution depends on the solution you computed for smaller instances of the problem.

You therefore call the function from within itself (here ``ComputeTotalFuel()`` is called inside of ``ComputeTotalFuel()``).

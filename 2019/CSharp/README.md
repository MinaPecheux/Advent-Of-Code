# [2019] CSharp (C#)

This subfolder contains my code solutions for challenges from the 2019 series, written in C# (5.0.7).

## Preliminary note: files organization
The main entrypoint for this C# project is the ``index.cs``. It is a simple console interpreter that takes in the number of the program you want to run (for example, 1 for ``day1.cs``) and runs the corresponding code.

Here is how to run the code for Day 1 using the .NET command line utilities:

```
dotnet run -- 1
```

Also, in the puzzle files, I try to always organize the code in the same way:

1. first, some imports if need be (usually C# built-in libs, sometimes my own extensions)

2. then, parsing functions to read and extract data from the provided input (that seems to always be a string of characters, or anyway lines in a text file)

3. then, the actual computation functions, separated in 3 bits:
  - util and common functions
  - functions for the Part I of the problem
  - functions for the Part II of the problem
  
4. a test function with a set of ``Debug.Assert``s to check that my computation functions seem to give an ok result (using the examples provided with the problem)

5. finally, the main part that solves the problem by running the computation functions on the actual inputs I was given (that depend on the user)

For data parsing and conversion, I will often rely on the [C# Linq utility](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) that allows you to quickly write very readable and optimized data pipelines :)

## Util extensions (``utils.cs``)

This file contains some static classes that define extension methods and other util methods or variables for the main scripts.

## Intcode interpreter (``intcode.cs``)

This year, several puzzles make use of an Intcode interpreter that is built gradually all throughout Day 2, 5, 7 and 9 (at this point, you're supposed to have a complete interpreter able to execute any Intcode program that you're given).

It is further used on Days 11, 13, 15, 17 and 19.

In order to avoid repeating code, I've coded up my Intcode interpreter into a dedicated file called ``intcode.cs``. To do that, I've used a key feature of C# that falls under the object-oriented programming paradigm: classes. It is a nice way of aggregating together bits of code that have a logical link.

To create a basic class you can instantiate, you should simply use the ``class`` keyword and then define at least a constructor:

```csharp
class IntcodeProgram {
  public IntcodeProgram() {}
}
```

This constructor will be called whenever you instantiate a new variable of type ``IntcodeProgram``. The neat thing with object-oriented programming, as I said just before, is that you can gather in the same place various variables or methods that are logically linked together; here, our class can contain other methods that implement the behavior we want one of program instance to have: a basic state check, memory updates, instructions execution...

My final ``IntcodeProgram`` class provided me with an easy-to-use interface for my actual computation functions in the puzzle scripts. In those functions, I just create instances of the ``IntcodeProgram`` class and play around with them, but the class abstracts away all the actual execution or memory management stuff so that these computation functions aren't too long.

This means that the true meat of the code resides in the ``IntcodeProgram`` class.

I've used a static class variable called ``INSTANCE_ID`` to assign auto-incrementing IDs to my instances. Rather than maintaining a counter outside of the class, I can just let it take care of it and automatically generate a new integer ID whenever I create a new instance of my class. However, I need to be careful to reset the counter whenever I want to reset my pool of instances from scratch (for example, in Day 7, whenever I want to try a new permutation of phase settings).

## Day 1: The Tyranny of the Rocket Equation

#### Answers
**Part I: 3345909 • Part II: 5015983**

This first challenge is a good opportunity to quickly discuss how we can use [C# Linq](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) to parse and convert our data to a more usable format. In our case, the puzzles are given as text files, i.e. multiple lines that are each a string, and you generally want to extract this info into a more easy-to-use data structure.

Here, we simply want to convert the strings to ints (checking if the line is not null). I do this in my ``ParseInput()`` function, at the top of the class, and I use ``Where()`` for filtering and ``Select()`` for re-mapping.

Other than that, this first puzzle is pretty straight-forward. The only notable thing is that Part II strongly indicates you should [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) to solve the problem. Given that you have a question of the form "compute a value for something, then compute the value for this new thing, and so on..." you want to create recursive function, i.e. a process where your top solution depends on the solution you computed for smaller instances of the problem.

You therefore call the function from within itself (here ``ComputeTotalFuel()`` is called inside of ``ComputeTotalFuel()``).

## Day 2: 1202 Program Alarm

#### Answers
**Part I: 3716293 • Part II: 6429**

> Day 2 relies on the Intcode interpreter that is implemented in the ``intcode.cs`` file.

This problem is an opportunity to talk about **mutability** in CSharp. We are making use of the Intcode interpreter for the first time and we need to pass it the code to execute (which is stored as a list of integers). In my ``IntcodeProgram`` class, this program is turned into a dictionary. This allows me to make a new "version" of the inputs that is independent from the initial array that I feed the instance so that it isn't touched by the code.

Mutable variables are variables that, even if they are passed as parameters to functions, still point to the same address in memory and can therefore be modified directly.

On the other hand, immutable classes like the basic types (``bool``, ``int``, ``float``, ``string``) and some particular containers (from the ``System.Collections.Immutable`` package) cannot be modified after being created. If you want to change the value, you need to reassign the variable to a brand new value in memory.

For example, in the ``ProcessInputs()`` function, I pass the ``inputs`` list to my Intcode program so that it makes its own copy of it.

If I removed this transformation, I would need to "copy" the inputs before running them through any processing code!

> For more info on immutable data structures in C#, you can check out [Microsoft's docs](https://docs.microsoft.com/en-us/dotnet/api/system.collections.immutable?view=net-5.0).

## Day 3: Crossed Wires

#### Answers
**Part I: 209 • Part II: 43258**

The challenge with this problem was to handle the large lists as quickly as possible. To do so, I used lists, dictionaries and enumerables and tried to make the best out of those worlds (depending on [the time complexity of various operations for each data type](http://c-sharp-snippets.blogspot.com/2010/03/runtime-complexity-of-net-generic.html)):

- lists are ordered, meaning that you can access elements by index, and they allow for ``min`` or ``max`` operations; this lets me easily refer to the "first" (at index 0) and the "second" (at index 1) wire, to take the smallest distance...

- dictionaries are hashable containers that work with key-value pairs; they are great for quick element access (it is in `O(1)`, i.e. in constant time, unless there is a collision)

- enumerables are interesting as "soon-to-be" data containers; basically, they are iterators that you can run through without storing everything in memory beforehand, which can help reduce your program overall load on the computer

By using the right data type at the right time, you can increase the computation time tremendously.

## Day 4: Secure Container

#### Answers
**Part I: 1019 • Part II: 660**

There is not much to say with this solution, except that I use:

- a little Linq trick, with ``GroupBy()``, to easily count the occurrences of each character in my stringified number
- a delegate with the prototype of my check functions (for Parts I and II) to pass either to my `GetCountOfValidNumbers()` method as an input parameter

Also, I take advantage of C#'s ability to quickly change from one type to another by treating my number and its digits either as integers or as characters depending on what I need.

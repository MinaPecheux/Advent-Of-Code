# [2019] Python

This subfolder contains my code solutions for challenges from the 2019 series, written in Python (3.6.5).

## Preliminary note: files organization
In these files, I try to always organize the code in the same way:

1. first, some imports if need be (either Python built-in libs or external packages, **even if I will try and stay as "built-in" as possible in my answers**)

2. then, parsing functions to read and extract data from the provided input (that seems to always be a string of characters)

3. then, the actual computation functions, separated in 3 bits:
  - util and common functions
  - functions for the Part I of the problem
  - functions for the Part II of the problem
  
4. a test of function with a set of ``assert``s to check that my computation function seem to give an ok result (using the examples provided with the problem)

5. finally, the main part that solves the problem by running the computation functions on the actual inputs I was given (that depend on the user)

## Day 1: The Tyranny of the Rocket Equation

#### Answers
**Part I: 3345909**
**Part II: 5015983**

This first challenge is pretty straight-forward. The only notable thing is that Part II strongly indicates you should [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) to solve the problem. Given that you have a question of the form "compute a value for something, then compute the value for this new thing, and so on..." you want to create recursive function, i.e. a process where your top solution depends on the solution you computed for smaller instances of the problem.

You therefore call the function from within itself (here ``compute_total_fuel()`` is called inside of ``compute_total_fuel()``).

## Day 2: 1202 Program Alarm

#### Answers
**Part I: 3716293**
**Part II: 6429**

This problem is an opportunity to talk about **mutability** in Python: in this solution, I extensively use the fact that ``list``s are mutable in Python. This means that even if they are passed as parameters to functions, the variables still point to the same address in memory and can therefore be modified directly.

On the other hand, immutable classes like the basic types (``bool``, ``int``, ``float``, ``str``) and some particular containers (``set``, ``tuple``, ``frozenset``) cannot be modified after being created. If you want to change the value, you need to reassign the variable to a brand new value in memory.

For example, in the ``process_inputs()`` function, I directly touch the ``inputs`` list that is passed as a parameter as I execute the Intcode program.

Hence the need to "restore" the inputs before running the code for Part II!

> For more info on immutability in Python, you can check out [Python's reference](https://docs.python.org/3/reference/datamodel.html?highlight=immutability) on the data model (Dec. 2019).

## Day 3: Crossed Wires

#### Answers
**Part I: 209**
**Part II: 43258**

The challenge with this problem was to handle the large lists as quickly as possible. To do so, I used lists, dictionaries and sets and tried to make the best out of those worlds (depending on [the time complexity of various operations for each data type](https://wiki.python.org/moin/TimeComplexity)):

- lists are ordered, meaning that you can access elements by index, and they allow for ``min`` or ``max`` operations; this lets me to easily refer to the "first" (at index 0) and the "second" (at index 1) wire, to take the smallest distance...

- dictionaries are hashable containers that work with key-value pairs; they are great for quick element access (it is in `O(1)`, i.e. in constant time)

- sets are quite close to dictionaries but they are super fast at union and intersection operations; this is a big plus for my ``intersections`` computation that just needs to check what keys are in common in two dictionaries

By using the right data type at the right time, you can increase the computation time tremendously.

## Day 4: Secure Container

#### Answers
**Part I: 1019**
**Part II: 660**

There is not much to say with this solution, except that I use a built-in Python lib, ``collections``. This package contains some very useful additional types that are optimized for a specific task. For example, here, I use a ``Counter`` that is very quick at creating a dict-like structure that associates each unique value in a list to the number of times it appears (see the function ``number_is_ok_p2()``).

Also, I take advantage of Python's ability to quickly change from one type to another by treating my number and its digits either as integers or as characters depending on what I need.

## Day 5: Sunny with a Chance of Asteroids

#### Answers
**Part I: 15508323**
**Part II: 9006327**

This challenge builds on Day 2. The code therefore is an extension of my solution for Day 2.

In this version, I have made 3 major modifications:

1. I have added a custom util ``Debugger`` class
2. I have reorganized the ``OPERATIONS`` dictionary to hold more information, namely the number of inputs for each operation (plus I've added the new operations defined in the problem)
3. I have improved the ``process_opcode()`` function to treat the program with the new important features:
  - instructions can have a variable number of parameters, which is why I have modified the ``OPERATIONS`` dictionary to automatically extract it
  - instructions have an execution mode (either in "address" or "immediate value" mode)
  
  Here, I have basically automated the impact of the number of inputs on the instruction pointer, I've coded up the new operations and I've dealt with the mode.
  
The ``Debugger`` class is a utility I had fun making that just allows me to have my Intcode program output its results to a specific stream rather than the usual ``sys.stdout`` used by Python when you do a ``print()``. It is a context manager class that simply puts a piece of code into a special "state" where it has a access to a global stream variable to write to.

In my ``process_opcode()`` function, for the output instruction (with code ``4``), I make use of this stream if possible.

Then, at the very end of the execution of my program, I can simply query the ``last_output()`` of the stream stored in my current ``Debugger`` instance to get my result. This significantly simplifies the test functions and the assertions. (Otherwise, I would have had to read back the printed output, somehow, and split it back to get the last line...).

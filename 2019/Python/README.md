# [2019] Python

This subfolder contains my code solutions for challenges from the 2019 series, written in Python (3.6.5).

## Day 1: Fuel Computation

This first challenge is pretty straight-forward. Rather than focusing on the problem itself, I will instead explain the general structure of the solution that will be copied over and over for the next solutions, too.

In these files, I try to always organize the code in the same way:

1. first, some imports if need be (either Python built-in libs or external packages, **even if I will try and stay as "built-in" as possible in my answers**)

2. then, parsing functions to read and extract data from the provided input (that seems to always be a string of characters)

3. then, the actual computation functions, separated in 3 bits:
  - util and common functions
  - functions for the Part I of the problem
  - functions for the Part II of the problem
  
4. a test of function with a set of ``assert``s to check that my computation function seem to give an ok result (using the examples provided with the problem)

5. finally, the main part that solves the problem by running the computation functions on the actual inputs I was given (that depend on the user)

## Day 2: Intcode programming

This problem is an opportunity to talk about mutability in Python: in this solution, I extensively use the fact that ``list``s are mutable in Python. This means that even if they are passed as parameters to functions, the variables still point to the same address in memory and can therefore be modified directly.

On the other hand, immutable classes like the basic types (``bool``, ``int``, ``float``, ``str``) and some particular containers (``set``, ``tuple``, ``frozenset``) cannot be modified after being created. If you want to change the value, you need to reassign the variable to a brand new value in memory.

For example, in the ``process_inputs()`` function, I directly touch the ``inputs`` list that is passed as a parameter as I execute the Intcode program.

Hence the need to "restore" the inputs before running the code for Part II!

> For more info on immutability in Python, you can check out [Python's reference](https://docs.python.org/3/reference/datamodel.html?highlight=immutability) on the data model (Dec. 2019).

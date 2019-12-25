# [2015] Python

This subfolder contains my code solutions for challenges from the 2015 series, written in Python (3.6.5).

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

## Day 1: Not Quite Lisp

#### Answers
**Part I: 74 • Part II: 1795**

Day 1 is pretty straight-forward. The only small ruse I've used is in data preparation: rather than keeping the ``(`` and ``)`` characters, I've replaced each with the corresponding movement (either +1 or -1 floor) so I would just have to basic sums further on.

## Day 2: I Was Told There Would Be No Math

#### Answers
**Part I: 1606483 • Part II: 3842356**

This challenge is not hard. In Python, we can easily write one-line versions of our list to reduce the number of lines of code...

[One-liners](https://wiki.python.org/moin/Powerful%20Python%20One-Liners) are a very powerful feature of Python that allows us to write complex programs in only one line. For example, for lists, it's a way of writing super condensed loops.

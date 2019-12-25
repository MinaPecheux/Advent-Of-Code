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

## Day 3: Perfectly Spherical Houses in a Vacuum

#### Answers
**Part I: 2081 • Part II: 2341**

For this puzzle, we can do a bit of data pre-processing as in Day 1, by replacing the ``<``, ``^``, ``>`` and ``v`` characters by the corresponding horizontal and vertical deltas. After this transformation, we can easily apply the move to our current coordinates.

In Part II, we can use a modulo on the current instruction index to know whether it should impact Santa's or the Robo-Santa's position.

## Day 4: The Ideal Stocking Stuffer

#### Answers
**Part I: 117946 • Part II: 3938038**

This time, I've relied on a built-in Python lib called ``hashlib`` to handle the MD5 hashing more easily. This module gives us access to several secure hash algorithms: MD5, SHA224, SHA256... With ``hashlib``, it is very easy to compute the digest or the hexadecimal digest of a given input using those functions.

Here, I've taken a really naïve approach: I simply check all the positive integers starting from 1 until I've found one that, when concatenating to the secret and passed through the MD5 hash object, gives a result hexadecimal digest that starts with the required number of zeroes.

*Note: this is probably not optimized, and Part I and II both take a few seconds to run, but it is not that terrible for now, and I don't see how to improve it...*

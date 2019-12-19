# [2019] C++

This subfolder contains my code solutions for challenges from the 2019 series, written in C++.

## Preliminary note: files organization
The C++ directory contains 2 (or 3, after compilation) subdirectories:

- ``src/``: contains the sources, the actual programs to compile; there are both the ``day{n}.c`` files for each puzzle and the util files
- ``include/``: contains the headers for the util files
- ``bin/`` (after compilation): contains the binary and executable files that are actually run

In the source files of each puzzle, I try to always organize the code in the same way:

1. first, some imports if need be (either C standard libs or personal util headers and associated sources - the headers are located in the ``include/`` subdirectory)

2. then, the actual computation functions, separated in 3 bits:
  - util and common functions
  - functions for the Part I of the problem
  - functions for the Part II of the problem
  
3. a test function with a set of ``assert``s to check that my computation functions seem to give an ok result (using the examples provided with the problem)

4. finally, the main part that imports and parses the data (that depends on the user), then  solves the problem by running the computation functions on the actual inputs I was given

## Day 1: The Tyranny of the Rocket Equation

#### Answers
**Part I: 3345909 • Part II: 5015983**

This first challenge is pretty straight-forward. The only notable thing is that Part II strongly indicates you should [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) to solve the problem. Given that you have a question of the form "compute a value for something, then compute the value for this new thing, and so on..." you want to create recursive function, i.e. a process where your top solution depends on the solution you computed for smaller instances of the problem.

You therefore call the function from within itself (here ``computeTotalFuel()`` is called inside of ``computeTotalFuel()``).

# [2016] Python

This subfolder contains my code solutions for challenges from the 2016 series, written in Python (3.6.5).

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

## Day 1: No Time for a Taxicab

#### Answers
**Part I: 230 • Part II: 154**

For Day 1, we need to compute a Taxicab distance on a grid. The first thing is to process the given moves to see where the instructions lead us to (more precisely, what coordinates we end up at the end of the moves).

If we call `xf` and `yf` those final coordinates, then the Taxicab distance from the origin point (`x = 0`, `y = 0`) to the final point (`x = xf`, `y = yf`) is simply: `abs(xf) + abs(yf)`.

Computing the actual path is quite straight-forward: we simply need to check what direction we are currently going in, update it according to the first letter in the instruction block and then move forward the provided number of steps.

For Part II, we also need to store the intermediate cells we walked through so that we can check what cell we already crossed, and optionnally stop as soon as we've gone in circle.

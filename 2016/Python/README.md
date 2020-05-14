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

## Day 2: Bathroom Security

#### Answers
**Part I: 53255 • Part II: 7423A**

In Day 2, we simulate a security panel with digits and letters and perform a series of moves on it.

In Part I, we have a standard panel with digits ranging from 1 to 9 (from top to bottom, from left to right). Let `x` and `y` be the current position on the panel. We start from the digit "5", so in the middle of the panel, meaning that the initial position is `x = 1` and `y = 1`. We can then update `x` and `y` with each move (e.g. `U` will reduce `y` by 1, unless `y` is already 0). At the end of each line of moves, we store the new code digit; it can be computed easily from `x` and `y` as: `1 + x + y * 3` (since we start from 1 and there are 3 digits per line on the panel).

In Part II, we have a special panel with digits from 1 to 9 and 4 letters (A, B, C, D). We use the same technique as before, except that:

- empty cells in the panel (stored as `None` in my script) prevent us from performing the move
- the new code digit is simply the value of the panel at the given `(x, y)` position

## Day 3: Squares With Three Sides

#### Answers
**Part I: 993 • Part II: 1849**

Day 3 is fairly easy with regard to the computation per se: once we've built our list of triangles candidates, we just need to iterate through and check if the various edge lengths verify the given constraint (i.e. "the sum of any two sides is larger than the remaining side").

Part I and II differ in how we actually read the input data to get our list of triangles.

In Part I, we suppose that each row defines a triangle (the 3 numbers on the rows being the edge lengths). In other words, the following data:

```
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
```

defines 6 triangles with edge lengths of (101, 301, 501), (102, 302, 502) and so on. In this case, creating the list of triangles simply means reading each line and splitting it into the 3 digits to get its edges. For this, I've used a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) (or Regex): the idea is to define a "pattern" to search for in a string, and then to see if the given string can be matched to this pattern. If so, we are even able to isolate the bit that match the different parts of our pattern and thus directly extract our values. Here, this helps us cut down our line of text into three numbers.

In Part II, we suppose that triangles are defined by the 3 numbers in the same column across 3 consecutive rows. In other words, for the same piece of data:

```
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
```

we instead get 6 triangles with edge lengths of (101, 102, 103), (201, 202, 203) and so on. I've decided to create three accumulators to iteratively add edge lengths to each triangle in a pack of 3 rows, and regularly "flush" it while adding to the full list of triangles. The small Python trick we can note is the use of the `enumerate` built-in to iterate on both the index and the value in the list at the same time (this method packs the index with the value in a tuple at each loop step).

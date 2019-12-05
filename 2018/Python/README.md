# [2018] Python

This subfolder contains my code solutions for challenges from the 2018 series, written in Python (3.6.5).

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

## Day 1: Frequency changes

Even though the challenge is quite basic, I have used two small Python tricks in my solution:
- some simple syntax stuff: in the ``compute_first_cycle()`` function, there is this line:

  ```
  i = i + 1 if i < len(changes) - 1 else 0
  ```

  This is an `inline` expression that assigns a new value to the variable ``i`` depending on the result of the test ``i < len(changes) - 1``: if it is true, then the value before it is taken (``i+1``), otherwise the one after is taken instead (``0``). This allows me to loop back at the beginning of the list of frequency changes if I haven't found the result yet.

- I use a ``set`` to store my previously encountered frequences; without diving too much into the time complexity of operations foreach available Python data type, I just want to point out that ``set``s are super efficient when you want to check if the container already includes a given item. On the other hand, a ``list`` takes way longer.

  *Note: if you want to check I'm telling the truth, just replace these two lines and execute the program... the solution will take ages to be computed!*
  
  ```
  def compute_first_cycle(changes):
      prev_freqs = [ 0 ] # replace by a basic list
      ...
      while True:
          ...
          while i < len(changes):
              ...
              else:
                # use the 'append' method for a list
                prev_freqs.append(freq)
              ...
      return None
  ```

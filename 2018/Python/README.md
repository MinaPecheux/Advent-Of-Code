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

## Day 1: Chronal Calibration

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

## Day 2: Inventory Management System

In this problem, we need to compare strings. There isn't much to it in my solution, but I'll still point out two tools I've used to solve it (quite) efficiently:

- for Part I, where we need to check if the IDs contain repetitions of letters, I'm using the ``Counter`` data type that is available in the Python built-in ``itertools`` lib. This package contains various useful additional containers that are optimized for a given task; for example, the ``Counter`` creates a dict-like structure that associates each unique element in a list with its number of occurrences.

- for Part II, when I need to check the matching letters in two IDs, I want to iterate through both "in parallel", meaning that I want to compare the first character of the first with the first character of the second, then the second character of the first with the second character of the second and so on. To do this, I used the ``zip()`` built-in method in Python that creates tuples from two lists by going through each and grouping together the elements at the current index.

## Day 3: No Matter How You Slice It

In this problem, the inputs parsing was a bit more evolved for the previous ones. Instead of just splitting lines or checking for a sign, I had to extract 5 values from each line: the id of the claim, its starting ``(x,y)`` coordinate and its ``width x height`` size in square inches. To deal with this, I used a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) (or Regex): the idea is to define a "pattern" to search for in a string, and then to see if the given string can be matched to this pattern. If so, we are even able to isolate the bit that match the different parts of our pattern and thus directly extract our values.

Day 3 is also an interesting problem because it required me to choose the Python data type I would use carefully. Indeed depending on the data structure you pick, the performance of your program will be very different.

I've already mentioned the ``Counter`` util for the previous problem but here I've also played around with ``dict``s, ``list``s and ``set``s to try and take advantage of each:

- lists are very good for append and extend operations; in other words, they are efficient when you need to add new items or add two lists together to form a bigger one

- dictionaries are hashable containers that work with key-value pairs; they are great for quick element access (it is in `O(1)`, i.e. in constant time); this allows me to easily check which square in the fabric band appear in more than one claim

- sets are quite close to dictionaries but they are super fast at union, intersection and difference operations; this is a big plus for my final operation that isolates the remaining claim from the rest of the IDs

*Note: at the end of my ``find_non_overlapping_claim()`` function, I use the ``pop()`` method on my set. In most cases, you ought to be careful with this operation because it returns a __random__ element from the set. However, here, I've been told in the problem that I should only expect a single value at this point.*

## Day 4: Repose Record

My solution to this problem mostly uses the same tools as the one before (regular expressions, ``dict``s and ``set``s...). It's interesting to note, though, that here data preparation really made the rest easier. This is something that is usually true in computer science - and is particularly true in data science and AI: the way your data is shaped and organized has a big impact on how efficient your algorithm can be. For this problem, I have a ``prepare_inputs()`` function that is dedicated to sorting the inputs in the right order, getting rid of the additional data I don't need anymore and extracting what I will exploit further down.

During my treatment of the inputs, I also used the super useful ``sorted()`` function that is available for ``list``s in Python and allows you to sort your elements using a specific key and optionally reversing the order (from ascending to descending).

Here, for example, in ``strategy1()``, when I sort my list of guards, I want to sort them by total time they spent asleep. I've stored this value as the third element of each tuple, so I can access it in my key lambda function to sort the list according to this criterion:

```
sortable_guards = sorted(sortable_guards, key=lambda x: x[2], reverse=True)
```

I also use the keyword ``reverse=True`` to have the guard with the *largest* value first, rather than at the end.

## Day 5: Alchemical Reduction

**Not yet optimized: ~10sec of execution for Part II!**

In this puzzle, we are working with strings of characters and in particular lower- or uppercase letters. In particular, we are interested in pairs of letters that contain the lowercase and the uppercase version of a letter, either way, but not both with the same case. In other words, we want to spot pairs such as "aA", "Aa", "cC"... but not "aa" or "CC".

To do this, a simple idea can be to use the [ASCII codes](https://en.wikipedia.org/wiki/ASCII) of those letters. In the ASCII table, the letters of our alphabets are organized in two ranges, first all the uppercase characters, then a bit further down the list all the lowercase characters. However, the difference between a lowercase and an uppercase version of the same letter will always be the same. There is therefore a basic test to check if we are dealing with the type of pairs we are searching for:

```
return abs(ord(chr1) - ord(chr2)) == LOW_UP_DIFF
# where LOW_UP_DIFF = ord('a') - ord('A')
```

This is what is implemented in the ``try_reaction()`` function. The ``ord`` built-in Python method transforms a character into the corresponding ASCII code. First, we get the (constant) difference between lower- and uppercase versions by using the "a" letter. Then, we just need to check if the difference between the ASCII codes of our characters is such that they are the same letter in lower- and uppercase version. If so, then the test is positive and, in the current context of the problem, a reaction occurs.

We now have an easily applicable test for any pair of characters.

Still, the other big question is: how can we efficiently generate all the possible pairs, so that we can then apply the test and filter out the pairs we are truly interested in? The answer is to use the built-in Python ``itertools`` package. This lib contains lots of utilities to create cartesian products, permutations, combinations... Here, we use the ``product`` function and the ``chr()`` built-in method to get a character from an ASCII code (this is the reverse of ``ord()``). By combining those together, we can generate a list of all possible lower- and uppercase letter pairs, and then we just filter out the ones where the letters aren't the same.

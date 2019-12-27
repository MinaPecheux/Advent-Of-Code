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

In both parts, I use sets. This built-in Python container type is useful here because it is a collection of *unique* items, thus whenever I add a coordinate that was already there it won't change anything, and I will end up with a list of all the unique houses that Santa visited. Then, taking the size of this container directly gives me the number of houses that were visited at least once.

In Part II, we can use a modulo on the current instruction index to know whether it should impact Santa's or the Robo-Santa's position.

## Day 4: The Ideal Stocking Stuffer

#### Answers
**Part I: 117946 • Part II: 3938038**

This time, I've relied on a built-in Python lib called ``hashlib`` to handle the MD5 hashing more easily. This module gives us access to several secure hash algorithms: MD5, SHA224, SHA256... With ``hashlib``, it is very easy to compute the digest or the hexadecimal digest of a given input using those functions.

Here, I've taken a really naïve approach: I simply check all the positive integers starting from 1 until I've found one that, when concatenating to the secret and passed through the MD5 hash object, gives a result hexadecimal digest that starts with the required number of zeroes.

*Note: this is probably not optimized, and Part I and II both take a few seconds to run, but it is not that terrible for now, and I don't see how to improve it...*

## Day 5: Doesn't He Have Intern-Elves For This?

#### Answers
**Part I: 255 • Part II: 55**

In my solution, I'm passing the check function to use to my computation function so I can easily switch between the criteria from Part I and the ones from Part II.

For the new criteria in Part II, I've also used a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) (or Regex): the idea is to define a "pattern" to search for in a string, and then to see if the given string can be matched to this pattern. If so, we are even able to isolate the bit that match the different parts of our pattern and thus directly extract our values. Here, this helps us check if we have at least one letter surrounded by the same letter on both sides.

## Day 6: Probably a Fire Hazard

#### Answers
**Part I: 569999 • Part II: 17836115**

Day 6 is mostly about parsing the data and storing in a (relatively) efficient way, since the algorithm itself is really basic.

For the data preprocessing part, I've used regular expressions once again to extract the action and the area to apply it to from each instruction line. In the end, I get a list of *tuples* that contain 5 integers: the action type (0 for "turn off", 1 for "turn on", 2 for "toggle"), the left ``x`` of the impact zone, the top ``y`` of the zone, the right ``x`` of the zone and the bottom ``y`` of the zone. All four coordinates are inclusive.

In my ``process_no_brightness()`` and ``process_with_brightness()`` methods, I'm using either sets or dicts to model my grid of 1 million lights efficiently. In particular:

- in Part I (``process_no_brightness()``), rather than storing all the lights with their initial value of 0, I'm just creating a set of the ones that are turned on at the end; sets are really great at adding, removing and checking the presence of elements quickly

- in Part II (``process_with_brightness()``), I use a ``defaultdict`` which is a container type from the built-in ``collections`` module; the advantage of a  ``defaultdict`` is that it is initialized with a default value depending on the given type (for integers, it is 0) and I can therefore simply increment or decrement the value to apply my action

Because computation is not instantaneous, I've also added a little debug mode with the great [tqdm](https://pypi.org/project/tqdm/) Python library. This package makes it easy to wrap an iterator (such as a ``range`` or a simple list) with the ``tqdm()`` method so that your shell displays the iterations with a progress bar and the total execution time.

## Day 7: Some Assembly Required

#### Answers
**Part I: 16076 • Part II: 2797**

To model the pieces in the circuit more easily, I've used a key feature of Python that falls under the object-oriented programming paradigm: classes. It is a nice way of aggregating together bits of code that have a logical link.

To create a basic class, you should inherit from the ``object`` built-in and then define a ``class`` that has at least an ``__init__()`` method:

```python
class CircuitPiece(object):
    
    def __init__(self):
        pass
```

This ``__init__()`` function will be called whenever you instantiate a new variable of type ``CircuitPiece``. The neat thing with object-oriented programming, as I said just before, is that you can gather in the same place various variables or methods that are logically linked together; here, our class can contain other methods that implement the behavior we want one of program instance to have: a basic state check, memory updates, instructions execution...

Other than that, a tiny detail in my solution is that I store the pieces in my circuit in a dictionary where the key is the label of each piece; this way, I can find a piece very quickly by its label.

*Note: I've also overridden another Python ["magic" method](https://www.python-course.eu/python3_magic_methods.php) for my ``CircuitPiece`` class, the ``__str__()`` function. Thanks to this, I can change the string representation of my instances and make my debugs a bit clearer if necessary.*

## Day 8: Matchsticks

#### Answers
**Part I: 1371 • Part II: 2117**

In this puzzle, we need to manipulate strings in various ways. In particular, I can't read the file as I did in my previous solutions because I need to keep the inputs in their "raw" format. This time, if I use the classic Python's ``open()`` method, the strings will be transformed automatically and I won't be able to keep my original ASCII characters intact - so I won't be able to compute the initial "encoded" string length. Instead, I rely on the ``codecs`` built-in Python lib that gives me the raw content of the file.

For Part I, we can use Python's built-in ``eval()`` function to transform the initial string into a "decoded" version where we have replaced the escaped backslashes, the escaped quotes and the ASCII hex characters by the corresponding real characters.

*Note: this method is quite powerful but it can be __risky__ because it runs the given text as a Python program directly and can thus be used to ["inject" malignant code](https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html)!*

For Part II, we can directly use Python's ``re`` module (that's used for regex) - it has a ``re.escape()`` method that automatically gives us the escaped version of a string. We just need to add the double quotes at both ends to get the "encoded" version of our string that is required for Part II.

### Day 9: All in a Single Night

#### Answers
**Part I: 207 • Part II: 804**

From an algorithmic point of view, this problem is focused on graphs. The cities we are given are linked to each other in such a way that we can draw a graph of their connections.

[Graph theory](https://en.wikipedia.org/wiki/Graph_theory) is a fascinating field. Re-implementing graphs from scratch is interesting but I could never have reached optimal performance, so I decided to instead use the Python package [NetworkX](https://networkx.github.io/documentation/stable/index.html). This lib contains efficient structures to represent and manipulate graphs: you can create nodes, edges (either directed or undirected), search for adjacent/successors/predecessors nodes, apply path computation algorithms...

Here, we want to create an undirected graph where:

- cities are node
- routes between cities are (undirected) edges
- edges are weighted with the distance between the two cities

Then, the lib's ``all_simple_paths()`` method helps us to find all possible paths between two points in the graph so that we can easily compute the shortest (Part I) and longest (Part II) distances in the graph.

I won't do a full detailed presentation of the lib itself but rather I'll take this opportunity to point out once again that, to me, a huge strength of Python is the ecosystem that has gradually been built for it by the community. Today, the Python language is not just a well-designed script language but also an abundant collection of packages that have been developed by the Python team or the community and help us solve lots of problems. In Python, the phrase "don't reinvent wheel" is usually very true: before trying to rebuild a complex system from the ground up, you should first check if there isn't already a lib that takes care of that. A good Python program is more often than not a well-organized suite of cleverly chosen efficient bricks.

*Note: this is particularly important in data science where you often deal with large amount of data. A common tech stack for data scientists includes the Numpy and Scipy libs - this is because these libraries have been super-optimized and partly rely on compiled and hardware-tuned code to speed up computation remarkably.*

*Note 2: here, we use the same info in both parts of the problem since Part I asks for the shortest distance and Part II for the longest one; by pre-computing and storing all the distances, we can get the result for Part II almost instantly, as opposed to a naïve re-compute of all distances a second time that requires a few seconds.*

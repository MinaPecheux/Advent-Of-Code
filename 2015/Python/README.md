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

### Day 10: Elves Look, Elves Say

#### Answers
**Part I: 252594 • Part II: 3579328**

Day 10 is pretty straight-forward in Python because the language provides us with the nice ``groupby()`` method in its built-in ``itertools`` module. Thanks to this function, we can easily compute the occurrence of each character in our current input (while keeping the order of these occurrences) and then reconstruct the new input for the next round.

My solution gives the right result however it could probably be optimized. For now, it is almost instantaneous for Part I but Part II takes several seconds (although I'm not restarting from scratch for Part II but re-using what I computed in Part I to skip some computation...).

In theory, we could parallelize the calculations because the input can be cut down in chunks that can be processed independently.

### Day 11: Corporate Policy

#### Answers
**Part I: hepxxyzz • Part II: heqaabcc**

For Day 11, we basically need two functions:

- one test function that checks whether a password is valid or not (by checking if the password meets the various given criteria): ``pwd_is_ok()``

- a function to generate the passwords and test them; it is a brute-force iteration of a generator that tries all the possibilities after the current one until we find a password that is valid: ``get_new_password()``

To avoid inefficient use of memory, we can use Python's generator rather true lists: the idea is to *not* generate all the possible passwords beforehand but rather generate them on the fly.

The generator works like an [odometer](https://en.wikipedia.org/wiki/Odometer): you have a row of "gears", you increase the rightmost one by one every time and whenever the "gear" rolls over, the one on its left increases by 1. There is a propagation of this pattern to the left so that we get a progression like:

```
abxyz
abxya
abxyb
...
abxyz
abxzz
abxaa
abxab
...
```

*Note: since tests are a bit long, I've put a little debug to warn the user when the tests are done. They can be commented out to gain some exec time and only compute the actual problem's solutions.*

### Day 12: JSAbacusFramework.io

#### Answers
**Part I: 191164 • Part II: 87842**

In this puzzle, we are provided with an object as a JSON-formatted string and we want to sum all the numbers that appear in the data.

The solution is both handy and short in Python since this language has a built-in ``json`` module that can easily transform a JSON string into the corresponding object and vice-versa. Then, we also have a very simple regex that we can apply to the stringified content to get all the numbers in the data and therefore compute the sum quickly.

All in all, the idea is as follows:

- for Part I and II: the method ``get_numbers_sum()`` uses a regex to find all the numbers in a JSON-formatted string, convert them to actual ints and get the sum

- for Part II: the function ``ignore_reds()`` recursively computes the new JSON data where all objects containing the string "red" as a value somewhere have been removed, and the method ``get_sum_no_reds()`` does a little string-to-object and object-to-string exchange (with the ``json`` package) to get the total sum of the numbers in the data after the ``ignore_reds()`` process

### Day 13: Knights of the Dinner Table

#### Answers
**Part I: 733 • Part II: 725**

This problem is about finding the optimal placement for a bunch of people in order to maximize the total amount of "happiness" of everyone, given their likes and dislikes of the other persons.

Thus we want to examine permutations of our group (which can be quickly be calculated using Python's built-in module ``itertools``). For each, we simply need to check the neighbors of each person in this configuration, compute the happiness of this person and add it to the total. This way, we can easily sort the configurations and find the optimal one.

Both parts use the exact same algorithm, only the input data changes.

*Note: the algorithm could perhaps be optimized but the execution time is still pretty good at the time, with an instantaneous Part I and only ~4 secs for Part II.*

### Day 14: Reindeer Olympics

#### Answers
**Part I: 2640 • Part II: 1102**

Day 14 is about a reindeers race! We have a group of reindeers that each have a name, a speed, a fly time and a rest time. The idea is as follows:

- a reindeer starts the race by flying for ``fly_time`` seconds - each second, it travels ``speed`` kilometers

- when ``fly_time`` seconds have passed, the reindeer is exhausted and must rest for ``rest_time`` seconds

- after resting for ``rest_time`` seconds, the reindeer can fly again for ``fly_time`` seconds

- and so on, until the race ends

The race lasts a given number of seconds.

To represent the reindeers easily and have them travel each second while checking for the fly/rest state, I have coded up a little ``Reindeer`` class. It has all the required data and methods to have each reindeer play its turn in the race properly at each second.

After parsing the input to instantiate our ``Reindeers`` items, we can update them with the 3 following functions:

1. ``reset()``: restores the initial state of the reindeer (effectively takes it back to the starting line)

2. ``travel_one()``: makes the reindeer travel forward during a second

3. ``travel()``: makes the reindeer travel forward for a given number of seconds

The meat of the code is in the ``travel_one()`` method. First, we check if the reindeer should change its state or not, i.e. if it was flying and has travelled during ``fly_time`` seconds or if it was resting and has rested during ``rest_time`` seconds. If either is true then the reindeer switches to the reverse state and sets the state timer to the new state length (``fly_time`` or ``rest_time``). Once this check is done, we see if the reindeer is flying: if it is, the animal travels ``speed`` kilometers forward by adding this value to its ``distance`` property (that will hold the total travelled distance at the end of the race). Finally, we update the state timer.

In Part II where we have bonus points too, we have a ``score`` property that can be incremented for the reindeer(s) in the lead at the end of the turn.

At the end of the race, depending on the way Santa counts the points, we evaluate who the winning reindeer is:

- if we only look at the total travelled distance and get the reindeer that has travelled the furthest (Part I), then we simply need to take the Reindeer instance that has the highest value for its ``distance`` property

- if we also have "bonus points" for the reindeer(s) are in the lead each second, then we use the ``score`` property instead

### Day 15: Science for Hungry People

#### Answers
**Part I: 18965440 • Part II: 15862900**

For Day 15, we can use the ``numpy`` lib to drastically reduce the execution time. This very common data science module is super-optimized and partly relies on compiled and hardware-tuned code that speed up computation remarkably.

I haven't found a way to have a generic solution: here, I make use of the fact that there are 4 ingredients in my input to prepare my loops and use ``numpy`` arrays whenever possible.

Part I and Part II are very similar: the second part only adds a new constraint to the valid recipes - they must have exactly 500 calories. To apply this criterion, we just need to add a little ``if`` statement with a ``numpy`` conditional selection.

*Note: once again, I've put some progress bar with the ``tqdm`` package so that the user keeps track of the computation process.*

### Day 16: Aunt Sue

#### Answers
**Part I: 103 • Part II: 405**

Day 16 is quite an easy-peasy problem that makes for a nice pause in the month! Once again, by using the right data type, we can significantly increase the efficiency of our program.

Here, I use dictionaries to quickly look up the matching parameters, and I isolate the ids of the aunts that match the given criteria.

In Part I, we only check equalities. In Part II, we also have some inequalities, depending on the checked key. Overall, we can create a list of potential matches that contains either 1 or 2 items.

I admit that, for Part II, I don't know if there is an actual way of choosing between the two candidates. My guess was that it couldn't be the same as the answer for Part I, but I don't know if it is a sound strategy... ;)

### Day 17: No Such Thing as Too Much

#### Answers
**Part I: 1304 • Part II: 18**

Solving this puzzle isn't too hard thanks to Python built-in ``itertools`` lib. By using its ``combinations()`` method, we can easily get all the possible containers' permutations.

We can compute those once, put them in a set, and then just extract the relevant info for Part I and Part II.

In Part I, we just need to get the number of unique combinations, so it's the length of our set. In Part II, we need to get the minimal number of containers to use first and then get all the combinations that fit this number.

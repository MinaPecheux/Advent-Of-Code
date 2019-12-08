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

#### Answers
**Part I: 576 • Part II: 77674**

Even though the challenge is quite basic, I have used two small Python tricks in my solution:
- some simple syntax stuff: in the ``compute_first_cycle()`` function, there is this line:

  ```python
  i = i + 1 if i < len(changes) - 1 else 0
  ```

  This is an `inline` expression that assigns a new value to the variable ``i`` depending on the result of the test ``i < len(changes) - 1``: if it is true, then the value before it is taken (``i+1``), otherwise the one after is taken instead (``0``). This allows me to loop back at the beginning of the list of frequency changes if I haven't found the result yet.

- I use a ``set`` to store my previously encountered frequences; without diving too much into the time complexity of operations foreach available Python data type, I just want to point out that ``set``s are super efficient when you want to check if the container already includes a given item. On the other hand, a ``list`` takes way longer.

  *Note: if you want to check I'm telling the truth, just replace these two lines and execute the program... the solution will take ages to be computed!*
  
  ```python
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

#### Answers
**Part I: 4693 • Part II: pebjqsalrdnckzfihvtxysomg**

In this problem, we need to compare strings. There isn't much to it in my solution, but I'll still point out two tools I've used to solve it (quite) efficiently:

- for Part I, where we need to check if the IDs contain repetitions of letters, I'm using the ``Counter`` data type that is available in the Python built-in ``itertools`` lib. This package contains various useful additional containers that are optimized for a given task; for example, the ``Counter`` creates a dict-like structure that associates each unique element in a list with its number of occurrences.

- for Part II, when I need to check the matching letters in two IDs, I want to iterate through both "in parallel", meaning that I want to compare the first character of the first with the first character of the second, then the second character of the first with the second character of the second and so on. To do this, I used the ``zip()`` built-in method in Python that creates tuples from two lists by going through each and grouping together the elements at the current index.

## Day 3: No Matter How You Slice It

#### Answers
**Part I: 107663 • Part II: 1166**

In this problem, the inputs parsing was a bit more evolved for the previous ones. Instead of just splitting lines or checking for a sign, I had to extract 5 values from each line: the id of the claim, its starting ``(x,y)`` coordinate and its ``width x height`` size in square inches. To deal with this, I used a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) (or Regex): the idea is to define a "pattern" to search for in a string, and then to see if the given string can be matched to this pattern. If so, we are even able to isolate the bit that match the different parts of our pattern and thus directly extract our values.

Day 3 is also an interesting problem because it required me to choose the Python data type I would use carefully. Indeed depending on the data structure you pick, the performance of your program will be very different.

I've already mentioned the ``Counter`` util for the previous problem but here I've also played around with ``dict``s, ``list``s and ``set``s to try and take advantage of each:

- lists are very good for append and extend operations; in other words, they are efficient when you need to add new items or add two lists together to form a bigger one

- dictionaries are hashable containers that work with key-value pairs; they are great for quick element access (it is in `O(1)`, i.e. in constant time); this allows me to easily check which square in the fabric band appear in more than one claim

- sets are quite close to dictionaries but they are super fast at union, intersection and difference operations; this is a big plus for my final operation that isolates the remaining claim from the rest of the IDs

*Note: at the end of my ``find_non_overlapping_claim()`` function, I use the ``pop()`` method on my set. In most cases, you ought to be careful with this operation because it returns a __random__ element from the set. However, here, I've been told in the problem that I should only expect a single value at this point.*

## Day 4: Repose Record

#### Answers
**Part I: 21083 • Part II: 53024**

My solution to this problem mostly uses the same tools as the one before (regular expressions, ``dict``s and ``set``s...). It's interesting to note, though, that here data preparation really made the rest easier. This is something that is usually true in computer science - and is particularly true in data science and AI: the way your data is shaped and organized has a big impact on how efficient your algorithm can be. For this problem, I have a ``prepare_inputs()`` function that is dedicated to sorting the inputs in the right order, getting rid of the additional data I don't need anymore and extracting what I will exploit further down.

During my treatment of the inputs, I also used the super useful ``sorted()`` function that is available for ``list``s in Python and allows you to sort your elements using a specific key and optionally reversing the order (from ascending to descending).

Here, for example, in ``strategy1()``, when I sort my list of guards, I want to sort them by total time they spent asleep. I've stored this value as the third element of each tuple, so I can access it in my key lambda function to sort the list according to this criterion:

```python
sortable_guards = sorted(sortable_guards, key=lambda x: x[2], reverse=True)
```

I also use the keyword ``reverse=True`` to have the guard with the *largest* value first, rather than at the end.

## Day 5: Alchemical Reduction

#### Answers
**Part I: 10250 • Part II: 6188**

In this puzzle, we are working with strings of characters and in particular lower- or uppercase letters. In particular, we are interested in pairs of letters that contain the lowercase and the uppercase version of a letter, either way, but not both with the same case. In other words, we want to spot pairs such as "aA", "Aa", "cC"... but not "aa" or "CC".

To do this, a simple idea can be to use the [ASCII codes](https://en.wikipedia.org/wiki/ASCII) of those letters. In the ASCII table, the letters of our alphabets are organized in two ranges, first all the uppercase characters, then a bit further down the list all the lowercase characters. However, the difference between a lowercase and an uppercase version of the same letter will always be the same. There is therefore a basic test to check if we are dealing with the type of pairs we are searching for:

```python
return abs(ord(chr1) - ord(chr2)) == LOW_UP_DIFF
# where LOW_UP_DIFF = ord('a') - ord('A')
```

This is what is implemented in the ``try_reaction()`` function. The ``ord`` built-in Python method transforms a character into the corresponding ASCII code. First, we get the (constant) difference between lower- and uppercase versions by using the "a" letter. Then, we just need to check if the difference between the ASCII codes of our characters is such that they are the same letter in lower- and uppercase version. If so, then the test is positive and, in the current context of the problem, a reaction occurs.

We now have an easily applicable test for any pair of characters.

Still, the other big question is: how can we efficiently generate all the possible pairs, so that we can then apply the test and filter out the pairs we are truly interested in? The answer is to use the built-in Python ``itertools`` package. This lib contains lots of utilities to create cartesian products, permutations, combinations... Here, we use the ``product`` function and the ``chr()`` built-in method to get a character from an ASCII code (this is the reverse of ``ord()``). By combining those together, we can generate a list of all possible lower- and uppercase letter pairs, and then we just filter out the ones where the letters aren't the same.

I had a problem optimizing the execution time for Part II. After searching for a while, I admit I went to [Advent of Code's dedicated Reddit thread](https://www.reddit.com/r/adventofcode) and browsed through the others' suggestions. Many people seem to be stuck like I was; I could not find a less brutal way of treating the problem than simply looping through the alphabet, removing the corresponding letter from the input polymer and running the algorithm from Part I. The trick was to actually use the reduced polymer already computed in Part I! This dropped my execution time from ~10 sec to about half a second. Thanks to [asger_blahimmel](https://www.reddit.com/user/asger_blahimmel/) for the tip! :)

## Day 6: Chronal Coordinates

#### Answers
**Part I: 4342 • Part II: 42966**

Nothing special to say, except that this problem talks about the Manhattan distance (or [Taxicab geometry](https://en.wikipedia.org/wiki/Taxicab_geometry)), a common math measurement whenever you have points on a grid.

## Day 7: The Sum of Its Parts

#### Answers
**Part I: LAPFCRGHVZOTKWENBXIMSUDJQY • Part II: 936**

*Note: the code finds the right answer and is efficient, still I have a feeling that it is not as "nice" as it could be. My guess is that we could some nice data structures (such as heaps? queues?) to make it better. If you have any ideas of improvements, feel free to send them to me, or comment somewhere! :)*

From an algorithmic point of view, this problem is focused on graphs. The steps we are given depend on each other in such a way that we can draw a graph of their connections.

[Graph theory](https://en.wikipedia.org/wiki/Graph_theory) is a fascinating field. Re-implementing graphs from scratch is interesting but I could never have reached optimal performance, so I decided to instead use the Python package [NetworkX](https://networkx.github.io/documentation/stable/index.html). This lib contains efficient structures to represent and manipulate graphs: you can create nodes, edges (either directed or undirected), search for adjacent/successors/predecessors nodes, apply path computation algorithms...

I won't do a full detailed presentation of the lib itself but rather I'll take this opportunity to point out once again that, to me, a huge strength of Python is the ecosystem that has gradually been built for it by the community. Today, the Python language is not just a well-designed script language but also an abundant collection of packages that have been developed by the Python team or the community and help us solve lots of problems. In Python, the phrase "don't reinvent wheel" is usually very true: before trying to rebuild a complex system from the ground up, you should first check if there isn't already a lib that takes care of that. A good Python program is more often than not a well-organized suite of cleverly chosen efficient bricks.

*Note: this is particularly important in data science where you often deal with large amount of data. A common tech stack for data scientists includes the Numpy and Scipy libs - this is because these libraries have been super-optimized and partly rely on compiled and hardware-tuned code to speed up computation remarkably.*

## Day 8: Memory Maneuver

#### Answers
**Part I: 37262 • Part II: 20839**

Fun fact: despite the problem's description, I actually didn't to use any sort of graph or tree to solve the problem (at least, not directly...)! Instead, I've mostly worked with [recursive](https://en.wikipedia.org/wiki/Recursion_(computer_science)) functions. (In truth, there *is* a tree behind all this; however, we don't need to apply graph theory here.) Recursion is a type of algorithms where your top solution depends on the solution you computed for smaller instances of the problem. You therefore call the function from within itself (here ``parse_rec()`` is called inside of ``parse_rec()``, for example).

In this solution, I've mostly reused tools I've mentioned before, or basic Python tech. A little new addition is the use of a [``try/except`` block](https://docs.python.org/3.5/tutorial/errors.html) in the ``compute_node_value()`` function. This Python statement is a way of handling exceptions and errors; here, we know that it can happen our script tries to access nodes that do not exist (if the metadata item taken as an address doesn't point to any real node). To avoid the program crashing if it does not find the required index in the list of children, we surround the item access with a ``try/except`` block and keep an eye out for any ``IndexError``. If none occurs, then the code in the ``try`` part will execute and we will indeed retrieve an element. Else, the code in the ``except`` block will execute and will continue directly to the next item in the list.

On another note, if we had a really big tree, it could be interesting to reduce the number of calculations by using *memoization*. This technique is a powerful way of drastically increasing your algorithm's performance whenever it relies extensively on multiple recomputations of the same value (i.e. a call to the same function with exactly the same parameters a huge amount of times). It uses suitable data structures to maintain a cache and therefore avoid re-calculating already prepared results.

For example, in our case, if we had an input with many nodes, then computing the value of the root would probably imply going down the same nodes several times (either directly, if the same child is accessed multiple times; or indirectly, if a child is needed more than once while going down all the recursions from the root). So, rather than recomputing the value of these nodes each time, we could use memoization and create a dictionary that associate a node index to its value. The first time we encounter the node, we need to compute the value; but then we will have its value stored and accessible way more quickly than if we had to redo the complete calculation.

*Note: dictionaries are the ideal Python structure for this task because they are hashed data structures that have a constant element access time, i.e. an access time in `O(1)`.*

To do this memoization, we can define a global variable to serve as cache. However, a more common (and, in my opinion, prettier) option is to use a [function wrapper](https://wiki.python.org/moin/FunctionWrappers). In Python, wrappers allow us to essentially "add behavior" to a function easily without having to modify the function itself. A wrapper is basically another function that can do some things before and after it calls the original function, therefore extending its behavior. By adding these "prologue" and "epilogue" tasks, we can automate various processes: resource allocation/deallocation, pre-/post-checks, caching...

For our specific example of memoizing the node value computation, we could define a wrapper like this one:

```python
def memoize(func):

    cache = {}  # holds the already computed values
      
    def wrapped_func(nodes, node):
        # if it is the first time we encounter this node index as input parameter,
        # we compute the value and we store it in the cache
        if node not in cache:
            cache[node] = func(nodes, node)
        # in any case, we can now access the (possibly newly) stored value
        # corresponding to this node index as input parameter
        return cache[node]
        
    return wrapped_func
```

And then "apply" this wrapper to our ``compute_node_value()`` function with a Python decorator:

```python
@memoize
def compute_node_value(nodes, node):
  ...
```

Now, our function will be able to "remember" if it has already computed a result for a given node; if that's the case, then it can fetch the result directly and gain a lot of time! We still call exactly as we would normally, the decorator will take care of wrapping our ``memoize()`` function "around" it.

*Note: if you do implement this, make sure that you don't "mix up" your inputs. What do I mean by that? Well, this is a pretty simple wrapper that isn't able to tell if the "node 0" you're referring to is from your first or your second graph. If it has a value for the node 0, it will consider it does not need to redo the computation. Suppose you've used ``compute_node_value()`` on another graph first, and that you use auto-incremented IDs like I do here; then your second graph will also contain nodes with ID 0, 1, 2... and so the function will just ignore the new graph structure and give you back the old value. To avoid this, you would have to improve the wrapper, add some uniqueness to your IDs that distinguishes the two graphs or reset the cache - but this would require to a class rather a wrapper approach of the memoizer (see [this Overflow thread](https://stackoverflow.com/questions/4431703/python-resettable-instance-method-memoization-decorator)).*

## Day 9: Marble Mania

#### Answers
**Part I: 375414 • Part II: 3168033673**

Aside from the way the problem is formulated that I do believe is a bit tricky to understand at first, Day 9 is actually not that hard. The thing is though that a brute force approach will work for Part I but might be way too long for Part II (that is exactly the same computation just with larger inputs).

My first idea was to represent the board of marbles with a list. However, this data structure is not the best for multiple insertions and removals everywhere. Here, the idea is to instead use a [*double linked list*](https://en.wikipedia.org/wiki/Doubly_linked_list). This data structure relies on a sequence of nodes that each have some data but also a direct link to whomever their predecessor and their successor is in the list. The list I've built is circular, meaning that the "last" node points to the head of the list and that you can cycle back - this represents the "circle of marbles" that can be looped through infinitely.

My ``DoubleLinkedList`` class implements the methods I needed for the problem: a notion of "currently selected node" (to represent the current marble), a way of adding a node at the "end" of the list and a way of inserting or removing nodes with an offset from the currently selected node. (I've also added a ``print()`` function to make debugging easier.)

By taking some time to prepare my data structure first, I've then managed to write a very short code for the actual processing function (``compute_highscore()``).

Still, on the large input, it takes ~30 sec. It's not catastrophic but could probably be improved. To keep an eye on the computation process, I've used a Python lib called [tqdm](https://pypi.org/project/tqdm/). This package allows you to easily wrap an iterator (such as a ``range``) with the ``tqdm()`` method so that your shell displays the iterations with a progress bar and the total execution time.

## Day 10: The Stars Align

#### Answers
**Part I: BFFZCNXE • Part II: 10391**

Day 10 is a bit different from the rest of the problems because it can (easily) be solved automatically: you are asked to see how stars move in the sky until they align to form a message, and therefore need to use your own human eye to spot the correct string of characters.

*Note: we __could__ use OCR (Optical Character Recognition) methods to automate the process, however I didn't want to dive into this at the moment and thus decided to rather stick with the "by-hand" method. But if you're interested, it looks like [pytesseract](https://pypi.org/project/pytesseract/) could be a nice Python wrapper around Google's ``tesseract`` OCR solution.*

Nevertheless, it is quite obvious that printing the board each time step won't work: it will just take forever and most of the time we will be facing jibberish! So the idea is to try and minimize the average between points, because we know that when they actually spell out the message, they should be "organized" and therefore each pair of points should have a low distance on average. We assume that finding the iteration when we have the minimal average distance is equivalent to finding the iteration at which the message is printed in the sky.

My solution was to:
- first decide on a maximal number of iterations (I've decided 15000 was enough, the message had to be somewhere in that range... and anyway, I could have just upped the bar gradually if I didn't get any result!)
- then compute the evolution of the sky by applying their velocity to the stars each round
- for each iteration, compute the average distance between the stars and store it
- finally, find the time step where the distance was minimal (i.e. the index of the minimal value in the array, or the *argmin*), recompute the board for that time step and display it

By the way, this directly gave me the solution for Part II, that asked for the time step at which the message would appear in the sky.

To compute the average distance, the naïve approach is to do a nested loop, going over the points in your board twice and adding all the distance, then dividing by the total number of points. This works, but it is a *very* slow process. Instead, we can use the [scipy](https://www.scipy.org/) along side with [numpy](https://numpy.org/) libs that are *the* most common Python packages for data processing. Among lots of other things, ``scipy`` has a function to compute all distances between two collections of points, ``cdist()``. With that and ``numpy``'s ``mean()`` function, I was able to compute my average distances really fast! Then, a simple ``numpy.argmin()`` gives me the time step at which the message appeared (according to the previous assumption).

*Note: just for the sake of it, I invite you to go and check out [the reddit thread](https://www.reddit.com/r/adventofcode/search/?q=2018%20Day%2010&restrict_sr=1) for this problem - people have talked about OCR and even done some movies for their own input where you see stars move in the sky, form a message and then part ways again.*

## Day 11: Chronal Charge

#### Answers
**Part I: 21,41 • Part II: 227,199,19**

This problem is a good opportunity to mention two concepts: convolution and data preprocessing for computation speed up.

Firstly, [convolution](https://en.wikipedia.org/wiki/Convolution) is a mathematical operation that uses 2 functions, say *f* and *g*, and basically "applies" one to the other. It is used in lots of domains like probability, stats, image processing, artificial intelligence... In particular, some neural networks of the CNN family have become famous for using "kernels" (or "sliding windows") that just "run over" an image and are applied on each pixel with this convolution process. If you take a "full kernel" of ones as your sliding window, then each time you will take the contribution of all the pixels beneath your window and thus perform a sum operation. Here, I used the ``scipy`` lib once again to do this computation.

Secondly, we can consider the problem as a [submatrix sum queries](https://www.geeksforgeeks.org/submatrix-sum-queries/) problem: we are asked to check out the sum of cells in squares with a growing size and find both the top-left corner coordinates and the size of the square that gives the highest sum. The brute force method would be to make our squares have a size ``s`` that grows continuously from 1 to 300 and to compute the convolution of our grid with an ``s x s`` kernel. However, it is super long. And it just keeps getting longer and longer as ``s`` increases, actually.

A better way to deal with this problem is to prepare an auxiliary matrix (created with ``compute_auxiliary_matrix()``) that contains cumulative sums in each of its cells and therefore gives us access in constant time (`O(1)`) to the sum of subsquares of the original grid. This allows us to get the total sum of a given rectangle very fast (see the ``get_sum_square()`` method). Now, we can loop through our possible sizes and find the optimal conditions.

*Note: some quick tests seem to indicate that for the small 3x3 kernel case, ``scipy`` is efficient enough for it to be faster to use convolutions rather than an auxiliary matrix and a submatrix sum queries approach...*

## Day 12: Subterranean Sustainability

#### Answers
**Part I: 2049 • Part II: 2300000000006**

Day 12 doesn't require any external libs; it's quite simple overall even though I'll admit I had some difficulties with off-by-one results... basically some indices shifting in the wrong place! :)

Part I is just about implementing the given algorithm while making sure you add new spaces for additional pots every generation (using buffers that depend on the rules of your problem, computed by ``padding_buffers()``).

Part II then asks you to just repeat the same process for a number of iterations that is way, way, way larger - thousand of millions larger, actually! It's obvious the same technique won't work in a reasonable time. However, you may quickly have the intuition that there must be patterns and cycles in these evolution rules... and, indeed, if you try to compute the pots evolution for a few hundreds of iterations, you might discover that at one point the state starts repeating itself, just shifted by one position on the right.

In other words, starting from some generation ``G`` (that depends on your input), the pots state will be the exact same pattern of "active" and "empty" pots (same intervals of ``#`` and ``.``) but the position of the first "active" pot will increase by 1 every time. In my case, the repetition started at iteration 102. From that point on, you know that there is no use re-applying the rules anymore: you will just be "translating" the whole shelf of pots to the right until you reach this insanely high iteration you're asked for.

So, instead of actually computing the remaining iterations, you can early stop your computation process and finish the process by applying this translation to your current state. With only a few additions, you will have inferred the state the system would have reached if you'd let it run until the final iteration - but you will have done it much, much faster!

This is a good example of something that is often true when solving this kind of problems, and when solving problems in general: it might be interesting to study "by hand" (or at least on a smaller sample) how your system behaves and evolves to try and spot an underlying pattern. If there is one, you might be able to predict the evolution accurately while skipping lots of steps and therefore gaining a lot of computing time.

## Day 13: Mine Cart Madness

#### Answers
**Part I: 53,133 • Part II: 111,68**

This problem is quite straight-forward and only requires you to focus when you compute the carts' movements. I've used classes extensively in my solution to easily manipulate the mine map and the carts (so I have a ``Mine`` and a ``Cart`` class that each have several methods and communicate together in various ways).

There is not much to say, the problem doesn't even ask for a lot of optimization since your input is quite small (a 150x150 grid).

I'll point out some tools I've played around with, though:

- for my ``Mine.display()`` method, when I show carts, I wanted them to stand out a bit more; so I've used [ANSI codes](https://en.wikipedia.org/wiki/ANSI_escape_code) to pump my shell output up a bit and carts are now shown in bold red. The basic idea of ANSI codes is to add special bits that the console won't interpret as strings but as commands and that can modify the format of the output it surrounds (add color, bold...).

- for the cart intersection crossing algorithm, in order to have the cycling directions ("first to left, then straight, then right; then it cycles back"), I've used a modulo operation to easily "wrap around" the third state

- for my test input data, I've used Python's docstrings (with triple quotes) to be able to include new lines into my strings (as if I were reading a multiline file)

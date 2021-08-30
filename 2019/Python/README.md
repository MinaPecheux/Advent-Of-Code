# [2019] Python

This subfolder contains my code solutions for challenges from the 2019 series, written in Python (3.6.5).

## Preliminary note: files organization
In these files, I try to always organize the code in the same way:

1. first, some imports if need be (either Python built-in libs or external packages)

2. then, parsing functions to read and extract data from the provided input (that seems to always be a string of characters)

3. then, the actual computation functions, separated in 3 bits:
  - util and common functions
  - functions for the Part I of the problem
  - functions for the Part II of the problem
  
4. a test function with a set of ``assert``s to check that my computation functions seem to give an ok result (using the examples provided with the problem)

5. finally, the main part that solves the problem by running the computation functions on the actual inputs I was given (that depend on the user)

## Intcode interpreter (``intcode.py``)

This year, several puzzles make use of an Intcode interpreter that is built gradually all throughout Day 2, 5, 7 and 9 (at this point, you're supposed to have a complete interpreter able to execute any Intcode program that you're given).

It is further used on Days 11, 13, 15, 17 and 19.

In order to avoid repeating code, I've coded up my Intcode interpreter into a dedicated file called ``intcode.py``. To do that, I've used a key feature of Python that falls under the object-oriented programming paradigm: classes. It is a nice way of aggregating together bits of code that have a logical link.

To create a basic class, you should inherit from the ``object`` built-in and then define a ``class`` that has at least an ``__init__()`` method:

```python
class IntcodeProgram(object):
    
    def __init__(self):
        pass
```

This ``__init__()`` function will be called whenever you instantiate a new variable of type ``IntcodeProgram``. The neat thing with object-oriented programming, as I said just before, is that you can gather in the same place various variables or methods that are logically linked together; here, our class can contain other methods that implement the behavior we want one of program instance to have: a basic state check, memory updates, instructions execution...

My final ``IntcodeProgram`` class provided me with an easy-to-use interface for my actual computation functions in the puzzle scripts. In those functions, I just create instances of the ``IntcodeProgram`` class and play around with them, but the class abstracts away all the actual execution or memory management stuff so that these computation functions aren't too long.

This means that the true meat of the code resides in the ``IntcodeProgram`` class.

I've used a class variable called ``INSTANCE_ID`` to assign auto-incrementing IDs to my instances. Rather than maintaining a counter outside of the class, I can just let it take care of it and automatically generate a new integer ID whenever I create a new instance of my class. However, I need to be careful to reset the counter whenever I want to reset my pool of instances from scratch (for example, in Day 7, whenever I want to try a new permutation of phase settings).

## Day 1: The Tyranny of the Rocket Equation

#### Answers
**Part I: 3345909 • Part II: 5015983**

This first challenge is pretty straight-forward. The only notable thing is that Part II strongly indicates you should [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) to solve the problem. Given that you have a question of the form "compute a value for something, then compute the value for this new thing, and so on..." you want to create recursive function, i.e. a process where your top solution depends on the solution you computed for smaller instances of the problem.

You therefore call the function from within itself (here ``compute_total_fuel()`` is called inside of ``compute_total_fuel()``).

## Day 2: 1202 Program Alarm

#### Answers
**Part I: 3716293 • Part II: 6429**

> Day 2 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

This problem is an opportunity to talk about **mutability** in Python. We are making use of the Intcode interpreter for the first time and we need to pass it the code to execute (which is stored as a list of integers). In my ``IntcodeProgram`` class, this program is turned into a dictionary. This allows me to make a new "version" of the inputs that is independent from the initial list that I feed the instance so that it isn't touched by the code.

Mutable variables are variables that, even if they are passed as parameters to functions, still point to the same address in memory and can therefore be modified directly.

On the other hand, immutable classes like the basic types (``bool``, ``int``, ``float``, ``str``) and some particular containers (``set``, ``tuple``, ``frozenset``) cannot be modified after being created. If you want to change the value, you need to reassign the variable to a brand new value in memory.

For example, in the ``process_inputs()`` function, I pass the ``inputs`` list to my Intcode program so that it makes its own copy of it.

If I removed this transformation, I would need to "copy" the inputs before running them through any processing code!

> For more info on immutability in Python, you can check out [Python's reference](https://docs.python.org/3/reference/datamodel.html?highlight=immutability) on the data model (Dec. 2019).

## Day 3: Crossed Wires

#### Answers
**Part I: 209 • Part II: 43258**

The challenge with this problem was to handle the large lists as quickly as possible. To do so, I used lists, dictionaries and sets and tried to make the best out of those worlds (depending on [the time complexity of various operations for each data type](https://wiki.python.org/moin/TimeComplexity)):

- lists are ordered, meaning that you can access elements by index, and they allow for ``min`` or ``max`` operations; this lets me easily refer to the "first" (at index 0) and the "second" (at index 1) wire, to take the smallest distance...

- dictionaries are hashable containers that work with key-value pairs; they are great for quick element access (it is in `O(1)`, i.e. in constant time)

- sets are quite close to dictionaries but they are super fast at union and intersection operations; this is a big plus for my ``intersections`` computation that just needs to check what keys are in common in two dictionaries

By using the right data type at the right time, you can increase the computation time tremendously.

## Day 4: Secure Container

#### Answers
**Part I: 1019 • Part II: 660**

There is not much to say with this solution, except that I use a built-in Python lib, ``collections``. This package contains some very useful additional types that are optimized for a specific task. For example, here, I use a ``Counter`` that is very quick at creating a dict-like structure that associates each unique value in a list to the number of times it appears (see the function ``number_is_ok_p2()``).

Also, I take advantage of Python's ability to quickly change from one type to another by treating my number and its digits either as integers or as characters depending on what I need.

## Day 5: Sunny with a Chance of Asteroids

#### Answers
**Part I: 15508323 • Part II: 9006327**

> Day 5 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

In this puzzle, I did some modifications on the common ``IntcodeProgram`` class to keep on improving its features (namely: I reorganized the ``OPERATIONS`` dictionary to hold more information and I've worked on the ``process_opcode()`` method to automate pointers evolution).

I've also made a secondary version for the Day 5 puzzle to play around with the notion of Python's context classes.

In this version, I don't directly use the common ``IntcodeProgram`` class but rather extract just the required features and use a a custom util ``Debugger`` class.
  
The ``Debugger`` class is a utility I had fun making that just allows me to have my program output its results to a specific stream rather than the usual ``sys.stdout`` used by Python when you do a ``print()``. It is a context manager class that simply puts a piece of code into a special "state" where it has a access to a global stream variable to write to.

In my local ``process_opcode()`` function, for the output instruction (with code ``4``), I make use of this stream if possible.

Then, at the very end of the execution of my program, I can simply query the ``last_output()`` of the stream stored in my current ``Debugger`` instance to get my result. This significantly simplifies the test functions and the assertions. (Otherwise, I would have had to read back the printed output, somehow, and split it back to get the last line...).

### Day 6: Universal Orbit Map

#### Answers
**Part I: 142915 • Part II: 283**

From an algorithmic point of view, this problem is focused on graphs. The orbits we are given depend on each other in such a way that we can draw a graph of their connections. More precisely, it is a tree because one node (namely the Center Of Mass, COM) has no parent, so there is no cycle and COM is called the "root".

[Graph theory](https://en.wikipedia.org/wiki/Graph_theory) is a fascinating field. Re-implementing graphs from scratch is interesting but I could never have reached optimal performance, so I decided to instead use the Python package [NetworkX](https://networkx.github.io/documentation/stable/index.html). This lib contains efficient structures to represent and manipulate graphs: you can create nodes, edges (either directed or undirected), search for adjacent/successors/predecessors nodes, apply path computation algorithms...

I won't do a full detailed presentation of the lib itself but rather I'll take this opportunity to point out once again that, to me, a huge strength of Python is the ecosystem that has gradually been built for it by the community. Today, the Python language is not just a well-designed script language but also an abundant collection of packages that have been developed by the Python team or the community and help us solve lots of problems. In Python, the phrase "don't reinvent wheel" is usually very true: before trying to rebuild a complex system from the ground up, you should first check if there isn't already a lib that takes care of that. A good Python program is more often than not a well-organized suite of cleverly chosen efficient bricks.

*Note: this is particularly important in data science where you often deal with large amount of data. A common tech stack for data scientists includes the Numpy and Scipy libs - this is because these libraries have been super-optimized and partly rely on compiled and hardware-tuned code to speed up computation remarkably.*

## Day 7: Amplification Circuit

#### Answers
**Part I: 116680 • Part II: 89603079**

> Day 7 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

For this problem, we need to run several instances of our Intcode program at the same time while making sure each has its own "environment". This lead me to implement the ``run_multiple()`` method in the shared ``IntcodeProgram`` class. It is not truly parallel execution, though, since some instances will depend on the output from others and thus need to wait for them before they can proceed. Hence the need to separate data for each instance, so that they don't overwrite sensible information that the other might use later on.

## Day 8: Space Image Format

#### Answers
**Part I: 2064 • Part II: KAUZA**

Day 8 is a nice easy peasy Sunday problem about image decoding. It is quite simple and does not require any external libs (some people in the threads talk about using ``numpy`` but, in truth, I feel like it's sort of overkill this time). You just need to be careful in how you represent a 2D image as a 1D string and compute your position transformations properly.

In Part II, the only tricky thing is the order of the layers: you're told that the first one comes first, then the second one, and so on. They can overwrite each other (if the pixel is not transparent), so the easiest way to deal with this is to process them in the reverse order: take a "result image" that you initializing with blanks everywhere; then iterate through your layers from last to first and simply turn on or off pixels if you find the corresponding value.

## Day 9: Sensor Boost

#### Answers
**Part I: 2752191671 • Part II: 87571**

> Day 9 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

To be honest, while I spent *hours* trying to debug some index shifting errors, the problem is not that hard *per se*: once again, I'm asked to improve the Intcode program I worked on during Days 2, 5 and 7. Compared to the previous Intcode interpreter, we need to add a new mode, called the "relative" mode, that allows for address references with a relative base (that can be modified) and the ``offset_relative_base`` instruction to update this aforementioned relative base.

My big issue was to properly understand what remain indices and what turn into data with the new mode... many thanks to [youaremean_YAM](https://www.reddit.com/user/youaremean_YAM/) for his/her JS solution that finally helped me get it right!

Part I and Part II only differ in the input you pass your processing function: ``1`` for the first, ``2`` for the second. Other than that, you should execute the exact same code.

*Note: the code could probably be further optimized... it takes about 7 seconds to solve Part II. Even though this is not that bad, it would be nice to have a faster execution (the JS code I talked about earlier gives me the answer instantaneously: fancy!).*

## Day 10: Monitoring Station

#### Answers
**Part I: 280 • Part II: 706**

*Disclaimer: my first solution for Part I was really ugly... I've drawn inspiration from [kcon1](https://www.reddit.com/user/kcon1/)'s answer on the reddit thread, [over here](https://www.reddit.com/r/adventofcode/comments/e8p9zz/2019_day_10_part_2_python_how_to_approach_part_2/) for Part I. Part II is loosely inspired by his/her suggestion.*

Overall, the solution relies on tools I've already mentioned before: classes, ``dict``s, ``set``s, ``list``s... One thing to note, however, is that we use the fact that Python ``set``s are unordered collections of *unique* items: whenever you add an item to the set, if it is already there, then the collection won't actually be updated.

This allows us to "overwrite" the asteroids that all have the same angle to the reference asteroid, in ``compute_asteroid_sights()``, and therefore to essentially "mask" the ones that are hidden.

## Day 11: Space Police

#### Answers
**Part I: 2093 • Part II: BJRKLJUP**

> Day 11 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

In this puzzle, we want to stop after we have outputted a certain number of digits with our program. Thus I added a ``pause_every`` optional parameter to my ``run()`` method in the shared ``IntcodeProgram`` class to be able to pause the execution after a given number of outputs.

The ``process_inputs()`` function simply makes use of the common class to give us the result both for Part I and Part II.

The basic idea of this method is to:
- create an instance of our ``IntcodeProgram`` class to execute the given inputs as an Intcode program
- have it run with a pause every 2 outputs
- whenever it pauses, parse the last two outputted digits to get the new color of the panel, the new rotation of the robot and move it on the board

There are some auxiliary variables to store what we need for the result: the current direction and coordinates of the robot, the set of panels that are currently painted white and therefore form a message (``board``) and finally the set of panels that have been painted at least once by the robot, even if they have been repainted black since the beginning (``painted``).

In Part I, we want to know how many panels the robot will paint. So we simply need to get the length of the ``painted`` set.

In Part II, we want to actually output the message. This time, I'm using the ``board`` set that only stores the panels that are currently painted white. At the end, I simply need to iterate through this set of positions to display the message.

*Note: a small hint about the ``x`` and ``y`` coordinate changes depending on the direction - while you might think that going "up" means increasing the ``y`` coordinate, it is better to decrease it so that the message prints correctly at the end of Part II. Otherwise, you will get a message reversed on the horizontal axis and you will have to iterate your ``y`` range in reverse order...*

## Day 12: The N-Body Problem

#### Answers
**Part I: 12082 • Part II: 295693702908636**

In this problem, Part I is a simple re-implementation of the given algorithm; once again, I use some iterators from ``itertools`` and the fact that ``list``s are mutable.

Part II, on the other hand, is a bit harder. It is clearly not feasible by brute-force. I admit I searched for a little while but didn't find the trick and finally headed up to the dedicated reddit thread. As explained for example in [this post](https://www.reddit.com/r/adventofcode/comments/e9jxh2/help_2019_day_12_part_2_what_am_i_not_seeing/), you need to spot that the 3 axis are actually independent. This means that the repetition period you need to find can be computed by finding the period of each axis and then finding the least common multiple of these 3 numbers.

To do this, I've used ``dict``s and the built-in ``hash`` Python method that is a neat way of quickly generating an efficient [hash](https://en.wikipedia.org/wiki/Hash_function) from a string. This allows me to easily get the period of each axis. Then, I implemented some classic ``GCD()`` and ``LCM()`` functions to perform the final computation.

*Note: for the input parsing part, I used a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) (or Regex): the idea is to define a "pattern" to search for in a string, and then to see if the given string can be matched to this pattern. If so, we are even able to isolate the bit that match the different parts of our pattern and thus directly extract our values.*

## Day 13: Care Package

#### Answers
**Part I: 268 • Part II: 13989**

> Day 13 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

There is no need to change anything in the actual ``IntcodeProgram`` class this time, it's just about providing the right inputs to the program to solve the problem!

Part I is quite straight-forward: you simply need to run the program and stop every 3 outputs, then parse the 3 digits to get the ``x``, ``y`` and ``id`` value at this stage, and finally use those to update the ``board``.

Part II is not that hard either, you simply need to:

- modify the initial program to "play in free mode", i.e. replace the first digit in the Intcode program by a ``2``
- move the horizontal paddle to catch the ball and not have the game stop immediately - this basically means you need to go right when the ball is on your right and left when it's on your left, which is done by putting the right digit in the ``IntcodeProgram``'s memory
- keep track of the number of remaining blocks
- whenever you output a score, if there are no blocks remaining, the game ends and you can return this last score as the player's final score

I've also added a feature in the ``compute_score()`` method to automatically export screenshots of the game while it is running. If you turn on the ``export`` option, then a folder ``day13/`` will be created in your current working directory and the board will be saved as JPG images regularly.

*Note: turning on the export mode will significantly slow down the computation, so you should only enable it if you want to create the images. It is disabled by default.*

It is then really easy to create a basic MP4 movie from all of those JPG images using the common audio/video conversion tool [ffmpeg](https://ffmpeg.org/):

```
ffmpeg -framerate 200 -i day13/%d.jpg day13.mp4
```

This will produce videos like [this one](resources/day13.mp4).

## Day 14: Space Stoichiometry

#### Answers
**Part I: 469536 • Part II: 3343477**

*Disclaimer: While I originally had a similar idea to the one presented here, I actually got completely stuck on this problem and could only solve some of the example cases with my initial algorithm! I eventually headed to the reddit thread and found for example [this answer](https://github.com/jcisio/adventofcode2019/blob/master/day14/d14.py) by [jcisio](https://www.reddit.com/user/jcisio/). My solution is simply a reimplementation of his/hers to fit my usual solution format.*

The issue I had with my original solution was that I couldn't process the materials in the proper order; so I had trouble accounting for the required amount of ``ORE``.

The trick to solve this problem is to use some sort of topological sort on the data to be able to consume the reagents "in the correct order". More specifically, here, we simply consider the "distance" each reagent has to the final raw material, ``ORE``.

Then, we can do the sort of loop I had in my initial algorithm but always take the material that is the "farthest" from ``ORE``, and thus use the "more complex" reactions in our list.

The only small improvement I've found upon ``jcisio``'s code is to use the ``defaultdict`` container (available in the ``itertools`` module) to have a dictionary of integers able to replace the missing values with a default automatically. This is a neat way of "adding" to a dictionary without having to explicitly handle the initial case when the key is not yet present in the dictionary: if this happens, then the ``defaultdict`` will simply assume a default value at this key and then process your action based on that (in the case of a ``defaultdict(int)``, the initial value is ``0.0``).

## Day 15: Oxygen System

#### Answers
**Part I: 240 • Part II: 322**

> Day 15 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

Day 15 is about maze exploration and traversal, hence I needed to reimplement some common graph-related algorithms. Namely, I've worked on flow algorithms, pathfinding algorithms and general recursive search (with a BFS-approach, here).

*Note: a detailed article about this challenge is available on my blog [over here](http://minapecheux.com/wp/exploring-and-traversing-a-maze/).*

Since we don't know what the room looks like, we first need to explore it to map out the tiles types at each coordinate ("wall", "empty" or "oxygen system"). To do this, we can proceed recursively by moving the robot through the entire board and storing its feedback for each tile; this allows us to get a match between an (x, y) coordinate and a tile type.

Then, we can use Dijkstra's algorithm to compute the shortest path between the initial position of the robot and the oxygen system.

Part II asks us to determine how long it takes (how many iterations it requires) to fill the entire maze with oxygen, starting from the oxygen system and then propagating oxygen to the neighbor tiles at each iteration. This can be solved both with a DFS- or BFS-approach; I originally coded up a DFS-based algorithm and eventually changed it to a BFS-approach to be able to do a visualization.

I've also played around with the ``NumPy`` and ``PIL`` packages to export the process frame by frame so that I could later assemble them into movies with ``ffmpeg``. If you turn the ``export`` option on, the solver will also store the state of the maze at various steps into various folders (``day15_explore/``, ``day15_path/`` and ``day15_fill/``). These images can then be turned into movies with ``ffmpeg`` like this:

```
ffmpeg -i day15_explore/%d.jpg day15_explore.mp4
```

If you want to control the speed of the movie, you can change the framerate (by default, it is of ``25``; a higher framerate means a faster video):

```
ffmpeg -framerate 60 -i day15_explore/%d.jpg day15_explore.mp4
```

This produces videos like the ones in the ``resources/`` subfolder available here: for the [explore](resources/day15_explore.mp4), [path finding](resources/day15_path.mp4) and [fill](resources/day15_fill.mp4) steps.

## Day 16: Flawed Frequency Transmission

#### Answers
**Part I: 50053207 • Part II: 32749588**

For this problem, we are once again faced with an optimization issue. Indeed, Part I can be solved with a very naive approach that basically reimplements the given algorithm and applies it 100 times to the inputs to compute the next phase each time. However, Part II cannot work the same way because the inputs we need to deal with are too big for this approach to compute the solution in a reasonable time.

The trick is actually quite specific to both the inputs and the applied pattern (though I had sort of felt the idea, I read it phrased more clearly in [this reddit thread](https://www.reddit.com/r/adventofcode/comments/ebf5cy/2019_day_16_part_2_understanding_how_to_come_up/)):

- because of the offset that is applied to the pattern, the first numbers in it are zeroes which act as a "filter" that simply ignores the beginning of the inputs for the new phase computation

- moreover, when you've passed those zeros, you then have a bunch of ones that basically sum the digits in the inputs on this portion

- in particular, suppose we have an input of length ``L``; then for the ``N``th digit of the new phase, if ``N >= L / 2``, we only have to sum the digits of the inputs from the index ``N`` to the end

- and it so happens that, in Part II, we are asked to skip a number of digits that is more than ``L / 2``!

- therefore, we are in this specific case and we can use that to significantly reduce the computation time: at each step, when we compute the next phase, we only need to take care of the end of the inputs and to sum them starting from the right index

To avoid summing lots of digits at once (``L / 2`` can still be a pretty huge number...), we can start from the last digit in the new phase that has to be a simple copy of the last digit in the previous phase, and then work back until we reach our "skip digits" head index. For every digit, we just sum the one we computed previously (and that represents the whole sum minus the current digit) and add it the current digit from the previous phase.

*Note: because this solution is tuned specifically for these types of inputs, we can't truly check it on the given tests - for the examples that Eric provides, the number of digits to skip is below the ``L / 2`` threshold and thus our method won't work properly...*

## Day 17: Set and Forget

#### Answers
**Part I: 3292 • Part II: 651043**

> Day 17 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

*Disclaimer: for now, my solution is a mix of automated and by-hand steps; in particular, I've determined the complete path automatically but the division in 3 subpatterns (the ``A``, ``B`` and ``C`` movements) was done just by looking at the result. I haven't found a way to do this without a human eye yet.*

Day 17 uses the Intcode interpreter yet another time! Today, I was asked to play around with ASCII encoding/decoding a bit and to move a little robot on a map uses an Intcode program.

Part I is pretty simple: you want to find the intersections on the map and to compute a basic checksum from them. So, you just need to:
- convert the ASCII codes to characters (thanks to Python's built-in ``chr`` for example)
- check where the characters correspond to a scaffold (i.e. the character is ``#``)
- see where one scaffold is surrounded by 4 others: this is an intersection
- then for each intersection of ``(x,y)`` coordinates, compute its checksum ``x * y``
- and sum all the checksums

Part II *could* have been a piece of cake but the fact that the robot has a limited memory forces you to use the ``A/B/C`` movements mechanism to compress the repeating patterns and have a complete path request that fits in storage.

My technique is as follows:

1. compute the full path that the robot needs to take to walk on each scaffold at least once

2. look at the path myself (with a human eye) and find out the repeating patterns, making sure that they aren't too long and that there are only 3. I actually gave it shot and had a final pattern that "overflowed" and moved the robot a bit too much... but it seems to be alright and to still give me the right answer! :)

3. encode the movements and the pattern of movements into ASCII (with Python's built-in ``ord``) and pass it to the robot, then wait for the program to complete its execution and get the last output as my final result

I've also implemented an export option just like in previous puzzles - it will create a subfolder ``day17/`` containing images of the robot's complete set of movements on the map. These images can then be turned into a movie (like [this one](resources/day17.mp4)) with ``ffmpeg``:

```
ffmpeg -framerate 30 -i day17/%d.jpg day17.mp4
```

## Day 18: Many-Worlds Interpretation

#### Answers
**Part I: 4620 • Part II: 1564**

*Disclaimer: the solution comes from [i_have_no_biscuits](https://www.reddit.com/user/i_have_no_biscuits/) (it's available [over here](https://repl.it/repls/DarkkhakiExcitableSnake)). I've merely organized it a bit, documented it and wrapped some useful functions into a ``Map`` class.*

While my first solution did well with the very basic examples, it got stuck with the last examples because I hadn't found a way to clearly sort paths so that I could avoid going the long way around and lose moves getting a far away key.

In truth, I think I was thinking more along the lines of a DFS whereas a BFS is better in this scenario. The technique used here is to first prepare a dictionary to match all interesting points on the map (i.e. entrances, doors and keys) to their distances to all the other interesting points and the optional points that are on the road between the two. This way, it is possible to easily sort according to distance and also check if all the obstacles on the way can be passed.

*Note: the code could perhaps be optimized since Part I currently takes ~5 seconds to solve...*

## Day 19: Tractor Beam

#### Answers
**Part I: 217 • Part II: 6840937**

> Day 19 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

In this puzzle, we talk about a tractor beam! The question is: what positions in the grid facing us are affected by this beam? To learn whether a position is affected or not, we can call a specific Intcode program that, once run with the ``(x, y)`` position as inputs, will return ``0`` if the position is not in the tractor beam and ``1`` otherwise.

I'll admit I brute-forced both Part I and Part II... but I did find a way of optimizing the map construction! All in all, both parts take about 1'30'' min to be completed.

Indeed, since the tractor beam is oriented to the bottom right corner, we can drastically reduce the number of positions to check. My technique was as follows (considering row ``y``):

- suppose that row ``y-1`` had "tracted positions" only from ``x_min`` to ``x_max`` (the rest of the row would return ``0`` if checked)

- then we can safely assume that the next row will roughly spread from ``x_min - 1`` to ``x_max + 1`` at most (the cone of the beam does not grow on its own, so it simply increases a bit with each row)

- so we basically need to check only 6 positions (to be really safe...):
  - ``(x_min - 1, y)``, ``(x_min, y)``, ``(x_min + 1, y)`` for the minimum boundary; this will also give us the new value of ``x_min`` which is the lowest value where the position is affected between ``x_min - 1``, ``x``, ``x_min + 1``
  - ``(x_max - 1, y)``, ``(x_max, y)``, ``(x_max + 1, y)`` for the maximum boundary; this will also give us the new value of ``x_max`` which is the highest value where the position is affected between ``x_max - 1``, ``x``, ``x_max + 1``

- then, we can "fill" the horizontal positions in the middle of the (updated) ``x_min -> x_max`` range

Here is a little representation of the scene to help you get the gist of it - the ``#`` are the positioned in the tractor beam from last row, the ``?`` are the positions that will be checked, the ``x`` are the positions that will be filled:

```
              x_min      x_max
                  |      |
                  v      v
ROW   y - 1   ....########........
          y   ...???xxxx???.......
```

This will still give us a linear execution time, but it will be greatly reduced! This means that we can examine quite a large grid in Part II without too unrealistic of a compute time.

In Part II, since I know I'm searching for a ``100 x 100`` square, I've decided to first prepare a ``2000 x 2000`` grid and to then search in it for the square matching this size that is the closest to the origin (at coordinates ``(0, 0)``). A disclaimer however: this size of 2000 fits my inputs (so that it's not too long but still enough for a ``100 x 100`` square is present in it). (My first trial with a ``1000 x 1000`` grid did not contain any solution.) Depending on your input, you might need to change this size in the ``find_closest_square()`` function.


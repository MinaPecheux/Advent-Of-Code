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

## Intcode interpreter (``intcode.cpp``, ``intcode.hpp``)

This year, several puzzles make use of an Intcode interpreter that is built gradually all throughout Day 2, 5, 7 and 9 (at this point, you're supposed to have a complete interpreter able to execute any Intcode program that you're given).

It is further used on Days 11, 13, 15, 17 and 19.

In order to avoid repeating code, I've coded up my Intcode interpreter into dedicated files called ``intcode.cpp`` and ``intcode.hpp`` (associated header file). To do that, I've used a key feature of C++ that falls under the object-oriented programming paradigm: classes. It is a nice way of aggregating together bits of code that have a logical link.

To create a basic class, you should have a constructor and a destructor:

```c++
// constructor
IntcodeProgram::IntcodeProgram() {
  // ... initialize instance variables
}
// destructor
IntcodeProgram::~IntcodeProgram() {
  // ... free dynamically allocated variables
}
```

This constructor will be called whenever you instantiate a new variable of type ``IntcodeProgram`` (with the ``new`` keyword). The neat thing with object-oriented programming, as I said just before, is that you can gather in the same place various variables or methods that are logically linked together; here, our class can contain other methods that implement the behavior we want one of program instance to have: a basic state check, memory updates, instructions execution...

My final ``IntcodeProgram`` class provided me with an easy-to-use interface for my actual computation functions in the puzzle scripts. In those functions, I just create instances of the ``IntcodeProgram`` class and play around with them, but the class abstracts away all the actual execution or memory management stuff so that these computation functions aren't too long.

This means that the true meat of the code resides in the ``IntcodeProgram`` class.

I've used a static class variable called ``INSTANCE_ID`` to assign auto-incrementing IDs to my instances. Rather than maintaining a counter outside of the class, I can just let it take care of it and automatically generate a new integer ID whenever I create a new instance of my class. However, I need to be careful to reset the counter whenever I want to reset my pool of instances from scratch (for example, in Day 7, whenever I want to try a new permutation of phase settings).

Moreover, since C++ is a typed language, we need to be careful of how we store the data in the ``IntcodeProgram`` instances (be it the actual program, the memory or the output): if we use basic ``int``s, we risk having overflows from Day 9 that forced our interpreter to handle very large numbers. To avoid any issue, we can take the ``long long`` type (that is a shorthand for ``long long int``); this will insure that we don't have overflow problems - even if it increases the size of our code quite a bit...

## Day 1: The Tyranny of the Rocket Equation

#### Answers
**Part I: 3345909 • Part II: 5015983**

This first challenge is pretty straight-forward. The only notable thing is that Part II strongly indicates you should [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) to solve the problem. Given that you have a question of the form "compute a value for something, then compute the value for this new thing, and so on..." you want to create recursive function, i.e. a process where your top solution depends on the solution you computed for smaller instances of the problem.

You therefore call the function from within itself (here ``computeTotalFuel()`` is called inside of ``computeTotalFuel()``).

## Day 2: 1202 Program Alarm

#### Answers
**Part I: 3716293 • Part II: 6429**

> Day 2 relies on the Intcode interpreter that is implemented in the ``intcode.cpp`` file.

To optimize for space, I'm using a usual container of the ``std`` standard C++ library, the ``map``, to store my Intcode program. This way, rather than having a long vector possible filled with zeros, I only retain the keys to the cells that have a value (and all the others are assumed to contain a 0).

## Day 3: Crossed Wires

#### Answers
**Part I: 209 • Part II: 43258**

The challenge with this problem was to handle the large lists as quickly as possible. To do so, I used vectors and maps and tried to make the best out of both worlds (depending on [the time complexity of various operations for each data type](https://users.cs.northwestern.edu/~riesbeck/programming/c++/stl-summary.html)):

- vectors are ordered, meaning that you can access elements by index (and in constant time, or `O(1)`); this lets me to easily refer to the "first" (at index 0) and the "second" (at index 1) wire, to take the smallest distance quickly...

- maps are containers that work with key-value pairs; they are great for quick element get or set (it is in `O(log n)` in both cases which is quite efficient) and they allow me to check if a key is present quickly too

By using the right data type at the right time, you can increase the computation time tremendously. These containers are provided in the built-in C++ standard library ``std``.

## Day 4: Secure Container

#### Answers
**Part I: 1019 • Part II: 660**

Here, I use the map container (from the ``std`` built-in C++ library) once again to store a count of each digit in my number for the ``numberIsOkP2()`` method.

Also, I take advantage of C++'s ability to quickly change from one type to another by treating my number and its digits either as integers or as characters depending on what I need.

## Day 5: Sunny with a Chance of Asteroids

#### Answers
**Part I: 15508323 • Part II: 9006327**

> Day 5 relies on the Intcode interpreter that is implemented in the ``intcode.cpp`` file.

In this puzzle, I did some modifications on the common ``IntcodeProgram`` class to keep on improving its features (namely: I reorganized the ``OPERATIONS`` dictionary to hold more information and I've worked on the ``processOpcode()`` method to automate pointers evolution).

## Day 6: (Passed)

## Day 7: Amplification Circuit

#### Answers
**Part I: 116680 • Part II: 89603079**

> Day 7 relies on the Intcode interpreter that is implemented in the ``intcode.cpp`` file.

For this problem, we need to run several instances of our Intcode program at the same time while making sure each has its own "environment". This lead me to implement the ``runMultiple()`` method in the shared ``IntcodeProgram`` class. It is not truly parallel execution, though, since some instances will depend on the output from others and thus need to wait for them before they can proceed. Hence the need to separate data for each instance, so that they don't overwrite sensible information that the other might use later on.

## Day 8: Space Image Format

#### Answers
**Part I: 2064 • Part II: KAUZA**

Day 8 is a nice easy peasy Sunday problem about image decoding. It is quite simple and does not require any complex lib imports. You just need to be careful in how you represent a 2D image as a 1D string and compute your position transformations properly.

In Part II, the only tricky thing is the order of the layers: you're told that the first one comes first, then the second one, and so on. They can overwrite each other (if the pixel is not transparent), so the easiest way to deal with this is to process them in the reverse order: take a "result image" that you initializing with blanks everywhere; then iterate through your layers from last to first and simply turn on or off pixels if you find the corresponding value.

*Note: since in C++ we care about variable type, I first thought I would optimize the space taken by the image in Part II by storing a 2D array of ``char``s. However, I also want to display my message with Unicode characters, so I can't actually store them into just a ``char``: I need ``std::string``s!*

## Day 9: Sensor Boost

#### Answers
**Part I: 2752191671 • Part II: 87571**

> Day 9 relies on the Intcode interpreter that is implemented in the ``intcode.cpp`` file.

To be honest, while I spent *hours* trying to debug some index shifting errors, the problem is not that hard *per se*: once again, I'm asked to improve the Intcode program I worked on during Days 2, 5 and 7. Compared to the previous Intcode interpreter, we need to add a new mode, called the "relative" mode, that allows for address references with a relative base (that can be modified) and the ``offset_relative_base`` instruction to update this aforementioned relative base.

My big issue was to properly understand what remain indices and what turn into data with the new mode... many thanks to [youaremean_YAM](https://www.reddit.com/user/youaremean_YAM/) for his/her JS solution that finally helped me get it right!

Part I and Part II only differ in the input you pass your processing function: ``1`` for the first, ``2`` for the second. Other than that, you should execute the exact same code.

## Day 10: Monitoring Station

#### Answers
**Part I: 280 • Part II: 706**

*Disclaimer: my first solution for Part I was really ugly... I've drawn inspiration from [kcon1](https://www.reddit.com/user/kcon1/)'s answer on the reddit thread, [over here](https://www.reddit.com/r/adventofcode/comments/e8p9zz/2019_day_10_part_2_python_how_to_approach_part_2/) for Part I. Part II is loosely inspired by his/her suggestion.*

Overall, the solution relies on tools I've already mentioned before (in particular from the ``std`` built-in C++ lib): classes, vectors, maps, sets... One thing to note, however, is that we use the fact that C++ sets are unordered collections of *unique* items: whenever you add an item to the set, if it is already there, then the collection won't actually be updated.

This allows us to "overwrite" the asteroids that all have the same angle to the reference asteroid, in ``findBestAsteroid()``, and therefore to essentially "mask" the ones that are hidden.

I also used ``struct``s and ``typedef``s here to manipulate my data a bit more easily; for example, I store all the relevant information about the asteroid in sight from my current reference position in an ``AsteroidInfo`` instance so that I can remember the relative angle, the relative distance and the position of the other asteroid compared to me. The ``SightsMap`` typedef is just a convenient way of not having to rewrite this whole map of vector every time I want to refer to my asteroid sights map.

## Day 11: Space Police

#### Answers
**Part I: 2093 • Part II: BJRKLJUP**

> Day 11 relies on the Intcode interpreter that is implemented in the ``intcode.cpp`` file.

In this puzzle, we want to stop after we have outputted a certain number of digits with our program. Thus I added a ``pauseEvery`` optional parameter to my ``run()`` method in the shared ``IntcodeProgram`` class to be able to pause the execution after a given number of outputs.

The ``processInputs()`` function simply makes use of the common class to give us the result both for Part I and Part II.

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

In this problem, Part I is a simple re-implementation of the given algorithm. In my utils, I have implemented a rough combinations computing function to be able to prepare all the possible pairs of indices with each of my moons. Then I use the fact that I can access elements in a vector easily to update the velocity and the position.

Part II, on the other hand, is a bit harder. It is clearly not feasible by brute-force. I admit I searched for a little while but didn't find the trick and finally headed up to the dedicated reddit thread. As explained for example in [this post](https://www.reddit.com/r/adventofcode/comments/e9jxh2/help_2019_day_12_part_2_what_am_i_not_seeing/), you need to spot that the 3 axis are actually independent. This means that the repetition period you need to find can be computed by finding the period of each axis and then finding the least common multiple of these 3 numbers.

To do this, I've used maps and the ``hash`` C++ method from the ``std`` library that is a neat way of quickly generating an efficient [hash](https://en.wikipedia.org/wiki/Hash_function) from a string. This allows me to easily get the period of each axis. Then, I implemented some classic ``GCD()`` and ``LCM()`` functions to perform the final computation.

I had to be careful however to choose a [variable type](https://fr.cppreference.com/w/cpp/language/types) that was big enough to hold the potentially large numbers that would I have in my final result. In particular, I've decided to use an ``unsigned`` type since I know that my number of steps can never be a negative number; this allows me to avoid "loosing" space with the negative values.

*Note: for the input parsing part, I used a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) (or Regex): the idea is to define a "pattern" to search for in a string, and then to see if the given string can be matched to this pattern. If so, we are even able to isolate the bit that match the different parts of our pattern and thus directly extract our values.*

## Day 13: Care Package

#### Answers
**Part I: 268 • Part II: 13989**

> Day 13 relies on the Intcode interpreter that is implemented in the ``intcode.cpp`` file.

There is no need to change anything in the actual ``IntcodeProgram`` class this time, it's just about providing the right inputs to the program to solve the problem!

Part I is quite straight-forward: you simply need to run the program and stop every 3 outputs, then parse the 3 digits to get the ``x``, ``y`` and ``id`` value at this stage, and finally use those to update the ``board``.

Part II is not that hard either, you simply need to:

- modify the initial program to "play in free mode", i.e. replace the first digit in the Intcode program by a ``2``
- move the horizontal paddle to catch the ball and not have the game stop immediately - this basically means you need to go right when the ball is on your right and left when it's on your left, which is done by putting the right digit in the ``IntcodeProgram``'s memory
- keep track of the number of remaining blocks
- whenever you output a score, if there are no blocks remaining, the game ends and you can return this last score as the player's final score

## Day 14: Space Stoichiometry

#### Answers
**Part I: 469536 • Part II: 3343477**

*Disclaimer: While I originally had a similar idea to the one presented here, I actually got completely stuck on this problem and could only solve some of the example cases with my initial algorithm! I eventually headed to the reddit thread and found for example [this answer](https://github.com/jcisio/adventofcode2019/blob/master/day14/d14.py) by [jcisio](https://www.reddit.com/user/jcisio/). My solution is simply a reimplementation of his/hers to fit my usual solution format.*

The issue I had with my original solution was that I couldn't process the materials in the proper order; so I had trouble accounting for the required amount of ``ORE``.

The trick to solve this problem is to use some sort of topological sort on the data to be able to consume the reagents "in the correct order". More specifically, here, we simply consider the "distance" each reagent has to the final raw material, ``ORE``.

Then, we can do the sort of loop I had in my initial algorithm but always take the material that is the "farthest" from ``ORE``, and thus use the "more complex" reactions in our list.

Once again, with C++ types, we need to make sure we have large enough types to hold the big amount of ``FUEL`` or ``ORE`` we will hold for big reactions. We can also take advantage of the fact that maps are automatically initialized to simply increment the value at a given key, without checking first if the already exists (by default, the value is 0).

## Day 15: Oxygen System

#### Answers
**Part I: 240 • Part II: 322**

> Day 15 relies on the Intcode interpreter that is implemented in the ``intcode.cpp`` file.

Day 15 is about maze exploration and traversal, hence I needed to reimplement some common graph-related algorithms. Namely, I've worked on flow algorithms, pathfinding algorithms and general recursive search (with a BFS-approach, here).

*Note: a detailed article about this challenge is available on my blog [over here](http://minapecheux.com/wp/exploring-and-traversing-a-maze/).*

Since we don't know what the room looks like, we first need to explore it to map out the tiles types at each coordinate ("wall", "empty" or "oxygen system"). To do this, we can proceed recursively by moving the robot through the entire board and storing its feedback for each tile; this allows us to get a match between an (x, y) coordinate and a tile type.

Then, we can use Dijkstra's algorithm to compute the shortest path between the initial position of the robot and the oxygen system.

Part II asks us to determine how long it takes (how many iterations it requires) to fill the entire maze with oxygen, starting from the oxygen system and then propagating oxygen to the neighbor tiles at each iteration. This can be solved both with a DFS- or BFS-approach; I originally coded up a DFS-based algorithm and eventually changed it to a BFS-approach to be able to do a visualization.

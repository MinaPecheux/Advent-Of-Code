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

## Day 1: The Tyranny of the Rocket Equation

#### Answers
**Part I: 3345909 • Part II: 5015983**

This first challenge is pretty straight-forward. The only notable thing is that Part II strongly indicates you should [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) to solve the problem. Given that you have a question of the form "compute a value for something, then compute the value for this new thing, and so on..." you want to create recursive function, i.e. a process where your top solution depends on the solution you computed for smaller instances of the problem.

You therefore call the function from within itself (here ``computeTotalFuel()`` is called inside of ``computeTotalFuel()``).

## Day 2: 1202 Program Alarm

#### Answers
**Part I: 3716293 • Part II: 6429**

> Day 2 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

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

> Day 5 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

In this puzzle, I did some modifications on the common ``IntcodeProgram`` class to keep on improving its features (namely: I reorganized the ``OPERATIONS`` dictionary to hold more information and I've worked on the ``processOpcode()`` method to automate pointers evolution).

## Day 6: (Passed)

## Day 7: Amplification Circuit

#### Answers
**Part I: 116680 • Part II: 89603079**

> Day 7 relies on the Intcode interpreter that is implemented in the ``intcode.py`` file.

For this problem, we need to run several instances of our Intcode program at the same time while making sure each has its own "environment". This lead me to implement the ``runMultiple()`` method in the shared ``IntcodeProgram`` class. It is not truly parallel execution, though, since some instances will depend on the output from others and thus need to wait for them before they can proceed. Hence the need to separate data for each instance, so that they don't overwrite sensible information that the other might use later on.

## Day 8: Space Image Format

#### Answers
**Part I: 2064 • Part II: KAUZA**

Day 8 is a nice easy peasy Sunday problem about image decoding. It is quite simple and does not require any complex lib imports. You just need to be careful in how you represent a 2D image as a 1D string and compute your position transformations properly.

In Part II, the only tricky thing is the order of the layers: you're told that the first one comes first, then the second one, and so on. They can overwrite each other (if the pixel is not transparent), so the easiest way to deal with this is to process them in the reverse order: take a "result image" that you initializing with blanks everywhere; then iterate through your layers from last to first and simply turn on or off pixels if you find the corresponding value.

*Note: since in C++ we care about variable type, I first thought I would optimize the space taken by the image in Part II by storing a 2D array of ``char``s. However, I also want to display my message with Unicode characters, so I can't actually store them into just a ``char``: I need ``std::string``s!*

# [2019] Javascript (Node JS)

This subfolder contains my code solutions for challenges from the 2019 series, written in Javascript (Node JS).

## Node packages

These scripts use several external Node packages:

- ``lodash``: a module with lots of utils to manipulate Arrays, Objects, Collections...
- ``chai``: a package to do some asserts and make some check tests
- ``fs``: a basic package for file content reading

The repo contains a ``package-lock.json`` file that lists the packages (and their version) used by these scripts, so hopefully, once the folder has been copied, they can be installed with a simple:

```
npm install
```

To run the scripts in the repo, use NodeJS in the following way:

```
node day1.js
```

## Preliminary note: files organization
In these files, I try to always organize the code in the same way:

1. first, some imports if need be (Node packages)

2. then, parsing functions to read and extract data from the provided input (that seems to always be a string of characters)

3. then, the actual computation functions, separated in 3 bits:
  - util and common functions
  - functions for the Part I of the problem
  - functions for the Part II of the problem
  
4. a test function with a set of ``chai`` tests to check that my computation functions seem to give an ok result (using the examples provided with the problem)

5. finally, the main part (inside of an [Immediately-Invoked Function Expression](https://developer.mozilla.org/en-US/docs/Glossary/IIFE)) that solves the problem by running the computation functions on the actual inputs I was given (that depend on the user)

## Day 1: The Tyranny of the Rocket Equation

#### Answers
**Part I: 3345909 • Part II: 5015983**

This first challenge is pretty straight-forward. The only notable thing is that Part II strongly indicates you should [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) to solve the problem. Given that you have a question of the form "compute a value for something, then compute the value for this new thing, and so on..." you want to create recursive function, i.e. a process where your top solution depends on the solution you computed for smaller instances of the problem.

You therefore call the function from within itself (here ``computeTotalFuel()`` is called inside of ``computeTotalFuel()``).

## Day 2: 1202 Program Alarm

#### Answers
**Part I: 3716293 • Part II: 6429**

This problem is an opportunity to talk about **mutability** in Javascript: in this solution, I extensively use the fact that ``Array``s are mutable in Javascript. This means that even if they are passed as parameters to functions, the variables still point to the same address in memory and can therefore be modified directly.

On the other hand, [primitive values](https://developer.mozilla.org/en-US/docs/Glossary/primitive) (``string``, ``number``, ``bigint``, ``boolean``, ``null``, ``undefined``, and ``symbol``) cannot be modified after being created. If you want to change the value, you need to reassign the variable to a brand new value in memory.

For example, in the ``processInputs()`` function, I directly touch the ``inputs`` Array that is passed as a parameter as I execute the Intcode program.

Hence the need to "copy" the inputs before running them through any processing code!

> For more info on immutability in Javascript, you can check out [Mozilla's reference](https://developer.mozilla.org/en-US/docs/Glossary/Mutable) on the word "Mutable" (Aug. 2019).

## Day 3: Crossed Wires

#### Answers
**Part I: 209 • Part II: 43258**

The challenge with this problem was to handle the large lists as quickly as possible. To do so, I used arrays and objects and tried to make the best out both worlds (depending on [the time complexity of various operations for each data type](https://wiki.python.org/moin/TimeComplexity)):

- arrays are ordered, meaning that you can access elements by index, and using the ``lodash`` module I have ``min`` or ``max`` operations; this lets me to easily refer to the "first" (at index 0) and the "second" (at index 1) wire, to take the smallest distance...

- dictionaries are hashable containers that work with key-value pairs; they are great for quick element access (it is in `O(1)`, i.e. in constant time)

By using the right data type at the right time, you can increase the computation time tremendously.

*Note: because I have the ``lodash`` package, some operations become really easy to do with objects. With pure Javascript, it is sometimes easier to use collection type such as the ``Map`` or the ``Set``... (see the [Mozilla doc](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects) on variable types).*

I also use [template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals) (aka template strings) to automatically build the keys of my dictionary: the `` `myVar = ${myVar}` `` syntax is a way of integrating the value of ``myVar`` directly into a string. It is very useful for debugs but also to create keys like these ones, where we want to concatenate the horizontal and vertical coordinates of the point.

## Day 4: Secure Container

#### Answers
**Part I: 1019 • Part II: 660**

There is not much to say with this solution, except that I use a ``lodash`` operation, ``countBy``. It is very quick at creating an object that associates each unique value in a list or a string to the number of times it appears (see the function ``numberIsOkP2()``).

Also, I take advantage of Javascript's ability to quickly change from one type to another by treating my number and its digits either as integers or as characters depending on what I need.

## Day 5: Sunny with a Chance of Asteroids

#### Answers
**Part I: 15508323 • Part II: 9006327**

This challenge builds on Day 2. The code therefore is an extension of my solution for Day 2.

In this version, I have made 2 major modifications:

1. I have reorganized the ``OPERATIONS`` dictionary to hold more information, namely the number of inputs for each operation (plus I've added the new operations defined in the problem)
2. I have improved the ``processOpcode()`` function to treat the program with the new important features:
  - instructions can have a variable number of parameters, which is why I have modified the ``OPERATIONS`` dictionary to automatically extract it
  - instructions have an execution mode (either in "address" or "immediate value" mode)
  
  Here, I have basically automated the impact of the number of inputs on the instruction pointer, I've coded up the new operations and I've dealt with the mode.
  
In my ``processOpcode()`` function, for the input instruction (with code ``3``), I use a global ``INPUT`` variable that is consumed by the program during the execution whenever it calls this operation. For the output instruction (with code ``4``), I use of a global ``OUTPUTS`` array where I can store the digits that the program outputs gradually.

Then, at the very end of the execution of my program, I can simply query the last element of this array, which allows for simply assertions and tests.

*Note: something quite important is that because we now have the mode to deal with, we should keep the program inputs as string so that we can extract all the relevant information from it. Consequently, we need to be careful whenever we set a value in our program to convert it back to a string... (see the ``processOpcode()`` method).*

## Day 6: (Passed)

## Day 7: Amplification Circuit

#### Answers
**Part I: 116680 • Part II: 89603079**

This problem continues building on the Intcode program that was first written on Day 2 and then improved on on Day 5. This time, we are going to need to run several instances of our Intcode program at the same time while making sure each has its own "environment". It is not truly parallel execution, though, since some instances will depend on the output from others and thus need to wait for them before they can proceed. Hence the need to separate data for each instance, so that they don't overwrite sensible information that the other might use later on.

To better separate and manage the different program instances, I've decided to use one feature of Javascript: classes! *(Note: [JS classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) aren't "true" classes, there are actually syntactic sugar over JS's existing prototype-based inheritance.)* Those fall in the object-oriented programming philosophy and are, to me, a nice way of aggregating together bits of code that have a logical link. So, I've coded up a ``ProgramInstance`` class that represents an instance of our Intcode program with its own copy of the program to execute (that will be modified in-place as it runs), its own instruction pointer, its own memory and its own running state.

To create a basic class, you should define a ``class`` that has at least an ``constructor()`` method:

```javascript
class ProgramInstance {
    constructor() {
      
    }
}
```

This ``constructor()`` function will be called whenever you instantiate a new variable of type ``ProgramInstance``. The neat thing with object-oriented programming, as I said just before, is that you can gather in the same place various variables or methods that are logically linked together; here, our class can contain other methods that implement the behavior we want one of program instance to have: a basic state check, memory updates, instructions execution...

My final ``ProgramInstance`` class provided me with an easy-to-use interface for my actual computation functions (``processInputs()`` and ``processInputsFeedback()``). In those functions, I just create instances of the ``ProgramInstance`` class and play around with them, but the class abstracts away all the actual execution or memory management stuff so that these computation functions aren't too long.

This means that the true meat of the code resides in the ``ProgramInstance`` class.

One thing to note is that for the "read" and "write" operations, we don't use global variables anymore but instead variables stored in the ``ProgramInstance``. The ``processOpcode()`` now returns a boolean representing whether or not the ``ProgramInstance`` we were executed should pause and wait for other processes to complete before resuming.

Finally, I've used a global variable called ``INSTANCE_ID`` to assign auto-incrementing IDs to my instances. Rather than passing the ID each time, I can just let the ``ProgramInstance`` class take care of it and automatically generate a new integer ID whenever I create a new instance of my class. However, I need to be careful to reset the counter whenever I want to reset my pool of instances from scratch (in our example, whenever I want to try a new permutation of phase settings).

## Day 8: Space Image Format

#### Answers
**Part I: 2064 • Part II: KAUZA**

Day 8 is a nice easy peasy Sunday problem about image decoding. It is quite simple; you just need to be careful in how you represent a 2D image as a 1D string and compute your position transformations properly.

In Part II, the only tricky thing is the order of the layers: you're told that the first one comes first, then the second one, and so on. They can overwrite each other (if the pixel is not transparent), so the easiest way to deal with this is to process them in the reverse order: take a "result image" that you initializing with blanks everywhere; then iterate through your layers from last to first and simply turn on or off pixels if you find the corresponding value.

## Day 9: Sensor Boost

#### Answers
**Part I: 2752191671 • Part II: 87571**

To be honest, while I spent *hours* trying to debug some index shifting errors, the problem is not that hard *per se*: once again, I'm asked to improve the Intcode program I worked on during Days 2, 5 and 7.

My big issue was to properly understand what remain indices and what turn into data with the new mode... many thanks to [youaremean_YAM](https://www.reddit.com/user/youaremean_YAM/) for his/her JS solution that finally helped me get it right!

Part I and Part II only differ in the input you pass your processing function: ``1`` for the first, ``2`` for the second. Other than that, you should execute the exact same code.

Compared to the previous Intcode interpreter, we need to add a new mode, called the "relative" mode, that allows for address references with a relative base (that can be modified) and the ``offset_relative_base`` to update this aforementioned relative base. I've also added a debug mode to show the instructions execution process step by step and I've cleaned up the code to better use the ``ProgramInstance``'s own variables.

*Note: I've also added a "debug" mode to the ``ProgramInstance`` class to allow for a step-by-step logging of the instructions execution.*

## Day 10: Monitoring Station

#### Answers
**Part I: 280 • Part II: 706**

*Disclaimer: my first solution for Part I was really ugly... I've drawn inspiration from [kcon1](https://www.reddit.com/user/kcon1/)'s answer on the reddit thread, [over here](https://www.reddit.com/r/adventofcode/comments/e8p9zz/2019_day_10_part_2_python_how_to_approach_part_2/) for Part I. Part II is loosely inspired by his/her suggestion.*

Overall, the solution relies on tools I've already mentioned before: classes, ``object``s, ``Set``s, ``array``s... One thing to note, however, is that we use the fact that JS ``Set``s are unordered collections of *unique* items: whenever you add an item to the set, if it is already there, then the collection won't actually be updated.

This allows us to "overwrite" the asteroids that all have the same angle to the reference asteroid, in ``computeAsteroidSights()``, and therefore to essentially "mask" the ones that are hidden.

## Day 11: Space Police

#### Answers
**Part I: 2093 • Part II: BJRKLJUP**

Once again, I needed to reuse the Intcode interpreter developed on Days 2, 5, 7 and 9. There are only really tiny changes to the ``ProgramInstance`` class this time, so that I can run my program and ask it to pause after a given number of outputs (see the ``run()`` method with its new parameter, ``pauseEvery``).

Then, the ``processInputs()`` function simply makes use of this class to give us the result both for Part I and Part II.

The basic idea of this method is to:
- create an instance of our ``ProgramInstance`` class to execute the given inputs as an Intcode program
- have it run with a pause every 2 outputs
- whenever it pauses, parse the last two outputted digits to get the new color of the panel, the new rotation of the robot and move it on the board

There are some auxiliary variables to store what we need for the result: the current direction and coordinates of the robot, the set of panels that are currently painted white and therefore form a message (``board``) and finally the set of panels that have been painted at least once by the robot, even if they have been repainted black since the beginning (``painted``).

In Part I, we want to know how many panels the robot will paint. So we simply need to get the size of the ``painted`` set.

In Part II, we want to actually output the message. This time, I'm using the ``board`` set that only stores the panels that are currently painted white. At the end, I simply need to iterate through this set of positions to display the message.

*Note: a small hint about the ``x`` and ``y`` coordinate changes depending on the direction - while you might think that going "up" means increasing the ``y`` coordinate, it is better to decrease it so that the message prints correctly at the end of Part II. Otherwise, you will get a message reversed on the horizontal axis and you will have to iterate your ``y`` range in reverse order...*

## Day 12: The N-Body Problem

#### Answers
**Part I: 12082 • Part II: 295693702908636**

In this problem, Part I is a simple re-implementation of the given algorithm; once again, I use a common implementation of a function that creates all pair combinations from an array and the fact that ``array``s and ``object``s are mutable.

Part II, on the other hand, is a bit harder. It is clearly not feasible by brute-force. I admit I searched for a little while but didn't find the trick and finally headed up to the dedicated reddit thread. As explained for example in [this post](https://www.reddit.com/r/adventofcode/comments/e9jxh2/help_2019_day_12_part_2_what_am_i_not_seeing/), you need to spot that the 3 axis are actually independent. This means that the repetition period you need to find can be computed by finding the period of each axis and then finding the least common multiple of these 3 numbers.

To do this, I've used ``object``s that allow me to easily get the period of each axis. Then, I implemented some classic ``GCD()`` and ``LCM()`` functions to perform the final computation.

*Note: for the input parsing part, I used a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) (or Regex): the idea is to define a "pattern" to search for in a string, and then to see if the given string can be matched to this pattern. If so, we are even able to isolate the bit that match the different parts of our pattern and thus directly extract our values.*

## Day 13: Care Package

#### Answers
**Part I: 268 • Part II: 13989**

Day 13 reuses once again the Intcode interpreter that was developed previously. No need to change anything in the actual ``ProgramInstance`` class this time, it's just about providing the right inputs to the program to solve the problem!

Part I is quite straight-forward: you simply need to run the program and stop every 3 outputs, then parse the 3 digits to get the ``x``, ``y`` and ``id`` value at this stage, and finally use those to update the ``board``.

Part II is not that hard either, you simply need to:

- modify the initial program to "play in free mode", i.e. replace the first digit in the Intcode program by a ``2``
- move the horizontal paddle to catch the ball and not have the game stop immediately - this basically means you need to go right when the ball is on your right and left when it's on your left, which is done by putting the right digit in the ``ProgramInstance``'s memory
- keep track of the number of remaining blocks
- whenever you output a score, if there are no blocks remaining, the game ends and you can return this last score as the player's final score

In the ``computeScore()`` method, I've used the ``process.stdout.write()`` function to be able to overwrite a line in the shell and therefore show a *decreasing progress bar* to track the number of remaining blocks in the board.

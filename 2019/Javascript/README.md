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

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

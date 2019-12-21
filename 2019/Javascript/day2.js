/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 2: 1202 Program Alarm
 * ================================================
 */
'use strict'

const _ = require('lodash')
const fs = require('fs')
const expect = require('chai').expect
const { IntcodeProgram } = require('./utils/intcode')

// [ Input parsing functions ]
// ---------------------------
/**
 * Parses the incoming data into processable inputs.
 * @param {string} data - Provided problem data.
 * @returns {array(int)} - Parsed data.
 */
const parseInput = (data) => {
  return _.map(_.filter(_.split(data, ','), (l) => l.length > 0), Number)
}

// [ Computation functions ]
// -------------------------
/* PART I */
/**
 * Executes the Intcode program on the provided inputs and computes the final
   result.
 * @param {array(int)} inputs - List of integers to execute as an Intcode
 *                              program.
 * @param {bool} restoreGravityAssist - Whether or not to restore the gravity
 *                                      assist by modifying the input program.
 * @returns {int} - Final output of the program.
 */
const processInputs = (inputs, restoreGravityAssist=false) => {
  // restore gravity assist?
  if (restoreGravityAssist) {
    inputs[1] = 12
    inputs[2] = 2
  }
  // create and execute program
  const program = new IntcodeProgram(inputs)
  program.run()
  // isolate final result
  return program.program[0]
}

/* PART II */
/** A brute-force algorithm to systematically try all possible input pairs
 * until we find the one that gave the desired output (we can determine a
 * finished set of possible candidates since we know that each number is in the
 * [0, 99] range).
 * @param {array(int)} inputs - List of integers to execute as an Intcode
 *                              program.
 * @param {int} wantedOutput - Desired output of the program.
 * @returns {int} - Specific checksum that matches the desired output.
 */
const findPair = (inputs, wantedOutput) => {
  // prepare program
  const program = new IntcodeProgram(inputs)
  let result, breakLoop
  _.each(_.range(100), (noun) => { // range is [0, 100[ = [0, 99]
    breakLoop = false
    _.each(_.range(100), (verb) => {
      // reset program to initial state
      program.reset()
      // set up noun and verb
      program.program[1] = noun
      program.program[2] = verb
      // run and compare result
      program.run()
      if (program.program[0] == wantedOutput) {
        result = 100 * noun + verb
        breakLoop = true
        return false
      }
    })
    if (breakLoop) return false
  })
  return result
}
    
// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  /* Part I */
  expect(processInputs([ 1,9,10,3,2,3,11,0,99,30,40,50 ])).to.equal(3500)
  expect(processInputs([ 1,0,0,0,99 ])).to.equal(2)
  expect(processInputs([ 2,3,0,3,99 ])).to.equal(2)
  expect(processInputs([ 2,4,4,5,99,0 ])).to.equal(2)
  expect(processInputs([ 1,1,1,4,99,5,6,0,99 ])).to.equal(30)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day2.txt')
  
  // Part I
  const solution1 = processInputs(parseInput(data), true)
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  const solution2 = findPair(parseInput(data), 19690720)
  console.log(`PART II: solution = ${solution2}`)
})()

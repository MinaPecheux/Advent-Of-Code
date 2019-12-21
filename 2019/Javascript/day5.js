/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 5: Sunny with a Chance of Asteroids
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
/* PART I + II */
/**
 * Executes the Intcode program on the provided inputs and computes the final
   result.
 * @param {array(string)} inputs - List of strings to execute as an Intcode
 *                                 program (can be parsed as integers).
 * @param {int} input - Specific input to insert in the program's memory to
 *                      begin with.
 * @returns {int} - Final output of the program.
 */
const processInputs = (inputs, input) => {
  // create program
  const program = new IntcodeProgram(inputs)
  // insert input in memory
  program.pushMemory(input)
  // execute program
  program.run()
  // return last output
  return _.last(program.output)
}
    
// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  /* Part I */
  expect(processInputs(parseInput('3,0,4,0,99'), 1)).to.equal(1)
  
  /* Part II */
  expect(processInputs(parseInput('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'), 0)).to.equal(0)
  expect(processInputs(parseInput('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'), 1)).to.equal(1)
  expect(processInputs(parseInput('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
    + '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,'
    + '1101,1000,1,20,4,20,1105,1,46,98,99'), 1)).to.equal(999)
  expect(processInputs(parseInput('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
    + '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,'
    + '1101,1000,1,20,4,20,1105,1,46,98,99'), 8)).to.equal(1000)
  expect(processInputs(parseInput('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
    + '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,'
    + '1101,1000,1,20,4,20,1105,1,46,98,99'), 12)).to.equal(1001)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day5.txt')
  
  // Part I
  const solution1 = processInputs(parseInput(data), 1)
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  const solution2 = processInputs(parseInput(data), 5)
  console.log(`PART II: solution = ${solution2}`)
})()

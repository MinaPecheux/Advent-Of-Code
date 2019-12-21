/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 9: Sensor Boost
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
 * @param {array(int)} inputs - List of integers to execute as an Intcode program.
 * @param {int} input - Integer to provide as input to the program.
 * @param {bool} debug - Whether or not the IntcodeProgram should debug its
 *                       execution at each instruction processing.
 * @returns {int} - Last output of the program.
 */
const processInputs = (inputs, input=null, debug=false) => {
  const program = new IntcodeProgram(inputs, debug)
  if (input !== null) {
    program.pushMemory(input)
  }
  program.run()
  return _.last(program.output)
}

// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  // test new instructions
  const ref = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
  const program = new IntcodeProgram([
    109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
  ])
  program.run()
  expect(_.join(program.output, ',')).to.equal(ref)
  
  /* Part I + II */
  const r = processInputs([ 1102,34915192,34915192,7,4,7,99,0 ])
  expect(r.toString().length).to.equal(16)
  expect(processInputs([ 104,1125899906842624,99 ])).to.equal(1125899906842624)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day9.txt')
  const inputs = parseInput(data)
  
  // Part I
  const solution1 = processInputs(inputs, 1)
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  const solution2 = processInputs(inputs, 2)
  console.log(`PART II: solution = ${solution2}`)
})()

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
let INPUT = null // specific value for the input instruction
let OUTPUTS = [] // outputs of the program
const OPERATIONS = {
  1: { op: (a, b) => a + b, n: 3 },
  2: { op: (a, b) => a * b, n: 3 },
  3: { op: () => INPUT, n: 1 },
  4: { op: null, n: 1 },
  5: { op: null, n: 2 },
  6: { op: null, n: 2 },
  7: { op: (a, b) => a < b, n: 3 },
  8: { op: (a, b) => a === b, n: 3 },
  99: { op: null, n: null }
}

/**
 * Gets the "address" or "immediate value" for a given set of inputs and
   data.
 * @param {array(int)} inputs - List of integers to execute as an Intcode program.
 * @param {int} data - Data to execute.
 * @param {int} mode - Execution mode (either 0, "address mode"; or 1, "immediate
 *                     value mode").
 * @returns {int} - Data value.
 */
const getValue = (inputs, data, mode) => {
  return (mode === 0) ? inputs[data] : data
}

/**
 * Processes an opcode by using the provided inputs and the current operation
   index.
 * @param {array(int)} inputs - List of integers to execute as an Intcode program.
 * @param {int} instructionPtr - Current instruction pointer.
 * @returns {int} - Updated instruction pointer.
 */
const processOpcode = (inputs, instructionPtr) => {
  const instruction = inputs[instructionPtr].toString()
  const code = parseInt(instruction.substring(instruction.length - 2))
  
  if (!_.has(OPERATIONS, code)) {
    return -1
  }
  const { op, n } = OPERATIONS[code]
  const modes = instruction.substring(0, instruction.length - 2)
  const opModes = _.concat(
    _.map(modes.split('').reverse().join(''), (m) => Number(m)),
    new Array(n - modes.length).fill(0)
  )
  
  let a, b, c, v
  const tmp = _.map(_.slice(inputs, instructionPtr+1, instructionPtr+n+1), Number)
  switch (code) {
    case 99:
      return null
    case 1: // add
    case 2: // multiply
      a = tmp[0]; b = tmp[1]; c = tmp[2]
      inputs[c] = op(
        getValue(inputs, a, opModes[0]), getValue(inputs, b, opModes[1])
      )
      return instructionPtr + n + 1
    case 3: // read
      a = inputs[instructionPtr+1]
      inputs[a] = op()
      return instructionPtr + n + 1
    case 4: // print
      a = inputs[instructionPtr+1]
      v = getValue(inputs, a, opModes[0])
      OUTPUTS.push(v)
      return instructionPtr + n + 1
    case 5: // jump if true
      a = tmp[0]; b = tmp[1]
      if (getValue(inputs, a, opModes[0]) !== 0) {
        return getValue(inputs, b, opModes[1])
      }
      return instructionPtr + n + 1
    case 6: // jump if false
      a = tmp[0]; b = tmp[1]
      if (getValue(inputs, a, opModes[0]) === 0) {
        return getValue(inputs, b, opModes[1])
      }
      return instructionPtr + n + 1
    case 7: // set if less than
    case 8: // set if equal
      a = tmp[0]; b = tmp[1]; c = tmp[2]
      inputs[c] = (op(
        getValue(inputs, a, opModes[0]), getValue(inputs, b, opModes[1])
      )) ? 1 : 0
      return instructionPtr + n + 1
    default:
      return -1
  }
}

/* PART I + II */
/**
 * Executes the Intcode program on the provided inputs and computes the final
   result.
 * @param {array(string)} inputs - List of strings to execute as an Intcode
 *                                 program (can be parsed as integers).
 * @returns {int} - Final output of the program.
 */
const processInputs = (inputs) => {
  // resets the output
  OUTPUTS = []
  // execute program (modifies the inputs in-place)
  let instructionPtr = 0
  while (!_.isNil(instructionPtr)) {
    instructionPtr = processOpcode(inputs, instructionPtr)
    if (instructionPtr === -1) {
      return null
    }
  }
  return _.last(OUTPUTS)
}
    
// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  /* Part I */
  INPUT = 1
  expect(processInputs(parseInput('3,0,4,0,99'))).to.equal(1)
  
  /* Part II */
  INPUT = 0
  expect(processInputs(parseInput('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'))).to.equal(0)
  INPUT = 1
  expect(processInputs(parseInput('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'))).to.equal(1)
  INPUT = 1
  expect(processInputs(parseInput('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
    + '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,'
    + '1101,1000,1,20,4,20,1105,1,46,98,99'))).to.equal(999)
  INPUT = 8
  expect(processInputs(parseInput('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
    + '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,'
    + '1101,1000,1,20,4,20,1105,1,46,98,99'))).to.equal(1000)
  INPUT = 12
  expect(processInputs(parseInput('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
    + '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,'
    + '1101,1000,1,20,4,20,1105,1,46,98,99'))).to.equal(1001)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day5.txt')
  
  // Part I
  INPUT = 1
  const solution1 = processInputs(parseInput(data))
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  INPUT = 5
  const solution2 = processInputs(parseInput(data))
  console.log(`PART II: solution = ${solution2}`)
})()

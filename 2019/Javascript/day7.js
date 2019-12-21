/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 7: Amplification Circuit
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
/**
 * Computes all the possible permutations of the input array.
 * @param {array(int)} input - Array to permute.
 * @returns {array(array(int))} - Possible permutations of the array.
 */
const permutator = (input) => {
  const result = []
  const permute = (arr, m = []) => {
    if (arr.length === 0) {
      result.push(m)
    } else {
      for (let i = 0; i < arr.length; i++) {
        let curr = arr.slice()
        let next = curr.splice(i, 1)
        permute(curr.slice(), m.concat(next))
      }
    }
  }
  permute(input)
  return result
}

/* PART I */
/**
 * Executes the Intcode program on the provided inputs and computes the final
   result. Here, we use the [0, 4] phase settings range and no feedback loop
   (so we only go through the amplifiers chain once).
 * @param {array(int)} inputs - List of integers to execute as an Intcode program.
 * @returns {int} - Maximum input to the thrusters.
 */
const processInputs = (inputs) => {
  // prepare all possible permutations for phase settings:
  // we have X possibilities for the first one, X-1 for the second one,
  // X-2 for the third one... (no replacement)
  const nAmplifiers = 5
  const candidatePhaseSettings = permutator(_.range(nAmplifiers))
  let output, maxThrust = -1

  IntcodeProgram.resetID() // reset global instances IDs
  // create pool of instances
  const amplifiers = _.map(_.range(5), (a) => {
    return new IntcodeProgram(inputs)
  })
  let curAmplifier, phase
  _.each(candidatePhaseSettings, (phaseSettings, idx) => {
    // reset all amplifiers
    _.each(amplifiers, (amp) => { amp.reset() })
    // prepare input for first amplifier
    amplifiers[0].pushMemory(0)
    for (curAmplifier = 0; curAmplifier < nAmplifiers; curAmplifier++) {
      phase = phaseSettings[curAmplifier]
      amplifiers[curAmplifier].checkRunning(phase)
      // execute program
      amplifiers[curAmplifier].runMultiple(amplifiers)
    }
    // check the power sent to the thrusters with these settings
    output = _.last(amplifiers[curAmplifier - 1].output)
    if (output > maxThrust) {
      maxThrust = output
    }
  })
  return maxThrust
}

/* PART II */
/**
 * Executes the Intcode program on the provided inputs and computes the final
   result. Here, we use the [5, 9] phase settings range and a feedback loop to
   pass through the amplifiers multiple times.
 * @param {array(int)} inputs - List of integers to execute as an Intcode program.
 * @returns {int} - Maximum input to the thrusters.
 */
const processInputsFeedback = (inputs) => {
  // prepare all possible permutations for phase settings:
  // we have X possibilities for the first one, X-1 for the second one,
  // X-2 for the third one... (no replacement)
  const nAmplifiers = 5
  const candidatePhaseSettings = permutator(_.range(5, 10))
  const thrusts = []

  IntcodeProgram.resetID() // reset global instances IDs
  // create pool of instances
  const amplifiers = _.map(_.range(nAmplifiers), (a) => {
    return new IntcodeProgram(inputs)
  })
  let curAmplifier, nextAmplifier, running, phase
  _.each(candidatePhaseSettings, (phaseSettings) => {
    // reset all amplifiers
    _.each(amplifiers, (amp) => { amp.reset() })
    // prepare input for first amplifier
    amplifiers[0].pushMemory(0)
    curAmplifier = 0
    running = true
    while (running) {
      // if necessary, initialize amplifier
      phase = phaseSettings[curAmplifier]
      amplifiers[curAmplifier].checkRunning(phase)
      // run amplifier (either from scratch or from where it last stopped)
      nextAmplifier = amplifiers[curAmplifier].runMultiple(amplifiers)
      // . if we errored somewhere
      if (nextAmplifier === null) {
        return null
      }
      // . else if amplifiers loop has halted
      else if (nextAmplifier === -1) {
        running = false
      }
      // . else reassign the current amplifier index for next iteration
      else {
        curAmplifier = nextAmplifier
      }
    }
    // remember the power sent to the thrusters with these settings
    thrusts.push(_.last(_.last(amplifiers).output))
  })
  return _.max(thrusts)
}
    
// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  /* Part I */
  expect(processInputs(
    parseInput('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
  )).to.equal(43210)
  
  /* Part II */
  expect(processInputsFeedback(
    parseInput('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,'
      + '28,-1,28,1005,28,6,99,0,0,5')
  )).to.equal(139629729)
  expect(processInputsFeedback(
    parseInput('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,'
      + '1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,'
      + '55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10')
  )).to.equal(18216)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day7.txt')
  
  // Part I
  const solution1 = processInputs(parseInput(data))
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  const solution2 = processInputsFeedback(parseInput(data))
  console.log(`PART II: solution = ${solution2}`)
})()

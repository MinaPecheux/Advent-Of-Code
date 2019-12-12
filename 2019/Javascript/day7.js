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
let INSTANCE_ID = 0 // class variable that is common to all instances
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
 * Util class to represent a program instance with its own instructions,
   memory, run state and instruction pointer. Allows for multiple instances
   in parallel to interact without overwriting data.
 * @class
 */
class ProgramInstance {
  
  /**
   * @constructs ProgramInstance
   * @param {array(string)} program - Original Intcode program to execute (will
   *                                  be copied to avoid in-place modification).
   */
  constructor(program) {
    this.id = INSTANCE_ID++
    this.program = _.reduce(program, (acc, inst, idx) => {
      return { ...acc, [idx]: inst }
    }, {})
    this.memory = []
    this.output = []
    this.modes = []
    this.instructionPtr = 0
    this.isRunning = false
    
    this._initialProgram = _.cloneDeep(this.program)
  }
  
  /**
   * Resets the program instance in case you want to re-run the same program
     with a fresh start.
   */
  reset() {
    this.instructionPtr = 0
    this.output = []
    this.memory = []
    this.isRunning = false
    this.program = _.cloneDeep(this._initialProgram)
  }
  
  /**
   * Inserts a value in the instance's memory, in first position.
   * @param {int} data - Value to insert.
   */
  memoryInsert(data) {
    this.memory.unshift(data)
  }
  
  /**
   * Checks if the instance is already running or if it should be initialized
     with its phase setting.
   * @param {int} phase - Phase setting for this instance.
   */
  checkRunning(phase) {
    if (!this.isRunning) {
      this.memoryInsert(phase)
      this.isRunning = true
    }
  }
  
  /**
   * Gets a value in the instance's program at a given position (if the position
     is out of range, returns 0).
   * @param {int} index - Position to get.
   * @returns {int} - Program data value.
   */
  programGetData(index) {
    return _.get(this.program, index, 0)
  }
  
  /**
   * Sets a value in the instance's program at a given position.
   * @param {int} index - Position to get.
   * @param {int} data - Value to insert.
   */
  programSetData (index, data) {
    this.program[index] = data
  }
  
  /**
   * Runs the instance by executing its Intcode program from start to finish
     (until it halts).
   */
  run() {
    while (this.instructionPtr !== null) {
      this.processOpcode()
      if (this.instructionPtr === -1) {
        return null
      }
    }
  }
  
  /**
   * Runs the instance by executing its Intcode program either from scratch or
     from where it last stopped, as part of a pool of instances that feed each
     other with output to input connection.
   * @param {array(ProgramInstance)} instances - List of all program instances
   *                                             in the pool.
   * @returns {int} - Index of the next instance in the pool to run, if any.
   */
  runMultiple(instances) {
    // if we stopped just before halting, we simply terminate the program
    // and go to the next instance
    let nextInstance
    if (!_.isEmpty(this.output) && this.instructionPtr === null) {
      nextInstance = (this.id + 1) % instances.length
      instances[nextInstance].memoryInsert(_.last(this.output))
      return nextInstance
    }
    // else we continue running the program from where we stopped
    let pause
    while (this.instructionPtr !== null) {
      pause = this.processOpcode()
      // if we reached the halt op for the last instance
      if (this.instructionPtr === null && this.id === instances.length - 1) {
        return -1
      }
      // else if we need to temporary pause the execution of this instance
      if (pause || this.instructionPtr === null) {
        nextInstance = (this.id + 1) % instances.length
        instances[nextInstance].memoryInsert(_.last(this.output))
        return nextInstance
      }
      // else if we errored
      if (this.instructionPtr === -1) {
        return null
      }
    }
  }
  
  /**
   * Gets the index corresponding to the cell pointed by the current instruction
     pointer plus the current input (in "address" or "immediate value").
   * @returns {object(int, int)} - Index and mode of the next input.
   */
  getIndex() {
    // check if there are no more inputs for this instruction; if so: abort
    if (_.isEmpty(this.modes)) {
      return { idx: null, mode: null }
    }
    // extract the mode for this input
    const mode = _.head(this.modes)
    this.modes = _.slice(this.modes, 1)
    // process the index depending on the mode
    let idx
    switch (mode) {
      case 0:
        idx = this.programGetData(this.instructionPtr)
        break
      case 1:
        idx = this.instructionPtr
        break
      default:
        return { idx: null, mode: null }
    }
    // increase the current instruction pointer
    this.instructionPtr++
    return { idx, mode }
  }
  
  /**
   * Gets the "address" or "immediate value" for a given set of inputs and data.
   * @param {bool} keepIndex - Whether or not the function should keep the index
   *                           as is, or interpret it as an address in the
   *                           program.
   * @returns {int} - Program data value.
   */
  getValue(keepIndex=false) {
    // get the index and mode
    const { idx, mode } = this.getIndex()
    if (idx === null) {
      return null
    }
    // if necessary, apply the index as an address in the program code
    return (keepIndex) ? idx : this.programGetData(idx)
  }
  
  /**
   * Processes the next instruction in the program with the current memory and
     instruction pointer.
   * @returns {bool} - Whether or not the program should pause (if pause is
   *                   activated).
   */
  processOpcode() {
    // get the current instruction
    const instruction = this.program[this.instructionPtr].toString()
    // extract the operation code (opcode) and check for halt or error
    const opcode = parseInt(instruction.substring(instruction.length - 2))
    if (!_.has(OPERATIONS, opcode)) {
      this.instructionPtr = -1
      return false
    }
    // get the information on this operation for further process
    const { op, n } = OPERATIONS[opcode]
    const modes = instruction.substring(0, instruction.length - 2)
    this.modes = _.concat(
      _.map(modes.split('').reverse().join(''), (m) => Number(m)),
      new Array(n - modes.length).fill(0)
    )
    // prepare the pause mode as False (could be modified by some operations)
    let pause = false
    // execute the right operation depending on the opcode
    this.instructionPtr++
    let a, b, c, m, v
    switch (opcode) {
      case 99:
        this.instructionPtr = null
        return false
      case 1: // add
      case 2: // multiply
        a = this.getValue(); b = this.getValue(); c = this.getValue(true)
        this.programSetData(c, op(a, b))
        break
      case 3: // read
        if (_.isEmpty(this.memory)) {
          return false
        }
        a = this.getValue(true)
        m = _.head(this.memory)
        this.memory = _.slice(this.memory, 1)
        this.programSetData(a, m)
        break
      case 4: // print
        v = this.getValue()
        this.output.push(v)
        pause = true
        break
      case 5: // jump if true
        a = this.getValue(); b = this.getValue()
        if (a !== 0) {
          this.instructionPtr = b
        }
        break
      case 6: // jump if false
        a = this.getValue(); b = this.getValue()
        if (a === 0) {
          this.instructionPtr = b
        }
        break
      case 7: // set if less than
      case 8: // set if equal
        a = this.getValue(); b = this.getValue(); c = this.getValue(true)
        this.programSetData(c, (op(a, b)) ? 1 : 0)
        break
      default:
        return false
    }
    return pause
  }
  
}

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
  const thrusts = []

  INSTANCE_ID = 0 // reset global instances IDs
  // create pool of instances
  const amplifiers = _.map(_.range(5), (a) => {
    return new ProgramInstance(inputs)
  })
  let curAmplifier, phase
  _.each(candidatePhaseSettings, (phaseSettings, idx) => {
    // reset all amplifiers
    _.each(amplifiers, (amp) => { amp.reset() })
    // prepare input for first amplifier
    amplifiers[0].memoryInsert(0)
    for (curAmplifier = 0; curAmplifier < nAmplifiers; curAmplifier++) {
      phase = phaseSettings[curAmplifier]
      amplifiers[curAmplifier].checkRunning(phase)
      // execute program
      amplifiers[curAmplifier].runMultiple(amplifiers)
    }
    // remember the power sent to the thrusters with these settings
    thrusts.push(_.last(amplifiers[curAmplifier - 1].output))
  })
  return _.max(thrusts)
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

  INSTANCE_ID = 0 // reset global instances IDs
  // create pool of instances
  const amplifiers = _.map(_.range(nAmplifiers), (a) => {
    return new ProgramInstance(inputs)
  })
  let curAmplifier, nextAmplifier, running, phase
  _.each(candidatePhaseSettings, (phaseSettings) => {
    // reset all amplifiers
    _.each(amplifiers, (amp) => { amp.reset() })
    // prepare input for first amplifier
    amplifiers[0].memoryInsert(0)
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

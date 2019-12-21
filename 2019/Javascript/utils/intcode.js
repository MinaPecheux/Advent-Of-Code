const _ = require('lodash')

let INSTANCE_ID = 0 // class variable that is common to all instances
let INPUT = null // specific value for the input instruction
let OUTPUTS = [] // outputs of the program
const OPERATIONS = {
  1: { name: 'add', op: (a, b) => a + b, n: 3 },
  2: { name: 'mult', op: (a, b) => a * b, n: 3 },
  3: { name: 'read', op: () => INPUT, n: 1 },
  4: { name: 'write', op: null, n: 1 },
  5: { name: 'jump_if_true', op: null, n: 2 },
  6: { name: 'jump_if_false', op: null, n: 2 },
  7: { name: 'set_if_lt', op: (a, b) => a < b, n: 3 },
  8: { name: 'set_if_eq', op: (a, b) => a === b, n: 3 },
  9: { name: 'offset_relative_base', op: null, n: 1 },
  99: { name: 'halt', op: null, n: null }
}

/**
 * Util class to represent a program instance with its own instructions,
   memory, run state and instruction pointer. Allows for multiple instances
   in parallel to interact without overwriting data.
 * @class
 */
class IntcodeProgram {
  
  /**
   * @constructs IntcodeProgram
   * @param {array(int)} program - Original Intcode program to execute (will
   *                               be copied to avoid in-place modification).
   * @param {bool} debug - Whether or not the IntcodeProgram should debug its
   *                       execution at each instruction processing.
   */
  constructor(program, debug=false) {
    this.id = INSTANCE_ID++
    this.program = _.reduce(program, (acc, inst, idx) => {
      return { ...acc, [idx]: inst }
    }, {})
    this.memory = []
    this.output = []
    this.modes = []
    this.instructionPtr = 0
    this.isRunning = false
    this.relativeBase = 0
    this.debug = debug
    
    this._initialProgram = _.cloneDeep(this.program)
    this._inputId = 0
    this._debugStr = ''
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
    this.relativeBase = 0
    this.program = _.cloneDeep(this._initialProgram)
  }
  
  /**
   * Inserts a value in the instance's memory, in first position.
   * @param {array(int)} program - Original Intcode program to execute (will
   *                               be copied to avoid in-place modification).
   */
  setProgram(program) {
    this._initialProgram = _.reduce(program, (acc, inst, idx) => {
      return { ...acc, [idx]: inst }
    }, {})
    this.reset()
  }
  
  /**
   * Resets the output of the program to a blank slate.
   */
  resetOutput() {
    this.output = []
  }
  
  /**
   * Pushes one or more value(s) in the instance's memory, at the end.
   * @param {int | array(int)} data - Value(s) to append.
   */
  pushMemory(data) {
    if (_.isArray(data)) {
      this.memory = _.concat(this.memory, data)
    } else {
      this.memory.push(data)
    }
  }
  
  /**
   * Inserts one or more value(s) in the instance's memory, in first position.
   * @param {int | array(int)} data - Value(s) to insert.
   */
  insertMemory(data) {
    if (_.isArray(data)) {
      this.memory = _.concat(data, this.memory)
    } else {
      this.memory.unshift(data)
    }
  }
  
  /**
   * Checks if the instance is already running or if it should be initialized
   * with its phase setting.
   * @param {int} phase - Phase setting for this instance.
   */
  checkRunning(phase) {
    if (!this.isRunning) {
      this.insertMemory(phase)
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
   * @param {null | int} pauseEvery - If not None, number of output digits to
   *                                  store before pausing. If None, the
   *                                  execution should proceed until it reached
   *                                  the halt operation.
   */
  run(pauseEvery=null) {
    let nPause = 0, pause
    while (this.instructionPtr !== null) {
      pause = this.processOpcode()
      // check for pause
      if (pause) {
        nPause++
      }
      if (pauseEvery === nPause) {
        nPause = 0
        return (this.instructionPtr !== null) ? 'pause' : null
      }
      if (this.instructionPtr === -1) {
        return null
      }
    }
    return null
  }
  
  /**
   * Runs the instance by executing its Intcode program either from scratch or
     from where it last stopped, as part of a pool of instances that feed each
     other with output to input connection.
   * @param {array(IntcodeProgram)} instances - List of all program instances
   *                                             in the pool.
   * @returns {int} - Index of the next instance in the pool to run, if any.
   */
  runMultiple(instances) {
    // if we stopped just before halting, we simply terminate the program
    // and go to the next instance
    let nextInstance
    if (!_.isEmpty(this.output) && this.instructionPtr === null) {
      nextInstance = (this.id + 1) % instances.length
      instances[nextInstance].pushMemory(_.last(this.output))
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
        instances[nextInstance].pushMemory(_.last(this.output))
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
      case 2:
        idx = this.programGetData(this.instructionPtr) + this.relativeBase
        break
      default:
        return { idx: null, mode: null }
    }
    // increase the current instruction pointer
    this.instructionPtr++
    // increase the input id (for debug)
    this._inputId++
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
    const val = (keepIndex) ? idx : this.programGetData(idx)
    // (fill the debug string in case of debug mode)
    this._debugStr += ` arg${this._inputId}=${val} (idx=${idx}, mode=${mode}) ;`
    return val
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
    const { name, op, n } = OPERATIONS[opcode]
    const modes = instruction.substring(0, instruction.length - 2)
    this.modes = _.concat(
      _.map(modes.split('').reverse().join(''), (m) => Number(m)),
      new Array(n - modes.length).fill(0)
    )
    // prepare the debug string in case the debug mode is active
    this._inputId = 0
    this._debugStr = (
      `[ ${this.instructionPtr.toString().padStart(3, ' ')} ]`
      + ` - inst = ${instruction.padStart(5, '0')} `
      + `:: op = ${name} (${opcode}), `
      + `modes = ${this.modes}\n`
    )
    // prepare the pause mode as False (could be modified by some operations)
    let pause = false
    // execute the right operation depending on the opcode
    this.instructionPtr++
    let a, b, c, m, v
    switch (opcode) {
      case 99:
        this.instructionPtr = null
        break
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
      case 9: // relative base offset
        this.relativeBase += this.getValue()
      default:
        return false
    }
    
    if (this.debug) {
      console.log(this._debugStr)
    }
    
    return pause
  }
  
}

/**
 * Resets the global ID for program instances.
 */
IntcodeProgram.resetID = () => {
  INSTANCE_ID = 0
}

module.exports = {
  IntcodeProgram
}

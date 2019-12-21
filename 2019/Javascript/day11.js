/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 11: Space Police
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
 * Executes the Intcode program on the provided inputs and finds out the
   number of panels that have been painted at least once. It can also display
   the message that has been painted if necessary.
 * @param {array(int)} inputs - List of integers to execute as an Intcode program.
 * @param {bool} startWhite - If true, then the starting panel is considered
 *                            painted white. Else, it is considered painted black.
 * @param {bool} display - If true, then the final state of the board is displayed
 *                         in the shell.
 * @param {bool} debug - Whether or not the IntcodeProgram should debug its
 *                       execution at each instruction processing.
 * @returns {int} - Number of panels painted at least once.
 */
const processInputs = (inputs, startWhite=false, display=false, debug=false) => {
  // prepare the board and the set of painted panels:
  // - the board only remembers the panels painted white
  // - the painted set remembers all the panels that have been painted at least
  // once
  const board = new Set([])
  const painted = new Set([])
  // initialize the painting robot: facing up, at the origin coordinates
  let dir = 0
  let x = 0, y = 0
  // (if starting white: mark the current panel as already painted white)
  if (startWhite) {
    board.add(`${x},${y}`)
  }
  
  // prepare the program instance to read the given inputs as an Intcode program
  const program = new IntcodeProgram(inputs, debug)
  let running = true
  let input, state, color, rotation, m
  // execute the program until it halts (but pause every 2 outputs)
  while (running) {
    // get the input depending on the state of the panel: if painted white
    // (i.e. visible in the board), the input is 1; else it is 0
    input = (board.has(`${x},${y}`)) ? 1 : 0
    // insert the input in the program's memory
    program.pushMemory(input)
    // execute until 2 digits have been outputted
    state = program.run(2)
    // check for state:
    // . if paused: parse outputs and apply the actions
    if (state === 'pause') {
      color = program.output[program.output.length - 2]
      rotation = program.output[program.output.length - 1]
      program.resetOutput()
      if (color === 1) {
        board.add(`${x},${y}`)
      } else {
        board.delete(`${x},${y}`)
      }
      painted.add(`${x},${y}`)
      m = (rotation === 0) ? -1 : 1
      dir += m
      dir = ((dir % 4) + 4) % 4
      switch (dir) {
        case 0: // up
          y--
          break
        case 1: // right
          x++
          break
        case 2: // down
          y++
          break
        case 3: // left
          x--
          break
        default:
          break
      }
    // . else: stop the program
    } else if (state === null) {
      running = false
      break
    }
  }
  
  // if necessary, display the final message, i.e. the board that
  // has been printed (and only contains the painted panels)
  if (display) {
    const marker = '█'
    // . separate horizontal from vertical coordinates
    x = [], y = []
    board.forEach((coord) => {
      const [ xx, yy ] = _.split(coord, ',')
      x.push(parseInt(xx))
      y.push(parseInt(yy))
    })
    // . find board boundaries
    const minX = _.min(x), maxX = _.max(x)
    const minY = _.min(y), maxY = _.max(y)
    // . iterate through the board to print out the message
    console.log('')
    let row
    _.each(_.range(minY, maxY + 1), (y) => {
      row = ''
      _.each(_.range(minX, maxX + 1), (x) => {
        row += (board.has(`${x},${y}`)) ? marker : ' '
      })
      console.log(row)
    })
    console.log('')
  }
  
  // get the number of panels that have been painted at least once (counts each
  // panel once, and counts the panels even if they have been repainted black)
  return painted.size
}

(() => {
  // get input data
  const data = fs.readFileSync('../data/day11.txt')
  const inputs = parseInput(data)
  
  // Part I
  const solution1 = processInputs(inputs)
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  const solution2 = processInputs(inputs, true, true)
  console.log('PART II: solution (see above in the shell)')
})()

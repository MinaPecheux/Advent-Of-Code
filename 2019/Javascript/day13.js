/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 13: Care Package
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
const DISPLAY_MAP = { null: ' ', 'W': '█', 'B': '□', 'H': '▂', 'O': '●' }

/**
 * Displays the board in the shell.
 * @param {object} board - Board to display.
 */
const displayBoard = (board) => {
  // find board boundaries
  const x = [], y = []
  _.each(_.keys(board), (coord) => {
    const [ xx, yy ] = _.split(coord, ',')
    x.push(parseInt(xx))
    y.push(parseInt(yy))
  })
  const minX = _.min(x), maxX = _.max(x)
  const minY = _.min(y), maxY = _.max(y)
  // print the grid
  console.log('')
  let row
  _.each(_.range(minY, maxY + 1), (y) => {
    row = ''
    _.each(_.range(minX, maxX + 1), (x) => {
      row += (_.has(board, `${x},${y}`)) ? DISPLAY_MAP[board[`${x},${y}`]] : ' '
    })
    console.log(row)
  })
  console.log('')
}

/* PART I */
/**
 * Executes the Intcode program on the provided inputs and finds out the
   number of blocks on the screen when the game exits. It also returns the
   board when the game exits (i.e. the initial board since no game was
   actually played).
 * @param {array(int)} inputs - List of integers to execute as an Intcode program.
 * @param {bool} display - Whether or not to display the board after the game exits.
 * @param {bool} debug - Whether or not the IntcodeProgram should debug its
 *                       execution at each instruction processing.
 * @returns {object} - Inital board (when no game was played) and number of blocks
 *                     on the screen when the game exits.
 */
const countBlocks = (inputs, display=false, debug=false) => {
  // prepare the board
  const board = {}  
  // prepare the program instance to read the given inputs as an Intcode program
  const program = new IntcodeProgram(inputs, debug)
  let running = true
  let state, x, y, id, marker
  // execute the program until it halts (but pause every 3 outputs)
  while (running) {
    // execute until 3 digits have been outputted
    state = program.run(3)
    // check for state:
    // . if paused: parse outputs and apply the actions
    if (state === 'pause') {
      x = program.output[program.output.length - 3]
      y = program.output[program.output.length - 2]
      id = program.output[program.output.length - 1]
      program.resetOutput()
      switch (id) {
        case 0:
          marker = null
          break
        case 1:
          marker = 'W'
          break
        case 2:
          marker = 'B'
          break
        case 3:
          marker = 'H'
          break
        default:
          marker = 'O'
          break
      }
      board[`${x},${y}`] = marker
    // . else: stop the program
    } else if (state === null) {
      running = false
      break
    }
  }
  
  if (display) {
    displayBoard(board)
  }
  
  const nBlocks = _.countBy(board).B
  return { board, nBlocks }
}

/* PART II */
/**
 * Executes the Intcode program on the provided inputs and finds out the
   score of the player when the last block has been destroyed.
 * @param {object} board - Initial board.
 * @param {array(int)} inputs - List of integers to execute as an Intcode program.
 * @param {bool} debug - Whether or not the IntcodeProgram should debug its
 *                       execution at each instruction processing.
 * @returns {int} - Final score of the player.
 */
const computeScore = (board, inputs, debug=false) => {
  // prepare the board and paddle/ball coordinates
  let px, py, bx, by, tmp
  _.each(board, (marker, coord) => {
    tmp = _.split(coord, ',')
    if (marker === 'H') {
      px = parseInt(tmp[0])
      py = parseInt(tmp[1])
    } else if (marker === 'O') {
      bx = parseInt(tmp[0])
      by = parseInt(tmp[1])
    }
  })
  let initNBlocks = null, lastNBlocks = null
  // prepare the program instance to read the given inputs as an Intcode program
  const program = new IntcodeProgram(inputs, debug)
  // insert quarters to run in "free mode"
  program.program[0] = 2
  
  let running = true
  let state, score = null, time = 0, nBlocks, x, y, id, marker
  // execute the program until it halts (but pause every 3 outputs)
  while (running) {
    // move the paddle to catch the ball and continue the game
    if (px < bx) { // move right
      program.insertMemory(1)
    } else if (px > bx) { // move left
      program.insertMemory(-1)
    } else { // reset movement to null
      program.insertMemory(0)
    }
    
    // execute until 3 digits have been outputted
    state = program.run(3)
    // check for state:
    // . if paused: parse outputs and apply the actions
    if (state === 'pause') {
      x = program.output[program.output.length - 3]
      y = program.output[program.output.length - 2]
      id = program.output[program.output.length - 1]
      program.resetOutput()
      if (x === -1 && y === 0) {
        score = id
        // if outputting score and no more blocks: game ends
        if (nBlocks === 0) {
          console.log('\n')
          running = false
          break
        }
      } else {
        switch (id) {
          case 0:
            marker = null
            break
          case 1:
            marker = 'W'
            break
          case 2:
            marker = 'B'
            break
          case 3:
            marker = 'H'
            px = x
            py = y
            break
          default:
            marker = 'O'
            bx = x
            by = y
            break
        }
        board[`${x},${y}`] = marker
      }
    // . else: stop the program
    } else if (state === null) {
      running = false
      break
    }
    
    // . check to see if all blocks have disappeared
    nBlocks = _.countBy(board).B || 0
    // (initialize if necessary)
    if (initNBlocks === null) {
      initNBlocks = nBlocks
      console.log('')
    }
    // (if number of remaining blocks changed, update the progress bar)
    if (lastNBlocks !== nBlocks) {
      const c = _.round(50.0 * nBlocks / initNBlocks)
      const suffix = nBlocks.toString().padStart(initNBlocks.toString().length, ' ')
      const bar = `[ ${'■'.repeat(c)}${' '.repeat(50-c)} ]`
      process.stdout.write(`\r${bar} ${suffix} / ${initNBlocks}`)
      lastNBlocks = nBlocks
    }    
  }
  
  return score
}

(() => {
  // get input data
  const data = fs.readFileSync('../data/day13.txt')
  const inputs = parseInput(data)
  
  // Part I
  const solution1 = countBlocks(inputs, true)
  console.log(`PART I: solution = ${solution1.nBlocks}`)
  
  // Part II
  const solution2 = computeScore(solution1.board, inputs)
  console.log(`PART II: solution = ${solution2}`)
})()

/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 4: Secure Container
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
  return _.map(_.split(data, '-'), Number)
}

// [ Computation functions ]
// -------------------------
/* Part I */
/**
 * Checks if a number meets the password criteria of Part I:
   - length of 6 digits
   - two adjacent digits are the same
   - going left from right, digits never decrease (i.e. they increase or
   stay the same)
 * @param {int} number - Number to check.
 * @returns {bool} - Number validity.
 */
const numberIsOkP1 = (number) => {
  const nStr = number.toString()
  if (nStr.length !== 6)
    return false
  let prevC = -1
  let hasDuplicate = false
  for (let i = 0; i < nStr.length; i++) {
    const c = parseInt(nStr[i])
    if (c < prevC) {
      return false
    }
    if (c == prevC) {
      hasDuplicate = true
    }
    prevC = c
  }
  return hasDuplicate
}

/* Part II */
/**
 * Checks if a number meets the password criteria of Part I:
   - length of 6 digits
   - two adjacent digits are the same
   - going left from right, digits never decrease (i.e. they increase or
   stay the same)
 * @param {int} number - Number to check.
 * @returns {bool} - Number validity.
 */
const numberIsOkP2 = (number) => {
  const nStr = number.toString()
  if (nStr.length !== 6)
    return false
  let prevC = -1
  for (let i = 0; i < nStr.length; i++) {
    const c = parseInt(nStr[i])
    if (c < prevC) {
      return false
    }
    prevC = c
  }
  const counts = _.countBy(nStr)
  return _.includes(_.values(counts), 2)
}

/**
 * Finds all the valid numbers (that meet the given password criteria) in the
   range given by the inputs.
 * @param {array(int)} inputs - Minimum and maximum value (inclusive) for the numbers
 *                              to check.
 * @param {function} check - Validity function to pass.
 * @returns {int} - Count of numbers in the range that pass the test.
 */
const getCountOfValidNumbers = (inputs, check) => {
  const [ min, max ] = inputs
  return _.sum(_.map(_.range(min, max+1), (n) => {
    return check(n) ? 1 : 0
  }))
}

// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  /* Part I */
  expect(numberIsOkP1(111111)).to.be.true
  expect(numberIsOkP1(223450)).to.be.false
  expect(numberIsOkP1(123789)).to.be.false
  
  /* Part II */
  expect(numberIsOkP2(112233)).to.be.true
  expect(numberIsOkP2(123444)).to.be.false
  expect(numberIsOkP2(111122)).to.be.true
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = '248345-746315'
  const inputs = parseInput(data)
  
  // Part I
  const solution1 = getCountOfValidNumbers(inputs, numberIsOkP1)
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  const solution2 = getCountOfValidNumbers(inputs, numberIsOkP2)
  console.log(`PART II: solution = ${solution2}`)
})()

/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 1: The Tyranny of the Rocket Equation
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
  return _.map(_.filter(_.split(data, '\n'), (l) => l.length > 0), Number)
}

// [ Computation functions ]
// -------------------------
/* PART I */
/**
 * Computes the required fuel for a module of given mass.
 * @param {int} mass - The mass of the module to compute the fuel consumption for.
 * @returns {int} - Required amount of fuel.
 */
const computeFuel = (mass) => _.floor(mass / 3) - 2

/* PART II */
/** Computes the total required fuel for a module of given mass and the
 * added fuel, and so on. It works recursively until the computed amount of
 * fuel is zero or negative.
 * @param {int} mass - The mass of the module to compute the fuel consumption for.
 * @returns {int} - Required amount of fuel.
 */
const computeTotalFuel = (mass) => {
  const f = computeFuel(mass)
  return (f <= 0) ? 0 : f + computeTotalFuel(f)
}
    
// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  /* Part I */
  expect(computeFuel(12)).to.equal(2)
  expect(computeFuel(14)).to.equal(2)
  expect(computeFuel(1969)).to.equal(654)
  expect(computeFuel(100756)).to.equal(33583)
  /* Part II */
  expect(computeTotalFuel(14)).to.equal(2)
  expect(computeTotalFuel(1969)).to.equal(966)
  expect(computeTotalFuel(100756)).to.equal(50346)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day1.txt')
  const inputs = parseInput(data)
  
  // Part I
  const solution1 = _.sum(_.map(inputs, (i) => computeFuel(i)))
  console.log(`PART I: solution = ${solution1}`)
  
  // Part I
  const solution2 = _.sum(_.map(inputs, (i) => computeTotalFuel(i)))
  console.log(`PART II: solution = ${solution2}`)
})()

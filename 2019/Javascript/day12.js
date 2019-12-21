/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 12: The N-Body Problem
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
 * @returns {array(object)} - Parsed data.
 */
const parseInput = (data) => {
  const reg = /<x=(-?\d+), y=(-?\d+), z=(-?\d+)>/
  const points = []
  let match
  _.each(_.split(data, '\n'), (line) => {
    if (line === '') return
    match = [ ...line.match(reg) ]
    points.push({
      x: parseInt(match[1]), y: parseInt(match[2]), z: parseInt(match[3]),
      vx: 0.0, vy: 0.0, vz: 0.0
    })
  })
  return points
}

// [ Computation functions ]
// -------------------------
/* Part I */

const combinations = (arr) => {
  return _.flatMap(arr, (v, i) => _.map(_.slice(arr, i+1), ((w) => [
    _.cloneDeep(v), _.cloneDeep(w)
  ] )))
}

/**
 * Computes the total energy of a moon based on its current position and
   velocity.
 * @param {object} moon - Current position and velocity of the moon.
 * @returns {int} - Total energy of the moon.
 */
const computeTotalEnergy = (moon) => {
  const { x, y, z, vx, vy, vz } = moon
  const potentialEnergy = Math.abs(x) + Math.abs(y) + Math.abs(z)
  const kineticEnergy = Math.abs(vx) + Math.abs(vy) + Math.abs(vz)
  return potentialEnergy * kineticEnergy
}

/**
 * Simulates the moons' movement over a given number of time steps and
  computes the final total energy of the entire system (i.e. the sum of the
  final total energies of each moon).
 * @param {list(object)} moons - Initial positions and velocities of the moons
 *                               to process.
 * @param {timesteps} int - Number of time steps to simulate.
 * @returns {int} - Total energy of the entire system at the end of the simulation.
 */
const simulateMoons = (moons, timesteps) => {
  // prepare all the unique moon pairs
  const moonPairs = combinations(_.range(moons.length))
  
  let m1, m2
  for (let time = 0; time < timesteps; time++) {
    // apply gravity
    _.each(moonPairs, ([ i1, i2 ]) => {
      m1 = moons[i1]
      m2 = moons[i2]
      if (m1.x > m2.x) {
        moons[i1].vx--
        moons[i2].vx++
      } else if (m1.x < m2.x) {
        moons[i1].vx++
        moons[i2].vx--
      }
      if (m1.y > m2.y) {
        moons[i1].vy--
        moons[i2].vy++
      } else if (m1.y < m2.y) {
        moons[i1].vy++
        moons[i2].vy--
      }
      if (m1.z > m2.z) {
        moons[i1].vz--
        moons[i2].vz++
      } else if (m1.z < m2.z) {
        moons[i1].vz++
        moons[i2].vz--
      }
    })
    // apply velocity
    _.each(moons, (moon) => {
      moon.x += moon.vx
      moon.y += moon.vy
      moon.z += moon.vz
    })
  }
  
  return _.sum(_.map(moons, (moon) => computeTotalEnergy(moon)))
}

/* Part II */
/**
 * Computes the greatest common divisor (GCD) of two numbers.
 * @param {int} x - First number to process.
 * @param {int} y - Second number to process.
 * @returns {int} - GCD of the two numbers.
 */
const GCD = (x, y) => {
  let tmp
  while (y) {
    tmp = x
    x = y
    y = tmp % y
  }
  return x
}

/**
 * Computes the least common multiple (LCM) of two numbers.
 * @param {int} x - First number to process.
 * @param {int} y - Second number to process.
 * @returns {int} - LCM of the two numbers.
 */
const LCM = (x, y) => _.floor((x*y) / GCD(x, y))

/**
 * Simulates the moons' movement until they repeat a previous state.
 * @param {list(object)} moons - Initial positions and velocities of the moons
 *                               to process.
 * @returns {int} - Number of steps until the first repetition.
 */
const findFirstRepetition = (moons) => {
  // prepare all the unique moon pairs
  const moonPairs = combinations(_.range(moons.length))
  
  const historyX = {}, historyY = {}, historyZ = {}
  let periodX = null, periodY = null, periodZ = null
  let time = 0, m1, m2, stateX, stateY, stateZ
  while (true) {
    // apply gravity
    _.each(moonPairs, ([ i1, i2 ]) => {
      m1 = moons[i1]
      m2 = moons[i2]
      if (m1.x > m2.x) {
        moons[i1].vx--
        moons[i2].vx++
      } else if (m1.x < m2.x) {
        moons[i1].vx++
        moons[i2].vx--
      }
      if (m1.y > m2.y) {
        moons[i1].vy--
        moons[i2].vy++
      } else if (m1.y < m2.y) {
        moons[i1].vy++
        moons[i2].vy--
      }
      if (m1.z > m2.z) {
        moons[i1].vz--
        moons[i2].vz++
      } else if (m1.z < m2.z) {
        moons[i1].vz++
        moons[i2].vz--
      }
    })
    // apply velocity
    _.each(moons, (moon) => {
      moon.x += moon.vx
      moon.y += moon.vy
      moon.z += moon.vz
    })
    // hash state
    // . hash each axis
    // . check the matching dict for a repetition
    // . store the hash with the current time for further checks
    stateX = _.join(_.map(moons, (m) => `${m.x},${m.vx}`), ',')
    if (_.has(historyX, stateX)) {
      periodX = time - historyX[stateX]
    }
    historyX[stateX] = time
    stateY = _.join(_.map(moons, (m) => `${m.y},${m.vy}`), ',')
    if (_.has(historyY, stateY)) {
      periodY = time - historyY[stateY]
    }
    historyY[stateY] = time
    stateZ = _.join(_.map(moons, (m) => `${m.z},${m.vz}`), ',')
    if (_.has(historyZ, stateZ)) {
      periodZ = time - historyZ[stateZ]
    }
    historyZ[stateZ] = time
    if (periodX !== null && periodY !== null && periodZ !== null) {
      break
    }
    time++
  }
  
  // find the total repetition period by getting the LCM of the three subperiods
  return LCM(LCM(periodX, periodY), LCM(periodY, periodZ))
}

// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  expect(computeTotalEnergy({
    x: 2, y: 1, z: -3, vx: -3, vy: -2, vz: 1
  })).to.equal(36)
  expect(computeTotalEnergy({
    x: 1, y: -8, z: 0, vx: -1, vy: 1, vz: 3
  })).to.equal(45)
  expect(computeTotalEnergy({
    x: 3, y: -6, z: 1, vx: 3, vy: 2, vz: -3
  })).to.equal(80)
  expect(computeTotalEnergy({
    x: 2, y: 0, z: 4, vx: 1, vy: -1, vz: -1
  })).to.equal(18)
  
  /* Part I */
  expect(simulateMoons([
    { x: -1, y: 0, z: 2, vx: 0, vy: 0, vz: 0 },
    { x: 2, y: -10, z: -7, vx: 0, vy: 0, vz: 0 },
    { x: 4, y: -8, z: 8, vx: 0, vy: 0, vz: 0 },
    { x: 3, y: 5, z: -1, vx: 0, vy: 0, vz: 0 }
  ], 10)).to.equal(179)
  
  /* Part II */
  expect(findFirstRepetition([
    { x: -1, y: 0, z: 2, vx: 0, vy: 0, vz: 0 },
    { x: 2, y: -10, z: -7, vx: 0, vy: 0, vz: 0 },
    { x: 4, y: -8, z: 8, vx: 0, vy: 0, vz: 0 },
    { x: 3, y: 5, z: -1, vx: 0, vy: 0, vz: 0 }
  ])).to.equal(2772)
  expect(findFirstRepetition([
    { x: -8, y: -10, z: 0, vx: 0, vy: 0, vz: 0 },
    { x: 5, y: 5, z: 10, vx: 0, vy: 0, vz: 0 },
    { x: 2, y: -7, z: 3, vx: 0, vy: 0, vz: 0 },
    { x: 9, y: -8, z: -3, vx: 0, vy: 0, vz: 0 }
  ])).to.equal(4686774924)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day12.txt')
  const moons = parseInput(data)
  
  // Part I
  const solution1 = simulateMoons(moons, 1000)
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  const solution2 = findFirstRepetition(moons)
  console.log(`PART II: solution = ${solution2}`)
})()

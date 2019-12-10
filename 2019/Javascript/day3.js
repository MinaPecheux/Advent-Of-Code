/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 3: Crossed Wires
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
 * @returns {array(string)} - Parsed data.
 */
const parseInput = (data) => {
  return _.map(_.filter(_.split(data, '\n'), (l) => l.length > 0), (line) => {
    return _.split(line, ',')
  })
}

// [ Computation functions ]
// -------------------------
/**
 * Computes the Manhattan (or Taxicab) distance between two 2D points.
 * @param {int} x1 - Horizontal coordinate of the first point.
 * @param {int} y1 - Vertical coordinate of the first point.
 * @param {int} x2 - Horizontal coordinate of the second point.
 * @param {int} y2 - Vertical coordinate of the second point.
 * @returns {int} - Taxicab distance between the two 2D points.
 */
const manhattanDistance = (x1, y1, x2, y2) => {
  return Math.abs(x2 - x1) + Math.abs(y2 - y1)
}

/**
 * Computes all the points a path goes through.
 * @param {array(string)} path - Path to walk, as a list of moves to take
 *                               (with a direction and an integer pace).
 * @returns {object(string, int)} - Points on the path.
 */
const findPathPoints = (path) => {
  let cx = 0, cy = 0, d = 1, dir, pace
  const points = {}
  _.each(path, (move) => {
    dir = move[0]
    pace = parseInt(move.substring(1))
    switch (dir) {
      case 'R':
        for (let x = cx + 1; x < cx + pace + 1; x++) {
          points[`${x},${cy}`] = d
          d++
        }
        cx += pace
        break
      case 'L':
        for (let x = cx - 1; x > cx - pace - 1; x--) {
          points[`${x},${cy}`] = d
          d++
        }
        cx -= pace
        break
      case 'U':
        for (let y = cy - 1; y > cy - pace - 1; y--) {
          points[`${cx},${y}`] = d
          d++
        }
        cy -= pace
        break
      case 'D':
        for (let y = cy + 1; y < cy + pace + 1; y++) {
          points[`${cx},${y}`] = d
          d++
        }
        cy += pace
        break
      default:
        break
    }
  })
  return points
}

/* PART I */
/**
 * Finds the intersection of given paths that is closest to the central port,
   considering the Manhattan distance.
 * @param {array(array(string))} paths - Paths to process.
 * @returns {int} - Distance of the closest intersection to the central port.
 */
const findClosestIntersectionWithDist = (paths) => {
  // compute all activated points on the grid
  const pathPoints =  _.map(paths, (path) => findPathPoints(path))
  // extract the intersections of all the paths
  const positions = _.map(pathPoints, (p) => _.keys(p))
  const intersections = _.intersection(...positions)
  // find the one closest to the central port (compute its Manhattan distance)
  const dists = _.map(intersections, (pos) => {
    const [ x, y ] = _.split(pos, ',')
    return manhattanDistance(parseInt(x), parseInt(y), 0, 0)
  })
  return _.min(dists)
}

/* PART II */
/**
 * Finds the intersection of given paths that is closest to the central port,
   considering the combined number of steps to the chosen intersection.
 * @param {array(array(string))} paths - Paths to process.
 * @returns {int} - Distance of the closest intersection to the central port.
 */
const findClosestIntersectionWithSteps = (paths) => {
  // compute all activated points on the grid
  const pathPoints =  _.map(paths, (path) => findPathPoints(path))
  // extract the intersections of all the paths
  const positions = _.map(pathPoints, (p) => _.keys(p))
  const intersections = _.intersection(...positions)
  // find the smallest sum of combined steps
  return _.min(_.map(intersections, (i) => pathPoints[0][i] + pathPoints[1][i]))
}

// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  /* Part I */
  expect(findClosestIntersectionWithDist([
    ['R8','U5','L5','D3'],
    ['U7','R6','D4','L4']
  ])).to.equal(6)
  expect(findClosestIntersectionWithDist([
    ['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
    ['U62','R66','U55','R34','D71','R55','D58','R83']
  ])).to.equal(159)
  expect(findClosestIntersectionWithDist([
    ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
    ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
  ])).to.equal(135)
  
  /* Part II */
  expect(findClosestIntersectionWithSteps([
    ['R8','U5','L5','D3'],
    ['U7','R6','D4','L4']
  ])).to.equal(30)
  expect(findClosestIntersectionWithSteps([
    ['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
    ['U62','R66','U55','R34','D71','R55','D58','R83']
  ])).to.equal(610)
  expect(findClosestIntersectionWithSteps([
    ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
    ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
  ])).to.equal(410)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day3.txt')
  const paths = parseInput(data)
  
  // Part I
  const solution1 = findClosestIntersectionWithDist(paths)
  console.log(`PART I: solution = ${solution1}`)
  
  // Part II
  const solution2 = findClosestIntersectionWithSteps(paths)
  console.log(`PART II: solution = ${solution2}`)
})()

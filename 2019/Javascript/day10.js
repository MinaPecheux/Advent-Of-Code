/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 10: Monitoring Station
 * ================================================
 */
'use strict'

const _ = require('lodash')
const fs = require('fs')
const expect = require('chai').expect

/**
 * Util class to represent the map of a field of asteroids.
 * @class
 */
class Map {
  
  /**
   * @constructs Map
   * @param {string} data - Data to create the map.
   */
  constructor(data) {
    this.parseData(data)
  }
  
  /**
   * Parses the data to get the positions of each asteroids.
   * @param {string} data - Data to create the map.
   */
  parseData(data) {
    this.asteroids = {}
    _.each(_.split(data, '\n'), (line, y) => {
      _.each(line, (char, x) => {
        if (char === '#') {
          this.asteroids[`${x},${y}`] = new Set([])
        }
      })
    })
  }
  
  /**
   * Computes all the other asteroids each asteroid in the map can "see".
     If the coordinates are not stores, then the function will overlap
     asteroids in the same line of sight (same angle); else, each asteroid
     will be stored with its angle, its distance to the reference asteroid
     and its position.
   * @param {bool} storeCoords - Whether or not to store the coordinates of the
   *                             other asteroids.
   * @returns {object} - Sights of each asteroid on the map.
   */
  computeAsteroidSights(storeCoords=false) {
    const sights = {}
    _.each(this.asteroids, (tmp, ast1) => {
      if (storeCoords) {
        sights[ast1] = []
        _.each(this.asteroids, (tmp, ast2) => {
          // ignore same location
          if (ast1 === ast2) {
            return
          }
          // else compute angle and distance, and add asteroid
          const a = angle(ast1, ast2)
          const d = dist(ast1, ast2)
          sights[ast1].push({ angle: a, distance: d, coords: ast2 })
        })
      } else {
        sights[ast1] = new Set([])
        _.each(this.asteroids, (tmp, ast2) => {
          // ignore same location
          if (ast1 === ast2) {
            return
          }
          // else compute angle and add asteroid to list
          sights[ast1].add(angle(ast1, ast2))
        })
      }
    })
    return sights
  }
  
}

// [ Input parsing functions ]
// ---------------------------
/**
 * Parses the incoming data into processable inputs.
 * @param {string} data - Provided problem data.
 * @returns {Map} - Parsed data.
 */
const parseInput = (data) => {
  return new Map(data.toString())
}

// [ Computation functions ]
// -------------------------
/**
 * Computes the Euclidean distance between two 2D points.
 * @param {string} ast1 - Coordinates of the first point (in the form "x,y").
 * @param {string} ast2 - Coordinates of the second point (in the form "x,y").
 * @returns {float} - Euclidean distance between the two 2D points.
 */
const dist = (ast1, ast2) => {
  let [ x1, y1 ] = _.split(ast1, ',')
  let [ x2, y2 ] = _.split(ast2, ',')
  x1 = parseInt(x1); y1 = parseInt(y1)
  x2 = parseInt(x2); y2 = parseInt(y2)
  return Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
}

/**
 * Computes the angle between two 2D points using the atan2 and rotates the
   result by 90° counterclockwise.
 * @param {string} ast1 - Coordinates of the first point (in the form "x,y").
 * @param {string} ast2 - Coordinates of the second point (in the form "x,y").
 * @returns {float} - Euclidean distance between the two 2D points.
 */
const angle = (ast1, ast2) => {
  let [ x1, y1 ] = _.split(ast1, ',')
  let [ x2, y2 ] = _.split(ast2, ',')
  x1 = parseInt(x1); y1 = parseInt(y1)
  x2 = parseInt(x2); y2 = parseInt(y2)
  const a = (Math.atan2(y1 - y2, x1 - x2) - (0.5 * Math.PI))
  const m = (2.0 * Math.PI)
  return ((a % m) + m) % m
}

/* Part I */
/**
 * Finds the asteroid from which the station would see the greatest number
   of asteroids.
 * @param {Map} map - Map of the asteroids in the neighborhood.
 * @returns {object} - Coordinates and number of asteroids visible from
 *                     the "best" asteroid.
 */
const findBestAsteroid = (map) => {
  // compute each asteroid sight (and overwrite the ones that are in the same
  // angle)
  const sights = map.computeAsteroidSights()
  // associate the number of visible asteroids to the asteroid position
  const nVisible = _.map(sights, (v, k) => ({ coords: k, count: v.size }))
  // return the best one, i.e. the position that "sees" the most asteroids
  return _.orderBy(nVisible, [ 'count' ], [ 'desc' ])[0]
}

/* Part II */
/**
 * Computes the whole laser vaporization process given some coordinates have
   been picked for the monitoring station.
 * @param {Map} map - Map of the asteroids in the neighborhood.
 * @param {string} station - Coordinates of the monitoring station in the form
 *                           "x,y".
 * @returns {int} - Checksum of the laser vaporization process.
 */
const processLaserVaporization = (map, station) => {
  // compute each asteroid sight (keep track of asteroids angle, distance and
  // position)
  const sights = map.computeAsteroidSights(true)[station]
  // sort the sights per angle, then per distance
  const sortedSights = _.sortBy(sights, [ 'angle', 'distance' ])
  // roll the laser until 200 asteroids have been destroyed
  let idx, tmp, a, d, p, lastAngle = -1.0
  for (let i = 0; i < 200; i++) {
    idx = 0
    a = sortedSights[idx].angle
    while (a <= lastAngle && idx < sortedSights.length - 1) {
      a = sortedSights[idx].angle
      if (a <= lastAngle) {
        idx++
      }
    }
    tmp = sortedSights[idx]
    a = tmp.angle
    d = tmp.distance
    p = tmp.coords
    lastAngle = a % (2.0 * Math.PI)
    _.remove(sortedSights, (s, j) => j === idx)
  }
  // compute the checksum for the position of the 200th destroyed asteroid
  const [ targetX, targetY ] = _.split(p, ',')
  return parseInt(targetX) * 100 + parseInt(targetY)
}

// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  /* Part I */
  let map = parseInput(`.#..#
.....
#####
....#
...##`)
  let tmp = findBestAsteroid(map)
  expect(tmp.count).to.equal(8)
  map = parseInput(`......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####`)
  tmp = findBestAsteroid(map)
  expect(tmp.count).to.equal(33)
  map = parseInput(`#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.`)
  tmp = findBestAsteroid(map)
  expect(tmp.count).to.equal(35)
  map = parseInput(`.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..`)
  tmp = findBestAsteroid(map)
  expect(tmp.count).to.equal(41)
  map = parseInput(`.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##`)
  tmp = findBestAsteroid(map)
  expect(tmp.count).to.equal(210)
  
  /* Part II */
  expect(processLaserVaporization(map, tmp.coords)).to.equal(802)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day10.txt')
  const map = parseInput(data)
  
  // Part I
  const solution1 = findBestAsteroid(map)
  console.log(`PART I: solution = ${solution1.count}`)
  
  // Part II
  const solution2 = processLaserVaporization(map, solution1.coords)
  console.log(`PART II: solution = ${solution2}`)
})()

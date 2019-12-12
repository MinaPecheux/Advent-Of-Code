/*
 * ================================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: Javascript (NodeJS) version
 * ------------------------------------------------
 * Day 8: Space Image Format
 * ================================================
 */
'use strict'

const _ = require('lodash')
const fs = require('fs')
const expect = require('chai').expect

// [ Computation functions ]
// -------------------------
/* Part I */
/**
 * Decodes the image layers by splitting it in even chunks.
 * @param {string} inputs - Content of the image (as a string).
 * @param {int} width - Width of each layer in the image.
 * @param {int} height - Height of each layer in the image.
 * @returns {array(string)} - Layers in the image.
 */
const decodeLayers = (inputs, width, height) => {
  const layerSize = width * height
  const nLayers = Math.round(inputs.length / layerSize)
  return _.map(_.range(nLayers), (l) => {
    return _.join(_.slice(inputs, l*layerSize, (l+1)*layerSize), '')
  })
}

/**
 * Computes a basic checksum to verify the image is intact by finding the layer
   that has the fewest layer and computing the product of its number of 1s and
   2s.
 * @param {string} inputs - Content of the image (as a string).
 * @param {int} width - Width of each layer in the image.
 * @param {int} height - Height of each layer in the image.
 * @returns {int} - Checksum to verify the image validity.
 */
const computeChecksum = (inputs, width, height) => {
  const layers = decodeLayers(inputs, width, height)
  let bestNZeros = null, bestValue = null, nZeros, nOnes, nTwos
  _.each(layers, (layer) => {
    nZeros = (layer.match(/0/g) || []).length
    if (bestNZeros === null || nZeros < bestNZeros) {
      nOnes = (layer.match(/1/g) || []).length
      nTwos = (layer.match(/2/g) || []).length
      bestNZeros = nZeros
      bestValue = nOnes * nTwos
    }
  })
  return { checksum: bestValue, layers }
}

/* Part II */
/**
 * Displays the message that was sent (and has previously been divided into
   even layers).
 * @param {array(string)} layers - Layers of the image.
 * @param {int} width - Width of each layer in the image.
 * @param {int} height - Height of each layer in the image.
 */
const displayMessage = (layers, width, height) => {
  const marker = '█'
  // iterate through layers in reverse order to have the right depht overwrite
  const img = _.map(_.range(height), () => new Array(width).fill(' '))
  _.each(_.reverse(layers), (layer) => {
    // go through grid
    _.each(_.range(height), (y) => {
      _.each(_.range(width), (x) => {
        // and turn on/off pixels depending on the value (transparent has no
        // impact)
        if (layer[x + y * width] === '1') {
          img[y][x] = marker
        } else if (layer[x + y * width] === '0') {
          img[y][x] = ' '
        }
      })
    })
  })
  // display the message
  console.log('')
  _.each(_.range(height), (y) => {
    console.log(_.join(img[y], ''))
  })
  console.log('')
}

// [ Base tests ]
// --------------
/**
 * Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
const makeTests = () => {
  expect(decodeLayers('123456789012', 3, 2)).to.deep.equal([ '123456', '789012' ])
  expect(decodeLayers('210012011212', 3, 2)).to.deep.equal([ '210012', '011212' ])

  /* Part I */
  let tmp = computeChecksum('123456789012', 3, 2)
  expect(tmp.checksum).to.equal(1)
  tmp = computeChecksum('210012011212', 3, 2)
  expect(tmp.checksum).to.equal(6)
}

(() => {
  // check function results on example cases
  makeTests()
  
  // get input data
  const data = fs.readFileSync('../data/day8.txt')
  const inputs = data.toString()
  
  // Part I
  const solution1 = computeChecksum(inputs, 25, 6)
  console.log(`PART I: solution = ${solution1.checksum}`)
  
  // Part II
  const solution2 = displayMessage(solution1.layers, 25, 6)
  console.log('PART II: solution = (see the shell)')
})()

/**
 * \file day8.cpp
 * \brief AoC 2019 - Day 8 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 8: Space Image Format
 * =============================================
 */
#include <algorithm>
#include "utils.hpp"

// [ Computation functions ]
// -------------------------

/**
 * \fn std::vector<std::string> decodeLayers(std::string inputs, int width, int height)
 * \brief Decodes the image layers by splitting it in even chunks.
 *
 * \param inputs Content of the image (as a string).
 * \param width Width of each layer in the image.
 * \param height Height of each layer in the image.
 * \return Layers in the image.
 */
std::vector<std::string> decodeLayers(std::string inputs, int width, int height) {
  std::vector<std::string> layers;
  int layerSize = width * height;
  int nLayers = inputs.length() / layerSize;
  for (int n = 0; n < nLayers; n++) {
    layers.push_back(inputs.substr(n*layerSize, layerSize));
  }
  return layers;
}

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/
/**
 * \fn int computeChecksum(std::vector<std::string>& layers, std::string inputs, int width, int height)
 * \brief Computes a basic checksum to verify the image is intact by finding the
 * layer that has the fewest layer and computing the product of its number of
 * 1s and 2s.
 *
 * \param layers Reference to the vector of layers (to fill).
 * \param inputs Content of the image (as a string).
 * \param width Width of each layer in the image.
 * \param height Height of each layer in the image.
 * \return Checksum to verify the image validity.
 */
int computeChecksum(std::vector<std::string>& layers, std::string inputs, int width, int height) {
  layers = decodeLayers(inputs, width, height);
  int bestNZeros = -1, bestValue = -1;
  int nZeros, nOnes, nTwos;
  for (auto layer : layers) {
    nZeros = std::count(layer.begin(), layer.end(), '0');
    if (bestNZeros == -1 || nZeros < bestNZeros) {
      nOnes = std::count(layer.begin(), layer.end(), '1');
      nTwos = std::count(layer.begin(), layer.end(), '2');
      bestNZeros = nZeros;
      bestValue = nOnes * nTwos;
    }
  }
  return bestValue;
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/
/**
 * \fn void displayMessage(std::vector<std::string>& layers, int width, int height)
 * \brief Displays the message that was sent (and has previously been divided into
   even layers).
 *
 * \param layers Layers of the image.
 * \param width Width of each layer in the image.
 * \param height Height of each layer in the image.
 */
void displayMessage(std::vector<std::string>& layers, int width, int height) {
  std::string marker = "█";
  // iterate through layers in reverse order to have the right depht overwrite
  std::string img[height][width];
  for (int l = layers.size() - 1; l >= 0; l--) {
    // go through grid
    for (int y = 0; y < height; y++) {
      for (int x = 0; x < width; x++) {
        // and turn on/off pixels depending on the value (transparent has no
        // impact)
        if (layers[l][x + y*width] == '1') {
          img[y][x] = marker;
        } else if (layers[l][x + y*width] == '0') {
          img[y][x] = " ";
        }
      }
    }
  }
  // display the message
  std::cout << "\n";
  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      std::cout << img[y][x];
    }
    std::cout << "\n";
  }
  std::cout << "\n";
}

// [ Base tests ]
// --------------

/**
 * \fn void makeTests()
 * \brief Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
void makeTests() {
  std::vector<std::string> layers1;
  assert(computeChecksum(layers1, "123456789012", 3, 2) == 1);
  std::vector<std::string> layers2;
  assert(computeChecksum(layers2, "210012011212", 3, 2) == 6);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();

  // get input data
  std::string dataPath = "../data/day8.txt";
  std::string data = readFile(dataPath);
  std::vector<std::string> layers;
  
  // Part I
  int solution1 = computeChecksum(layers, data, 25, 6);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  displayMessage(layers, 25, 6);
  std::cout << "PART II (see the shell)" << '\n';
  
  return 0;
}

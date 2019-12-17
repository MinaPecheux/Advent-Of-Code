/**
 * \file day1.c
 * \brief AoC 2019 - Day 17 (C version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 1: The Tyranny of the Rocket Equation
 * =============================================
 */
#include "utils.h"
#include "parser.h"

/**
 * \fn int computeFuel(int mass)
 * \brief Computes the required fuel for a module of given mass.
 *
 * \param mass The mass of the module to compute the fuel consumption for.
 * \return Required amount of fuel.
 */
int computeFuel(int mass) {
  return mass / 3 - 2;
}

/**
 * \fn int computeTotalFuel(int mass)
 * \brief Computes the total required fuel for a module of given mass and the
 * added fuel, and so on. It works recursively until the computed amount of
 * fuel is zero or negative.
 *
 * \param mass The mass of the module to compute the fuel consumption for.
 * \return Required amount of fuel.
 */
int computeTotalFuel(int mass) {
  int f = computeFuel(mass);
  return (f <= 0) ? 0 : f + computeTotalFuel(f);
}

/**
 * \fn void makeTests()
 * \brief Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
void makeTests() {
  // Part I
  assert(computeFuel(12) == 2);
  assert(computeFuel(14) == 2);
  assert(computeFuel(1969) == 654);
  assert(computeFuel(100756) == 33583);
  // Part II
  assert(computeTotalFuel(14) == 2);
  assert(computeTotalFuel(1969) == 966);
  assert(computeTotalFuel(100756) == 50346);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();
  
  // get input data
  const char* dataPath = "../data/day1.txt";
  char* data = readFile(dataPath, 100);
  
  size_t dataLength;
  int* inputs = parseToIntsWithDelimiter(data, '\n', &dataLength);
  
  // Part I
  int solution1 = 0;
  int i;
  for (i = 0; i < dataLength; i++) {
    solution1 += computeFuel(inputs[i]);
  }
  printf("PART I: solution = %d\n", solution1);
  
  // Part II
  int solution2 = 0;
  for (i = 0; i < dataLength; i++) {
    solution2 += computeTotalFuel(inputs[i]);
  }
  printf("PART II: solution = %d\n", solution2);
  
  // clean up data
  free(data);
  free(inputs);
  return 0;
}

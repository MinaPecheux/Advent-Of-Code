/**
 * \file day1.cpp
 * \brief AoC 2019 - Day 1 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 1: The Tyranny of the Rocket Equation
 * =============================================
 */
#include "utils.hpp"
#include "parser.hpp"

// [ Computation functions ]
// -------------------------

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

// [ Base tests ]
// --------------

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
  std::string dataPath = "../data/day1.txt";
  std::string data = readFile(dataPath);
  std::vector<int> inputs = parseToIntsWithDelimiter(data, "\n");
  
  // Part I
  int solution1 = 0;
  for (auto i : inputs) {
    solution1 += computeFuel(i);
  }
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = 0;
  for (auto i : inputs) {
    solution2 += computeTotalFuel(i);
  }
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

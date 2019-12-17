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

int computeFuel(int mass) {
  return mass / 3 - 2;
}

int computeTotalFuel(int mass) {
  int f = computeFuel(mass);
  if (f <= 0) {
    return 0;
  }
  return f + computeTotalFuel(f);
}

void makeTests() {
  assert(computeFuel(12) == 2);
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

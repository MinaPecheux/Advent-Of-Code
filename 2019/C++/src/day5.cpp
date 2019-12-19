/**
 * \file day5.cpp
 * \brief AoC 2019 - Day 5 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 5: Sunny with a Chance of Asteroids
 * =============================================
 */
#include "utils.hpp"
#include "parser.hpp"
#include "intcode.hpp"

// [ Computation functions ]
// -------------------------

/*------------------------------------------------------------------------------
  Part I + II
------------------------------------------------------------------------------*/
/**
 * \fn int processInputs(std::vector<long> inputs, int input, bool debug=false)
 * \brief Executes the Intcode program on the provided inputs and computes the
 * final result.
 *
 * \param inputs List of long integers to execute as an Intcode program.
 * \param input Specific input for the program execution.
 * \return Final output of the program.
 */
int processInputs(std::vector<long> inputs, int input, bool debug=false) {
  // create program
  IntcodeProgram* program = new IntcodeProgram(inputs, debug);
  // insert input in memory
  program->pushMemory(input);
  // execute memory
  program->run();
  // extract result
  int result = (int)(program->getLastOutput());
  // clean up data
  delete program;
  return result;
}

// [ Base tests ]
// --------------

/**
 * \fn void makeTests()
 * \brief Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
void makeTests() {
  // Part I + II
  std::vector<long> inputs1 = { 3,0,4,0,99 };
  assert(processInputs(inputs1, 1) == 1);
  std::vector<long> inputs2 = { 3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 };
  assert(processInputs(inputs2, 0) == 0);
  assert(processInputs(inputs2, 1) == 1);
  std::vector<long> inputs3 = { 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,
    20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,
    1101,1000,1,20,4,20,1105,1,46,98,99 };
  assert(processInputs(inputs3, 1) == 999);
  assert(processInputs(inputs3, 8) == 1000);
  assert(processInputs(inputs3, 12) == 1001);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();
  
  // get input data
  std::string dataPath = "../data/day5.txt";
  std::string data = readFile(dataPath);
  std::vector<long> inputs = parseToLongsWithDelimiter(data, ",");
  
  // Part I
  int solution1 = processInputs(inputs, 1);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = processInputs(inputs, 5);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

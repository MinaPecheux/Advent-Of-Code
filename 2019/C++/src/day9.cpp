/**
 * \file day9.cpp
 * \brief AoC 2019 - Day 9 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 9: Sensor Boost
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
 * \fn long long processInputs(std::vector<long long> inputs, int input=-1, bool debug=false)
 * \brief Executes the Intcode program on the provided inputs and computes the
 * final result. Here, we use the [0, 4] phase settings range and no feedback
 * loop (so we only go through the amplifiers chain once).
 *
 * \param inputs List of long long integers to execute as an Intcode program.
 * \param input Integer to provide as input to the program.
 * \param debug Whether or not the IntcodeProgram should debug its execution at
 * each instruction processing.
 * \return Last output of the program.
 */
long long processInputs(std::vector<long long> inputs, int input=-1, bool debug=false) {
  // create program
  IntcodeProgram* program = new IntcodeProgram(inputs, debug);
  // insert input in memory
  if (input != -1) {
    program->pushMemory(input);
  }
  // execute memory
  program->run();
  // extract result
  long long result = program->getLastOutput();
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
  // test new instructions
  std::vector<long long> inputs1 = { 109,1,204,-1,1001,100,1,100,1008,100,16,101,
    1006,101,0,99 };
  IntcodeProgram* program = new IntcodeProgram(inputs1);
  program->run();
  std::string output;
  for (auto o : program->getOutput()) {
    output += std::to_string(o) + ",";
  }
  output = output.substr(0, output.length() - 1);
  assert(output == "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99");
  delete program;
  
  // Part II
  std::vector<long long> inputs2 = { 1102,34915192,34915192,7,4,7,99,0 };
  assert((std::to_string(processInputs(inputs2))).length() == 16);
  std::vector<long long> inputs3 = { 104,1125899906842624,99 };
  assert(processInputs(inputs3) == 1125899906842624);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();
  
  // get input data
  std::string dataPath = "../data/day9.txt";
  std::string data = readFile(dataPath);
  std::vector<long long> inputs = parseToLongLongsWithDelimiter(data, ",");
  
  // Part I
  long long solution1 = processInputs(inputs, 1);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  long long solution2 = processInputs(inputs, 2);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

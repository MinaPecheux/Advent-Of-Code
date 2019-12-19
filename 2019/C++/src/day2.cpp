/**
 * \file day2.cpp
 * \brief AoC 2019 - Day 2 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 2: 1202 Program Alarm
 * =============================================
 */
#include "utils.hpp"
#include "parser.hpp"
#include "intcode.hpp"

// [ Computation functions ]
// -------------------------

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/
/**
 * \fn int processInputs(std::vector<long long> inputs, bool restoreGravityAssist=false, bool debug=false)
 * \brief Executes the Intcode program on the provided inputs and computes the
 * final result.
 *
 * \param inputs List of long long integers to execute as an Intcode program.
 * \param restoreGravityAssist Whether or not to restore the gravity assist
 * by modifying the input program.
 * \param debug Whether or not the IntcodeProgram should debug its execution at
 * each instruction processing.
 * \return Final output of the program.
 */
int processInputs(std::vector<long long> inputs, bool restoreGravityAssist=false, bool debug=false) {
  // create and execute program
  IntcodeProgram* program = new IntcodeProgram(inputs, debug);
  // restore gravity assist?
  if (restoreGravityAssist) {
    program->setProgramData(1, 12);
    program->setProgramData(2, 2);
  }
  program->run();
  
  // extract result
  int result = (int)(program->getProgramData(0));
  
  // clean up data
  delete program;
  return result;
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/
/**
 * \fn int findPair(std::vector<long long> inputs, int wantedOutput, bool debug=false)
 * \brief A brute-force algorithm to systematically try all possible input pairs
 * until we find the one that gave the desired output (we can determine a
 * finished set of possible candidates since we know that each number is in the
 * [0, 99] range).
 *
 * \param inputs List of long long integers to execute as an Intcode program.
 * \param wantedOutput Desired output of the program.
 * \param debug Whether or not the IntcodeProgram should debug its execution at
 * each instruction processing.
 * \return Specific checksum that matches the desired output.
 */
int findPair(std::vector<long long> inputs, int wantedOutput, bool debug=false) {
  // prepare program
  IntcodeProgram* program = new IntcodeProgram(inputs, debug);
  int noun, verb;
  for (noun = 0; noun < 100; noun++) {
    for (verb = 0; verb < 100; verb++) {
      // reset program to initial state
      program->reset();
      // set up noun and verb
      program->setProgramData(1, noun);
      program->setProgramData(2, verb);
      // run and compare result
      program->run();
      if ((int)(program->getProgramData(0)) == wantedOutput) {
        // clean up data
        delete program;
        // return result
        return 100 * noun + verb;
      }
    }
  }
  // clean up data
  delete program;
  return -1;
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
  std::vector<long long> inputs1 = { 1,9,10,3,2,3,11,0,99,30,40,50 };
  assert(processInputs(inputs1) == 3500);
  std::vector<long long> inputs2 = { 1,0,0,0,99 };
  assert(processInputs(inputs2) == 2);
  std::vector<long long> inputs3 = { 2,3,0,3,99 };
  assert(processInputs(inputs3) == 2);
  std::vector<long long> inputs4 = { 2,4,4,5,99,0 };
  assert(processInputs(inputs4) == 2);
  std::vector<long long> inputs5 = { 1,1,1,4,99,5,6,0,99 };
  assert(processInputs(inputs5) == 30);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();
  
  // get input data
  std::string dataPath = "../data/day2.txt";
  std::string data = readFile(dataPath);
  std::vector<long long> inputs = parseToLongLongsWithDelimiter(data, ",");
  
  // Part I
  int solution1 = processInputs(inputs, true);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = findPair(inputs, 19690720);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

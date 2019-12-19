/**
 * \file day7.cpp
 * \brief AoC 2019 - Day 7 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 7: Amplification Circuit
 * =============================================
 */
#include <set>
#include <algorithm>
#include "utils.hpp"
#include "parser.hpp"
#include "intcode.hpp"

// [ Computation functions ]
// -------------------------
/**
 * \fn std::set<std::vector<int> > findPermutations(std::string s)
 * \brief Finds all the permutations of the digits in the given string of digits.
 *
 * \param s String of digits to permute.
 * \return All possible permutations.
 */
std::set<std::vector<int> > findPermutations(std::string s) {
  std::set<std::vector<int> > permutations;
  std::sort(s.begin(), s.end());
  std::string tmp;
  do {
    tmp = s.substr(0, 5);
    permutations.insert({ tmp[0] - '0', tmp[1] - '0', tmp[2] - '0',
      tmp[3] - '0', tmp[4] - '0' });
  } while(std::next_permutation(s.begin(), s.end()));
  return permutations;
}

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/
/**
 * \fn int processInputs(std::vector<long long> inputs, bool debug=false)
 * \brief Executes the Intcode program on the provided inputs and computes the
 * final result. Here, we use the [0, 4] phase settings range and no feedback
 * loop (so we only go through the amplifiers chain once).
 *
 * \param inputs List of long long integers to execute as an Intcode program.
 * \param debug Whether or not the IntcodeProgram should debug its execution at
 * each instruction processing.
 * \return Maximum input to the thrusters.
 */
int processInputs(std::vector<long long> inputs, bool debug=false) {
  // prepare all possible permutations for phase settings: we have X
  // possibilities for the first one, X-1 for the second one, X-2 for the third
  // one... (no replacement)
  int nAmplifiers = 5;
  std::set<std::vector<int> > candidatePhaseSettings = findPermutations("01234");
  // reset global instances IDs
  IntcodeProgram::INSTANCE_ID = 0;
  // create program instances
  std::vector<IntcodeProgram*> amplifiers;
  for (int i = 0; i < nAmplifiers; i++) {
    amplifiers.push_back(new IntcodeProgram(inputs, debug));
  }
  // check all possible settings
  int maxThrust = -1;
  int curAmplifier, phase, output;
  for (auto phaseSettings : candidatePhaseSettings) {
    // reset all amplifiers
    for (auto a : amplifiers) {
      a->reset();
    }
    // prepare input for first amplifier
    amplifiers[0]->pushMemory(0);
    for (curAmplifier = 0; curAmplifier < nAmplifiers; curAmplifier++) {
      phase = phaseSettings[curAmplifier];
      amplifiers[curAmplifier]->checkRunning(phase);
      // execut program
      amplifiers[curAmplifier]->runMultiple(amplifiers);
    }
    // check for max power
    output = (int)(amplifiers[curAmplifier - 1]->getLastOutput());
    if (output > maxThrust) {
      maxThrust = output;
    }
  }
  // clean up data
  for (auto a : amplifiers) {
    delete a;
  }
  return maxThrust;
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/
/**
 * \fn int processInputsFeedback(std::vector<long long> inputs, bool debug=false)
 * \brief Executes the Intcode program on the provided inputs and computes the
 * final result. Here, we use the [5, 9] phase settings range and a feedback
 * loop to pass through the amplifiers multiple times.
 *
 * \param inputs List of long long integers to execute as an Intcode program.
 * \param debug Whether or not the IntcodeProgram should debug its execution at
 * each instruction processing.
 * \return Maximum input to the thrusters.
 */
int processInputsFeedback(std::vector<long long> inputs, bool debug=false) {
  // prepare all possible permutations for phase settings: we have X
  // possibilities for the first one, X-1 for the second one, X-2 for the third
  // one... (no replacement)
  int nAmplifiers = 5;
  std::set<std::vector<int> > candidatePhaseSettings = findPermutations("56789");
  // reset global instances IDs
  IntcodeProgram::INSTANCE_ID = 0;
  // create program instances
  std::vector<IntcodeProgram*> amplifiers;
  for (int i = 0; i < nAmplifiers; i++) {
    amplifiers.push_back(new IntcodeProgram(inputs, debug));
  }
  // check all possible settings
  int maxThrust = -1;
  bool running;
  int curAmplifier, nextAmplifier, phase, output;
  for (auto phaseSettings : candidatePhaseSettings) {
    // reset all amplifiers
    for (auto a : amplifiers) {
      a->reset();
    }
    // prepare input for first amplifier
    amplifiers[0]->pushMemory(0);
    curAmplifier = 0;
    running = true;
    while (running) {
      // if necessary, initialize amplifier
      phase = phaseSettings[curAmplifier];
      amplifiers[curAmplifier]->checkRunning(phase);
      // run amplifier (either from scratch or from where it last stopped)
      nextAmplifier = amplifiers[curAmplifier]->runMultiple(amplifiers);
      // if amplifiers loop has halted
      if (nextAmplifier == -1) {
        running = false;
        break;
      }
      // else reassign the current amplifier index for next iteration
      else {
        curAmplifier = nextAmplifier;
      }
     }
    // check for max power
    output = (int)(amplifiers[curAmplifier]->getLastOutput());
    if (output > maxThrust) {
      maxThrust = output;
    }
  }
  // clean up data
  for (auto a : amplifiers) {
    delete a;
  }
  return maxThrust;
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
  std::vector<long long> inputs1 = { 3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0 };
  assert(processInputs(inputs1) == 43210);
  
  // Part II
  std::vector<long long> inputs2 = { 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,
    4,27,1001,28,-1,28,1005,28,6,99,0,0,5 };
  assert(processInputsFeedback(inputs2) == 139629729);
  std::vector<long long> inputs3 = { 3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,
    1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,
    55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10 };
  assert(processInputsFeedback(inputs3) == 18216);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();
  
  // get input data
  std::string dataPath = "../data/day7.txt";
  std::string data = readFile(dataPath);
  std::vector<long long> inputs = parseToLongLongsWithDelimiter(data, ",");
  
  // Part I
  int solution1 = processInputs(inputs);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = processInputsFeedback(inputs);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

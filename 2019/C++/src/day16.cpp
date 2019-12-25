/**
 * \file day16.cpp
 * \brief AoC 2019 - Day 16 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 16: Flawed Frequency Transmission
 * =============================================
 */
#include "utils.hpp"
#include "parser.hpp"

// [ Computation functions ]
// -------------------------

int extractOnesDigit(int value) {
  std::string s = std::to_string(value);
  return s[s.length() - 1] - '0';
}

/**
 * \fn std::vector<int> computePhase(std::vector<int> inputs, int skipDigits=-1)
 * \brief Computes the next phase by applying the pattern to the given inputs.
 *
 * \param inputs Current inputs to apply the pattern to.
 * \param skipDigits Number of digits to skip in the computation. The function
 * assumes that if this variable is not None, then it is greater than or equal
 * to half of the length of inputs.
 * \return New phase state.
 */
std::vector<int> computePhase(std::vector<int> inputs, int skipDigits=-1) {
  int n = inputs.size();
  std::vector<int> output;
  // compute the full result
  int i, idx;
  if (skipDigits == -1) {
    int s, l, d;
    for (idx = 0; idx < n; idx++) {
      s = 0;
      l = idx + 1;
      // apply the pattern on the inputs: either positive (+1) or negative (-1)
      // contribution from some parts of the inputs
      i = idx;
      while (i < n) {
        for (int j = i; j < i+l && j < n; j++) s += inputs[j];
        for (int j = i+2*l; j < i+3*l && j < n; j++) s -= inputs[j];
        i += 4 * l;
      }
      // keep only ones digits
      d = extractOnesDigit(s);
      output.push_back(d);
    }
  }
  // or skip ahead to only compute the end (assumes that the skip index is
  // greather than or equal to half of the inputs length)
  else {
    output = std::vector<int>(n, 0);
    output.back() = inputs.back();
    i = n - 2;
    for (idx = n - 2; idx > skipDigits - 1; idx--) {
      output[idx] = extractOnesDigit(output[idx + 1] + inputs[i]);
      i--;
    }
  }
  return output;
}

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/

/**
 * \fn std::string computePhases(int nPhases, std::vector<int> inputs)
 * \brief Process the inputs phase by phase until the required number of phases
 * has been reached.
 *
 * \param nPhases Number of phases to compute.
 * \param inputs Initial problem input to process.
 * \return Final state of the inputs after all the phases have been computed
 * (only the first eight digits, as a string).
 */
std::string computePhases(int nPhases, std::vector<int> inputs) {
  // compute iterations
  std::vector<int> current = inputs;
  for (int i = 0; i < nPhases; i++) {
    current = computePhase(current);
  }
  // return just the first eight digits as a string
  std::string result = "";
  for (int i = 0; i < 8; i++) {
    result += std::to_string(current[i]);
  }
  return result;
}

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/

/**
 * \fn std::string computePhasesNohead(int nPhases, std::vector<int> inputs, int skipDigits)
 * \brief Process the inputs phase by phase until the required number of phases
 * has been reached and returns only a part of it while skipping a given
 * number of digits from the start. It assumes that the number of passed digits
 * is greater than or equal to half of the length of initial inputs.
 *
 * \param nPhases Number of phases to compute.
 * \param inputs Initial problem input to process.
 * \param skipDigits Number of digits to skip in the final result.
 * \return Final state of the inputs after all the phases have been computed
 * (only the first eight digits, as a string).
 */
std::string computePhasesNohead(int nPhases, std::vector<int> inputs, int skipDigits) {
  // compute iterations
  std::vector<int> current = inputs;
  for (int i = 0; i < nPhases; i++) {
    current = computePhase(current, skipDigits);
  }
  // return just the first eight digits as a string
  std::string result = "";
  for (int i = skipDigits; i < skipDigits + 8; i++) {
    result += std::to_string(current[i]);
  }
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
  std::vector<int> inputs1 = { 1,2,3,4,5,6,7,8 };
  assert(computePhases(4, inputs1) == "01029498");
  std::vector<int> inputs2 = { 8,0,8,7,1,2,2,4,5,8,5,9,1,4,5,4,6,6,1,9,0,8,3,2,1,
    8,6,4,5,5,9,5 };
  assert(computePhases(100, inputs2) == "24176176");
  std::vector<int> inputs3 = { 1,9,6,1,7,8,0,4,2,0,7,2,0,2,2,0,9,1,4,4,9,1,6,0,4,
    4,1,8,9,9,1,7 };
  assert(computePhases(100, inputs3) == "73745418");
  std::vector<int> inputs4 = { 6,9,3,1,7,1,6,3,4,9,2,9,4,8,6,0,6,3,3,5,9,9,5,
    9,2,4,3,1,9,8,7,3 };
  assert(computePhases(100, inputs4) == "52432133");
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  // makeTests();
  
  // get input data
  std::string dataPath = "../data/day16.txt";
  std::string data = readFile(dataPath);
  std::vector<int> inputs = parseCharacters<int>(data);
  
  // Part I
  std::string solution1 = computePhases(100, inputs);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  std::vector<int> inp;
  for (int n = 0; n < 10000; n++) {
    inp.insert(inp.end(), inputs.begin(), inputs.end());
  }
  int skipDigits = std::stoi(data.substr(0, 7));
  std::string solution2 = computePhasesNohead(100, inp, skipDigits);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

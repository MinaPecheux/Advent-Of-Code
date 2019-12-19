/**
 * \file day4.cpp
 * \brief AoC 2019 - Day 4 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 4: Secure Container
 * =============================================
 */
#include <map>
#include "utils.hpp"

// [ Computation functions ]
// -------------------------

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/
/**
 * \fn bool numberIsOkP1(int number)
 * \brief Checks if a number meets the password criteria of Part I:
 * - length of 6 digits
 * - two adjacent digits are the same
 * - going left from right, digits never decrease (i.e. they increase or
 * stay the same)
 *
 * \param number Number to check.
 * \return Number validity.
 */
bool numberIsOkP1(int number) {
  std::string nStr = std::to_string(number);
  if (nStr.length() != 6) {
    return false;
  }
  bool hasDuplicate = false;
  int prevC = -1, c;
  for (auto cStr : nStr) {
    c = cStr - '0';
    if (c < prevC) {
      return false;
    }
    if (c == prevC) {
      hasDuplicate = true;
    }
    prevC = c;
  }
  return hasDuplicate;
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/
/**
 * \fn bool numberIsOkP2(int number)
 * \brief Checks if a number meets the password criteria of Part I:
 * - same as criteria for Part I
 * - plus the two adjacent digits are not part of a larger group of matching
 * digits (i.e. they are just a double, not a longer sequence of same digit)
 *
 * \param number Number to check.
 * \return Number validity.
 */
bool numberIsOkP2(int number) {
  std::string nStr = std::to_string(number);
  if (nStr.length() != 6) {
    return false;
  }
  int prevC = -1, c;
  std::map<int,int> counts;
  for (auto cStr : nStr) {
    c = cStr - '0';
    if (c < prevC) {
      return false;
    }
    prevC = c;
    counts[c]++;
  }
  for (auto c : counts) {
    if (c.second == 2) {
      return true;
    }
  }
  return false;
}

/**
 * \fn int getCountOfValidNumbers(int min, int max, int partNumber)
 * \brief Finds all the valid numbers (that meet the given password criteria) in
 * the range given by the inputs.
 *
 * \param min Minimum value (inclusive) for the numbers to check.
 * \param max Maximum value (inclusive) for the numbers to check.
 * \param partNumber Reference of the problem part number (to know which check
 * function to call).
 * \return Count of numbers in the range that pass the test.
 */
int getCountOfValidNumbers(int min, int max, int partNumber) {
  int count = 0;
  if (partNumber == 1) {
    for (int n = min; n < max + 1; n++) {
      if (numberIsOkP1(n)) {
        count ++;
      }
    }
  } else if (partNumber == 2) {
    for (int n = min; n < max + 1; n++) {
      if (numberIsOkP2(n)) {
        count ++;
      }
    }
  }
  return count;
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
  assert(numberIsOkP1(111111) == true);
  assert(numberIsOkP1(223450) == false);
  assert(numberIsOkP1(123789) == false);
  
  // Part II
  assert(numberIsOkP2(112233) == true);
  assert(numberIsOkP2(123444) == false);
  assert(numberIsOkP2(111122) == true);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();
  
  // Part I
  int solution1 = getCountOfValidNumbers(248345, 746315, 1);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = getCountOfValidNumbers(248345, 746315, 2);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

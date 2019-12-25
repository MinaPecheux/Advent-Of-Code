/**
 * \file utils.hpp
 * \brief AoC 2019 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Header file for utils.cpp.
 * Set of util functions for the Advent of Code 2019 challenge.
 * Contains methods for the processing of files, strings...
 */
#pragma once

#include <iostream>
#include <vector>
#include <set>
#include <string>
#include <cassert>

/*------------------------------------------------------------------------------
  FILES
------------------------------------------------------------------------------*/
std::string readFile(std::string filepath);

/*------------------------------------------------------------------------------
  STRINGS
------------------------------------------------------------------------------*/
std::string strFormat(const std::string fmt_str, ...);
std::vector<std::string> strSplit(std::string srcStr, std::string delimiter);

/*------------------------------------------------------------------------------
  COMBINATORICS
------------------------------------------------------------------------------*/
std::string rangeToStr(int min, int max);

// (template functions must be prototyped and defined in the same file!)
/**
 * \fn template<typename T> std::set<std::vector<T> > permutations(std::string s, int length)
 * \brief Finds all the permutations of the digits in the given string of digits
 * with a given length.
 *
 * \param s String of digits to permute.
 * \param length Number of items in each permutation.
 * \return All possible permutations.
 */
template<typename T>
std::set<std::vector<T> > permutations(std::string s, int length) {
  std::set<std::vector<T> > perms;
  std::sort(s.begin(), s.end());
  std::string tmp;
  std::vector<T> v;
  do {
    v.clear();
    tmp = s.substr(0, length);
    for (int i = 0; i < length; i++) {
      v.push_back(tmp[i] - '0');
    }
    perms.insert(v);
  } while(std::next_permutation(s.begin(), s.end()));
  return perms;
}

/**
 * \fn template<typename T> std::set<std::vector<T> > combinations(std::string s, int length)
 * \brief Finds all the combinations of the digits in the given string of digits
 * with a given length.
 *
 * \param s String of digits to combine.
 * \param length Number of items in each combination.
 * \return All possible combinations.
 */
template<typename T>
std::set<std::vector<T> > combinations(std::string s, int length) {
  std::set<std::vector<T> > combs;
  std::sort(s.begin(), s.end());
  std::string tmp;
  std::vector<T> v;
  do {
    v.clear();
    tmp = s.substr(0, length);
    for (int i = 0; i < length; i++) {
      v.push_back(tmp[i] - '0');
    }
    std::sort(v.begin(), v.end());
    combs.insert(v);
  } while(std::next_permutation(s.begin(), s.end()));
  return combs;
}

/*------------------------------------------------------------------------------
  CONVERTERS
------------------------------------------------------------------------------*/
void decomposeCoordinates(std::string pos, int& x, int& y);

/**
 * \file parser.hpp
 * \brief AoC 2019 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Header file for parser.cpp.
 * Set of parsing functions for the Advent of Code 2019 challenge.
 * Contains various methods to transform an incoming string into an array of
 * values (ints, longs...) using different processes (split by delimiter...).
 */
#pragma once

#include <iostream>
#include <vector>
#include <string>

#include <utils.hpp>

/*------------------------------------------------------------------------------
  WITH DELIMITER
------------------------------------------------------------------------------*/

// (template functions must be prototyped and defined in the same file!)
/**
 * \fn template<typename T> std::vector<T> parseWithDelimiter(std::string data, std::string delimiter)
 * \brief Parses the incoming data into an array of values (with the given type).
 *
 * \param data Provided data to split.
 * \param delimiter Delimiter to use to split the data.
 * \return Parsed data.
 */
template<typename T>
std::vector<T> parseWithDelimiter(std::string data, std::string delimiter) {
  std::vector<std::string> parts = strSplit(data, delimiter);
  std::vector<T> parsed;
  for (auto p : parts) {
    if (std::is_same<T,int>::value) {
      parsed.push_back(stoi(p));
    } else if (std::is_same<T,long>::value) {
      parsed.push_back(stol(p));
    } else if (std::is_same<T,long long>::value) {
      parsed.push_back(stoll(p));
    }
  }
  return parsed;
}

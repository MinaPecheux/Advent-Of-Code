/**
 * \file parser.cpp
 * \brief AoC 2019 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Set of parsing functions for the Advent of Code 2019 challenge.
 * Contains various methods to transform an incoming string into an array of
 * values (ints, longs...) using different processes (split by delimiter...).
 */
#include "parser.hpp"
#include "utils.hpp"

using namespace std;

/*------------------------------------------------------------------------------
  WITH DELIMITER
------------------------------------------------------------------------------*/
/**
 * \fn vector<int> parseToIntsWithDelimiter(string data, string delimiter)
 * \brief Parses the incoming data into an array of ints.
 *
 * \param data Provided problem data.
 * \param delimiter Delimiter to use to split the data.
 * \return Parsed data.
 */
vector<int> parseToIntsWithDelimiter(string data, string delimiter) {
  vector<string> parts = strSplit(data, delimiter);
  vector<int> parsed;
  for (auto p : parts) {
    parsed.push_back(stoi(p));
  }
  return parsed;
}

/**
 * \fn vector<long> parseToIntsWithDelimiter(string data, string delimiter)
 * \brief Parses the incoming data into an array of ints.
 *
 * \param data Provided problem data.
 * \param delimiter Delimiter to use to split the data.
 * \return Parsed data.
 */
vector<long> parseToLongsWithDelimiter(string data, string delimiter) {
  vector<string> parts = strSplit(data, delimiter);
  vector<long> parsed;
  for (auto p : parts) {
    parsed.push_back(stol(p));
  }
  return parsed;
}

/**
 * \fn vector<long long> parseToLongLongsWithDelimiter(string data, string delimiter)
 * \brief Parses the incoming data into an array of ints.
 *
 * \param data Provided problem data.
 * \param delimiter Delimiter to use to split the data.
 * \return Parsed data.
 */
vector<long long> parseToLongLongsWithDelimiter(string data, string delimiter) {
  vector<string> parts = strSplit(data, delimiter);
  vector<long long> parsed;
  for (auto p : parts) {
    parsed.push_back(stoll(p));
  }
  return parsed;
}

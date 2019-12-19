/**
 * \file utils.cpp
 * \brief AoC 2019 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Set of util functions for the Advent of Code 2019 challenge.
 * Contains methods for the processing of files, strings...
 */
#include <fstream>
#include <sstream>
#include "utils.hpp"

using namespace std;

// [ Files ]
// ---------

/**
 * \fn string readFile(string filepath)
 * \brief Reads the content of a file entirely.
 *
 * \param filepath Path of the file to read.
 * \return Content of the file (as a string).
 */
string readFile(string filepath) {
  // open file (and check)
  ifstream f(filepath);
  if (!f.is_open()) {
    cerr << "Error: cannot read file \"" << filepath << "\"! Aborting." << endl;
    exit(1);
  }
  stringstream buffer;
  buffer << f.rdbuf();
  f.close();
  return buffer.str();
}

// [ Strings ]
// -----------

/**
 * \fn vector<string> strSplit(string s, string delimiter)
 * \brief Splits a string into an array of substrings using the given delimiter.
 * (From: https://stackoverflow.com/questions/14265581/parse-split-a-string-in-c-using-string-delimiter-standard-c)
 *
 * \param s String to split.
 * \param delimiter Delimiter to use to split the data.
 * \return Array of substrings after the split.
 */
vector<string> strSplit(string s, string delimiter) {
  size_t pos = 0;
  string token;
  vector<string> parts;
  while ((pos = s.find(delimiter)) != string::npos) {
      token = s.substr(0, pos);
      if (token.length() > 0) {
        parts.push_back(token);
      }
      s.erase(0, pos + delimiter.length());
  }
  token = s.substr(0, pos);
  if (token.length() > 0) {
    parts.push_back(token);
  }
  return parts;
}

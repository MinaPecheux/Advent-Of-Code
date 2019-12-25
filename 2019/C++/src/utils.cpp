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
#include <cstdarg>
#include <memory>
#include <algorithm>
#include "utils.hpp"

using namespace std;

/*------------------------------------------------------------------------------
  FILES
------------------------------------------------------------------------------*/

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

/*------------------------------------------------------------------------------
  STRINGS
------------------------------------------------------------------------------*/

/**
 * \fn string strFormat(const string fmt_str, ...)
 * \brief Formats a string with the given variables and returns the result as
 * another string.
 * (From: https://stackoverflow.com/questions/2342162/stdstring-formatting-like-sprintf)
 *
 * \param fmtStr Formatting string.
 * \return Formatted string.
 */
string strFormat(const string fmtStr, ...) {
  /* Reserve two times as much as the length of the fmtStr */
  int finalN, n = ((int)fmtStr.size()) * 2;
  unique_ptr<char[]> formatted;
  va_list ap;
  while (1) {
    /* Wrap the plain char array into the unique_ptr */
    formatted.reset(new char[n]);
    strcpy(&formatted[0], fmtStr.c_str());
    va_start(ap, fmtStr);
    finalN = vsnprintf(&formatted[0], n, fmtStr.c_str(), ap);
    va_end(ap);
    if (finalN < 0 || finalN >= n)
      n += abs(finalN - n + 1);
    else
      break;
  }
  return string(formatted.get());
}

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

/**
 * \fn void progressBar(int current, int total, int width=50)
 * \brief Shows a progress bar.
 *
 * \param current Current progress value.
 * \param total Total progress value.
 * \param width Total display width.
 */
void progressBar(int current, int total, int width) {
  int debugLength = to_string(total).length();
  int c = width * current / total;
  cout << "\r";
  for (int i = 0; i < c; i++) cout << "■";
  for (int i = c; i < width; i++) cout << " ";
  for (int i = to_string(current).length(); i <= debugLength; i++) {
    cout << " ";
  }
  cout << current << "/" << total;
}

/*------------------------------------------------------------------------------
  COMBINATORICS
------------------------------------------------------------------------------*/
/**
 * \fn std::string rangeToStr(int min, int max)
 * \brief Creates a string of digits iterating through the given range from min
 * (inclusive) to max (exclusive).
 *
 * \param min Minimum value in the range.
 * \param max Maximum value up the range.
 * \return String of all digits in the range.
 */
std::string rangeToStr(int min, int max) {
  std::string s;
  for (int i = min; i < max; i++) {
    s += std::to_string(i);
  }
  return s;
}

/*------------------------------------------------------------------------------
  CONVERTERS
------------------------------------------------------------------------------*/
/**
 * \fn void decomposeCoordinates(std::string pos, int& x, int& y)
 * \brief Decomposes a string in the "x,y" format into two integer coordinates.
 *
 * \param pos Coordinate to decompose.
 * \param x Reference to the integer where to store the horizontal coordinate.
 * \param y Reference to the integer where to store the vertical coordinate.
 */
void decomposeCoordinates(string pos, int& x, int& y) {
  vector<string> tmp = strSplit(pos, ",");
  x = stoi(tmp[0]);
  y = stoi(tmp[1]);
}

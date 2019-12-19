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
#ifndef __BASE_LIBS_H__
#define __BASE_LIBS_H__
#include <iostream>
#include <vector>
#include <string>
#include <cassert>
#endif

// [ Files ]
std::string readFile(std::string filepath);

// [ Strings ]
std::vector<std::string> strSplit(std::string srcStr, std::string delimiter);

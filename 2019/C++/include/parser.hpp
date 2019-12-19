/**
 * \file parser.hpp
 * \brief AoC 2019 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Header file for parser.cpp.
 * Set of parsing functions for the Advent of Code 2019 challenge.
 * Contains various methods to transform an incoming string into an array of
 * values (ints, floats...) using different processes (split by delimiter...).
 */
#ifndef __BASE_LIBS_H__
#define __BASE_LIBS_H__
#include <iostream>
#include <vector>
#include <string>
#endif

std::vector<int> parseToIntsWithDelimiter(std::string data, std::string delimiter);
std::vector<long> parseToLongsWithDelimiter(std::string data, std::string delimiter);

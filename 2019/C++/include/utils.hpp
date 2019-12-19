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

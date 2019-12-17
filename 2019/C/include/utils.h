/**
 * \file utils.h
 * \brief AoC 2019 (C version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Header file for utils.c.
 * Set of util functions for the Advent of Code 2019 challenge.
 * Contains methods for the processing of files, strings...
 */
#ifndef __BASE_LIBS_H__
#define __BASE_LIBS_H__
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <assert.h>
#endif

// [ Files ]
char* readFile(const char* filepath, int maxLength);

// [ Strings ]
char** strSplit(char* srcStr, const char delimiter, size_t* numSubStr);

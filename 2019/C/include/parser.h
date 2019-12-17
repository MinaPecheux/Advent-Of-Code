/**
 * \file parser.c
 * \brief AoC 2019 (C version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Header file for parser.c.
 * Set of parsing functions for the Advent of Code 2019 challenge.
 * Contains various methods to transform an incoming string into an array of
 * values (ints, floats...) using different processes (split by delimiter...).
 */
#ifndef __BASE_LIBS_H__
#define __BASE_LIBS_H__
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#endif

int* parseToIntsWithDelimiter(char* data, const char delimiter, size_t* dataLength);

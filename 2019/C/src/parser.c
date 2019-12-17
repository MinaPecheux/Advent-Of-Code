/**
 * \file parser.c
 * \brief AoC 2019 (C version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Set of parsing functions for the Advent of Code 2019 challenge.
 * Contains various methods to transform an incoming string into an array of
 * values (ints, floats...) using different processes (split by delimiter...).
 */
#include "parser.h"
#include "utils.h"

/**
 * \fn int* parseToIntsWithDelimiter(char* data, const char delimiter, size_t* dataLength)
 * \brief Parses the incoming data into processable inputs.
 *
 * \param data Provided problem data.
 * \param delimiter Delimiter to use to split the data.
 * \param dataLength Placeholder for the number of items in the splitted data.
 * \return Parsed data.
 */
int* parseToIntsWithDelimiter(char* data, const char delimiter, size_t* dataLength) {
  char* srcStr = strdup(data);
  char** subStr = strSplit(srcStr, delimiter, dataLength);
  if (subStr == NULL) {
    return NULL;
  }
  int* parsed = (int*)malloc((*dataLength) * sizeof(int));
  int i;
  for (i = 0; i < *dataLength; i++) {
    parsed[i] = atoi(subStr[i]);
  }
  free(srcStr);
  free(subStr);
  return parsed;
}

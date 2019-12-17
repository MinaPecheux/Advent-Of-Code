/**
 * \file utils.c
 * \brief AoC 2019 (C version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * Set of util functions for the Advent of Code 2019 challenge.
 * Contains methods for the processing of files, strings...
 */
#include "utils.h"

// [ Files ]
// ---------

/**
 * \fn char* readFile(const char* filepath, int maxLength)
 * \brief Reads the content of a file entirely.
 *
 * \param filepath Path of the file to read.
 * \param maxLength Maximum number of characters in the file.
 * \return Content of the file (as a string).
 */
char* readFile(const char* filepath, int maxLength) {
  FILE *fp = fopen(filepath, "r");
  char* content = (char *) malloc(maxLength * sizeof(char));
  char *c = content;
  while (fscanf(fp, "%c", c) == 1) ++c;
  fclose(fp);
  return content;
}

// [ Strings ]
// -----------

/**
 * \fn char** strSplit(char* srcStr, const char delimiter, size_t* numSubStr)
 * \brief Splits a string into an array of substrings using the given delimiter.
 * (From: https://stackoverflow.com/questions/9210528/split-string-with-delimiters-in-c)
 *
 * \param srcStr String to split.
 * \param delimiter Delimiter to use to split the data.
 * \param numSubStr Placeholder for the number of items in the splitted data.
 * \return Array of substrings after the split.
 */
char** strSplit(char* srcStr, const char delimiter, size_t* numSubStr) {
  //replace delimiter's with zeros and count how many
  //sub strings with length >= 1 exist
  *numSubStr = 0;
  char *srcStrTmp = srcStr;
  int foundDelim = 1;
  while (*srcStrTmp) {
    if (*srcStrTmp == delimiter) {
      *srcStrTmp = 0;
      foundDelim = 1;
    } else if (foundDelim) { //found first character of a new string
      (*numSubStr)++;
      foundDelim = 0;
    }
    srcStrTmp++;
  }
  if (*numSubStr <= 0) {
    return NULL;
  }

  char **subStrings = (char **) malloc((*numSubStr) * (sizeof(char*)) + 1);
  const char *src_str_terminator = srcStrTmp;
  srcStrTmp = srcStr;
  int foundNull = 1;
  size_t idx = 0;
  while (srcStrTmp < src_str_terminator) {
    if (!*srcStrTmp) {
      foundNull = 1;
    } else if (foundNull) {
      subStrings[idx++] = srcStrTmp;
      foundNull = 0;
    }
    srcStrTmp++;
  }
  subStrings[*numSubStr] = NULL;

  return subStrings;
}

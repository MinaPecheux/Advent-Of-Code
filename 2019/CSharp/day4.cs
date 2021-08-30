/*
 * =============================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: C# version
 * ---------------------------------------------
 * Day 4: Secure Container
 * ============================================= */

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace CSharp2019
{
    class Day4
    {
        // [ Input parsing functions ]
        // ---------------------------

        /// <summary>Parses the incoming data into processable inputs.</summary>
        /// <param name="data">Provided problem data.</param>
        /// <returns>Parsed data as a list of ints.</returns>
        static int[] ParseInput(string data)
        {
          return data
            .Split('-')
            .Select(l => int.Parse(l))
            .ToArray();
        }

        // [ Computation functions ]
        // -------------------------

        delegate bool CheckFunction(int number);

        /// <summary>Finds all the valid numbers (that meet the given password criteria) in
        /// the range given by the inputs.</summary>
        /// <param name="inputs">Minimum and maximum value (inclusive) for the numbers to check.</param>
        /// <param name="checkFn">Validity function to pass.</param>
        /// <returns>Count of numbers in the range that pass the test.</returns>
        static int GetCountOfValidNumbers(int[] inputs, CheckFunction checkFn)
        {
          int min = inputs[0];
          int max = inputs[1];
          int count = 0;
          for (int n = min; n <= max; n++) {
            if (checkFn(n)) count++;
          }
          return count;
        }

        // == PART I

        /// <summary>Checks if a number meets the password criteria of Part I:
        /// - length of 6 digits
        /// - two adjacent digits are the same
        /// - going left from right, digits never decrease (i.e. they increase or
        /// stay the same)</summary>
        /// <param name="number">Number to check.</param>
        /// <returns>Number validity.</returns>
        static bool NumberIsOkPartI(int number)
        {
          string nStr = number.ToString();
          if (nStr.Length != 6) return false;
          int prevC = -1, c;
          bool hasDuplicate = false;
          foreach (char cStr in nStr) {
            c = (int) (cStr);
            if (c < prevC) return false;
            if (c == prevC) hasDuplicate = true;
            prevC = c;
          }
          return hasDuplicate;
        }

        // == PART II

        /// <summary>Checks if a number meets the password criteria of Part II:
        /// - same as criteria for Part I
        /// - plus the two adjacent digits are not part of a larger group of matching
        /// digits (i.e. they are just a double, not a longer sequence of same digit)</summary>
        /// <param name="number">Number to check.</param>
        /// <returns>Number validity.</returns>
        static bool NumberIsOkPartII(int number)
        {
          string nStr = number.ToString();
          if (nStr.Length != 6) return false;
          int prevC = -1, c;
          foreach (char cStr in nStr) {
            c = (int) (cStr);
            if (c < prevC) return false;
            prevC = c;
          }
          Dictionary<char, int> counts = nStr.GroupBy(x => x).ToDictionary(gr => gr.Key, gr => gr.Count());
          return counts.Values.ToList().Contains(2);
        }

        // [ Base tests ]
        // --------------
        static void MakeTests()
        {
          // == PART I
          Debug.Assert(NumberIsOkPartI(111111) == true);
          Debug.Assert(NumberIsOkPartI(223450) == false);
          Debug.Assert(NumberIsOkPartI(123789) == false);

          // == PART II
          Debug.Assert(NumberIsOkPartII(112233) == true);
          Debug.Assert(NumberIsOkPartII(123444) == false);
          Debug.Assert(NumberIsOkPartII(111122) == true);
        }

        public static void Run()
        {
            // check function results on example cases
            MakeTests();

            // get input data
            string data = "248345-746315";
            int[] inputs = ParseInput(data);

            // == PART I
            int solution = GetCountOfValidNumbers(inputs, NumberIsOkPartI);
            Console.WriteLine($"PART I: solution = {solution}");

            // == PART II
            solution = GetCountOfValidNumbers(inputs, NumberIsOkPartII);
            Console.WriteLine($"PART II: solution = {solution}");
        }
    }
}

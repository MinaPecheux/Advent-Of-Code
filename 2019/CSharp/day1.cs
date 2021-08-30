/*
 * =============================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: C# version
 * ---------------------------------------------
 * Day 1: The Tyranny of the Rocket Equation
 * ============================================= */

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace CSharp2019
{
    class Day1
    {
        // [ Input parsing functions ]
        // ---------------------------

        /// <summary>Parses the incoming data into processable inputs.</summary>
        /// <param name="lines">Provided problem data.</param>
        /// <returns>Parsed data as a list of ints.</returns>
        static int[] ParseInput(IEnumerable<string> lines)
        {
            return lines
                .Where(l => l.Length > 0)
                .Select(l => int.Parse(l))
                .ToArray();
        }

        // [ Computation functions ]
        // -------------------------
        // == PART I

        /// <summary>Computes the required fuel for a module of given mass.</summary>
        /// <param name="moduleMass">The mass of the module to compute the fuel consumption for.</param>
        /// <returns>Required amount of fuel.</returns>
        static int ComputeFuel(int moduleMass)
        {
            return (int) Math.Floor(moduleMass / 3.0f) - 2;
        }

        // == PART II

        /// <summary>Computes the total required fuel for a module of given mass and the
        /// added fuel, and so on. It works recursively until the computed amount of
        /// fuel is zero or negative.</summary>
        /// <param name="moduleMass">The mass of the module to compute the fuel consumption for.</param>
        /// <returns>Required amount of fuel.</returns>
        static int ComputeTotalFuel(int moduleMass)
        {
            int fuel = ComputeFuel(moduleMass);
            return fuel <= 0 ? 0 : fuel + ComputeTotalFuel(fuel);
        }

        // [ Base tests ]
        // --------------
        static void MakeTests()
        {
            // == PART I
            Debug.Assert(ComputeFuel(12) == 2);
            Debug.Assert(ComputeFuel(14) == 2);
            Debug.Assert(ComputeFuel(1969) == 654);
            Debug.Assert(ComputeFuel(100756) == 33583);

            // == PART II
            Debug.Assert(ComputeTotalFuel(14) == 2);
            Debug.Assert(ComputeTotalFuel(1969) == 966);
            Debug.Assert(ComputeTotalFuel(100756) == 50346);
        }

        static void Main(string[] args)
        {
            // check function results on example cases
            MakeTests();

            // get input data
            string dataPath = "../data/day1.txt";
            int[] inputs = ParseInput(File.ReadLines(dataPath));

            // == PART I
            int solution = inputs.Select(i => ComputeFuel(i)).Sum();
            Console.WriteLine($"PART I: solution = {solution}");

            // == PART II
            solution = inputs.Select(i => ComputeTotalFuel(i)).Sum();
            Console.WriteLine($"PART II: solution = {solution}");
        }
    }
}

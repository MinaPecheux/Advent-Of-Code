/*
 * =============================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: C# version
 * ---------------------------------------------
 * Day 2: 1202 Program Alarm
 * ============================================= */

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace CSharp2019
{
    class Day2
    {
        // [ Input parsing functions ]
        // ---------------------------

        /// <summary>Parses the incoming data into processable inputs.</summary>
        /// <param name="data">Provided problem data.</param>
        /// <returns>Parsed data as a list of ints.</returns>
        static int[] ParseInput(string data)
        {
            return data
                .Split(',')
                .Where(l => l.Length > 0)
                .Select(l => int.Parse(l))
                .ToArray();
        }

        // [ Computation functions ]
        // -------------------------

        // == PART I

        /// <summary>Executes the Intcode program on the provided inputs and computes the final
        /// result.</summary>
        /// <param name="inputs">List of integers to execute as an Intcode program.</param>
        /// <param name="restoreGravityAssist">Whether or not to restore the gravity assist
        /// by modifying the input program.</param>
        /// <returns>Final output of the program.</returns>
        static int ProcessInputs(int[] inputs, bool restoreGravityAssist = false)
        {
          // restore gravity assist?
          if (restoreGravityAssist) {
            inputs[1] = 12;
            inputs[2] = 2;
          }
          // create and execute the program
          IntcodeProgram program = new IntcodeProgram(inputs);
          program.Run();
          // isolate final result
          return program.Program[0];
        }

        // == PART II

        /// <summary>A brute-force algorithm to systematically try all possible input pairs
        /// until we find the one that gave the desired output (we can determine a
        /// finished set of possible candidates since we know that each number is in the
        /// [0, 99] range).</summary>
        /// <param name="inputs">List of integers to execute as an Intcode program.</param>
        /// <param name="wantedOutput">Desired output of the program.</param>
        /// <returns>Specific checksum that matches the desired output.</returns>
        static int FindChecksum(int[] inputs, int wantedOutput)
        {
          // prepare program
          IntcodeProgram program = new IntcodeProgram(inputs);
          for (int noun = 0; noun < 100; noun++) { // range is [0, 100[ = [0, 99]
            for (int verb = 0; verb < 100; verb++) {
              // reset program to initial state
              program.Reset();
              // set up noun and verb
              program.Program[1] = noun;
              program.Program[2] = verb;
              // run and compare result
              program.Run();
              if (program.Program[0] == wantedOutput) {
                return 100 * noun + verb;
              }
            }
          }

          return -1;
        }

        // [ Base tests ]
        // --------------
        static void MakeTests()
        {
            // == PART I
            Debug.Assert(ProcessInputs(
              new int[] { 1,9,10,3,2,3,11,0,99,30,40,50 }
            ) == 3500);
            Debug.Assert(ProcessInputs(
              new int[] { 1,0,0,0,99 }
            ) == 2);
            Debug.Assert(ProcessInputs(
              new int[] { 2,3,0,3,99 }
            ) == 2);
            Debug.Assert(ProcessInputs(
              new int[] { 2,4,4,5,99,0 }
            ) == 2);
            Debug.Assert(ProcessInputs(
              new int[] { 1,1,1,4,99,5,6,0,99 }
            ) == 30);
        }

        public static void Run()
        {
            // check function results on example cases
            MakeTests();

            // get input data
            string dataPath = "../data/day2.txt";
            int[] inputs = ParseInput(File.ReadAllText(dataPath));

            // == PART I
            int solution = ProcessInputs(inputs, true);
            Console.WriteLine($"PART I: solution = {solution}");

            // == PART II
            // (reparse inputs to get back original data)
            inputs = ParseInput(File.ReadAllText(dataPath));
            solution = FindChecksum(inputs, 19690720);
            Console.WriteLine($"PART II: solution = {solution}");
        }
    }
}

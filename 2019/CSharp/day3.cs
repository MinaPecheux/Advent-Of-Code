/*
 * =============================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: C# version
 * ---------------------------------------------
 * Day 3: Crossed Wires
 * ============================================= */

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace CSharp2019
{
    class Day3
    {
        // [ Input parsing functions ]
        // ---------------------------

        /// <summary>Parses the incoming data into processable inputs.</summary>
        /// <param name="lines">Provided problem data.</param>
        /// <returns>Parsed data as a list of strings.</returns>
        static string[][] ParseInput(IEnumerable<string> lines)
        {
          return lines
            .Where(l => l.Length > 0)
            .Select(l => l.Split(','))
            .ToArray();
        }

        struct Point {
          public int x;
          public int y;

          public Point(int x, int y) {
            this.x = x;
            this.y = y;
          }
        }

        // [ Computation functions ]
        // -------------------------

        /// <summary>Computes the Manhattan (or Taxicab) distance between two 2D points.</summary>
        /// <param name="x1">Horizontal coordinate of the first point.</param>
        /// <param name="y1">Vertical coordinate of the first point.</param>
        /// <param name="x2">Horizontal coordinate of the second point.</param>
        /// <param name="y2">Vertical coordinate of the second point.</param>
        /// <returns>Taxicab distance between the two 2D points.</returns>
        static int ManhattanDistance(int x1, int y1, int x2, int y2)
        {
          return Math.Abs(x2 - x1) + Math.Abs(y2 - y1);
        }

        /// <summary>Computes all the points a path goes through.</summary>
        /// <param name="path">Path to walk, as a list of moves to take (with a direction and
        /// an integer pace).</param>
        /// <returns>Points on the path.</returns>
        static Dictionary<Point, int> FindPathPoints(string[] path)
        {
          int cx = 0, cy = 0, d = 1;
          char dir;
          int pace;
          Dictionary<Point, int> points = new Dictionary<Point, int>();
          foreach (string move in path) {
            dir = move[0];
            pace = int.Parse(move.Substring(1));
            switch (dir) {
              case 'R':
                for (int x = cx + 1; x < cx + pace + 1; x++) {
                  points[new Point(x, cy)] = d;
                  d++;
                }
                cx += pace;
                break;
              case 'L':
                for (int x = cx - 1; x > cx - pace - 1; x--) {
                  points[new Point(x, cy)] = d;
                  d++;
                }
                cx -= pace;
                break;
              case 'U':
                for (int y = cy - 1; y > cy - pace - 1; y--) {
                  points[new Point(cx, y)] = d;
                  d++;
                }
                cy -= pace;
                break;
              case 'D':
                for (int y = cy + 1; y < cy + pace + 1; y++) {
                  points[new Point(cx, y)] = d;
                  d++;
                }
                cy += pace;
                break;
            }
          }

          return points;
        }

        // == PART I

        /// <summary>Finds the intersection of given paths that is closest to the central port,
        /// considering the Manhattan distance.</summary>
        /// <param name="paths">Paths to process.</param>
        /// <returns>Distance to the closest intersection to the central port.</returns>
        static int FindClosestInteresectionWithDist(string[][] paths)
        {
          // compute all activated points on the grid
          Dictionary<Point, int>[] pathPoints = paths.Select(path => FindPathPoints(path)).ToArray();
          IEnumerable<Point>[] points = pathPoints.Select(p => p.Select(k => k.Key)).ToArray();
          // extract the intersections of all the paths
          Point[] intersections = points[0].Intersect(points[1]).ToArray();
          // find the one closest to the central port (compute its Manhattan distance)
          IEnumerable<int> dists = intersections.Select(i => ManhattanDistance(i.x, i.y, 0, 0));
          return dists.Min();
        }

        // == PART II

        /// <summary>Finds the intersection of given paths that is closest to the central port,
        /// considering the combined number of steps to the chosen intersection.</summary>
        /// <param name="paths">Paths to process.</param>
        /// <returns>Distance to the closest intersection to the central port.</returns>
        static int FindClosestInteresectionWithSteps(string[][] paths)
        {
          // compute all activated points on the grid
          Dictionary<Point, int>[] pathPoints = paths.Select(path => FindPathPoints(path)).ToArray();
          IEnumerable<Point>[] points = pathPoints.Select(p => p.Select(k => k.Key)).ToArray();
          // extract the intersections of all the paths
          Point[] intersections = points[0].Intersect(points[1]).ToArray();
          // find the smallest sum of combined steps
          IEnumerable<int> totalSteps = intersections.Select(i => pathPoints.Select(path => path[i]).Sum());
          return totalSteps.Min();
        }

        // == PART II

        // [ Base tests ]
        // --------------
        static void MakeTests()
        {
            // == PART I
            Debug.Assert(FindClosestInteresectionWithDist(new string[][] {
              new string[] { "R8","U5","L5","D3" },
              new string[] { "U7","R6","D4","L4" },
            }) == 6);
            Debug.Assert(FindClosestInteresectionWithDist(new string[][] {
              new string[] { "R75","D30","R83","U83","L12","D49","R71","U7","L72" },
              new string[] { "U62","R66","U55","R34","D71","R55","D58","R83" },
            }) == 159);
            Debug.Assert(FindClosestInteresectionWithDist(new string[][] {
              new string[] { "R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51" },
              new string[] { "U98","R91","D20","R16","D67","R40","U7","R15","U6","R7" },
            }) == 135);

            // == PART II
            Debug.Assert(FindClosestInteresectionWithSteps(new string[][] {
              new string[] { "R8","U5","L5","D3" },
              new string[] { "U7","R6","D4","L4" },
            }) == 30);
            Debug.Assert(FindClosestInteresectionWithSteps(new string[][] {
              new string[] { "R75","D30","R83","U83","L12","D49","R71","U7","L72" },
              new string[] { "U62","R66","U55","R34","D71","R55","D58","R83" },
            }) == 610);
            Debug.Assert(FindClosestInteresectionWithSteps(new string[][] {
              new string[] { "R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51" },
              new string[] { "U98","R91","D20","R16","D67","R40","U7","R15","U6","R7" },
            }) == 410);
        }

        public static void Run()
        {
            // check function results on example cases
            MakeTests();

            // get input data
            string dataPath = "../data/day3.txt";
            string[][] inputs = ParseInput(File.ReadLines(dataPath));

            // == PART I
            int solution = FindClosestInteresectionWithDist(inputs);
            Console.WriteLine($"PART I: solution = {solution}");

            // == PART II
            solution = FindClosestInteresectionWithSteps(inputs);
            Console.WriteLine($"PART II: solution = {solution}");
        }
    }
}

/*
 * =============================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: C# version
 * ---------------------------------------------
 * Day 1: The Tyranny of the Rocket Equation
 * ============================================= */

using System;
using System.Reflection;

namespace CSharp2019
{
  class Index
  {
    static void Main(string[] args)
    {
      if (args.Length == 0) {
        Console.WriteLine("[ ERROR ] Pass in the number of the program you want to run! (eg: 1 for day 1)");
      }

      int programIndex;
      if (int.TryParse(args[0], out programIndex)) {
        Type t = Type.GetType($"CSharp2019.Day{programIndex}");
        MethodInfo runMethod = t.GetMethod("Run", BindingFlags.Static | BindingFlags.Public);
        runMethod.Invoke(null, null);
      } else {
        Console.WriteLine("[ ERROR ] Please pass in a valid integer for the program number! (eg: 1 for day 1)");
      }
    }
  }
}

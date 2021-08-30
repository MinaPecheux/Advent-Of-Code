/*
 * =============================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: C# version
 * ---------------------------------------------
 * Day 1: The Tyranny of the Rocket Equation
 * ============================================= */

using System;
using System.Collections.Generic;

namespace CSharpUtils
{
  public static class MyListExtensions
  {
    /// <summary>Util extension method to pop an item from a list, i.e. remove
    /// it and retrieve it at the same time.</summary>
    public static T Pop<T>(this List<T> list, int index)
    {
      T val = list[index];
      list.RemoveAt(index);
      return val;
    }
  }
}

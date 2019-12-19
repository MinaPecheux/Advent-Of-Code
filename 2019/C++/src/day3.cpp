/**
 * \file day3.cpp
 * \brief AoC 2019 - Day 3 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 3: Crossed Wires
 * =============================================
 */
#include <cmath>
#include <map>
#include "utils.hpp"

typedef struct {
  int x;
  int y;
} Point;

// [ Computation functions ]
// -------------------------
/**
 * \fn int manhattanDistance(int x1, int y1, int x2, int y2)
 * \brief Computes the Manhattan (or Taxicab) distance between two 2D points.
 *
 * \param x1 Horizontal coordinate of the first point.
 * \param y1 Vertical coordinate of the first point.
 * \param x2 Horizontal coordinate of the second point.
 * \param y2 Horizontal coordinate of the second point.
 * \return Taxicab distance between the two 2D points.
 */
int manhattanDistance(int x1, int y1, int x2, int y2) {
  return abs(x2 - x1) + abs(y2 - y1);
}

/**
 * \fn std::vector<std::string> findPathPoints(std::vector<std::string> path)
 * \brief Computes all the points a path goes through.
 *
 * \param path Path to walk, as a list of moves to take (with a direction and
 * an integer pace).
 * \return Points on the path.
 */
std::map<std::string,int> findPathPoints(std::vector<std::string> path) {
  std::map<std::string,int> points;
  int cx = 0, cy = 0, d = 1;
  char dir;
  int pace;
  for (auto move : path) {
    dir = move[0];
    pace = stoi(move.substr(1));
    switch (dir) {
      case 'R':
        for (int x = cx+1; x < cx+pace+1; x++) {
          points[strFormat("%d,%d", x, cy)] = d;
          d++;
        }
        cx += pace;
        break;
      case 'L':
        for (int x = cx-1; x > cx-pace-1; x--) {
          points[strFormat("%d,%d", x, cy)] = d;
          d++;
        }
        cx -= pace;
        break;
      case 'U':
        for (int y = cy-1; y > cy-pace-1; y--) {
          points[strFormat("%d,%d", cx, y)] = d;
          d++;
        }
        cy -= pace;
        break;
      case 'D':
        for (int y = cy+1; y < cy+pace+1; y++) {
          points[strFormat("%d,%d", cx, y)] = d;
          d++;
        }
        cy += pace;
        break;
    }
  }
  return points;
}

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/
/**
 * \fn int findClosestIntersectionWithDist(std::vector< std::vector<std::string> > paths)
 * \brief Finds the intersection of given paths that is closest to the central
 * port, considering the Manhattan distance.
 *
 * \param paths Paths to process.
 * \return Distance of the closest intersection to the central port.
 */
int findClosestIntersectionWithDist(std::vector<std::vector<std::string> > paths) {
  // compute all activated points on the grid
  std::vector<std::map<std::string,int> > pathPoints;
  for (auto path : paths) {
    pathPoints.push_back(findPathPoints(path));
  }
  // extract the intersections of all the paths
  std::vector<std::string> intersections;
  for (auto i : pathPoints[0]) {
    if (pathPoints[1].find(i.first) != pathPoints[1].end()) {
      intersections.push_back(i.first);
    }
  }
  // find the one closest to the central port (compute its Manhattan distance)
  int minDist = -1;
  int dist;
  std::vector<std::string> tmp;
  int x, y;
  for (auto i : intersections) {
    tmp = strSplit(i, ",");
    x = stoi(tmp[0]);
    y = stoi(tmp[1]);
    dist = manhattanDistance(x, y, 0, 0);
    if (minDist == -1 || dist < minDist) {
      minDist = dist;
    }
  }
  return minDist;
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/
/**
 * \fn int findClosestIntersectionWithSteps(std::vector< std::vector<std::string> > paths)
 * \brief Finds the intersection of given paths that is closest to the central
 * port, the combined number of steps to the chosen intersection.
 *
 * \param paths Paths to process.
 * \return Distance of the closest intersection to the central port.
 */
int findClosestIntersectionWithSteps(std::vector<std::vector<std::string> > paths) {
  // compute all activated points on the grid
  std::vector<std::map<std::string,int> > pathPoints;
  for (auto path : paths) {
    pathPoints.push_back(findPathPoints(path));
  }
  // extract the intersections of all the paths
  std::vector<std::string> intersections;
  for (auto i : pathPoints[0]) {
    if (pathPoints[1].find(i.first) != pathPoints[1].end()) {
      intersections.push_back(i.first);
    }
  }
  // find the smallest sum of combined steps
  int minSum = -1;
  int sum;
  for (auto i : intersections) {
    sum = pathPoints[0][i] + pathPoints[1][i];
    if (minSum == -1 || sum < minSum) {
      minSum = sum;
    }
  }
  return minSum;
}

// [ Base tests ]
// --------------

/**
 * \fn void makeTests()
 * \brief Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
void makeTests() {
  std::vector<std::vector<std::string> > paths1 = {
    { "R8","U5","L5","D3" }, { "U7","R6","D4","L4" }
  };
  std::vector<std::vector<std::string> > paths2 = {
    { "R75","D30","R83","U83","L12","D49","R71","U7","L72" },
    { "U62","R66","U55","R34","D71","R55","D58","R83" }
  };
  std::vector<std::vector<std::string> > paths3 = {
    { "R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51" },
    { "U98","R91","D20","R16","D67","R40","U7","R15","U6","R7" }
  };

  // Part I
  assert(findClosestIntersectionWithDist(paths1) == 6);
  assert(findClosestIntersectionWithDist(paths2) == 159);
  assert(findClosestIntersectionWithDist(paths3) == 135);
  
  // Part II
  assert(findClosestIntersectionWithSteps(paths1) == 30);
  assert(findClosestIntersectionWithSteps(paths2) == 610);
  assert(findClosestIntersectionWithSteps(paths3) == 410);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();
  
  // get input data
  std::string dataPath = "../data/day3.txt";
  std::string data = readFile(dataPath);
  std::vector<std::string> inputs = strSplit(data, "\n");
  
  std::vector<std::vector<std::string> > paths;
  for (auto path : inputs) {
    paths.push_back(strSplit(path, ","));
  }
  
  // Part I
  int solution1 = findClosestIntersectionWithDist(paths);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = findClosestIntersectionWithSteps(paths);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

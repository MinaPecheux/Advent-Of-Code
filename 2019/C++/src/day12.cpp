/**
 * \file day12.cpp
 * \brief AoC 2019 - Day 12 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 12: The N-Body Problem
 * =============================================
 */
#include <regex>
#include <cmath>
#include <map>
#include <functional>
#include "utils.hpp"

// [ Util structs and definitions ]
// --------------------------------
typedef struct {
  int x, y, z;
  int vx, vy, vz;
} Moon;

// [ Input parsing functions ]
// ---------------------------

/**
 * \fn std::vector<std::string> parseData(std::string data)
 * \brief Parses the incoming data into a list of asteroids coordinates (in the
 * "x,y" format).
 *
 * \param data Provided problem data.
 * \return Parsed data.
 */
std::vector<Moon> parseData(std::string data) {
  std::regex reg ("<x=(-?\\d+), y=(-?\\d+), z=(-?\\d+)>");
  std::cmatch match;
  std::vector<Moon> moons;
  std::vector<std::string> lines = strSplit(data, "\n");
  for (auto line : lines) {
    if (line.length() == 0) continue;
    std::regex_match (line.c_str(), match, reg);
    moons.push_back({ stoi(match[1]), stoi(match[2]), stoi(match[3]), 0, 0, 0 });
  }
  return moons;
}

// [ Computation functions ]
// -------------------------

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/
int computeTotalEnergy(Moon& moon) {
  int potentialEnergy = abs(moon.x) + abs(moon.y) + abs(moon.z);
  int kineticEnergy = abs(moon.vx) + abs(moon.vy) + abs(moon.vz);
  return potentialEnergy * kineticEnergy;
}

/**
 * \fn int simulateMoons(std::vector<Moon>& moons, int timesteps)
 * \brief Simulates the moons' movement over a given number of time steps and
 * computes the final total energy of the entire system (i.e. the sum of the
 * final total energies of each moon).
 *
 * \param moons Initial states of the moons to process.
 * \param timesteps Number of time steps to simulate.
 * \return Total energy of the entire system at the end of the simulation.
 */
int simulateMoons(std::vector<Moon>& moons, int timesteps) {
  // prepare all unique moon pairs
  std::set<std::vector<int> > moonPairs = combinations<int>(
    rangeToStr(0, moons.size()), 2);
  Moon m1, m2;
  for (int time = 0; time < timesteps; time++) {
    // apply gravity
    for (auto p : moonPairs) {
      m1 = moons[p[0]];
      m2 = moons[p[1]];
      if (m1.x > m2.x) {
        moons[p[0]].vx--; moons[p[1]].vx++;
      } else if (m1.x < m2.x) {
        moons[p[0]].vx++; moons[p[1]].vx--;
      }
      if (m1.y > m2.y) {
        moons[p[0]].vy--; moons[p[1]].vy++;
      } else if (m1.y < m2.y) {
        moons[p[0]].vy++; moons[p[1]].vy--;
      }
      if (m1.z > m2.z) {
        moons[p[0]].vz--; moons[p[1]].vz++;
      } else if (m1.z < m2.z) {
        moons[p[0]].vz++; moons[p[1]].vz--;
      }
    }
    // apply velocity
    for (int i = 0; i < moons.size(); i++) {
      moons[i].x += moons[i].vx;
      moons[i].y += moons[i].vy;
      moons[i].z += moons[i].vz;
    }
  }
  
  int totalEnergy = 0;
  for (auto moon : moons) {
    totalEnergy += computeTotalEnergy(moon);
  }
  return totalEnergy;
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/
/**
 * \fn unsigned long GCD(unsigned long x, unsigned long y)
 * \brief Computes the greatest common divisor (GCD) of two numbers.
 *
 * \param x First number to process.
 * \param y Second number to process.
 * \return GCD of the two numbers.
 */
unsigned long GCD(unsigned long x, unsigned long y) {
  unsigned long tmp;
  while (y) {
    tmp = x;
    x = y;
    y = tmp % y;
  }
  return x;
}

/**
 * \fn unsigned long LCM(unsigned long x, unsigned long y)
 * \brief Computes the least common multiple (LCM) of two numbers.
 *
 * \param x First number to process.
 * \param y Second number to process.
 * \return LCM of the two numbers.
 */
unsigned long LCM(unsigned long x, unsigned long y) {
  return (x / GCD(x, y)) * y;
}

/**
 * \fn unsigned long findFirstRepetition(std::vector<Moon>& moons)
 * \brief Simulates the moons' movement until they repeat a previous state.
 *
 * \param moons Initial states of the moons to process.
 * \return Number of steps until the first repetition.
 */
unsigned long findFirstRepetition(std::vector<Moon>& moons) {
  // prepare all unique moon pairs
  std::set<std::vector<int> > moonPairs = combinations<int>(
    rangeToStr(0, moons.size()), 2);
  Moon m1, m2;
  int time = 0;
  std::map<std::size_t,int> historyX, historyY, historyZ;
  int periodX = -1, periodY = -1, periodZ = -1;
  std::size_t stateX, stateY, stateZ;
  std::string xStr, yStr, zStr;
  while (1) {
    // apply gravity
    for (auto p : moonPairs) {
      m1 = moons[p[0]];
      m2 = moons[p[1]];
      if (m1.x > m2.x) {
        moons[p[0]].vx--; moons[p[1]].vx++;
      } else if (m1.x < m2.x) {
        moons[p[0]].vx++; moons[p[1]].vx--;
      }
      if (m1.y > m2.y) {
        moons[p[0]].vy--; moons[p[1]].vy++;
      } else if (m1.y < m2.y) {
        moons[p[0]].vy++; moons[p[1]].vy--;
      }
      if (m1.z > m2.z) {
        moons[p[0]].vz--; moons[p[1]].vz++;
      } else if (m1.z < m2.z) {
        moons[p[0]].vz++; moons[p[1]].vz--;
      }
    }
    // apply velocity
    for (int i = 0; i < moons.size(); i++) {
      moons[i].x += moons[i].vx;
      moons[i].y += moons[i].vy;
      moons[i].z += moons[i].vz;
    }
    // hash state:
    // . hash each axis
    xStr = ""; yStr = ""; zStr = "";
    for (auto moon : moons) {
      xStr += strFormat("%d/%d,", moon.x, moon.vx);
      yStr += strFormat("%d/%d,", moon.y, moon.vy);
      zStr += strFormat("%d/%d,", moon.z, moon.vz);
    }
    stateX = std::hash<std::string>{}(xStr);
    stateY = std::hash<std::string>{}(yStr);
    stateZ = std::hash<std::string>{}(zStr);
    // . check the matching dict for a repetition
    if (periodX == -1 && historyX.find(stateX) != historyX.end()) {
      periodX = time - historyX[stateX];
    }
    if (periodY == -1 && historyY.find(stateY) != historyY.end()) {
      periodY = time - historyY[stateY];
    }
    if (periodZ == -1 && historyZ.find(stateZ) != historyZ.end()) {
      periodZ = time - historyZ[stateZ];
    }
    if (periodX != -1 && periodY != -1 && periodZ != -1) {
      break;
    }
    // . store the hash with the current time for further checks
    historyX[stateX] = time;
    historyY[stateY] = time;
    historyZ[stateZ] = time;
    time++;
  }
  
  // find the total repetition period by getting the LCM of the three subperiods
  return LCM(LCM(periodX, periodY), LCM(periodY, periodZ));
}

// [ Base tests ]
// --------------

/**
 * \fn void makeTests()
 * \brief Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
void makeTests() {
  Moon m1 = { 2, 1, -3, -3, -2, 1 };
  assert(computeTotalEnergy(m1) == 36);  
  Moon m2 = { 1, -8, 0, -1, 1, 3 };
  assert(computeTotalEnergy(m2) == 45);  
  Moon m3 = { 3, -6, 1, 3, 2, -3 };
  assert(computeTotalEnergy(m3) == 80);  
  Moon m4 = { 2, 0, 4, 1, -1, -1 };
  assert(computeTotalEnergy(m4) == 18);
  
  std::vector<Moon> moons1 = {
    { -1, 0, 2, 0, 0, 0 }, { 2, -10, -7, 0, 0, 0 }, { 4, -8, 8, 0, 0, 0 },
    { 3, 5, -1, 0, 0, 0 }
  };
  std::vector<Moon> moons2 = {
    { -8, -10, 0, 0, 0, 0 }, { 5, 5, 10, 0, 0, 0 }, { 2, -7, 3, 0, 0, 0 },
    { 9, -8, -3, 0, 0, 0 }
  };
  // Part I
  assert(simulateMoons(moons1, 10) == 179);
  
  // Part II  
  assert(findFirstRepetition(moons1) == 2772);
  assert(findFirstRepetition(moons2) == 4686774924);
}

int main(int argc, char const *argv[]) {  
  // check function results on example cases
  makeTests();

  // get input data
  std::string dataPath = "../data/day12.txt";
  std::string data = readFile(dataPath);
  
  // Part I
  std::vector<Moon> moons = parseData(data);
  int solution1 = simulateMoons(moons, 1000);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  moons = parseData(data);
  unsigned long solution2 = findFirstRepetition(moons);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

/**
 * \file day10.cpp
 * \brief AoC 2019 - Day 10 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 10: Monitoring Station
 * =============================================
 */
#include <algorithm>
#include <cmath>
#include <map>
#include "utils.hpp"

// [ Util structs and definitions ]
// --------------------------------
typedef struct {
  float angle;
  float distance;
  std::string pos;
} AsteroidInfo;
bool operator<(const AsteroidInfo& first, const AsteroidInfo& second) {
  if (first.angle > second.angle) {
    return false;
  }
  if (first.angle == second.angle) {
    return first.distance < second.distance;
  }
  return true;
}

typedef std::map<std::string,std::vector<AsteroidInfo> > SightsMap;

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
std::vector<std::string> parseData(std::string data) {
  std::vector<std::string> asteroids;
  std::vector<std::string> lines = strSplit(data, "\n");
  int height = lines.size();
  int width = lines[0].length();
  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      if (lines[y][x] == '#') {
        asteroids.push_back(strFormat("%d,%d", x, y));
      }
    }
  }
  return asteroids;
}

/**
 * \fn void decomposeCoordinates(std::string pos, int& x, int& y)
 * \brief Decomposes a string in the "x,y" format into two integer coordinates.
 *
 * \param pos Coordinate to decompose.
 * \param x Reference to the integer where to store the horizontal coordinate.
 * \param y Reference to the integer where to store the vertical coordinate.
 */
void decomposeCoordinates(std::string pos, int& x, int& y) {
  std::vector<std::string> tmp = strSplit(pos, ",");
  x = stoi(tmp[0]);
  y = stoi(tmp[1]);
}

/**
 * \fn float dist(std::string& p1, std::string& p2)
 * \brief Computes the angle between two 2D points using the atan2 and rotates
 * the result by 90° counterclockwise.
 *
 * \param p1 Coordinates of the first point (in the "x,y" string format).
 * \param p2 Coordinates of the second point (in the "x,y" string format).
 * \return Modified angle between the two 2D points.
 */
float angle(std::string& p1, std::string& p2) {
  int x1, y1, x2, y2;
  decomposeCoordinates(p1, x1, y1);
  decomposeCoordinates(p2, x2, y2);
  float m = 2.0 * M_PI;
  float a = fmod(atan2(y1 - y2, x1 - x2) - 0.5 * M_PI, m);
  return fmod(a + m, m);
}

/**
 * \fn float dist(std::string& p1, std::string& p2)
 * \brief Computes the Euclidean distance between two 2D points.
 *
 * \param p1 Coordinates of the first point (in the "x,y" string format).
 * \param p2 Coordinates of the second point (in the "x,y" string format).
 * \return Euclidean distance between the two 2D points.
 */
float dist(std::string& p1, std::string& p2) {
  int x1, y1, x2, y2;
  decomposeCoordinates(p1, x1, y1);
  decomposeCoordinates(p2, x2, y2);
  return sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1));
}

/**
 * \fn SightsMap prepareMap (std::string data)
 * \brief Computes all the other asteroids each asteroid in the map can "see"
 * with its angle, its distance to the reference asteroid and its position.
 *
 * \param asteroids List of asteroids to process.
 * \return Map of asteroid sights.
 */
SightsMap computeAsteroidSights (std::vector<std::string>& asteroids) {
  SightsMap sights;
  std::string tmp;
  for (auto ast1 : asteroids) {
    for (auto ast2 : asteroids) {
      if (ast1 == ast2) continue; // ignore same location
      // else compute angle and distance, and add asteroid
      sights[ast1].push_back({ angle(ast1, ast2), dist(ast1, ast2), ast2 });
    }
  }
  return sights;
}

/**
 * \fn SightsMap prepareMap (std::string data)
 * \brief Reads the given data to prepare the map by computing the sights of
 * all the asteroids.
 *
 * \param data Data to parse into an asteroids map.
 * \return Map of asteroid sights.
 */
SightsMap prepareMap (std::string data) {
  std::vector<std::string> asteroids = parseData(data);
  return computeAsteroidSights(asteroids);
}


// [ Computation functions ]
// -------------------------

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/

/**
 * \fn int findBestAsteroid(SightsMap& sights, std::string& station)
 * \brief Finds the asteroid from which the station would see the greatest
 * number of asteroids.
 *
 * \param sights Sights of the asteroids in the neighborhood.
 * \param station Reference to the "best" station position (to fill).
 * \return Number of asteroids visible from the "best" asteroid.
 */
int findBestAsteroid(SightsMap& sights, std::string& station) {
  // associate the number of visible asteroids to the asteroid position and
  // return the best one, i.e. the position that "sees" the most asteroids
  std::string bestPos;
  int bestCount = -1, c;
  std::set<float> differentAngles;
  for (auto s : sights) {
    differentAngles.clear();
    for (auto i : s.second) {
      differentAngles.insert(i.angle);
    }
    c = differentAngles.size();
    if (c > bestCount) {
      bestPos = s.first;
      bestCount = c;
    }
  }
  station = bestPos;
  return bestCount;
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/

/**
 * \fn void int processLaserVaporization(SightsMap& sights, std::string station)
 * \brief Computes the whole laser vaporization process given some coordinates
 * have been picked for the monitoring station.
 *
 * \param sights Sights of the asteroids in the neighborhood.
 * \param station Coordinates of the monitoring station (as an "x,y" string).
 */
int processLaserVaporization(SightsMap& sights, std::string station) {
  // get station sight
  std::vector<AsteroidInfo> sight = sights[station];
  // sort the sights per angle, then per distance
  std::sort(sight.begin(), sight.end());
  // roll the laser until 200 asteroids have been destroyed
  float lastAngle = -1.0;
  int idx, x, y;
  float a, d;
  for (int i = 0; i < 200; i++) {
    idx = 0;
    a = sight[idx].angle;
    while (a <= lastAngle && idx < sight.size()) {
      a = sight[idx].angle;
      if (a <= lastAngle) {
        idx++;
      }
    }
    a = sight[idx].angle;
    d = sight[idx].distance;
    decomposeCoordinates(sight[idx].pos, x, y);
    lastAngle = fmod(a, 2.0 * M_PI);
  }
  // compute the checksum for the position of the 200th destroyed asteroid
  return x * 100 + y;
}

// [ Base tests ]
// --------------

/**
 * \fn void makeTests()
 * \brief Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
void makeTests() {
  // Part I
  std::string station;
  SightsMap sights1 = prepareMap(".#..#\n.....\n#####\n....#\n...##");
  assert(findBestAsteroid(sights1, station) == 8);
  SightsMap sights2 = prepareMap("......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####");
  assert(findBestAsteroid(sights2, station) == 33);
  SightsMap sights3 = prepareMap("#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.");
  assert(findBestAsteroid(sights3, station) == 35);
  SightsMap sights4 = prepareMap(".#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..");
  assert(findBestAsteroid(sights4, station) == 41);
  SightsMap sights5 = prepareMap(".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##");
  assert(findBestAsteroid(sights5, station) == 210);
  
  // Part II
  assert(processLaserVaporization(sights5, station) == 802);
}

int main(int argc, char const *argv[]) {
  // check function results on example cases
  makeTests();

  // get input data
  std::string dataPath = "../data/day10.txt";
  std::string data = readFile(dataPath);
  SightsMap sights = prepareMap(data);
  std::string station;
  
  // Part I
  int solution1 = findBestAsteroid(sights, station);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = processLaserVaporization(sights, station);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

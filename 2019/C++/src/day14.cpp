/**
 * \file day14.cpp
 * \brief AoC 2019 - Day 14 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 14: Space Stoichiometry
 * =============================================
 */
#include <cmath>
#include <map>
#include "utils.hpp"

// [ Util structs and definitions ]
// --------------------------------
typedef struct {
  std::map<std::string,unsigned long long> reagents;
  unsigned long long amount;
} ProductInfo;
typedef std::map<std::string,ProductInfo> ReactionsMap;

// [ Input parsing functions ]
// ---------------------------

/**
 * \fn ReactionsMap parseData(std::string data, std::set<std::string>& materials)
 * \brief Parses the incoming data into a list of chemical reactions and a set
 * of all the materials used in those reactions.
 *
 * \param data Provided problem data.
 * \param materials Reference to the set of used materials (to fill).
 * \return Parsed data.
 */
ReactionsMap parseData(std::string data, std::set<std::string>& materials) {
  if (materials.size() > 0) materials.clear();
  materials.insert("ORE");
  ReactionsMap reactions;
  std::vector<std::string> lines = strSplit(data, "\n");
  std::vector<std::string> tmp, reags, prods;
  std::map<std::string,unsigned long long> reagents;
  for (auto line : lines) {
    if (line.length() == 0) continue;
    tmp = strSplit(line, " => ");
    reags = strSplit(tmp[0], ", ");
    prods = strSplit(tmp[1], ", ");
    reagents.clear();
    for (auto r : reags) {
      tmp = strSplit(r, " ");
      reagents[tmp[1]] = std::stoull(tmp[0]);
      materials.insert(tmp[1]);
    }
    for (auto p : prods) {
      tmp = strSplit(p, " ");
      ProductInfo pi = { reagents, std::stoull(tmp[0]) };
      reactions[tmp[1]] = pi;
      materials.insert(tmp[1]);
    }
  }
  return reactions;
}

// [ Computation functions ]
// -------------------------

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/
/**
 * \fn std::map<std::string,int> computeDistances(std::set<std::string>& materials, ReactionsMap& reactions)
 * \brief Computes the "distance" of each material to ORE so that we can evaluate
 * in which order they should processed further on.
 *
 * \param materials Set of all materials used in the list of reactions.
 * \param reactions All possible reactions (keyed by product).
 * \return Distances of all materials to ORE.
 */
std::map<std::string,int> computeDistances(std::set<std::string>& materials, ReactionsMap& reactions) {
  std::map<std::string,int> distances;
  distances["ORE"] = 0;
  int dist, maxDist;
  while (distances.size() < materials.size()) {
    for (auto material : materials) {
      if (distances.find(material) != distances.end()) continue;
      dist = 0;
      for (auto reagent : reactions[material].reagents) {
        if (distances.find(reagent.first) == distances.end()) {
          dist = -1;
        }
      }
      if (dist == -1) continue;
      maxDist = -1;
      for (auto reagent : reactions[material].reagents) {
        dist = distances[reagent.first];
        if (dist > maxDist) {
          maxDist = dist;
        }
      }
      distances[material] = maxDist + 1;
    }
  }
  return distances;
}

/**
 * \fn unsigned long long requiredOre(std::set<std::string>& materials, ReactionsMap& reactions, unsigned long long fuelAmount)
 * \brief Gets the required amount of raw ORE to produce the given quantity of
 * fuel, depending on the materials and reactions used.
 *
 * \param materials Set of all materials used in the list of reactions.
 * \param reactions All possible reactions (keyed by product).
 * \param fuelAmount Amount of fuel to produce.
 * \return Required amount of ORE.
 */
unsigned long long requiredOre(std::set<std::string>& materials, ReactionsMap& reactions, unsigned long long fuelAmount) {
  std::map<std::string,int> distances = computeDistances(materials, reactions);
  std::map<std::string,unsigned long long> requiredProducts, reagents;
  requiredProducts["FUEL"] = fuelAmount;
  std::string product;
  unsigned long requiredQty, ratio;
  int dist, maxDist;
  while (requiredProducts.size() > 1
    || requiredProducts.find("ORE") == requiredProducts.end()) {
    maxDist = -1;
    for (auto p : requiredProducts) {
      dist = distances[p.first];
      if (dist > maxDist) {
        product = p.first;
        maxDist = dist;
      }
    }
    requiredQty = requiredProducts[product];
    reagents = reactions[product].reagents;
    requiredProducts.erase(product);
    if (product == "ORE") {
      requiredProducts[product] = requiredQty;
      continue;
    }
    for (auto reagent : reagents) {
      ratio = ceil(requiredQty / (double)(reactions[product].amount));
      requiredProducts[reagent.first] += ratio * reagent.second;
    }
  }
  return requiredProducts["ORE"];
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/

/**
 * \fn unsigned long long computeFuelAmount(std::set<std::string>& materials, ReactionsMap& reactions, unsigned long long oreAmount)
 * \brief Computes the amount of fuel that can be produced with the given amount
 * of ore, depending on the materials and reactions used.
 *
 * \param materials Set of all materials used in the list of reactions.
 * \param reactions All possible reactions (keyed by product).
 * \param oreAmount Available amount of ore.
 * \return Amount of fuel that can be produced.
 */
unsigned long long computeFuelAmount(std::set<std::string>& materials, ReactionsMap& reactions, unsigned long long oreAmount) {
  unsigned long long oneFuelOres = requiredOre(materials, reactions, 1);
  unsigned long long target = oreAmount / oneFuelOres;
  unsigned long long totalOres = requiredOre(materials, reactions, target);
  while (1) {
    target += (oreAmount - totalOres) / oneFuelOres + 1;
    totalOres = requiredOre(materials, reactions, target);
    if (totalOres > oreAmount) {
      break;
    }
  }
  return target - 1;
}

// [ Base tests ]
// --------------

/**
 * \fn void makeTests()
 * \brief Performs tests on the provided examples to check the result of the
 * computation functions is ok.
 */
void makeTests() {
  std::set<std::string> materials;
  ReactionsMap reactions;
  
  // Part I
  reactions = parseData("10 ORE => 10 A\n1 ORE => 1 B\n7 A, 1 B => 1 C\n7 A, 1 C => 1 D\n7 A, 1 D => 1 E\n7 A, 1 E => 1 FUEL", materials);
  assert(requiredOre(materials, reactions, 1) == 31);
  reactions = parseData("9 ORE => 2 A\n8 ORE => 3 B\n7 ORE => 5 C\n3 A, 4 B => 1 AB\n5 B, 7 C => 1 BC\n4 C, 1 A => 1 CA\n2 AB, 3 BC, 4 CA => 1 FUEL", materials);
  assert(requiredOre(materials, reactions, 1) == 165);
  reactions = parseData("157 ORE => 5 NZVS\n165 ORE => 6 DCFZ\n44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL\n12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ\n179 ORE => 7 PSHF\n177 ORE => 5 HKGWZ\n7 DCFZ, 7 PSHF => 2 XJWVT\n165 ORE => 2 GPVTF\n3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT", materials);
  assert(requiredOre(materials, reactions, 1) == 13312);
  reactions = parseData("2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG\n17 NVRVD, 3 JNWZP => 8 VPVL\n53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL\n22 VJHF, 37 MNCFX => 5 FWMGM\n139 ORE => 4 NVRVD\n144 ORE => 7 JNWZP\n5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC\n5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV\n145 ORE => 6 MNCFX\n1 NVRVD => 8 CXFTF\n1 VJHF, 6 MNCFX => 4 RFSQX\n176 ORE => 6 VJHF", materials);
  assert(requiredOre(materials, reactions, 1) == 180697);
  reactions = parseData("171 ORE => 8 CNZTR\n7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL\n114 ORE => 4 BHXH\n14 VRPVC => 6 BMBT\n6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL\n6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT\n15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW\n13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW\n5 BMBT => 4 WPTQ\n189 ORE => 9 KTJDG\n1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP\n12 VRPVC, 27 CNZTR => 2 XDBXC\n15 KTJDG, 12 BHXH => 5 XCVML\n3 BHXH, 2 VRPVC => 7 MZWV\n121 ORE => 7 VRPVC\n7 XCVML => 6 RJRHP\n5 BHXH, 4 VRPVC => 5 LTCX", materials);
  assert(requiredOre(materials, reactions, 1) == 2210736);
  
  // Part II
  reactions = parseData("157 ORE => 5 NZVS\n165 ORE => 6 DCFZ\n44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL\n12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ\n179 ORE => 7 PSHF\n177 ORE => 5 HKGWZ\n7 DCFZ, 7 PSHF => 2 XJWVT\n165 ORE => 2 GPVTF\n3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT", materials);
  assert(computeFuelAmount(materials, reactions, 1000000000000) == 82892753);
  reactions = parseData("2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG\n17 NVRVD, 3 JNWZP => 8 VPVL\n53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL\n22 VJHF, 37 MNCFX => 5 FWMGM\n139 ORE => 4 NVRVD\n144 ORE => 7 JNWZP\n5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC\n5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV\n145 ORE => 6 MNCFX\n1 NVRVD => 8 CXFTF\n1 VJHF, 6 MNCFX => 4 RFSQX\n176 ORE => 6 VJHF", materials);
  assert(computeFuelAmount(materials, reactions, 1000000000000) == 5586022);
  reactions = parseData("171 ORE => 8 CNZTR\n7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL\n114 ORE => 4 BHXH\n14 VRPVC => 6 BMBT\n6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL\n6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT\n15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW\n13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW\n5 BMBT => 4 WPTQ\n189 ORE => 9 KTJDG\n1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP\n12 VRPVC, 27 CNZTR => 2 XDBXC\n15 KTJDG, 12 BHXH => 5 XCVML\n3 BHXH, 2 VRPVC => 7 MZWV\n121 ORE => 7 VRPVC\n7 XCVML => 6 RJRHP\n5 BHXH, 4 VRPVC => 5 LTCX", materials);
  assert(computeFuelAmount(materials, reactions, 1000000000000) == 460664);
}

int main(int argc, char const *argv[]) {  
  // check function results on example cases
  makeTests();

  // get input data
  std::string dataPath = "../data/day14.txt";
  std::string data = readFile(dataPath);
  std::set<std::string> materials;
  ReactionsMap reactions = parseData(data, materials);
  
  // Part I
  int solution1 = requiredOre(materials, reactions, 1);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  unsigned long long solution2 = computeFuelAmount(materials, reactions, 1000000000000);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

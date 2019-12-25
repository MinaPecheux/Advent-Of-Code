/**
 * \file day11.cpp
 * \brief AoC 2019 - Day 11 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 11: Space Police
 * =============================================
 */
#include "utils.hpp"
#include "parser.hpp"
#include "intcode.hpp"

// [ Computation functions ]
// -------------------------

/*------------------------------------------------------------------------------
  Part I + II
------------------------------------------------------------------------------*/
/**
 * \fn long long processInputs(std::vector<long long> inputs, bool startWhite=false, bool display=false, bool debug=false)
 * \brief Executes the Intcode program on the provided inputs and finds out the
 * number of panels that have been painted at least once. It can also display
 * the message that has been painted if necessary.
 *
 * \param inputs List of long long integers to execute as an Intcode program.
 * \param startWhite If true, then the starting panel is considered painted
 * white. Else, it is considered painted black.
 * \param display If true, then the final state of the board is displayed in
 * the shell.
 * \param debug Whether or not the IntcodeProgram should debug its execution at
 * each instruction processing.
 * \return Last output of the program.
 */
long long processInputs(std::vector<long long> inputs, bool startWhite=false, bool display=false, bool debug=false) {
  // prepare the board and the set of painted panels:
  // - the board only remembers the panels painted white
  // - the painted set remembers all the panels that have been painted at least
  // once
  std::set<std::string> board;
  std::set<std::string> painted;
  // initialize the painting robot: facing up, at the origin coordinates
  int dir = 0, x = 0, y = 0;
  std::string pos = strFormat("%d,%d", x, y);
  // (if starting white: mark the current panel as already painted white)
  if (startWhite) {
    board.insert(pos);
  }

  // create program
  IntcodeProgram* program = new IntcodeProgram(inputs, debug);
  bool running = true;
  int input, state, color, rotation, m;
  int minX = 1e8, maxX = -1e8, minY = 1e8, maxY = -1e8;
  // execute the program until it halts (but pause every 2 outputs)
  while (running) {
    // get the input depending on the state of the panel: if painted white
    // (i.e. visible in the board), the input is 1; else it is 0
    input = (board.find(pos) != board.end()) ? 1 : 0;
    // insert the input in the program's memory
    program->pushMemory(input);
    // execute until 2 digits have been outputted
    state = program->run(2);
    // check for state:
    // . if paused: parse outputs and apply the actions
    if (state == 1) {
      color = (int)(program->getOutputAt(0));
      rotation = (int)(program->getOutputAt(1));
      program->resetOutput();
      if (color == 1) {
        board.insert(pos);
      } else {
        board.erase(pos);
      }
      painted.insert(pos);
      m = (rotation == 0) ? -1 : 1;
      dir += m;
      dir = ((dir % 4) + 4) % 4;
      switch (dir) {
        case 0: y--; break; // up
        case 1: x++; break; // right
        case 2: y++; break; // down
        case 3: x--; break; // left
        default: break;
      }
      pos = strFormat("%d,%d", x, y);
      // (update boundaries for optional display)
      if (x < minX) minX = x;
      if (x > maxX) maxX = x;
      if (y < minY) minY = y;
      if (y > maxY) maxY = y;
    }
    // . else: stop the program
    else {
      running = false;
      break;
    }
  }
  
  // if necessary, display the final message, i.e. the board that has been
  // printed (and only contains the painted panels)
  if (display) {
    std::cout << "\n";
    for (int y = minY; y <= maxY; y++) {
      for (int x = minX; x <= maxX; x++) {
        pos = strFormat("%d,%d", x, y);
        if (board.find(pos) != board.end()) {
          std::cout << "█";
        } else {
          std::cout << " ";
        }
      }
      std::cout << "\n";
    }
    std::cout << "\n";
  }
  
  // clean up data
  delete program;
  return painted.size();
}

int main(int argc, char const *argv[]) {
  // get input data
  std::string dataPath = "../data/day11.txt";
  std::string data = readFile(dataPath);
  std::vector<long long> inputs = parseToLongLongsWithDelimiter(data, ",");
  
  // Part I
  long long solution1 = processInputs(inputs);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  processInputs(inputs, true, true);
  std::cout << "PART II (see the shell)" << '\n';
  
  return 0;
}

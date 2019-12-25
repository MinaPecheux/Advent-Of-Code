/**
 * \file day13.cpp
 * \brief AoC 2019 - Day 13 (C++ version)
 * \author Mina Pêcheux
 * \date 2019
 *
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * ---------------------------------------------
 * Day 13: Care Package
 * =============================================
 */
#include "utils.hpp"
#include "parser.hpp"
#include "intcode.hpp"

// [ Computation functions ]
// -------------------------

typedef std::map<std::string,char> Board;
int X_MIN, X_MAX, Y_MIN, Y_MAX;

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/

/**
 * \fn void displayBoard(Board& board)
 * \brief Displays the board in the shell.
 *
 * \param board Reference to the board to display.
 */
void displayBoard(Board& board) {
  std::string pos;
  for (int y = Y_MIN; y <= Y_MAX; y++) {
    for (int x = X_MIN; x <= X_MAX; x++) {
      pos = strFormat("%d,%d", x, y);
      if (board.find(pos) != board.end()) {
        switch (board[pos]) {
          case 'N': std::cout << " "; break;
          case 'W': std::cout << "█"; break;
          case 'B': std::cout << "□"; break;
          case 'H': std::cout << "▂"; break;
          case 'O': std::cout << "●"; break;
          default: break;
        }
      } else {
        std::cout << " ";
      }
    }
    std::cout << "\n";
  }
  std::cout << "\n";
}

/**
 * \fn int countBlocks(std::vector<long long> inputs, Board& board, bool display=false, bool debug=false)
 * \brief Executes the Intcode program on the provided inputs and finds out the
 * number of blocks on the screen when the game exits. It also returns the
 * board when the game exits (i.e. the initial board since no game was actually
 * played).
 *
 * \param inputs List of long long integers to execute as an Intcode program.
 * \param board Reference to the initial game board (to fill).
 * \param display Whether or not to display the board after the game exits.
 * \param debug Whether or not the IntcodeProgram should debug its execution at
 * each instruction processing.
 * \return Number of blocks on the screen when the game exits.
 */
int countBlocks(std::vector<long long> inputs, Board& board, bool display=false, bool debug=false) {
  // create program
  IntcodeProgram* program = new IntcodeProgram(inputs, debug);
  bool running = true;
  int x, y, id, state, nBlocks = 0;
  int xMin = 1e8, xMax = -1e8, yMin = 1e8, yMax = -1e8;
  std::string pos;
  char marker;
  // execute the program until it halts (but pause every 3 outputs)
  while (running) {
    // execute until 3 digits have been outputted
    state = program->run(3);
    // check for state:
    // . if paused: parse outputs and apply the actions
    if (state == 1) {
      x = (int)(program->getOutputAt(0));
      y = (int)(program->getOutputAt(1));
      id = (int)(program->getOutputAt(2));
      program->resetOutput();
      pos = strFormat("%d,%d", x, y);
      switch (id) {
        case 0: marker = 'N'; break;
        case 1: marker = 'W'; break;
        case 2: marker = 'B'; nBlocks++; break;
        case 3: marker = 'H'; break;
        default: marker = 'O'; break;
      }
      board[pos] = marker;
      // (update boundaries for optional display)
      if (x < xMin) xMin = x;
      if (x > xMax) xMax = x;
      if (y < yMin) yMin = y;
      if (y > yMax) yMax = y;
    }
    // . else: stop the program
    else {
      running = false;
      break;
    }
  }
  X_MIN = xMin; X_MAX = xMax; Y_MIN = yMin; Y_MAX = yMax;
  if (display) {
    displayBoard(board);
  }

  return nBlocks;
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/

/**
 * \fn int computeScore(Board& board, std::vector<long long> inputs, bool debug=false)
 * \brief Executes the Intcode program on the provided inputs and finds out the
 * score of the player when the last block has been destroyed.
 *
 * \param board Reference to the initial game board (already filled).
 * \param inputs List of long long integers to execute as an Intcode program.
 * \param debug Whether or not the IntcodeProgram should debug its execution at
 * each instruction processing.
 * \return Final score of the player.
 */
int computeScore(Board& board, std::vector<long long> inputs, bool debug=false) {
  int x, y;
  int px, bx;
  // get paddle and ball coordinates
  for (auto b : board) {
    if (b.second == 'H') {
      decomposeCoordinates(b.first, x, y);
      px = x;
    } else if (b.second == 'O') {
      decomposeCoordinates(b.first, x, y);
      bx = x;
    }
  }
  int initNBlocks = -1, lastNBlocks = -1, nBlocks = -1;
  
  // create program
  IntcodeProgram* program = new IntcodeProgram(inputs, debug);
  // insert quarters to run in "free mode"
  program->setProgramData(0, 2);
  
  bool running = true;
  int state, id, c, score = -1;
  size_t debugLength;
  std::string pos;
  char marker;
  std::cout << "Remaining block(s):\n";
  // execute the program until it halts (but pause every 3 outputs)
  while (running) {
    // move the paddle to catch the ball and continue the game
    if (px < bx) { // move right
      program->insertMemory(1);
    } else if (px > bx) { // move left
      program->insertMemory(-1);
    } else { // reset movement to null
      program->insertMemory(0);
    }
    
    // execute until 3 digits have been outputted
    state = program->run(3);
    // check for state:
    // . if paused: parse outputs and apply the actions
    if (state == 1) {
      x = (int)(program->getOutputAt(0));
      y = (int)(program->getOutputAt(1));
      id = (int)(program->getOutputAt(2));
      program->resetOutput();
      if (x == -1 && y == 0) {
        score = id;
        // if outputting score and no more blocks: game ends
        if (nBlocks == 0) {
          running = false;
          std::cout << "\n";
          break;
        }
      } else {
        pos = strFormat("%d,%d", x, y);
        switch (id) {
          case 0: marker = 'N'; break;
          case 1: marker = 'W'; break;
          case 2: marker = 'B'; break;
          case 3:
            marker = 'H';
            px = x;
            break;
          default:
            marker = 'O';
            bx = x;
            break;
        }
        board[pos] = marker;
      }
    } else {
      running = false;
      break;
    }
    // . check to see if all blocks have disappeared
    nBlocks = 0;
    for (auto b : board) {
      if (b.second == 'B') nBlocks++;
    }
    // (initial blocks count, if need be)
    if (initNBlocks == -1) {
      initNBlocks = nBlocks;
      debugLength = std::to_string(initNBlocks).length();
    }
    // (if number of remaining blocks changed, output it)
    if (lastNBlocks != nBlocks) {
      c = 50 * nBlocks / initNBlocks;
      std::cout << "\r";
      for (int i = 0; i < c; i++) std::cout << "■";
      for (int i = c; i < 50; i++) std::cout << " ";
      for (int i = std::to_string(nBlocks).length(); i <= debugLength; i++) {
        std::cout << " ";
      }
      std::cout << nBlocks;
      lastNBlocks = nBlocks;
    }
  }
  return score;
}

int main(int argc, char const *argv[]) {
  // get input data
  std::string dataPath = "../data/day13.txt";
  std::string data = readFile(dataPath);
  std::vector<long long> inputs = parseToLongLongsWithDelimiter(data, ",");
  Board board;
  
  // Part I
  int solution1 = countBlocks(inputs, board, true);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = computeScore(board, inputs);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  return 0;
}

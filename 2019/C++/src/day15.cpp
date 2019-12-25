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
#include <map>
#include <queue>
#include "utils.hpp"
#include "parser.hpp"
#include "intcode.hpp"

// [ Util class ]
// --------------

/**
 * \class MazeSolver
 * \brief Util class to explore the maze. The exploration is done by a robot
 * running an Intcode program. The solver can also find the shortest path to
 * a specific point in the maze and compute flows from a given source point.
 * 
 * The robot can move in 4 direction, therefore a move is an integer that can
 * be 1: "north", 2: "south", 3: "west", 4: "east". Tiles in the maze board can
 * be 0: "walls", 1: "empty", 2: "oxygen source" or 3: "oxygen filled".
 */
class MazeSolver {
  
public:
  const std::map<int,int> BACKTRACK = { {1, 2}, {2, 1}, {3, 4}, {4, 3} };
  
  /**
   * \fn Constructor
   * \brief Builds a new instance of MazeSolver.
   *
   * \param program Instance of Intcode program to run to move the robot.
   * \param startX Initial horizontal position of the robot in the maze.
   * \param startY Initial vertical position of the robot in the maze.
   */
  MazeSolver(IntcodeProgram* program, int startX, int startY) {
    this->program_ = program;
    this->board_[strFormat("%d,%d", startX, startY)] = 1;
    this->startX_ = startX;
    this->startY_ = startY;
    this->targetPosition_ = "";
    this->xMin_ = 1e8; this->xMax_ = -1;
    this->yMin_ = 1e8; this->yMax_ = -1;
  }
  /**
   * \fn Destructor
   * \brief Destroys an instance of MazeSolver.
   */
  ~MazeSolver() {}
  
  /**
   * \fn void explore()
   * \brief Explores the maze to get value of all the tiles in it.
   */
  void explore() {
    // launch recursive discovery of the maze
    this->x_ = this->startX_;
    this->y_ = this->startY_;
    this->walk_();
    // get board boundaries
    int x, y;
    for (auto tile : this->board_) {
      decomposeCoordinates(tile.first, x, y);
      if (x < this->xMin_) this->xMin_ = x;
      if (x > this->xMax_) this->xMax_ = x;
      if (y < this->yMin_) this->yMin_ = y;
      if (y > this->yMax_) this->yMax_ = y;
    }
  }
  
  /**
   * \fn std::vector<std::string> findShortestPath(std::string source="", std::string target="")
   * \brief Finds the shortest path between two positions in the maze board by
   * applying Dijkstra's algorithm.
   *
   * \param source If not empty, start position of the path. Else, the start
   * position that was stored for the MazeSolver instance is taken.
   * \param target If not empty, target position of the path. Else, the target
   * position that was found by exploring the MazeSolver instance is taken.
   * \return Shortest path between the two positions in the maze.
   */
  std::vector<std::string> findShortestPath(std::string source="", std::string target="") {
    std::vector<std::string> path;
    
    // prepare source and target positions
    if (source == "") {
      source = strFormat("%d,%d", this->startX_, this->startY_);
    }
    if (target == "") {
      target = this->targetPosition_;
    }
    
    std::map<std::string,std::pair<std::string,int> > shortestPaths, destinations;
    shortestPaths[source] = std::make_pair("", 0);
    std::string currentPosition = source;
    std::set<std::string> visited;
    std::vector<std::string> neighbors;
    int minDistance = -1;
    int currentWeight, currentShortestWeight, weight;
    // compute shortest paths for each position
    while (currentPosition != target) {
      visited.insert(currentPosition);
      neighbors = this->getNeighbors_(currentPosition);
      currentWeight = shortestPaths[currentPosition].second;
      for (auto neighbor : neighbors) {
        weight = currentWeight + 1;
        if (shortestPaths.find(neighbor) == shortestPaths.end()) {
          shortestPaths[neighbor] = std::make_pair(currentPosition, weight);
        } else {
          currentShortestWeight = shortestPaths[neighbor].second;
          if (currentShortestWeight > weight) {
            shortestPaths[neighbor] = std::make_pair(currentPosition, weight);
          }
        }
      }
      
      minDistance = -1;
      destinations.clear();
      for (auto p : shortestPaths) {
        if (visited.find(p.first) == visited.end()) {
          destinations[p.first] = p.second;
        }
      }
      if (destinations.size() == 0) {
        return path;
      }
      for (auto d : destinations) {
        if (minDistance == -1 || d.second.second < minDistance) {
          currentPosition = d.first;
          minDistance = d.second.second;
        }
      }
    }
    
    // work back through destinations in shortest path
    std::string nextPosition;
    while (currentPosition != "") {
      path.push_back(currentPosition);
      nextPosition = shortestPaths[currentPosition].first;
      currentPosition = nextPosition;
    }
    return path;
  }
  
  /**
   * \fn int oxygenFill()
   * \brief Fills the maze with oxygen from the oxygen source that was found
   * during the exploration process and returns the number of required
   * iterations to complete the action.
   *
   * \return Number of iterations required to fill the entire maze board.
   */
  int oxygenFill() {
    // (if target position has not been found yet, abort!)
    if (this->targetPosition_ == "") {
      return -1;
    }
    // fill the board with oxygen starting from the oxygen system position
    return this->fill_();
  }

  /**
   * \fn void printBoard()
   * \brief Displays the board in the shell.
   */
  void printBoard() {
    std::string pos;
    for (int y = this->yMin_; y <= this->yMax_; y++) {
      for (int x = this->xMin_; x <= this->xMax_; x++) {
        if (x == this->startX_ && y == this->startY_) {
          std::cout << "S";
        } else {
          pos = strFormat("%d,%d", x, y);
          if (this->board_.find(pos) != this->board_.end()) {
            switch (this->board_[pos]) {
              case 0: std::cout << "█"; break;
              case 1: std::cout << " "; break;
              case 2: std::cout << "●"; break;
              default: break;
            }
          } else {
            std::cout << " ";
          }
        }
      }
      std::cout << "\n";
    }
    std::cout << "\n";
  }
  
private:
  std::string getNeighborPosition_(int x, int y, int move) {
    switch (move) {
      case 1: return strFormat("%d,%d", x, y-1);
      case 2: return strFormat("%d,%d", x, y+1);
      case 3: return strFormat("%d,%d", x-1, y);
      case 4: return strFormat("%d,%d", x+1, y);
      default: break;
    }
    return strFormat("%d,%d", x, y);
  }
  
  std::vector<std::string> getNeighbors_(std::string pos) {
    int x, y;
    decomposeCoordinates(pos, x, y);
    return this->getNeighbors_(x, y);
  }
  std::vector<std::string> getNeighbors_(int x, int y) {
    std::vector<std::string> neighbors;
    std::string neighborPos;
    int v;
    for (int dir = 1; dir < 5; dir++) {
      neighborPos = this->getNeighborPosition_(x, y, dir);
      if (this->board_.find(neighborPos) != this->board_.end()) {
        v = this->board_[neighborPos];
        if (v == 1 || v == 2) {
          neighbors.push_back(neighborPos);
        }
      }
    }
    return neighbors;
  }
  
  /**
   * \fn void walk_(int lastDir=0)
   * \brief Recursively walks through the maze to explore it.
   *
   * \param lastDir Last direction the robot took - can be used to backtrack if
   * the robot is stuck.
   */
  void walk_(int lastDir=0) {
    // get all accessible neighbor tiles
    std::vector<std::string> neighbors;
    for (int dir = 1; dir < 5; dir++) {
      neighbors.push_back(this->getNeighborPosition_(this->x_, this->y_, dir));
    }
    std::vector<bool> explored;
    for (auto n : neighbors) {
      if (this->board_.find(n) == this->board_.end()) {
        explored.push_back(false);
      } else {
        explored.push_back(true);
      }
    }
    // remember the robot's program current state for further restore
    IntcodeProgramState* currentState = this->program_->memorizeState();
    // try each direction
    int result;
    for (int dir = 1; dir < 5; dir++) {
      // (check if the tile is not yet explored)
      if (!explored[dir - 1]) {
        // restore cached store and prepare next movement + make robot action
        this->program_->restoreState(currentState);
        this->program_->insertMemory(dir);
        this->program_->run(1);
        result = (int)(this->program_->getLastOutput());
        this->program_->resetOutput();
        // use robot's feedback to update the board
        this->board_[neighbors[dir - 1]] = result;
        // recurse depending on feedback
        if (result != 0) { // if no wall
          if (result == 2) { // if reached target
            this->targetPosition_ = neighbors[dir - 1];
          }
          decomposeCoordinates(neighbors[dir - 1], this->x_, this->y_);
          this->walk_(dir);
        }
      }
    }
    // if stuck: backtrack!
    if (this->x_ != this->startX_ && this->y_ != this->startY_) {
      this->program_->restoreState(currentState);
      int r = MazeSolver::BACKTRACK.at(lastDir);
      this->program_->insertMemory(r);
      this->program_->run(1);
      decomposeCoordinates(
        this->getNeighborPosition_(this->x_, this->y_, lastDir),
        this->x_, this->y_
      );
    }

    delete(currentState);
  }
  
  /**
   * \fn int fill_()
   * \brief Util function that actually fills the maze in a BFS-like process and
   * finds out how many iterations the process requires.
   *
   * \return Number of iterations required to fill the entire maze board.
   */
  int fill_() {
    int iterations = 0;
    // tiles to check (store the target position initially)
    std::queue<std::pair<std::string,int> > toCheck;
    toCheck.push(std::make_pair(this->targetPosition_, 0));
    this->board_[this->targetPosition_] = 3;
    // compute until there are no tiles left
    std::string pos;
    int generation;
    std::vector<std::string> neighbors;
    while (!toCheck.empty()) {
      // . get back tile information
      pos = toCheck.front().first;
      generation = toCheck.front().second;
      toCheck.pop();
      // get all neighbors of the current position (only returns the ones that
      // are empty, i.e. not already filled with oxygen)
      neighbors = this->getNeighbors_(pos);
      // . for each, fill it and add it to the queue of positions
      for (auto neighbor : neighbors) {
        this->board_[neighbor] = 3;
        toCheck.push(std::make_pair(neighbor, generation + 1));
      }
      // update the total number of flow iterations
      if (generation > iterations) {
        iterations = generation;
      }
    }
    
    return iterations;
  }
  
  IntcodeProgram* program_;
  std::map<std::string,int> board_;
  std::set<std::string> visited_;
  int startX_; int startY_;
  int x_; int y_;
  int xMin_; int xMax_; int yMin_; int yMax_;
  std::string targetPosition_;
};

// [ Computation functions ]
// -------------------------

/*------------------------------------------------------------------------------
  Part I
------------------------------------------------------------------------------*/

/**
 * \fn int findOxygenSystem(MazeSolver* solver, bool display=false)
 * \brief Executes the Intcode program on the provided inputs and finds out the
 * required number of moves to reach the oxygen system in the room.
 *
 * \param solver Pointer to the MazeSolver instance (already created).
 * \param display Whether or not to display the board after the game exits.
 * \return Number of moves required to reach the oxygen system (i.e. length of
 * the shortest path to the system).
 */
int findOxygenSystem(MazeSolver* solver, bool display=false) {
  // run the maze solver to explore the maze fully
  solver->explore();
  // use Dijkstra's algorithm to get the shortest path between the start
  // position of the robot and the target position (position of the oxygen
  // system)
  std::vector<std::string> path = solver->findShortestPath();
  // optionally print the board and the shortest path
  if (display) {
    solver->printBoard();
  }
  return path.size() - 1; // remove 1 for the start position
}

/*------------------------------------------------------------------------------
  Part II
------------------------------------------------------------------------------*/

/**
 * \fn int fillOxygen(MazeSolver* solver)
 * \brief Uses the previously prepared maze solver to see how many iterations
 * are required to fill the whole map with oxygen.
 *
 * \param solver Pointer to the MazeSolver instance (already created).
 * \return Number of required iterations to fill the whole map with oxygen.
 */
int fillOxygen(MazeSolver* solver) {
  return solver->oxygenFill();
}


int main(int argc, char const *argv[]) {
  // get input data
  std::string dataPath = "../data/day15.txt";
  std::string data = readFile(dataPath);
  std::vector<long long> inputs = parseToLongLongsWithDelimiter(data, ",");

  // create program
  IntcodeProgram* program = new IntcodeProgram(inputs);
  // prepare the maze solver
  MazeSolver* solver = new MazeSolver(program, 0, 0);
  
  // Part I
  int solution1 = findOxygenSystem(solver);
  std::cout << "PART I: solution = " << solution1 << '\n';
  
  // Part II
  int solution2 = fillOxygen(solver);
  std::cout << "PART II: solution = " << solution2 << '\n';
  
  // clean up data
  delete(solver);
  return 0;
}

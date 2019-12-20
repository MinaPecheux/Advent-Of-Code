/**
 * \file intcode.h
 * \brief AoC 2019 - Intcode interpreter
 * \author Mina Pêcheux
 * \date 2019
 *
 * Header file for intcode.c.
 * Intcode interpreter used multiple times in AoC 2019
 * puzzles.
 */
#pragma once

#include <vector>
#include <map>

#define OP_HALT                  99
#define OP_ADD                    1
#define OP_MULT                   2
#define OP_READ                   3
#define OP_WRITE                  4
#define OP_JUMP_IF_TRUE           5
#define OP_JUMP_IF_FALSE          6
#define OP_SET_IF_LT              7
#define OP_SET_IF_EQ              8
#define OP_OFFSET_RELATIVE_BASE   9

extern const char* OPERATION_NAMES[];

/**
 * \class IntcodeProgram
 * \brief Util class to represent a program instance with its own instructions,
 * memory, run state and instruction pointer. Allows for multiple instances
 * in parallel to interact without overwriting data.
 */
class IntcodeProgram {
  
public:
  static int INSTANCE_ID;
  
  /**
   * \fn Constructor
   * \brief Builds a new instance of IntcodeProgram.
   *
   * \param program Original Intcode program to execute (will be copied to avoid
   * in-place modification).
   * \param debug Whether or not the IntcodeProgram should debug its execution
   * at each instruction processing.
   */
  IntcodeProgram(std::vector<long long> program, bool debug=false);
  /**
   * \fn Destructor
   * \brief Destroys an instance of IntcodeProgram.
   */
  ~IntcodeProgram();
  
  // getters and setters
  /**
   * \fn long long getProgramData(int index) const
   * \brief Gets a value in the instance's program at a given position (if the
   * position is not associated to any value, returns 0).
   *
   * \param index Position to get.
   * \return Program data value.
   */
  long long getProgramData(int index) const;
  /**
   * \fn std::vector<long long> getOutput() const
   * \brief Gets the current output of the program instance.
   *
   * \return Currently outputted data.
   */
  std::vector<long long> getOutput() const;
  /**
   * \fn long long getOutputAt(int index) const
   * \brief Gets a value outputted by the program, by index.
   *
   * \return Outputtted data value at index.
   */
  long long getOutputAt(int index) const;
  /**
   * \fn long long getLastOutput() const
   * \brief Gets the last value outputted in the program instance.
   *
   * \return Last outputtted data value.
   */
  long long getLastOutput() const;
  /**
   * \fn long long popMemory()
   * \brief Pops the last value in the program instance's memory and returns it.
   *
   * \return Last data value in memory.
   */
  long long popMemory();
  /**
   * \fn void setProgramData(int index, long long value)
   * \brief Sets a value in the instance's program at a given position.
   *
   * \param index Position to insert at.
   * \param value Value to insert.
   */
  void setProgramData(int index, long long value);
  /**
   * \fn void pushMemory(long long value)
   * \brief Pushes a value at the end of the program instance's memory.
   *
   * \param value Value to insert.
   */
  void pushMemory(long long value);
  /**
   * \fn void pushMemory(long long value)
   * \brief Pushes a value at the end of the program instance's memory.
   *
   * \param value Value to insert.
   */
  void pushMemoryMultiple(std::vector<long long> values);
  
  // methods
  /**
   * \fn void run(unsigned int pauseEvery=0)
   * \brief Runs the instance by executing its Intcode program from start to
   * finish (until it halts).
   *
   * \param pauseEvery If not null, number of output digits to store before
   * pausing. If it is zero, the execution should proceed until it reached the
   * halt operation.
   * \return Status code (0: halted, 1: paused).
   */
  int run(unsigned int pauseEvery=0);
  /**
   * \fn void runMultiple(std::vector<IntcodeProgram*> instances)
   * \brief Runs the instance by executing its Intcode program either from
   * scratch or from where it last stopped, as part of a pool of instances
   * that feed each other with output to input connection.
   *
   * \param instances List of all program instances in the pool.
   * \return Index of the next instance in the pool to run, if any.
   */
  int runMultiple(std::vector<IntcodeProgram*> instances);
  /**
   * \fn void checkRunning(unsigned int phase)
   * \brief Checks if the instance is already running or if it should be
   * initialized with its phase setting.
   *
   * \param phase Phase setting for this instance.
   */
  void checkRunning(unsigned int phase);
  /**
   * \fn void reset()
   * \brief Resets the program instance in case you want to re-run the same
   * program with a fresh start.
   */
  void reset();
  /**
   * \fn void resetOutput()
   * \brief Resets the program output.
   */
  void resetOutput();
  
  /**
   * \fn void printProgram() const
   * \brief Prints the current state of the instruction pointer and the program
   * in the instance.
   */
  void printProgram() const;
  
private:
  // private methods
  /**
   * \fn bool processOpcode_()
   * \brief Processes the next instruction in the program with the current
   * memory and instruction pointer.
   *
   * \return Whether or not the program should pause (if pause is activated).
   */
  bool processOpcode_();
  /**
   * \fn void getIndex_(long long& index, int& mode)
   * \brief Gets the index and the mode corresponding to the cell pointed by the
   * current instruction pointer (in "address", "immediate value" or "relative"
   * mode).
   *
   * \param index Reference to the index variable to update.
   * \param mode Reference to the mode variable to update.
   */
  void getIndex_(long long& index, int& mode);
  /**
   * \fn long long getValue_(bool keepIndex=false)
   * \brief Gets the value corresponding to the next input in the program data.
   * The function also fills a debug string in case the debug is activated for
   * the IntcodeProgram.
   *
   * \param keepIndex Whether or not the function should keep the index as is,
   * or interpret it as an address in the program.
   * \return Program data value.
   */
  long long getValue_(bool keepIndex=false);
  /**
   * \fn void pushOutput_(long long value)
   * \brief Pushes a value to the current output of the program instance.
   *
   * \param value Value to insert.
   */
  void pushOutput_(long long value);
  
  // private attributes
  int id_;
  std::map<int, long long> program_;
  std::map<int, long long> initialProgram_;
  std::vector<long long> memory_;
  std::vector<long long> output_;
  int mode1_; int mode2_; int mode3_;
  int inputId_;
  int instructionPtr_;
  int relativeBase_;
  bool debug_;
  bool isRunning_;
  std::string debugStr_;
};

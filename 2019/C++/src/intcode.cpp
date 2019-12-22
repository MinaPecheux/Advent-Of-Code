/**
 * \file intcode.cpp
 * \brief AoC 2019 (C++ version) - Intcode interpreter
 * \author Mina Pêcheux
 * \date 2019
 *
 * Intcode interpreter used multiple times in AoC 2019
 * puzzles.
 */
#include "utils.hpp"
#include "intcode.hpp"

using namespace std;

/*------------------------------------------------------------------------------
  VARIABLES
------------------------------------------------------------------------------*/

int IntcodeProgram::INSTANCE_ID = 0;
const char* OPERATION_NAMES[] = { "", "add", "mult", "read", "write",
  "jump_if_true", "jump_if_false", "set_if_lt", "set_if_eq",
  "offset_relative_base" };

/*------------------------------------------------------------------------------
  FUNCTIONS
------------------------------------------------------------------------------*/
/* Constructor/Destructor ----------------------------------------------------*/
IntcodeProgram::IntcodeProgram(vector<long long> program, bool debug) {
  for (int i = 0; i < program.size(); i++) {
    this->program_[i] = program[i];
    this->initialProgram_[i] = program[i];
  }
  this->debug_ = debug;
  this->id_ = IntcodeProgram::INSTANCE_ID++;
  this->instructionPtr_ = 0;
  this->relativeBase_ = 0;
  this->isRunning_ = false;
}

IntcodeProgram::~IntcodeProgram() {}

/* Getters and Setters -------------------------------------------------------*/
long long IntcodeProgram::getProgramData(int index) const {
  map<int,long long>::const_iterator it = this->program_.find(index);
  return (it != this->program_.end()) ? it->second : 0;
}
int IntcodeProgram::getInstructionPtr() const {
  return this->instructionPtr_;
}
std::vector<long long> IntcodeProgram::getOutput() const {
  return this->output_;
}
long long IntcodeProgram::getOutputAt(int index) const {
  if (index < 0) index += this->output_.size();
  return (this->output_.size() == 0) ? -1 : this->output_[index];
}
long long IntcodeProgram::getLastOutput() const {
  return (this->output_.size() == 0) ? -1 : this->output_.back();
}
long long IntcodeProgram::popMemory() {
  long long v = this->memory_.front();
  // this->memory_.pop_front();
  this->memory_.erase(this->memory_.begin());
  return v;
}
void IntcodeProgram::setProgramData(int index, long long value) {
  this->program_[index] = value;
}
void IntcodeProgram::pushMemory(long long value) {
  this->memory_.push_back(value);
}
void IntcodeProgram::pushMemory(std::vector<long long> values) {
  this->memory_.insert(this->memory_.end(), values.begin(), values.end());
}
void IntcodeProgram::insertMemory(long long value) {
  this->memory_.insert(this->memory_.begin(), value);
}
void IntcodeProgram::insertMemory(std::vector<long long> values) {
  this->memory_.insert(this->memory_.begin(), values.begin(), values.end());
}

/* Private methods -----------------------------------------------------------*/
bool IntcodeProgram::processOpcode_() {
  // get the current instruction
  int instruction = (int)(this->getProgramData(this->instructionPtr_));
  // extract the operation code (opcode) and check for halt or error
  int opcode = instruction % 10 + 10 * ((instruction / 10) % 10);
  if (opcode == OP_HALT) {
    if (this->debug_) {
      cout << "\n[ 99 ] - Exiting\n";
    }
    this->instructionPtr_ = -1;
    return false;
  }
  if (opcode < 1 || opcode > 9) {
    this->instructionPtr_ = -1;
    return false;
  }
  // get the information on this operation for further process and debug
  const char* opname = OPERATION_NAMES[opcode];
  this->mode1_ = (instruction / 100) % 10;
  this->mode2_ = (instruction / 1000) % 10;
  this->mode3_ = (instruction / 10000) % 10;
  this->inputId_ = 0;
  if (this->debug_) {
    this->debugStr_ = strFormat(
      "\n[ % 3d ] - inst = %05d :: op = %s (%d), modes = %d, %d, %d\n",
      this->instructionPtr_, instruction, opname, opcode, this->mode1_,
      this->mode2_, this->mode3_
    );
  }
  // prepare the pause mode as false (could be modified by some operations)
  bool pause = false;
  // execute the right operation depending on the opcode
  this->instructionPtr_++;
  long long va, vb, vc, vm;
  switch (opcode) {
    case OP_ADD:
      va = this->getValue_();
      vb = this->getValue_();
      vc = this->getValue_(true);
      this->setProgramData(vc, va + vb);
      break;
    case OP_MULT:
      va = this->getValue_();
      vb = this->getValue_();
      vc = this->getValue_(true);
      this->setProgramData(vc, va * vb);
      break;
    case OP_READ:
      vm = this->popMemory();
      if (this->memory_.size() == 0) {
        this->instructionPtr_ = -1;
        return false;
      }
      va = this->getValue_(true);
      this->setProgramData(va, vm);
      break;
    case OP_WRITE:
      va = this->getValue_();
      this->pushOutput_(va);
      pause = true;
      break;
    case OP_JUMP_IF_TRUE:
      va = this->getValue_();
      vb = this->getValue_();
      if (va != 0) {
        this->instructionPtr_ = vb;
      }
      break;
    case OP_JUMP_IF_FALSE:
      va = this->getValue_();
      vb = this->getValue_();
      if (va == 0) {
        this->instructionPtr_ = vb;
      }
      break;
    case OP_SET_IF_LT:
      va = this->getValue_();
      vb = this->getValue_();
      vc = this->getValue_(true);
      this->setProgramData(vc, (va < vb) ? 1 : 0);
      break;
    case OP_SET_IF_EQ:
      va = this->getValue_();
      vb = this->getValue_();
      vc = this->getValue_(true);
      this->setProgramData(vc, (va == vb) ? 1 : 0);
      break;
    case OP_OFFSET_RELATIVE_BASE:
      this->relativeBase_ += this->getValue_();
      break;
  }
  
  if (this->debug_) {
    cout << this->debugStr_ << '\n';
  }
  
  return pause;
}

void IntcodeProgram::getIndex_(long long& index, int& mode) {
  // extract the mode for this input (and check if there are no more inputs for
  // this instruction; if so: abort)
  switch (this->inputId_) {
    case 0: mode = this->mode1_; break;
    case 1: mode = this->mode2_; break;
    case 2: mode = this->mode3_; break;
    default: mode = -1; break;
  }
  if (mode == -1) {
    index = -1;
    return;
  }
  // process the index depending on the mode
  switch (mode) {
    case 0:
      index = this->getProgramData(this->instructionPtr_);
      break;
    case 1:
      index = (long long)(this->instructionPtr_);
      break;
    case 2:
      index = this->getProgramData(this->instructionPtr_) + (long long)(this->relativeBase_);
      break;
    default:
      break;
  }
  // increase pointers
  this->instructionPtr_++;
  this->inputId_++;
}

long long IntcodeProgram::getValue_(bool keepIndex) {
  // get the index and mode
  long long index;
  int mode;
  this->getIndex_(index, mode);
  if (index == -1) {
    return -1;
  }
  // if necessary, apply the index as an address in the program code
  long long val = (!keepIndex) ? this->getProgramData((int)(index)) : index;
  // (fill the debug string in case of debug mode)
  this->debugStr_ += strFormat(" arg%d=%ld (idx=%ld, mode=%d) ;", this->inputId_,
    val, index, mode);
  return val;
}

void IntcodeProgram::pushOutput_(long long value) {
  this->output_.push_back(value);
}

/* Public methods ------------------------------------------------------------*/
int IntcodeProgram::run(unsigned int pauseEvery) {
  if (pauseEvery == 0) {
    // process while operation is not "halt"
    while (this->instructionPtr_ != -1) {
      this->processOpcode_();
    }
  } else {
    int nPause = 0;
    bool pause;
    // process while operation is not "halt"
    while (this->instructionPtr_ != -1) {
      pause = this->processOpcode_();
      if (pause) {
        nPause++;
      }
      if (pauseEvery == nPause) {
        nPause = 0;
        return (this->instructionPtr_ != -1) ? 1 : 0;
      }
    }
  }
  return 0;
}

int IntcodeProgram::runMultiple(vector<IntcodeProgram*> instances) {
  int nextInstance;
  long long output;
  int nInstances = instances.size();
  // if we stopped just before halting, we simply terminate the program and go
  // to the next instance
  if (this->output_.size() > 0 && this->instructionPtr_ == -1) {
    nextInstance = (this->id_ + 1) % nInstances;
    output = this->getLastOutput();
    instances[nextInstance]->pushMemory(output);
    return nextInstance;
  }
  // else we continue running the program from where we stopped
  bool pause;
  while (this->instructionPtr_ != -1) {
    pause = this->processOpcode_();
    // if we reached the halt op for the last instance
    if (this->instructionPtr_ == -1 && this->id_ == nInstances - 1) {
      return -1;
    }
    // else if we need to temporary pause the execution of this instance
    if (pause || this->instructionPtr_ == -1) {
      nextInstance = (this->id_ + 1) % nInstances;
      output = this->getLastOutput();
      instances[nextInstance]->pushMemory(output);
      return nextInstance;
    }
  }
  return -1;
}

void IntcodeProgram::checkRunning(unsigned int phase) {
  if (!this->isRunning_) {
    this->pushMemory(phase);
    this->isRunning_ = true;
  }
}

void IntcodeProgram::reset() {
  this->program_.clear();
  for (auto i : this->initialProgram_) {
    this->program_[i.first] = i.second;
  }
  this->memory_.clear();
  this->output_.clear();
  this->instructionPtr_ = 0;
  this->relativeBase_ = 0;
  this->isRunning_ = false;
}

void IntcodeProgram::resetOutput() {
  this->output_.clear();
}

void IntcodeProgram::printProgram() const {
  cout << "Current pointer: " << this->instructionPtr_ << '\n';
  for (auto p : this->program_) {
    cout << "program[" << p.first << "] = " << p.second << '\n';
  }
}

void IntcodeProgram::printMemory() const {
  for (int i = 0; i < this->memory_.size(); i++) {
    cout << "memory[" << i << "] = " << this->memory_[i] << '\n';
  }
}

void IntcodeProgram::printOutput() const {
  for (int i = 0; i < this->output_.size(); i++) {
    cout << "output[" << i << "] = " << this->output_[i] << '\n';
  }
}

/*
 * =============================================
 * [ ADVENT OF CODE ] (https://adventofcode.com)
 * 2019 - Mina Pêcheux: C# version
 * ---------------------------------------------
 * Intcode interpreter used in multiple puzzles.
 * ============================================= */

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

using CSharpUtils;

namespace CSharp2019
{
  /// <summary>Util class to represent a program instance with its own instructions,
  /// memory, run state and instruction pointer. Allows for multiple instances
  /// in parallel to interact without overwriting data.</summary>

  class IntcodeProgram
  {

    private delegate int PointerUpdateFunc(int a, int b);
    struct Operation
    {
      public string name;
      public PointerUpdateFunc pointerUpdate;
      public int nInputs;

      public Operation(string name, PointerUpdateFunc pointerUpdate, int nInputs) {
        this.name = name;
        this.pointerUpdate = pointerUpdate;
        this.nInputs = nInputs;
      }
    }

    private static Dictionary<int, Operation> OPERATIONS = new Dictionary<int, Operation>()
    {
      { 1, new Operation("add", (int a, int b) => a + b, 3) },
      { 2, new Operation("mult", (int a, int b) => a * b, 3) },
      { 3, new Operation("read", null, 1) },
      { 4, new Operation("write", null, 1) },
      { 5, new Operation("jumpIfTrue", null, 2) },
      { 6, new Operation("jumpIfFalse", null, 2) },
      { 7, new Operation("setIfLt", (int a, int b) => a < b ? 1 : 0, 3) },
      { 8, new Operation("setIfEq", (int a, int b) => a == b ? 1 : 0, 3) },
      { 9, new Operation("offsetRelativeBase", null, 1) },
    };
    private static int INSTANCE_ID = 0;

    private int _id;
    private Dictionary<int, int> _program;
    private Dictionary<int, int> _initialProgram; // safe copy for reset
    private List<int> _memory, _output, _modes;
    private int _instructionPtr;
    private int _relativeBase;

    private bool _isRunning;
    private int _inputId;
    private bool _debug;
    private string _debugStr;

    public Dictionary<int, int> Program { get => _program; }
    public List<int> Output { get => _output; }

    /// <summary>Constructor for the instance.</summary>
    /// <param name="program">Original Intcode program to execute (will be copied to
    /// avoid in-place modification), provided as an array of integers.</param>
    /// <param name="debug">Whether or not the IntcodeProgram should debug its
    /// execution at each instruction processing.</param>
    public IntcodeProgram(int[] program, bool debug = false)
    {
      _id = INSTANCE_ID++;
      _program = program.Select((v, i) => new { v, i }).ToDictionary(x => x.i, x => x.v);
      _initialProgram = new Dictionary<int, int>(_program);
      _memory = new List<int>();
      _output = new List<int>();

      _instructionPtr = 0;
      _relativeBase = 0;

      _isRunning = false;
      _inputId = 0;
      _debug = debug;
      _debugStr = string.Empty;
    }

    /// <summary>Changes the program in the program instance (i.e. gives new
    /// instructions) and resets the instance.</summary>
    /// <param name="program">Original Intcode program to execute (will be copied to
    /// avoid in-place modification), provided as an array of integers.</param>
    public void SetProgram(int[] program)
    {
      _initialProgram = program.Select((v, i) => new { v, i }).ToDictionary(x => x.i, x => x.v);
      Reset();
    }

    /// <summary>Resets the program instance in case you want to re-run the same
    /// program with a fresh start.</summary>
    public void Reset()
    {
      _program = new Dictionary<int, int>(_initialProgram);
      _instructionPtr = 0;
      _relativeBase = 0;

      _memory.Clear();
      _output.Clear();

      _isRunning = false;
      _inputId = 0;
      _debugStr = string.Empty;
    }

    /// <summary>Resets the output of the program to a blank slate.</summary>
    public void ResetOutput()
    {
      _output.Clear();
    }

    /// <summary>Creates a snapshot of the program's current state (for further
    /// restore).</summary>
    public (List<int>, Dictionary<int, int>, int) MemorizeState()
    {
      return (
        new List<int>(_memory),
        new Dictionary<int, int>(_program),
        _instructionPtr
      );
    }

    /// <summary>Restores a previous state in the instance.</summary>
    /// <param name="memory">Memory to restore.</param>
    /// <param name="program">Program to restore.</param>
    /// <param name="instructionPtr">Instruction pointer to restore.</param>
    public void RestoreState(List<int> memory, Dictionary<int, int> program, int instructionPtr)
    {
      _memory = memory;
      _program = program;
      _instructionPtr = instructionPtr;
    }

    /// <summary>Appends one or more value(s) in the instance's memory, in last
    /// position.</summary>
    /// <param name="data">Value(s) to insert.</param>
    public void PushMemory(params int[] data)
    {
      _memory.AddRange(data);
    }

    /// <summary>Inserts one or more value(s) in the instance's memory, in first
    /// position.</summary>
    /// <param name="data">Value(s) to insert.</param>
    public void InsertMemory(params int[] data)
    {
      _memory.InsertRange(0, data);
    }

    /// <summary>Checks if the instance is already running or if it should be
    /// initialized with its phase setting.</summary>
    /// <param name="phase">Phase setting for this instance.</param>
    public void CheckRunning(int phase)
    {
      if (!_isRunning) {
        InsertMemory(phase);
        _isRunning = true;
      }
    }

    /// <summary>Gets a value in the instance's program at a given position (if the
    /// position is not associated to any value, returns 0).</summary>
    /// <param name="index">Position to get.</param>
    /// <returns>Program data value.</returns>
    public int ProgramGetData(int index)
    {
      int value;
      return _program.TryGetValue(index, out value) ? value : 0;
    }

    /// <summary>Sets a value in the instance's program at a given position.</summary>
    /// <param name="index">Position to insert at.</param>
    /// <param name="data">Value to insert.</param>
    public void ProgramSetData(int index, int data)
    {
      _program[index] = data;
    }

    /// <summary>Runs the instance by executing its Intcode program from start to
    /// finish (until it halts).</summary>
    /// <param name="pauseEvery">If not -1, number of output digits to store before
    /// pausing. If -1, the execution should proceed until it reached the
    /// halt operation.</param>
    public int Run(int pauseEvery = -1)
    {
      // process while operation is not "halt"
      int nPause = 0;
      bool pause;
      while (_instructionPtr >= 0) {
        pause = ProcessOpcode();
        // check for pause
        if (pause)
          nPause++;
        if (pauseEvery == nPause) {
          nPause = 0;
          if (_instructionPtr != -1)
            return -2; // 'pause' state
          else
            return -3; // 'null' state
        }

        if (_instructionPtr == -4) {
          return -4; // 'error' state
        }
      }

      return 0; // 'finished' state
    }

    /// <summary>Gets the index and the mode corresponding to the cell pointed by the
    /// current instruction pointer (in "address", "immediate value" or
    /// "relative" mode).</summary>
    /// <returns>Index and mode of the next input.</returns>
    public (int, int) GetIndex()
    {
      // check if there are no more inputs for this instruction; if so: abort
      if (_modes.Count() == 0) return (-1, -1);
      // extract the mode for this input
      int mode = _modes.Pop<int>(0);
      // process the index depending on the mode
      int index;
      if (mode == 0) {
        index = ProgramGetData(_instructionPtr);
      } else if (mode == 1) {
        index = _instructionPtr;
      } else {
        index = ProgramGetData(_instructionPtr) + _relativeBase;
      }

      // increase the current instuction pointer
      _instructionPtr++;
      // increase the input id (for debug)
      if (_debug) _inputId++;
      
      return (index, mode);
    }

    /// <summary>Gets the value corresponding to the next input in the program data.
    /// The function also fills a debug string in case the debug is activated
    /// for the IntcodeProgram.</summary>
    /// <param name="keepIndex">Whether or not the function should keep the index as
    /// is, or interpret it as an address in the program.</param>
    /// <returns>Program data value.</returns>
    public int GetValue(bool keepIndex = false)
    {
      // get the index and mode
      (int index, int mode) = GetIndex();
      // if necessary, apply the index as an address in the program code
      if (index == -1) return -1;
      int val;
      if (!keepIndex) {
        val = ProgramGetData(index);
      } else {
        val = index;
      }
      
      // (fill the debug string in case of debug mode)
      _debugStr += $" arg{_inputId}={val} (idx={index}, mode={mode}) ;";

      return val;
    }

    /// <summary>Processes the next instruction in the program with the current memory
    /// and instruction pointer.</summary>
    /// <returns>Whether or not the program should pause (if pause is activated).</returns>
    public bool ProcessOpcode()
    {
      // get the current instruction
      string instruction = _program[_instructionPtr].ToString();
      // extract the operation code (opcode) and check for halt or error
      int opcode = int.Parse(instruction.Substring(Math.Max(0, instruction.Length - 2)));
      if (opcode == 99) {
        if (_debug) Console.WriteLine("[  99 ] - Exiting");
        _instructionPtr = -1;
        return false;
      }
      if (!OPERATIONS.ContainsKey(opcode)) {
        _instructionPtr = -4;
        return false;
      }

      // get the information on this operation for further process and debug
      Operation opData = OPERATIONS[opcode];
      string opname = opData.name;
      PointerUpdateFunc op = opData.pointerUpdate;
      int nInputs = opData.nInputs;
      string m = instruction.Substring(0, Math.Max(0, instruction.Length - 2));
      _modes = m
        .Reverse()
        .Select(c => int.Parse(c.ToString()))
        .ToList();
      for (int i = 0; i < nInputs - m.Length; i++)
        _modes.Add(0);
      List<int> opModes = new List<int>(_modes);

      // prepare the debug string in case debug mode is active
      if (_debug) {
          _inputId = 0;
          _debugStr = $"[ {_instructionPtr.ToString("000")} ] " +
            $"- inst = {int.Parse(instruction).ToString("00000")} " +
            $":: op = {opname} ({opcode}), "+
            $"modes = {String.Join(",", opModes.Select(x => x.ToString()))}\n";
      }
      // prepare the pause mode as false (could be modified by some operations)
      bool pause = false;

      // execute the right operation depending on the opcode
      _instructionPtr++;

      if (opcode == 1 || opcode == 2) { // add, multiply
        int va = GetValue();
        int vb = GetValue();
        int vc = GetValue(true);
        ProgramSetData(vc, op(va, vb));
      }
      else if (opcode == 3) { // read
        if (_memory.Count() == 0) {
          _instructionPtr = -1;
          return false;
        }
        int va = GetValue(true);
        int vm = _memory.Pop<int>(0);
        ProgramSetData(va, vm);
      }
      else if (opcode == 4) { // write
        int v = GetValue();
        _output.Add(v);
        pause = true;
      }
      else if (opcode == 5) { // jump if true
        int va = GetValue();
        int vb = GetValue();
        if (va != 0)
          _instructionPtr = vb;
      }
      else if (opcode == 6) { // jump if false
        int va = GetValue();
        int vb = GetValue();
        if (va == 0)
          _instructionPtr = vb;
      }
      else if (opcode == 7 || opcode == 8) { // set if less than, set if equal
        int va = GetValue();
        int vb = GetValue();
        int vc = GetValue(true);
        ProgramSetData(vc, op(va, vb) == 1 ? 1 : 0);
      }
      else if (opcode == 9) { // relative base offset
        _relativeBase += GetValue();
      }

      // if needed, print the debug string
      if (_debug) {
        _debugStr += "\n";
        Console.WriteLine(_debugStr);
      }

      return pause;
    }
  }
}

### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 11: Space Police
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: list(int)
    '''
    return [ int(x) for x in data.split(',') if x != '' ]

# [ Computation functions ]
# -------------------------
OPERATIONS = {
    1: ('add', lambda a, b: a + b, 3),
    2: ('mult', lambda a, b: a * b, 3),
    3: ('read', None, 1),
    4: ('write', None, 1),
    5: ('jump_if_true', None, 2),
    6: ('jump_if_false', None, 2),
    7: ('set_if_lt', lambda a, b: a < b, 3),
    8: ('set_if_eq', lambda a, b: a == b, 3),
    9: ('offset_relative_base', None, 1)
}

class ProgramInstance(object):
    
    '''Util class to represent a program instance with its own instructions,
    memory, run state and instruction pointer. Allows for multiple instances
    in parallel to interact without overwriting data.'''
    
    INSTANCE_ID = 0 # class variable that is common to all instances
    
    def __init__(self, program, debug=False):
        '''Initialization function for the instance.
        
        :param program: Original Intcode program to execute (will be copied to
            avoid in-place modification).
        :type program: list(int)
        :param debug: Whether or not the ProgramInstance should debug its
            execution at each instruction processing.
        :type debug: bool
        '''
        self.id = ProgramInstance.INSTANCE_ID
        ProgramInstance.INSTANCE_ID += 1
        self.program = { i: inst for i, inst in enumerate(program) }
        self.memory = []
        self.output = []
        self.modes = []
        self.instruction_ptr = 0
        self.relative_base = 0
        
        self.is_running = False
        self.debug = debug
        self._input_id = 0
        self._debug_str = ''
    
    def reset(self):
        '''Resets the program instance in case you want to re-run the same
        program with a fresh start.'''
        self.instruction_ptr = 0
        self.output = []
        self.memory = []
        self.is_running = False
        self._input_id = 0
        self._debug_str = ''
        
    def set_program(self, program):
        '''Changes the program in the program instance (i.e. gives new
        instructions) and resets the instance.
        
        :param program: Original Intcode program to execute (will be copied to
            avoid in-place modification).
        :type program: list(int)
        '''
        self.program = { i: inst for i, inst in enumerate(program) }
        self.reset()
        
    def reset_output(self):
        '''Resets the output of the program to a blank slate.'''
        self.output = []
    
    def memory_insert(self, data):
        '''Inserts a value in the instance's memory, in first position.
        
        :param data: Value to insert.
        :type data: int
        '''
        self.memory = [ data ] + self.memory
        
    def program_get_data(self, index):
        '''Gets a value in the instance's program at a given position (if the
        position is out of range, returns 0).
        
        :param index: Position to get.
        :type index: int
        :return: Program data value.
        :rtype: int
        '''
        return self.program.get(index, 0)
        
    def program_set_data(self, index, data):
        '''Sets a value in the instance's program at a given position (adds
        the intermediary indices if need be).
        
        :param index: Position to insert at.
        :type index: int
        :param data: Value to insert.
        :type data: int
        '''
        self.program[index] = data
        
    def run(self, pause_every=None):
        '''Runs the instance by executing its Intcode program from start to
        finish (until it halts).
        
        :param pause_every: If not None, number of output digits to store before
            pausing. If None, the execution should proceed until it reached the
            halt operation.
        :type pause_every: None or int
        '''
        # process while operation is not "halt"
        n_pause = 0
        while self.instruction_ptr is not None:
            pause = self.process_opcode()
            # check for pause
            if pause:
                n_pause += 1
            if pause_every == n_pause:
                n_pause = 0
                if self.instruction_ptr is not None:
                    return 'pause'
                else:
                    return None
            # abort if we errored
            if self.instruction_ptr == -1:
                return -1
        
    def run_multiple(self, instances):
        '''Runs the instance by executing its Intcode program either from
        scratch or from where it last stopped, as part of a pool of instances
        that feed each other with output to input connection.
        
        :param instances: List of all program instances in the pool.
        :type instances: list(ProgramInstance)
        :return: Index of the next instance in the pool to run, if any.
        :rtype: int
        '''
        # if we stopped just before halting, we simply terminate the program
        # and go to the next instance
        if self.instruction_ptr is None:
            next_instance = (self.id + 1) % len(instances)
            output = self.memory[-1]
            instances[next_instance].memory_insert(output)
            return next_instance
        # else we continue running the program from where we stopped
        while self.instruction_ptr is not None:
            pause = self.process_opcode()
            # if we reached the halt op for the last instance
            if self.instruction_ptr is None and self.id == len(instances) - 1:
                return -1
            # else if we need to temporary pause the execution of this
            # instance
            if pause or self.instruction_ptr is None:
                next_instance = (self.id + 1) % len(instances)
                output = self.memory[-1]
                instances[next_instance].memory_insert(output)
                return next_instance
            # else if we errored
            if self.instruction_ptr == -1:
                return None

    def get_index(self):
        '''Gets the index corresponding to the cell pointed by the current
        instruction pointer plus the current input (in "address", "immediate
        value" or "relative" mode).
        
        :return: Index and mode of the next input.
        :rtype: tuple(int, int)
        '''
        # check if there are no more inputs for this instruction; if so: abort
        if len(self.modes) == 0:
            return None, None
        # extract the mode for this input
        mode = self.modes.pop(0)
        # process the index depending on the mode
        if mode == 0:
            val = self.program_get_data(self.instruction_ptr)
        elif mode == 1:
            val = self.instruction_ptr
        else:
            val = self.program_get_data(self.instruction_ptr) + self.relative_base
        # increase the current instruction pointer
        self.instruction_ptr += 1
        # increase the input id (for debug)
        self._input_id += 1
        return val, mode

    def get_value(self, keep_index=False):
        '''Gets the "address" or "immediate value" for a given set of inputs and
        data. The function also fills a debug string in case the debug is
        activated for the ProgramInstance.
        
        :param keep_index: Whether or not the function should keep the index as
            is, or interpret it as an address in the program.
        :type keep_index: bool
        :return: Program data value.
        :rtype: int
        '''
        # get the index and mode
        idx, mode = self.get_index()
        # if necessary, apply the index as an address in the program code.
        if idx is None: return None
        if not keep_index:
            val = self.program_get_data(idx)
        else:
            val = idx
        # (fill the debug string in case of debug mode)
        self._debug_str += ' arg{}={} (idx={}, mode={}) ;'.format(
            self._input_id, val, idx, mode
        )
        return val

    def process_opcode(self):
        '''Processes the next instruction in the program with the current memory
        and instruction pointer.
        
        :return: Whether or not the program should pause (if pause is activated).
        :rtype: bool
        '''
        # get the current instruction
        instruction = str(self.program[self.instruction_ptr])
        # extract the operation code (opcode) and check for halt or error
        opcode = int(instruction[-2:])
        if opcode == 99:
            if self.debug:
                print('[  99 ] - Exiting')
            self.instruction_ptr = None
            return False
        if opcode not in OPERATIONS:
            self.instruction_ptr = -1
            return False
        # get the information on this operation for further process and debug
        opname, op, n_inputs = OPERATIONS[opcode]
        m = instruction[:-2]
        self.modes = [ int(m) for m in m[::-1] ] + [ 0 ] * (n_inputs - len(m))
        op_modes = [ m for m in self.modes ]
        # prepare the debug string in case the debug mode is active
        self._input_id = 0
        self._debug_str = (
            '[ {:3d} ]'.format(self.instruction_ptr)
            + ' - inst = {:05d} '.format(int(instruction))
            + ':: op = {} ({}), '.format(opname, opcode)
            + 'modes = {}\n'.format(op_modes)
        )
        # prepare the pause mode as False (could be modified by some operations)
        pause = False
        # execute the right operation depending on the opopcode
        self.instruction_ptr += 1
        if opcode == 1 or opcode == 2: # add, multiply
            va = self.get_value()
            vb = self.get_value()
            vc = self.get_value(True)
            self.program_set_data(vc, op(va, vb))
        elif opcode == 3: # read
            if len(self.memory) == 0:
                return None, False
            va = self.get_value(True)
            vm = self.memory.pop(0)
            self.program_set_data(va, vm)
        elif opcode == 4: # write
            v = self.get_value()
            # self.memory.append(v)
            self.output.append(v)
            pause = True
        elif opcode == 5: # jump if true
            va = self.get_value()
            vb = self.get_value()
            if va != 0:
                self.instruction_ptr = vb
        elif opcode == 6: # jump if false
            va = self.get_value()
            vb = self.get_value()
            if va == 0:
                self.instruction_ptr = vb
        elif opcode == 7 or opcode == 8: # set if less than, set if equal
            va = self.get_value()
            vb = self.get_value()
            vc = self.get_value(True)
            if op(va, vb):
                self.program_set_data(vc, 1)
            else:
                self.program_set_data(vc, 0)
        elif opcode == 9: # relative base offset
            self.relative_base += self.get_value()
        else:
            pass
        
        # if needed, print the debug string
        self._debug_str += '\n'
        if self.debug:
            print(self._debug_str)
        
        return pause

### Part I + II
def process_inputs(inputs, start_white=False, display=False, debug=False):
    '''Executes the Intcode program on the provided inputs and finds out the
    number of panels that have been painted at least once. It can also display
    the message that has been painted if necessary.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param start_white: If true, then the starting panel is considered painted
        white. Else, it is considered painted black.
    :type start_white: bool
    :param display: If true, then the final state of the board is displayed in
        the shell.
    :type display: bool
    :param debug: Whether or not the ProgramInstance should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Number of panels painted at least once.
    :rtype: int
    '''
    # prepare the board and the set of painted panels:
    # - the board only remembers the panels painted white
    # - the painted set remembers all the panels that have been painted at least
    # once
    board = set()
    painted = set()
    # initialize the painting robot: facing up, at the origin coordinates
    dir = 0
    x, y = 0, 0
    # (if starting white: mark the current panel as already painted white)
    if start_white:
        board.add((x, y))

    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = ProgramInstance(inputs, debug=debug)
    running = True
    # execute the program until it halts (but pause every 2 outputs)
    while running:
        # get the input depending on the state of the panel: if painted white
        # (i.e. visible in the board), the input is 1; else it is 0
        input = 1 if (x, y) in board else 0
        # insert the input in the program's memory
        program.memory_insert(input)
        # execute until 2 digits have been outputted
        state = program.run(pause_every=2)
        # check for state:
        # . if paused: parse outputs and apply the actions
        if state == 'pause':
            color, rotation = program.output
            program.reset_output()
            if color == 1:
                board.add((x, y))
            else:
                board.discard((x, y))
            painted.add((x, y))
            m = -1 if rotation == 0 else 1
            dir = (dir + m) % 4
            if dir == 0: # up
                y -= 1
            elif dir == 1: # right
                x += 1
            elif dir == 2: # down
                y += 1
            elif dir == 3: # left
                x -= 1
        # . else: stop the program
        elif state is None:
            running = False
            break
            
    # if necessary, display the final message, i.e. the board that
    # has been printed (and only contains the painted panels)
    if display:
        # . separate horizontal from vertical coordinates
        x, y = zip(*board)
        # . find board boundaries
        min_x, max_x = min(x), max(x)
        min_y, max_y = min(y), max(y)
        # . iterate through the board to print out the message
        print('')
        for y in range(min_y, max_y + 1):
            row = ''
            for x in range(min_x, max_x + 1):
                if (x, y) in board:
                    row += '█'
                else:
                    row += ' '
            print(row)
        print('')
        
    # get the number of panels that have been painted at least once
    # (counts each panel once, and counts the panels even if they have been
    # repainted black)
    return len(painted)

if __name__ == '__main__':
    # get input data
    data_path = '../data/day11.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = process_inputs(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = process_inputs(inputs, start_white=True, display=True)
    print('PART II: solution (see above in the shell)')
    

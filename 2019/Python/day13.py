### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 13: Care Package
### =============================================
import os
import numpy as np
from PIL import Image

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

DISPLAY_MAP = { None: ' ', 'W': '█', 'B': '□', 'H': '▂', 'O': '●' }
def display_board(board):
    '''Displays the board in the shell.
    
    :param board: Board to display.
    :type board: dict
    '''
    # get the board boundaries
    x, y = zip(*list(board.keys()))
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)
    # print the grid
    for y in range(min_y, max_y+1):
        row = ''
        for x in range(min_x, max_x+1):
            if (x, y) in board:
                row += DISPLAY_MAP[board[(x, y)]]
            else:
                row += ' '
        print(row)

EXPORT_DIR = os.path.join(os.getcwd(), 'export')
EXPORT_MAP = {
    None: (0, 0, 0), 'W': (255, 255, 255), 'B': (255, 255, 0),
    'H': (100, 100, 255), 'O': (255, 0, 0)
}
def export_board(time, board, scale=10):
    '''Saves the board as a .jpg image (the file name is determined by the given
    time: "{time}.jpg"). The function also applies a scale to make the image
    bigger and thus more readable.
    
    :param time: Time step corresponding to the export.
    :type time: int
    :param board: Board to export as an image.
    :type board: dict
    :param scale: Export scale to apply to the image.
    :type scale: int
    '''
    # create the export path if necessary
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
    # get the image boundaries (with export scale)
    x, y = zip(*list(board.keys()))
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)
    w = (max_x - min_x + 1) * scale
    h = (max_y - min_y + 1) * scale
    # create the grid as a NumPy array (with export scale)
    arr = np.zeros((h, w, 3))
    for (x, y), marker in board.items():
        mr, mg, mb = EXPORT_MAP[marker]
        arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 0] = mr
        arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 1] = mg
        arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 2] = mb
    # export as a JPG image
    img = Image.fromarray(arr.astype(np.uint8)).convert('RGB')
    img.save(os.path.join(EXPORT_DIR, '{}.jpg'.format(time)))

### Part I
def count_blocks(inputs, display=False, debug=False):
    '''Executes the Intcode program on the provided inputs and finds out the
    number of blocks on the screen when the game exits. It also returns the
    board when the game exits (i.e. the initial board since no game was
    actually played).
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param display: Whether or not to display the board after the game exits.
    :type display: bool
    :param debug: Whether or not the ProgramInstance should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Inital board (when no game was played) and number of blocks on the
        screen when the game exits.
    :rtype: dict, int
    '''
    # prepare the board and paddle/ball coordinates
    board = {}
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = ProgramInstance(inputs, debug=debug)
    running = True
    # execute the program until it halts (but pause every 3 outputs)
    while running:
        # execute until 3 digits have been outputted
        state = program.run(pause_every=3)
        # check for state:
        # . if paused: parse outputs and apply the actions
        if state == 'pause':
            x, y, id = program.output
            program.reset_output()
            if id == 0:
                marker = None
            elif id == 1:
                marker = 'W'
            elif id == 2:
                marker = 'B'
            elif id == 3:
                marker = 'H'
            else:
                marker = 'O'
            board[(x, y)] = marker
        # . else: stop the program
        elif state is None:
            running = False
            break
            
    if display:
        display_board(board)
            
    return board, sum([ 1 if m == 'B' else 0 for m in board.values() ])

### Part II
def compute_score(board, inputs, export=False, debug=False):
    '''Executes the Intcode program on the provided inputs and finds out the
    score of the player when the last block has been destroyed.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param export: Whether or not to export the board as an image at each game
        move.
    :type export: bool
    :param debug: Whether or not the ProgramInstance should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Final score of the player.
    :rtype: int
    '''
    # prepare the board and paddle/ball coordinates
    for (x, y), marker in board.items():
        if marker == 'H':
            px, py = x, y
        elif marker == 'O':
            bx, by = x, y
    init_n_blocks = None
    last_n_blocks = None
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = ProgramInstance(inputs, debug=debug)
    # insert quarters to run in "free mode"
    program.program[0] = 2

    running = True
    score = None
    time = 0
    # execute the program until it halts (but pause every 3 outputs)
    while running:
        # move the paddle to catch the ball and continue the game
        if px < bx: # move right
            program.memory_insert(1)
        elif px > bx: # move left
            program.memory_insert(-1)
        else: # reset movement to null
            program.memory_insert(0)

        # execute until 3 digits have been outputted
        state = program.run(pause_every=3)
        # check for state:
        # . if paused: parse outputs and apply the actions
        if state == 'pause':
            x, y, id = program.output
            program.reset_output()
            if x == -1 and y == 0:
                score = id
                # if outputting score and no more blocks: game ends
                if n_blocks == 0:
                    # (export board?)
                    if export:
                        export_board(time, board)
                    running = False
                    break
            else:
                if id == 0:
                    marker = None
                elif id == 1:
                    marker = 'W'
                elif id == 2:
                    marker = 'B'
                elif id == 3:
                    marker = 'H'
                    px, py = x, y
                else:
                    marker = 'O'
                    bx, by = x, y
                board[(x, y)] = marker
        # . else: stop the program
        elif state is None:
            running = False
            break
            
        # . check to see if all blocks have disappeared
        n_blocks = sum([ 1 if m == 'B' else 0 for m in board.values() ])
        # (if number of remaining blocks changed, output it)
        if last_n_blocks != n_blocks:
            print('{} block(s) left'.format(n_blocks))
            last_n_blocks = n_blocks
        
        # (initial blocks count and initial export, if need be)
        if init_n_blocks is None:
            init_n_blocks = n_blocks
            if export:
                export_board(0, board)
                time += 1
        # (export board?)
        if export and n_blocks != init_n_blocks:
            if time % 2 == 0:
                export_board(time // 2, board)
            time += 1

    return score

if __name__ == '__main__':
    # get input data
    data_path = '../data/day13.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    board, solution = count_blocks(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = compute_score(board, inputs) # use: export=True to enable exports
    print('PART II: solution = {}'.format(solution))
    

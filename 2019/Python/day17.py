### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 17: Set and Forget
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
        
    def restore_state(self, memory, program, instruction_ptr):
        self.memory = [ m for m in memory ]
        self.program = { k: v for k, v in program.items() }
        self.instruction_ptr = instruction_ptr
    
    def memorize_state(self):
        return (self.memory, self.program, self.instruction_ptr)
    
    def memory_insert(self, data):
        '''Inserts a value in the instance's memory, in first position.
        
        :param data: Value to insert.
        :type data: list(int) or int
        '''
        if isinstance(data, list):
            self.memory = data + self.memory
        else:
            self.memory = [ data ] + self.memory
    
    def memory_append(self, data):
        '''Appends a value in the instance's memory, in last position.
        
        :param data: Value to insert.
        :type data: list(int) or int
        '''
        if isinstance(data, list):
            self.memory.extend(data)
        else:
            self.memory.append(data)
        
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

### Part I
def get_map(inputs, display=False, debug=False):
    '''Executes the Intcode program on the provided inputs and finds out the
    required number of moves to reach the oxygen system in the room.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param display: Whether or not to display the map at the end of the scan.
    :type display: bool
    :param debug: Whether or not the ProgramInstance should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Current map of the scaffolds and simplified map.
    :rtype: list(str), dict(tuple(int, int), int)
    '''
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = ProgramInstance(inputs, debug=debug)
    # run the program to get the current map
    program.run()
    map = [ chr(x) for x in program.output ]

    # get simple map with only the coordinates of the scaffolds and of the robot
    # (ignore empty space)
    simple_map = {}
    # . get map (width, height) dimensions
    w = map.index('\n')
    h = len(map) // w
    # . remove new lines from map to avoid offset
    m = [ item for item in map if item != '\n' ]
    for y in range(h):
        for x in range(w):
            v = m[x + y * w]
            if v == '#':
                simple_map[(x, y)] = 1
            elif v == '^':
                simple_map[(x, y)] = 2
            elif v == '>':
                simple_map[(x, y)] = 3
            elif v == 'v':
                simple_map[(x, y)] = 4
            elif v == '<':
                simple_map[(x, y)] = 5
    
    # optionally display the map
    if display:
        display_map(map)
    
    return map, simple_map
    
def display_map(map):
    '''Displays the map in the shell.
    
    :param map: Map to display.
    :type map: list(str)
    '''
    print(''.join(map))

EXPORT_DIR = os.path.join(os.getcwd(), 'day17')
EXPORT_MAP = {
    '.': (0, 0, 0), '#': (255, 255, 255), '^': (0, 255, 0), '>': (0, 255, 0),
    '<': (0, 255, 0), 'v': (0, 255, 0), 'X': (255, 0, 0)
}
def export_map(iter, map, export_size=None, scale=20):
    '''Saves the board as a .jpg image (the file name is determined by the
    current iteration number: "{iter}.jpg"). The function also applies a
    scale to make the image bigger and thus more readable.
    
    :param path: List of positions in the current path to show with a
        different color on the map.
    :type path: list(tuple(int, int))
    :param scale: Export scale to apply to the image.
    :type scale: int
    '''
    # if no size is provided, get the image boundaries
    if export_size is None:
        init_w = map.index('\n')
        init_h = len(map) // init_w
    else:
        init_w, init_h = export_size
    # apply export scale
    w = init_w * scale
    h = init_h * scale
    # create the grid as a NumPy array (with export scale)
    m = [ item for item in map if item != '\n' ]
    arr = np.zeros((h, w, 3))
    for y in range(init_h):
        for x in range(init_w):
            marker = m[x + y * init_w]
            mr, mg, mb = EXPORT_MAP[marker]
            arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 0] = mr
            arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 1] = mg
            arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 2] = mb
    # export as a JPG image
    img = Image.fromarray(arr.astype(np.uint8)).convert('RGB')
    img.save(os.path.join(EXPORT_DIR, '{}.jpg'.format(iter)))
    
### Part I
def get_intersections_checksum(simple_map):
    '''Gets the checksum of all the intersections on the given map.
    
    :param simple_map: Map to display.
    :type simple_map: dict(tuple(int, int), int)
    :return: Checksum of the intersections.
    :rtype: int
    '''
    # find intersection on the map and compute their checksum    
    intersections = {}
    for x, y in simple_map:
        if (x-1, y) in simple_map and (x+1, y) in simple_map \
            and (x, y-1) in simple_map and (x, y+1) in simple_map:
            intersections[(x, y)] = x * y
    # return total checksum
    return sum(intersections.values())
    
### Part II
def encode_movement(movement):
    '''Encodes a set of moves into the correct format to feed the program (i.e.
    convert to ASCII value and add a newline).
    
    :param movement: Set of moves to convert.
    :type movement: list(str)
    :return: Encoded movement.
    :type: list(int)
    '''
    return [ ord(c) for c in movement ] + [ 10 ]

DIRECTION_DELTAS = { 2: (0, -1), 3: (1, 0), 4: (0, 1), 5: (-1, 0) }
DIRECTION_POSSIBILITES = { 2: (5, 2, 3), 3: (2, 3, 4), 4: (3, 4, 5), 5: (4, 5, 2) }
def save_robots(simple_map, inputs, export=False, debug=False):
    '''Saves the robots by walking on the scaffolds, and also collects dust.
    
    :param simple_map: Map to walk.
    :type simple_map: dict(tuple(int, int), int)
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param export: Whether or not to ask for a continuous video feed and to
        export the resulting images.
    :type export: bool
    :param debug: Whether or not the ProgramInstance should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Amount of dust collected during the process.
    :rtype: int
    '''
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = ProgramInstance(inputs, debug=debug)
    # force the robot to wake up
    program.program[0] = 2
    
    # get full path
    (x, y), dir = [ (k, v) for k, v in simple_map.items() if v != 1 ][0]
    visited = set([ (x, y) ])
    path = []
    steps = 0
    while len(visited) != len(simple_map):
        # get all possible directions from current state (the robot cannot make
        # a U-turn!)
        possible_dirs = DIRECTION_POSSIBILITES[dir]
        # get relevant neighbors
        neighbors = {}
        for move_dir in range(2, 6):
            # robot cannot make a U-turn!
            if move_dir not in possible_dirs:
                continue
            dx, dy = DIRECTION_DELTAS[move_dir]
            nx, ny = x + dx, y + dy
            if (nx, ny) in simple_map:
                val = 1 if (nx, ny) in visited else 0
                if move_dir == dir:
                    val -= 1
                neighbors[(nx, ny)] = (val, move_dir)
        # get best neighbor: if possible, not already visited
        neighbor, (_, d) = sorted(neighbors.items(), key=lambda k: k[1][0])[0]
        x, y = neighbor
        if d != dir:
            if steps > 0:
                steps += 1
                path.append(str(steps))
            steps = 0
            if possible_dirs.index(d) > possible_dirs.index(dir):
                path.append('R')
                dir = dir + 1 if dir < 5 else 2
            else:
                path.append('L')
                dir = dir - 1 if dir > 2 else 5
        else:
            steps += 1
        visited.add((x, y))
    
    if path[-1] == 'L' or path[-1] == 'R':
        path = path[:-1]
    path_str = ','.join(path)
    print(path_str)
    
    # separate paths into subpatterns (done by hand)
    A = encode_movement('L,12,R,4,R,4,L,6')
    B = encode_movement('L,12,R,4,R,4,R,12')
    C = encode_movement('L,10,L,6,R,4')
    movements = encode_movement('A,B,A,C,A,B,C,B,C,A')
        
    # prepare movements
    program.memory_append(movements)
    program.memory_append(A)
    program.memory_append(B)
    program.memory_append(C)
    program.memory_append([ ord('y' if export else 'n'), 10 ])
    
    # run the program to move the robot
    program.run()
    print('Finished computing.')
    # export maps if need be
    if export:
        full_map = ''.join([ chr(x) for x in program.output ])
        all_maps = [ m for m in full_map.split('\n\n') if len(m) > 0 and m[0] == '.' ]
        if not os.path.exists(EXPORT_DIR):
            os.makedirs(EXPORT_DIR)
        for i, map in enumerate(all_maps):
            export_map(i, map)
    
    return program.output[-1]
    
if __name__ == '__main__':
    # get input data
    data_path = '../data/day17.txt'
    inputs = parse_input(open(data_path, 'r').read())    
    map, simple_map = get_map(inputs, display=False)
    
    ### PART I
    solution = get_intersections_checksum(simple_map)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = save_robots(simple_map, inputs)
    print('PART II: solution = {}'.format(solution)) # 46: wrong
    

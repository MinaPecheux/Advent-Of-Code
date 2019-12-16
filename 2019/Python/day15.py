### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 15: Oxygen System
### =============================================
import os
from collections import defaultdict
from queue import Queue
from copy import copy

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

### Part I
class MazeSolver(object):
    
    '''Util class to explore the maze. The exploration is done by a robot
    running an Intcode program. The solver can also find the shortest path to
    a specific point in the maze and compute flows from a given source point.
    
    The robot can move in 4 direction, therefore a move is an integer that can
    be 1: "north", 2: "south", 3: "west", 4: "east". Tiles in the maze board can
    be 0: "walls", 1: "empty", 2: "oxygen source" or 3: "oxygen filled".
    '''
    
    DISPLAY_MAP = { None: 'x', 0: '█', 1: ' ', 2: '●', 'start': 'S' }
    EXPORT_DIR_EXPLORE = os.path.join(os.getcwd(), 'day15_explore')
    EXPORT_DIR_PATH = os.path.join(os.getcwd(), 'day15_path')
    EXPORT_DIR_FILL = os.path.join(os.getcwd(), 'day15_fill')
    EXPORT_MAP = {
        None: (0, 0, 0), 0: (50, 50, 50), 1: (255, 255, 255),
        2: (255, 0, 0), 3: (150, 150, 255), 'start': (0, 255, 0),
        'path': (255, 255, 0)
    }
    
    BACKTRACK = { 1: 2, 2: 1, 3: 4, 4: 3 }
    
    def __init__(self, program, start_position=(0, 0), export=False, export_size=None):
        '''Initialization function of a new MazeSolver.
        
        :param program: List of integers to execute as an Intcode program.
        :type program: list(int)
        :param start_position: Initial position of the robot in the maze.
        :type start_position: tuple(int, int)
        :param export: Whether or not the solve algorithms should export their
            results frame by frame to be further reprocessed as movies.
        :type export: bool
        :param export_size: If export is enabled and if this size is not None,
            then all exports will use an image with a size fixed by this value.
            Else, exports will adapt to the current boundaries of the maze board.
        :type export_size: None or tuple(int, int) or list(int, int)
        '''
        self.program = program
        self.board = {}
        self.board[start_position] = 1
        self.visited = set()
        self.correct_path = set()
        self.start_x, self.start_y = start_position
        self.target_position = None
        self.min_dist = 1e8
        
        self._export = export
        self._export_iter = 0
        if isinstance(export_size, tuple) or isinstance(export_size, list):
            self._export_width, self._export_height = export_size
        self._last_export = {}
        self._last_path = []
        self._export_mode = None

    def get_board_value(self, move):
        '''Gets the value of a tile in the board by moving the robot to this
        position and waiting for its output.
        
        :param move: Move the robot needs to take.
        :type move: int
        :return: Tile value.
        :rtype: int
        '''
        # move the robot
        self.program.memory_insert(move)
        # execute "forever": will stop when 1 digit has been outputted
        self.program.run(pause_every=1)
        # parse output and apply the actions
        result = self.program.output[-1]
        self.program.reset_output()
        return result
        
    @staticmethod
    def get_neighbor_position(x, y, move):
        '''Gets the position of a neighbor tile, starting from the given (x, y)
        coordinates and applying the given move.
        
        :param x: Horizontal coordinate of the tile to search around of.
        :type x: int
        :param y: Vertical coordinate of the tile to search around of.
        :type y: int
        :param move: Move to apply.
        :type move: int
        :return: Position of the neighbor tile.
        :rtype: tuple(int, int)
        '''
        if move == 1:
            return (x, y-1)
        elif move == 2:
            return (x, y+1)
        elif move == 3:
            return (x-1, y)
        elif move == 4:
            return (x+1, y)
        return (x, y)

    def get_neighbors(self, x, y):
        '''Get the neighbor tiles of a tile at a given (x, y) position, ignoring
        walls.
        
        :param x: Horizontal coordinate of the tile to search around of.
        :type x: int
        :param y: Vertical coordinate of the tile to search around of.
        :type y: int
        :return: List of neighbors' positions.
        :rtype: list(tuple(int, int))
        '''
        neighbors = []
        for dir in range(1, 5):
            neighbor_pos = MazeSolver.get_neighbor_position(x, y, dir)
            v = self.board.get(neighbor_pos, None)
            if v == 1 or v == 2:
                neighbors.append(neighbor_pos)
        return neighbors
        
    def print_board(self, path=[]):
        '''Prints the board of the maze in the shell.
        
        :param path: List of positions to debug as "in the current path" with a
            "." character on the map.
        :type path: list(tuple(int, int))
        '''
        # find the current board boundaries
        x, y = zip(*list(self.board.keys()))
        min_x, max_x = min(x), max(x)
        min_y, max_y = min(y), max(y)
        # print the grid
        for y in range(min_y, max_y+1):
            row = ''
            for x in range(min_x, max_x+1):
                if x == self.start_x and y == self.start_y:
                    row += MazeSolver.DISPLAY_MAP['start']
                elif (x, y) in path and (x, y) != self.target_position:
                    row += '.'
                else:
                    row += MazeSolver.DISPLAY_MAP[self.board.get((x, y), None)]
            print(row)
    
    def export_board(self, path=[], scale=10):
        '''Saves the board as a .jpg image (the file name is determined by the
        current iteration number: "{iter}.jpg"). The function also applies a
        scale to make the image bigger and thus more readable.
        
        :param path: List of positions in the current path to show with a
            different color on the map.
        :type path: list(tuple(int, int))
        :param scale: Export scale to apply to the image.
        :type scale: int
        '''
        # for explore mode: check if board is the same (avoid exporting same
        # board multiple times)
        if self._export_mode == 'explore' and \
            self.board.keys() == self._last_export.keys():
            return
        self._last_export = { k: v for k, v in self.board.items() }
        # get coordinates extrema
        x, y = zip(*list(self.board.keys()))
        min_x, max_x = min(x), max(x)
        min_y, max_y = min(y), max(y)
        # if no size is provided, get the image boundaries
        if self._export_width is None or self._export_height is None:
            w = (max_x - min_x + 1)
            h = (max_y - min_y + 1)
        else:
            w = self._export_width
            h = self._export_height
        # apply export scale
        w *= scale
        h *= scale
        # create the grid as a NumPy array (with export scale)
        arr = np.zeros((h, w, 3))
        for (x, y), marker in self.board.items():
            if x == self.start_x and y == self.start_y:
                mr, mg, mb = MazeSolver.EXPORT_MAP['start']
            elif (x, y) in path and (x, y) != self.target_position:
                mr, mg, mb = MazeSolver.EXPORT_MAP['path']
            else:
                mr, mg, mb = MazeSolver.EXPORT_MAP[marker]
            x -= min_x
            y -= min_y
            arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 0] = mr
            arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 1] = mg
            arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 2] = mb
        # export as a JPG image
        img = Image.fromarray(arr.astype(np.uint8)).convert('RGB')
        if self._export_mode == 'explore':
            dir = MazeSolver.EXPORT_DIR_EXPLORE
        elif self._export_mode == 'path':
            dir = MazeSolver.EXPORT_DIR_PATH
        elif self._export_mode == 'fill':
            dir = MazeSolver.EXPORT_DIR_FILL
        img.save(os.path.join(dir, '{}.jpg'.format(self._export_iter)))
        # increment iteration number
        self._export_iter += 1

    def explore(self):
        '''Explores the maze to get value of all the tiles in it.'''
        # create the export path if necessary
        if self._export and not os.path.exists(MazeSolver.EXPORT_DIR_EXPLORE):
            os.makedirs(MazeSolver.EXPORT_DIR_EXPLORE)
            self._export_iter = 0
        # launch recursive discovery of the maze
        self.x = self.start_x
        self.y = self.start_y
        self._export_mode = 'explore'
        self.walk()
        self._export_mode = None
        
    def walk(self, last_dir=0):
        '''Recursively walks through the maze to explore it.
        
        :param last_dir: Last direction the robot took - can be used to
            backtrack if the robot is stuck.
        :type last_dir: int
        '''
        if self._export:
            self.export_board()
        
        # get all accessible neighbor tiles
        neighbors = [ MazeSolver.get_neighbor_position(self.x, self.y, dir) \
            for dir in range(1, 5) ]
        explored = [ self.board.get(n, None) is not None for n in neighbors ]
        # remember the robot's program current state for further restore
        current_state = self.program.memorize_state()
        # try each direction
        for dir in range(1, 5):
            # (check if the tile is not yet explored)
            if not explored[dir - 1]:
                # restore cached store and prepare next movement
                # + make robot action
                self.program.restore_state(*current_state)
                self.program.memory_insert(dir)
                self.program.run(pause_every=1)
                result = self.program.output[-1]
                self.program.reset_output()
                # use robot's feedback to update the board
                self.board[neighbors[dir - 1]] = result
                # recurse depending on feedback
                if result != 0: # if no wall
                    if result == 2: # if reached target
                        self.target_position = neighbors[dir - 1]
                    self.x, self.y = MazeSolver.get_neighbor_position(self.x,
                        self.y, dir)
                    self.walk(dir)
        # if stuck: backtrack!
        if (self.x, self.y) != (self.start_x, self.start_y):
            self.program.restore_state(*current_state)
            r = MazeSolver.BACKTRACK[last_dir]
            self.program.memory_insert(r)
            self.program.run(pause_every=1)
            self.x, self.y = MazeSolver.get_neighbor_position(self.x, self.y,
                MazeSolver.BACKTRACK[last_dir])
        
    def find_shortest_path(self, source=None, target=None):
        '''Finds the shortest path between two positions in the maze board by
        applying Dijkstra's algorithm.
        
        :param source: If not null, start position of the path. Else, the start
            position that was stored for the MazeSolver instance is taken.
        :type source: tuple(int, int)
        :param target: If not null, target position of the path. Else, the end
            position that was found by exploring the MazeSolver instance is taken.
        :type target: tuple(int, int)
        :return: Shortest path between the two positions in the maze.
        :rtype: list(tuple(int, int))
        '''
        self._export_mode = 'path'
        self._export_iter = 0
        # create the export path if necessary
        if self._export and not os.path.exists(MazeSolver.EXPORT_DIR_PATH):
            os.makedirs(MazeSolver.EXPORT_DIR_PATH)

        # prepare source and target positions
        if source is None:
            source = (self.start_x, self.start_y)
        if target is None:
            target = self.target_position
            
        shortest_paths = { source: (None, 0) }
        current_position = source
        visited = set()
        
        # compute shortest paths for each position
        while current_position != target:
            visited.add(current_position)
            neighbors = self.get_neighbors(*current_position)
            current_weight = shortest_paths[current_position][1]
            for neighbor in neighbors:
                weight = current_weight + 1
                if neighbor not in shortest_paths:
                    shortest_paths[neighbor] = (current_position, weight)
                else:
                    current_shortest_weight = shortest_paths[neighbor][1]
                    if current_shortest_weight > weight:
                        shortest_paths[neighbor] = (current_position, weight)
                        
            destinations = { pos: shortest_paths[pos] for pos in shortest_paths \
                if pos not in visited }
            if not destinations:
                return None
            current_position = min(destinations, key=lambda x: destinations[x][1])
        
        # work back through destinations in shortest path
        path = []
        while current_position is not None:
            if self._export:
                self.export_board(path=path)
            path.append(current_position)
            next_position = shortest_paths[current_position][0]
            current_position = next_position
        # reverse path
        path = path[::-1]

        self._export_mode = None
        return path
        
    def oxygen_fill(self, export=False):
        '''Fills the maze with oxygen from the oxygen source that was found
        during the exploration process and returns the number of required
        iterations to complete the action.
        
        :param export: Whether or not to export the process frame by frame (can
            override the MazeSolver instance's general export parameter).
        :type export: bool
        :return: Number of required iterations to fill the entire maze board.
        :rtype: int
        '''
        # create the export path if necessary
        self._export = export
        if self._export and not os.path.exists(MazeSolver.EXPORT_DIR_FILL):
            os.makedirs(MazeSolver.EXPORT_DIR_FILL)
            self._export_iter = 0
        # (if target position has not been found yet, abort!)
        if self.target_position is None:
            return -1
        # fill the board with oxygen starting from the oxygen system position
        self._export_mode = 'fill'
        fill_time = self.fill(*self.target_position)
        self._export_mode = None
        return fill_time

    def fill(self, x, y):
        '''Util function that actually fills the maze in a BFS-like process and
        finds out how many iterations the process requires.
        
        :param x: Current horizontal position in the maze.
        :type x: int
        :param y: Current vertical position in the maze.
        :type y: int
        :return: Number of required iterations to fill the entire maze board.
        :rtype: int
        '''
        # get coordinates extrema
        x, y = zip(*list(self.board.keys()))
        min_x, max_x = min(x), max(x)
        min_y, max_y = min(y), max(y)

        iterations = 0
        # tiles to check (store the target position initially)
        to_check = Queue()
        to_check.put((self.target_position, 0))
        self.board[self.target_position] = 3
        # compute until there are no tiles left
        while not to_check.empty():
            # . get back tile information
            pos, generation = to_check.get()
            # . get all neighbors of the current position (only returns the
            # ones that are empty, i.e. not already filled with oxygen)
            neighbors = self.get_neighbors(*pos)
            # . for each, fill it and add it to the queue of positions
            for neighbor in neighbors:
                self.board[neighbor] = 3
                to_check.put((neighbor, generation + 1))
            # (export the board?)
            if self._export:
                self.export_board()
            # update the total number of flow iterations
            iterations = max(iterations, generation)
        return iterations

def find_oxygen_system(inputs, display=False, export=False, debug=False):
    '''Executes the Intcode program on the provided inputs and finds out the
    required number of moves to reach the oxygen system in the room.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param display: Whether or not to display the board at the end.
    :type display: bool
    :param export: Whether or not to export the board at each iteration of
        exploration and path building.
    :type export: bool
    :param debug: Whether or not the ProgramInstance should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: MazeSolver instance and number of moves required to reach the
        oxygen system (i.e. length of the shortest path to the system).
    :rtype: MazeSolver, int
    '''
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = ProgramInstance(inputs, debug=debug)
    # prepare and run the maze solver to explore the maze fully
    solver = MazeSolver(program, export=export, export_size=(41, 41))
    solver.explore()
    # use Dijkstra's algorithm to get the shortest path between the start
    # position of the robot and the target position (position of the oxygen
    # system)
    path = solver.find_shortest_path()
    # optionally print the board and the shortest path
    if display:
        solver.print_board(path)
    return solver, len(path) - 1 # remove 1 for the start position
    
def fill_oxygen(solver, export=None):
    '''Uses the previously prepared maze solver to see how many iterations are
    required to fill the whole map with oxygen.
    
    :param solver: Previously prepared maze solver.
    :type solver: MazeSolver
    :returns: Number of required iterations to fill the whole map with oxygen.
    :rtype: int
    '''
    if export is None:
        export = solver._export
    return solver.oxygen_fill(export=export)
    
if __name__ == '__main__':
    # get input data
    data_path = '../data/day15.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solver, solution = find_oxygen_system(inputs, export=False)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = fill_oxygen(solver, export=False)
    print('PART II: solution = {}'.format(solution))
    

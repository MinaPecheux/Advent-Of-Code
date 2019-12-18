### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 17: Set and Forget
### =============================================
import os

import numpy as np
from PIL import Image

from intcode import IntcodeProgram

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
### Part I
def get_map(inputs, display=False, debug=False):
    '''Executes the Intcode program on the provided inputs and finds out the
    required number of moves to reach the oxygen system in the room.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param display: Whether or not to display the map at the end of the scan.
    :type display: bool
    :param debug: Whether or not the IntcodeProgram should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Current map of the scaffolds and simplified map.
    :rtype: list(str), dict(tuple(int, int), int)
    '''
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = IntcodeProgram(inputs, debug=debug)
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
    :param debug: Whether or not the IntcodeProgram should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Amount of dust collected during the process.
    :rtype: int
    '''
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = IntcodeProgram(inputs, debug=debug)
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

    # movements = { 'A': [], 'B': [], 'C': [] }
    # movement = ''
    # c = 0
    # for m in [ 'A', 'B', 'C' ]:
    #     while movement in path_str[len(movement):]:
    #         movement += path_str[c]
    #         c += 1
    #     movements[m] = movement
    # print(movements)
    # # A L,11,R,3,R,3,L,5,
    # # B L,11,R,3,R,3,R,11,
    # # A L,11,R,3,R,3,L,5,
    # # C L,9,L,5,R,3,
    # # A L,11,R,3,R,3,L,5,
    # # B L,11,R,3,R,3,R,11,
    # # C L,9,L,5,R,3,
    # # B L,11,R,3,R,3,R,11,
    # # C L,9,L,5,R,3,
    # # A/B L,11,R,3,R,3
    # 
    # movements_chain = []
    # for move, pattern in movements.items():
    #     if path_str.startswith(pattern):
    #         movements_chain.append(move)
    #         path_str = path_str[len(move)-1:]
    #         print(path_str)
    # print(movements_chain)
    # return
    
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
    print('PART II: solution = {}'.format(solution))
    

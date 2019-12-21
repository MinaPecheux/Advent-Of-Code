### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 19: Tractor Beam
### =============================================
from tqdm import tqdm

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
def check_coordinates(program, x, y):
    '''Checks if the cell at the given coordinates is within the tractor beam
    or not.
    
    :param program: Program to run to get the result.
    :type program: ProgramInstance
    :param x: Horizontal coordinate to check.
    :type x: int
    :param y: Vertical coordinate to check.
    :type y: int
    :return: Whether or not the cell is within the tractor beam.
    :rtype: bool
    '''
    # reset program instance to original settings
    program.reset()
    # deploy robot
    program.push_memory([ x, y ])
    # run the program and get the result
    program.run()
    return program.output[-1] == 1

def get_map(program, map_size):
    '''Gets the map of required size with the set of positions that are within
    the tractor beam.
    
    :param program: Program to run to get the result.
    :type program: ProgramInstance
    :param map_size: Size of the map to build.
    :type map_size: int
    :return: Map with the positions affected by the tractor beam.
    :rtype: set(tuple(int, int))
    '''
    # go through the grid
    map = set([ (0, 0) ])
    x_min, x_max = 0, 0
    for y in tqdm(range(map_size), total=map_size):
        row = set()
        # check some buffered borders
        # .. min border
        last_x_min, last_x_max = x_min, x_max
        checked_inf = False
        if last_x_min - 1 >= 0 and check_coordinates(program, last_x_min - 1, y):
            row.add((last_x_min - 1, y))
            x_min = last_x_min - 1
            checked_inf = True
        if not checked_inf and last_x_min >= 0 \
            and check_coordinates(program, last_x_min, y):
            row.add((last_x_min, y))
            x_min = last_x_min
            checked_inf = True
        if not checked_inf and last_x_min + 1 >= 0 \
            and check_coordinates(program, last_x_min + 1, y):
            row.add((last_x_min + 1, y))
            x_min = last_x_min + 1
        # .. max border
        checked_sup = False
        if last_x_max + 1 >= 0 and check_coordinates(program, last_x_max + 1, y):
            row.add((last_x_max + 1, y))
            x_max = last_x_max + 1
            checked_sup = True
        if not checked_sup and last_x_max >= 0 \
            and check_coordinates(program, last_x_max, y):
            row.add((last_x_max, y))
            x_max = last_x_max
            checked_sup = True
        if not checked_sup and last_x_max - 1 >= 0 \
            and check_coordinates(program, last_x_max - 1, y):
            row.add((last_x_max - 1, y))
            x_max = last_x_max - 1
        # fill in the middle
        for x in range(x_min + 1, x_max):
            if x >= 0:
                row.add((x, y))
        map = map.union(row)
        xx = [ x for x, _ in row ]
        if len(xx) > 0:
            x_min = min(xx)
            x_max = max(xx)
        else:
            x_min += 1
            x_max += 1
    return map

### Part I
def get_affected_positions(inputs, display=False, debug=False):
    '''Executes the Intcode program on the provided inputs and checks how many
    positions on the grid are affected by the tractor beam.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param display: Whether or not to display the grid at the end of the scan.
    :type display: bool
    :param debug: Whether or not the IntcodeProgram should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Number of positions affected by the tractor beam.
    :rtype: int
    '''
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = IntcodeProgram(inputs)
    # get the map of 50x50
    map = get_map(program, 50)
    
    # optionally display the map
    if display:
        for y in range(50):
            row = ''
            for x in range(50):
                row += '#' if (x, y) in map else '.'
            print(row)
    
    return len(map)

### Part II
def find_closest_square(inputs, square_size):
    '''Executes the Intcode program on the provided inputs and searches for the
    closet square of given size that fits in the tractor beam. Returns a custom
    checksum for its top-left corner coordinate.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param square_size: Size of the edge of the square to find in the grid.
    :type square_size: int
    :return: Top-left corner coordinate checksum.
    :rtype: int
    '''
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = IntcodeProgram(inputs)
    # get a large grid to inspect
    size = 2000
    map = get_map(program, size)

    # find a square in it... if possible!
    # (else, retry with a larger size)
    candidates = set()
    for position in map:
        x, y = position
        if ((x, y + square_size - 1)) in map and \
            ((x + square_size - 1, y)) in map and \
            ((x + square_size - 1, y + square_size - 1)) in map:
            candidates.add((x, y))
    if len(candidates) > 0:
        square = sorted(candidates, key=lambda x: x[0] * 10000 + x[1])[0]
    else:
        return -1
    # compute checksum of square
    return square[0] * 10000 + square[1]
    
if __name__ == '__main__':
    # get input data
    data_path = '../data/day19.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = get_affected_positions(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_closest_square(inputs, 100)
    print('PART II: solution = {}'.format(solution))
    

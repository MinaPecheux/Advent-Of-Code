### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 10: The Stars Align
### =============================================
import re
import numpy as np
from scipy.spatial.distance import cdist
from tqdm import tqdm

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    reg = r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>'
    points = []
    for line in data.split('\n'):
        if line == '': continue
        match = re.match(reg, line)
        points.append((int(match.group(1)), int(match.group(2)),
            int(match.group(3)), int(match.group(4))))
    return points

# [ Computation functions ]
# -------------------------
def print_board(board, min_x, max_x, min_y, max_y):
    '''Prints the current board, showing only the stars that are lit up, i.e.
    the pixels that are active.
    
    :param board: Positions that are active.
    :type board: list(tuple(int, int))
    :param min_x: Minimum horizontal coordinate.
    :type min_x: int
    :param max_x: Maximum horizontal coordinate.
    :type max_x: int
    :param min_y: Minimum vertical coordinate.
    :type min_y: int
    :param max_y: Maximum vertical coordinate.
    :type max_y: int
    '''
    print('')
    for yy in range(min_y, max_y+1):
        row = ''
        for xx in range(min_x, max_x+1):
            row += '█' if (xx, yy) in board else ' '
        print(row)
    print('')

### Part I + II
def process_message(points):
    '''Moves the points from their original points with the given velocities and
    prints the resulting board for the configuration that has the minimal
    average distance between all points (likely to be the "most ordered" one,
    i.e. the one that spells out the message).
    
    :param points: List of points with their original positions and their
        velocities.
    :type points: list(tuple(int, int, int, int))
    '''
    MAX_ITERS = 15000
    time = 0
    avg_distances = []
    for time in tqdm(range(MAX_ITERS), total=MAX_ITERS):
        # compute the new board: for each point, compute its position after
        # moving during "time" iterations
        board = []
        for pos_x, pos_y, move_x, move_y in points:
            x = pos_x + time * move_x
            y = pos_y + time * move_y
            board.append((x, y))
        # compute and store the average distance between all points on the board
        avg_distances.append(np.mean(cdist(board, board)))
        
    # find the time where points were closest to each order (average distance
    # was minimal)
    closest_time = np.argmin(avg_distances)
    # recompute the board for this time step
    board = []
    min_x, max_x = 1e8, 0
    min_y, max_y = 1e8, 0
    for pos_x, pos_y, move_x, move_y in points:
        x = pos_x + closest_time * move_x
        y = pos_y + closest_time * move_y
        board.append((x, y))
        # (update the board bounds for the display)
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y
    # print the time board
    print_board(board, min_x, max_x, min_y, max_y)
    # return the time step at which the message printed (probably)
    return closest_time
        
if __name__ == '__main__':    
    # get input data
    data_path = '../data/day10.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I + II
    solution = process_message(inputs)
    print('PART I (see above)')
    print('PART II: solution = {}'.format(solution))

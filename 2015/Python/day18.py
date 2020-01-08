### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 18: Like a GIF For Your Yard
### =============================================
import os

import numpy as np
from PIL import Image
from tqdm import tqdm

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Message board.
    :rtype: dict(tuple(int, int), str)
    '''
    board = {}
    for y, line in enumerate(data.strip().split('\n')):
        for x, char in enumerate(line):
            board[(x, y)] = char
    return board

# [ Computation functions ]
# -------------------------
GRID_SIZE = 100
EXPORT_DIR = 'day18'
def export_board(board, iter, grid_size, scale=10):
    '''Saves the board as a .jpg image (the file name is determined by the
    current iteration number: "{iter}.jpg"). The function also applies a
    scale to make the image bigger and thus more readable.
    
    :param board: Current board to render.
    :type board: dict(tuple(int, int), str)
    :param iter: Current iteration number.
    :type iter: int
    :param scale: Export scale to apply to the image.
    :type scale: int
    '''
    # get coordinates extrema
    x, y = zip(*list(board.keys()))
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)
    w, h = grid_size, grid_size
    # apply export scale
    w *= scale
    h *= scale
    # create the grid as a NumPy array (with export scale)
    arr = np.zeros((h, w, 3))
    for (x, y), marker in board.items():
        if marker == '#':
            mr, mg, mb = (255, 255, 255)
        else:
            mr, mg, mb = (0, 0, 0)
        arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 0] = mr
        arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 1] = mg
        arr[scale*y:scale*(y+1), scale*x:scale*(x+1), 2] = mb
    # export as a JPG image
    img = Image.fromarray(arr.astype(np.uint8)).convert('RGB')
    img.save(os.path.join(EXPORT_DIR, '{}.jpg'.format(iter)))

def find_neighbors(x, y, grid_size):
    '''Finds the neighbor positions of a given (x, y) coordinate.
    
    :param x: Horizontal coordinate.
    :type x: int
    :param y: Vertical coordinate.
    :type y: int
    :param grid_size: Size of the grid.
    :type grid_size: int
    '''
    neighbors = []
    for xx in range(x-1, x+2):
        for yy in range(y-1, y+2):
            if not (xx < 0 or yy < 0 or xx >= grid_size or yy >= grid_size or \
                (xx == x and yy == y)):
                neighbors.append((xx, yy))
    return neighbors

def is_corner(x, y, grid_size):
    '''Checks if a position is one of the four corners of the grid.
    
    :param x: Horizontal coordinate.
    :type x: int
    :param y: Vertical coordinate.
    :type y: int
    :param grid_size: Size of the grid.
    :type grid_size: int
    '''
    return (x == 0 and y == 0) or (x == 0 and y == grid_size - 1) or \
        (x == grid_size - 1 and y == 0) or (x == grid_size - 1 and y == grid_size - 1)

def process_board(board, steps, stuck_lights=False, grid_size=100, export=False, debug=False):
    '''Processes the initial board for a given number of steps and exports it at
    each iteration.
    
    :param board: Available container sizes.
    :type board: dict(tuple(int, int), str)
    :param steps: Number of steps to process.
    :type steps: int
    :param stuck_lights: Whether or not the four corners of the grid are stuck
        in the "on" position.
    :type stuck_lights: bool
    :param grid_size: Size of the grid to compute the board on.
    :type grid_size: int
    :param export: Whether or not to export the board at each iteration.
    :type export: bool
    :param debug: Whether or not to show a progress bar during computation.
    :type debug: bool
    :return: Number of "on" lights in the final board state.
    :rtype: int
    '''
    # if need be, prepare the export
    if export:
        if not os.path.exists(EXPORT_DIR):
            os.makedirs(EXPORT_DIR)
        export_board(board, 0, grid_size)
    # process for a given amount of steps
    iterator = range(steps)
    if debug:
        iterator = tqdm(iterator, total=steps)
    for step in iterator:
        # . update board
        new_board = {}
        for x in range(grid_size):
            for y in range(grid_size):
                if stuck_lights and is_corner(x, y, grid_size):
                    marker = '#'
                else:
                    neighbors = find_neighbors(x, y, grid_size)
                    n_neighbors_on = sum([ 1 for n in neighbors if board[n] == '#' ])
                    marker = board[(x, y)]
                    if marker == '#':
                        if n_neighbors_on != 2 and n_neighbors_on != 3:
                            marker = '.'
                    elif n_neighbors_on == 3:
                        marker = '#'
                new_board[(x, y)] = marker
        board = new_board
        # . export it if need be
        if export:
            export_board(board, step+1, grid_size)
    # get the number of "on" lights in the final state
    return sum([ 1 for v in board.values() if v == '#' ])

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    board = parse_input('''.#.#.#
...##.
#....#
..#...
#.#..#
####..''')
    assert process_board(board, 4, grid_size=6) == 4

if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    # get input data
    data_path = '../data/day18.txt'
    board = parse_input(open(data_path, 'r').read()) #1658: too high
    
    ### PART I
    solution = process_board(board, 100, debug=True, export=True)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = process_board(board, 100, stuck_lights=True, debug=True)
    print('PART II: solution = {}'.format(solution))
    
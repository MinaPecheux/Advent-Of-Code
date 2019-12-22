### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 13: Care Package
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

EXPORT_DIR = os.path.join(os.getcwd(), 'day13')
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
    :param debug: Whether or not the IntcodeProgram should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Inital board (when no game was played) and number of blocks on the
        screen when the game exits.
    :rtype: dict, int
    '''
    # prepare the board
    board = {}
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = IntcodeProgram(inputs, debug=debug)
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
    
    :param board: Initial board.
    :type board: dict
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param export: Whether or not to export the board as an image at each game
        move.
    :type export: bool
    :param debug: Whether or not the IntcodeProgram should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Final score of the player.
    :rtype: int
    '''
    # get paddle and ball coordinates
    for (x, y), marker in board.items():
        if marker == 'H':
            px = x
        elif marker == 'O':
            bx = x
    init_n_blocks = None
    last_n_blocks = None
    # prepare the program instance to read the given inputs as an Intcode
    # program
    program = IntcodeProgram(inputs, debug=debug)
    # insert quarters to run in "free mode"
    program.program[0] = 2

    running = True
    score = None
    time = 0
    print('Remaining block(s):')
    # execute the program until it halts (but pause every 3 outputs)
    while running:
        # move the paddle to catch the ball and continue the game
        if px < bx: # move right
            program.insert_memory(1)
        elif px > bx: # move left
            program.insert_memory(-1)
        else: # reset movement to null
            program.insert_memory(0)

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
                    print('\n')
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
                    px = x
                else:
                    marker = 'O'
                    bx = x
                board[(x, y)] = marker
        # . else: stop the program
        elif state is None:
            running = False
            break
            
        # . check to see if all blocks have disappeared
        n_blocks = sum([ 1 if m == 'B' else 0 for m in board.values() ])
        # (initial blocks count and initial export, if need be)
        if init_n_blocks is None:
            init_n_blocks = n_blocks
            if export:
                export_board(0, board)
                time += 1
        # (if number of remaining blocks changed, output it)
        if last_n_blocks != n_blocks:
            c = 50 * n_blocks // init_n_blocks
            suffix = ('{:%dd}' % (len(str(init_n_blocks)))).format(n_blocks)
            bar = '■' * c + ' ' * (50 - c)
            print('{} {} / {}'.format(bar, suffix, init_n_blocks), end='\r')
            last_n_blocks = n_blocks        
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
    

### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 11: Space Police
### =============================================
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
    :param debug: Whether or not the IntcodeProgram should debug its
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
    program = IntcodeProgram(inputs, debug=debug)
    running = True
    # execute the program until it halts (but pause every 2 outputs)
    while running:
        # get the input depending on the state of the panel: if painted white
        # (i.e. visible in the board), the input is 1; else it is 0
        input = 1 if (x, y) in board else 0
        # insert the input in the program's memory
        program.push_memory(input)
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
    

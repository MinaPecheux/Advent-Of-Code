### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2016 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 2: Bathroom Security
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of moves.
    :rtype: list(int)
    '''
    return [ list(line) for line in data.split('\n') ]

# [ Computation functions ]
# -------------------------

### PART I
def compute_normal_panel(inputs):
    '''Computes the bathroom code from the list of moves.
    
    :param inputs: List of moves to make.
    :type inputs: list(str)
    :return: Bathroom code.
    :rtype: str
    '''
    code = ''
    x, y = 1, 1
    for line in inputs:
        for move in line:
            if move == 'U' and y > 0:
                y -= 1
            elif move == 'D' and y < 2:
                y += 1
            elif move == 'L' and x > 0:
                x -= 1
            elif move == 'R' and x < 2:
                x += 1
        code += str(1 + x + y * 3)
    return code

### PART II
def compute_special_panel(inputs):
    '''Computes the bathroom code from the list of moves.
    
    :param inputs: List of moves to make.
    :type inputs: list(str)
    :return: Bathroom code.
    :rtype: str
    '''
    panel = [ [None, None, '1', None, None],
              [None,  '2', '3',  '4', None],
              [ '5',  '6', '7',  '8',  '9'],
              [None,  'A', 'B',  'C', None],
              [None, None, 'D', None, None] ]
    W, H = 5, 5
    code = ''
    x, y = 0, 2
    for line in inputs:
        for move in line:
            new_x, new_y = x, y
            if move == 'U':
                new_y -= 1
            elif move == 'D':
                new_y += 1
            elif move == 'L':
                new_x -= 1
            elif move == 'R':
                new_x += 1
            if new_x < 0 or new_x >= W or new_y < 0 or new_y >= H \
                or panel[new_y][new_x] is None:
                continue
            x, y = new_x, new_y
        code += panel[y][x]
    return code
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    moves = parse_input('ULL\nRRDDD\nLURDL\nUUUUD')
    assert compute_normal_panel(moves) == '1985'
    ### PART II
    assert compute_special_panel(moves) == '5DB3'

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day2.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = compute_normal_panel(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = compute_special_panel(inputs)
    print('PART II: solution = {}'.format(solution))

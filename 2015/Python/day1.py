### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 1: Not Quite Lisp
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of floor moves.
    :rtype: list(int)
    '''
    return [ 1 if c == '(' else -1 for c in data.strip() ]

# [ Computation functions ]
# -------------------------
### PART I
def compute_floor(inputs):
    '''Computes the final floor Santa should reach by processing the given floor
    moves.
    
    :param inputs: List of floor moves.
    :type inputs: list(int)
    :return: Final floor.
    :rtype: int
    '''
    return sum(inputs)
    
### PART II
def find_basement_position(inputs):
    '''Finds the position in the list of moves that makes Santa reach the
    basement (floor -1) the first time.
    
    :param changes: List of floor moves.
    :type changes: list(int)
    :return: Position of the character that makes Santa reach floor -1 the
        first time.
    :rtype: int
    '''
    floor = 0
    i = 0
    while floor >= 0:
        floor += inputs[i]
        i += 1
    return i
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert compute_floor(parse_input('(())')) == 0
    assert compute_floor(parse_input('()()')) == 0
    assert compute_floor(parse_input('(((')) == 3
    assert compute_floor(parse_input('(()(()(')) == 3
    assert compute_floor(parse_input('))(((((')) == 3
    assert compute_floor(parse_input('())')) == -1
    assert compute_floor(parse_input('))(')) == -1
    assert compute_floor(parse_input(')))')) == -3
    assert compute_floor(parse_input(')())())')) == -3
    ### PART II
    assert find_basement_position(parse_input(')')) == 1
    assert find_basement_position(parse_input('()())')) == 5

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day1.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = compute_floor(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_basement_position(inputs)
    print('PART II: solution = {}'.format(solution))

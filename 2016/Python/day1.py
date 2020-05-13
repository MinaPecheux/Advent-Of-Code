### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2016 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 1: No Time for a Taxicab
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
    return [ x.strip() for x in data.split(',') ]

# [ Computation functions ]
# -------------------------
def get_taxicab_distance(x, y):
    '''Computes the taxicab distance to the target point.
    
    :param inputs: List of moves to make.
    :type inputs: list(str)
    :return: Total taxicab distance.
    :rtype: int
    '''
    return abs(x) + abs(y)

### PART I + II
def process_moves(inputs, stop_already_visited=False):
    '''Computes the taxicab distance to the target point.
    
    :param inputs: List of moves to make.
    :type inputs: list(str)
    :param stop_already_visited: Whether or not to stop at the
        location that has been visited twice first.
    :type stop_already_visited: bool
    :return: Total taxicab distance.
    :rtype: int
    '''
    x, y = 0, 0
    direction = 0 # 0: north, 1: east, 2: south, 3: west
    visited = set()
    visited.add((0, 0))
    for move in inputs:
        d = move[0]
        step = int(move[1:])
        if d == 'L':
            direction = (direction - 1) % 4
        elif d == 'R':
            direction = (direction + 1) % 4

        walking_through = []
        if direction == 0:
            for yy in range(step):
                walking_through.append((x, y + 1 + yy))
            y += step
        elif direction == 1:
            for xx in range(step):
                walking_through.append((x + 1 + xx, y))
            x += step
        elif direction == 2:
            for yy in range(step):
                walking_through.append((x, y - 1 - yy))
            y -= step
        elif direction == 3:
            for xx in range(step):
                walking_through.append((x - 1 - xx, y))
            x -= step

        for s in walking_through:
            if stop_already_visited and s in visited:
                return get_taxicab_distance(*s)
            visited.add(s)
    return get_taxicab_distance(x, y)
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert process_moves(parse_input('R2, L3')) == 5
    assert process_moves(parse_input('R2, R2, R2')) == 2
    assert process_moves(parse_input('R5, L5, R5, R3')) == 12
    ### PART II
    assert process_moves(parse_input('R8, R4, R4, R8'),
                         stop_already_visited=True) == 4

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day1.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = process_moves(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = process_moves(inputs, stop_already_visited=True)
    print('PART II: solution = {}'.format(solution))

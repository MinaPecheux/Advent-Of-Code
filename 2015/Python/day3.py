### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 3: Perfectly Spherical Houses in a Vacuum
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of moves for Santa.
    :rtype: list(tuple(int, int))
    '''
    moves = []
    for c in data.strip():
        if c == '^':
            moves.append((0, -1))
        elif c == '>':
            moves.append((1, 0))
        elif c == 'v':
            moves.append((0, 1))
        elif c == '<':
            moves.append((-1, 0))
    return moves

# [ Computation functions ]
# -------------------------
### PART I
def find_n_houses(moves):
    '''Computes the number of houses that receive at least one present.
    
    :param moves: List of moves for Santa.
    :type moves: list(tuple(int, int))
    :return: Number of houses with at least one present.
    :rtype: int
    '''
    visited_houses = set()
    # set initial position
    x, y = 0, 0
    # deliver present to initial house
    visited_houses.add((x, y))
    # follow instructions to visit other houses
    for move_x, move_y in moves:
        x += move_x
        y += move_y
        visited_houses.add((x, y))
    return len(visited_houses)
    
### PART II
def find_n_houses_with_robot(moves):
    '''Computes the number of houses that receive at least one present when
    Santa is helped with a Robo-Santa bot.
    
    :param moves: List of moves for Santa and the bot.
    :type moves: list(tuple(int, int))
    :return: Number of houses with at least one present.
    :rtype: int
    '''
    visited_houses = set()
    # set initial positions
    sx, sy = 0, 0 # (Santa)
    rx, ry = 0, 0 # (robot)
    # deliver present to initial house
    visited_houses.add((sx, sy))
    # follow instructions to visit other houses
    for i, (move_x, move_y) in enumerate(moves):
        if i % 2 == 0:
            sx += move_x
            sy += move_y
            visited_houses.add((sx, sy))
        else:
            rx += move_x
            ry += move_y
            visited_houses.add((rx, ry))
    return len(visited_houses)
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert find_n_houses(parse_input('>')) == 2
    assert find_n_houses(parse_input('^>v<')) == 4
    assert find_n_houses(parse_input('^v^v^v^v^v')) == 2
    ### PART II
    assert find_n_houses_with_robot(parse_input('^v')) == 3
    assert find_n_houses_with_robot(parse_input('^>v<')) == 3
    assert find_n_houses_with_robot(parse_input('^v^v^v^v^v')) == 11

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day3.txt'
    moves = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = find_n_houses(moves)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_n_houses_with_robot(moves)
    print('PART II: solution = {}'.format(solution))

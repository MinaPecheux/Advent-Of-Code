### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 6: Probably a Fire Hazard
### =============================================
import re
from collections import defaultdict

from tqdm import tqdm

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of strings to check.
    :rtype: list(str)
    '''
    reg = r'(.*)\s(\d+),(\d+).*\s(\d+),(\d+)'
    instructions = []
    for line in data.strip().split('\n'):
        if line == '': continue
        match = re.match(reg, line)
        action = 1
        if match.group(1) == 'turn off':
            action = 0
        elif match.group(1) == 'toggle':
            action = 2
        x1 = int(match.group(2))
        y1 = int(match.group(3))
        x2 = int(match.group(4))
        y2 = int(match.group(5))
        instructions.append((action, x1, y1, x2, y2))
    return instructions

# [ Computation functions ]
# -------------------------

### PART I
def process_no_brightness(instructions, debug=False):
    '''Processes the instructions list to change the grid and returns the number
    of lights that are switched on in the end. The function does NOT use the
    brightness variations but instead turns on/off or toggles completely.
    
    :param instructions: Instructions to use on the grid to switch the lights.
    :type instructions: list(tuple(int, int, int, int, int))
    :return: Number of lit lights in the end.
    :rtype: int
    '''
    grid = set()
    iterator = instructions
    if debug:
        iterator = tqdm(iterator, total=len(iterator))
    for action, x1, y1, x2, y2 in iterator:
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                if action == 0:
                    grid.discard((x, y))
                elif action == 1:
                    grid.add((x, y))
                else:
                    if (x, y) in grid:
                        grid.discard((x, y))
                    else:
                        grid.add((x, y))
    return len(grid)

### PART II
def process_with_brightness(instructions, debug=False):
    '''Processes the instructions list to change the grid and returns the total
    brightness of the grid in the end. The function uses the brightness
    variations.
    
    :param instructions: Instructions to use on the grid to switch the lights.
    :type instructions: list(tuple(int, int, int, int, int))
    :return: Total brightness of the grid in the end.
    :rtype: int
    '''
    grid = defaultdict(int)
    iterator = instructions
    if debug:
        iterator = tqdm(iterator, total=len(iterator))
    for action, x1, y1, x2, y2 in iterator:
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                if action == 0:
                    grid[(x, y)] = max(grid[(x, y)] - 1, 0)
                elif action == 1:
                    grid[(x, y)] += 1
                else:
                    grid[(x, y)] += 2
    return sum(grid.values())
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    assert process_no_brightness([ (0, 0, 0, 999, 999) ]) == 0
    assert process_no_brightness([ (2, 0, 0, 999, 999) ]) == 1000000
    assert process_no_brightness([ (2, 0, 0, 999, 999) ]) == 1000000
    ### Part II
    assert process_with_brightness([ (1, 0, 0, 0, 0) ]) == 1
    assert process_with_brightness([ (2, 0, 0, 999, 999) ]) == 2000000
    
if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    # get input data
    data_path = '../data/day6.txt'
    instructions = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = process_no_brightness(instructions, debug=True)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = process_with_brightness(instructions, debug=True)
    print('PART II: solution = {}'.format(solution))

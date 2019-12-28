### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 13: Knights of the Dinner Table
### =============================================
from itertools import permutations

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of placements.
    :rtype: dict(str, tuple(str, int))
    '''
    placements = {}
    for line in data.strip().split('\n'):
        words = line.split()
        effect = int(words[3])
        if 'lose' in words:
            effect = -effect
        person = words[0]
        neighbor = words[-1].replace('.', '')
        if person in placements:
            placements[person].append((neighbor, effect))
        else:
            placements[person] = [ (neighbor, effect) ]
    return placements

# [ Computation functions ]
# -------------------------
def compute_configuration_happiness(placements, configuration):
    '''Computes the total amount of happiness for this configuration (by
    checking the amount of happiness for every person depending on their two
    neighbors).
    
    :param placements: List of placements.
    :type placements: dict(str, tuple(str, int))
    :param configuration: Placement order for everyone.
    :type configuration: list(str)
    :return: Total happiness.
    :rtype: int
    '''
    n = len(configuration)
    happiness = 0
    for i, person in enumerate(configuration):
        prev = configuration[(i-1) % n]
        next = configuration[(i+1) % n]
        for neighbor, happ in placements[person]:
            if neighbor == prev or neighbor == next:
                happiness += happ
    return happiness

def find_optimal_configuration(placements):
    '''Gets the optimal configuration that maximizes everyone's happiness and
    calculates its total happiness change.
    
    :param placements: List of placements.
    :type placements: dict(str, tuple(str, int))
    :return: Total happiness change.
    :rtype: int
    '''
    persons = list(placements.keys())
    configurations = permutations(persons, len(persons))
    return max([ compute_configuration_happiness(placements, configuration) \
        for configuration in configurations ])

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    placements = parse_input(
    '''Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.''')
    assert find_optimal_configuration(placements) == 330

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day13.txt'
    placements = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = find_optimal_configuration(placements)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    # . add myself to the list with null happiness change for everyone
    persons = list(placements.keys())
    placements['Me'] = []
    for p in persons:
        placements['Me'].append((p, 0))
        placements[p].append(('Me', 0))
    # . find the new optimal placement
    solution = find_optimal_configuration(placements)
    print('PART II: solution = {}'.format(solution))

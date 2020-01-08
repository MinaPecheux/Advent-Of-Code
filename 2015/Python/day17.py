### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 17: No Such Thing as Too Much
### =============================================
from itertools import combinations

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Available container sizes.
    :rtype: list(int)
    '''
    return [ int(x) for x in data.strip().split('\n') ]

# [ Computation functions ]
# -------------------------
def find_container_combinations(containers, amount):
    '''Finds out the number of possible combinations that can fit the given
    amount of eggnog.
    
    :param containers: Available container sizes.
    :type containers: list(int)
    :param amount: Amount of eggnog to fit.
    :type amount: int
    :return: Number of different combinations.
    :rtype: int
    '''
    possibilities = set()
    for n in range(len(containers)):
        combs = combinations([ (i, v) for i, v in enumerate(containers) ], n)
        for comb in combs:
            s = sum([ v for _, v in comb ])
            if s == amount:
                possibilities.add(tuple([ i for i, _ in comb ]))
    return possibilities

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    containers = [ 20, 15, 10, 5, 5 ]
    assert len(find_container_combinations(containers, 25)) == 4

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day17.txt'
    containers = parse_input(open(data_path, 'r').read())
    combs = find_container_combinations(containers, 150)
    
    ### PART I
    solution = len(combs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    lengths = [ len(c) for c in combs ]
    min_n_containers = min(lengths)
    solution = len([ c for c in combs if len(c) == min_n_containers ])
    print('PART II: solution = {}'.format(solution))
    
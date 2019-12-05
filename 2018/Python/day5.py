### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 5: Alchemical Reduction
### =============================================
from itertools import chain, product
from random import choice

# [ Computation functions ]
# -------------------------
### PART I
LOW_UP_DIFF = ord('a') - ord('A')
def try_reaction(units):
    '''Checks to see if the two units react together and annihilate each other
    or if they stay identical.
    
    :param units: Units in the reaction.
    :type units: list(str)
    '''
    unit1, unit2 = units
    return abs(ord(unit1) - ord(unit2)) == LOW_UP_DIFF
    
def apply_reactions(polymer):
    '''Applies the reaction process to the polymer iteratively until there is
    no reaction anymore.
    
    :param polymer: Polymer to apply the reactions to.
    :type polymer: str
    '''
    upp_letters = [ chr(i) for i in range(65, 91) ]
    low_letters = [ chr(i) for i in range(97, 123) ]
    annihilating_pairs = [ ''.join(p) for p in chain(
        product(low_letters, upp_letters), product(upp_letters, low_letters)
    ) if try_reaction(p) ]
    while True:
        original = polymer
        for pair in annihilating_pairs:
            polymer = polymer.replace(pair, '')
        if original == polymer: return polymer
        
### Part II
def find_shortest_polymer(polymer):
    '''Finds the shortest possible polymer after removing one unit from the
    possible combinations (e.g.: removing all a/A, all b/B...) in the polymer
    before fully reducing it.
    
    :param polymer: Polymer to apply the reactions to.
    :type polymer: str
    '''
    upp_letters = [ chr(i) for i in range(65, 91) ]
    low_letters = [ chr(i) for i in range(97, 123) ]
    annihilating_pairs = [ ''.join(p) for p in chain(
        product(low_letters, upp_letters), product(upp_letters, low_letters)
    ) if try_reaction(p) ]
    
    polymer_lengths = []
    for c in range(65, 91):
        test_polymer = polymer
        test_polymer = test_polymer.replace(chr(c), '')
        test_polymer = test_polymer.replace(chr(c).lower(), '')
        pairs = [ p for p in annihilating_pairs if not chr(c) in p ]
        while True:
            original = test_polymer
            for pair in pairs:
                test_polymer = test_polymer.replace(pair, '')
            if original == test_polymer: break
        polymer_lengths.append(len(test_polymer))
    return min(polymer_lengths)
        
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert apply_reactions('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'
    ### PART II
    assert find_shortest_polymer('dabAcCaCBAcCcaDA') == 4

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day5.txt'
    input = open(data_path, 'r').read().strip()

    ### PART I
    solution = len(apply_reactions(input))
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_shortest_polymer(input)
    print('PART II: solution = {}'.format(solution))

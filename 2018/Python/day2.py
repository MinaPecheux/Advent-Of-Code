### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 2: Inventory Management System
### =============================================
from collections import Counter

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    return data.split('\n')

# [ Computation functions ]
# -------------------------
### PART I
def compute_checksum(ids):
    '''Computes the checksum of a list of box IDs by checking the ones that
    contain the same letter two or three times.
    
    :param ids: List of box IDs to compute the checksum for.
    :type ids: list(str)
    '''
    doubles_count = 0
    triples_count = 0
    for id in ids:
        counts = Counter(list(id)).values()
        if 2 in counts: doubles_count += 1
        if 3 in counts: triples_count += 1
    return doubles_count * triples_count
    
### PART II
def ids_match(id1, id2):
    '''Computes the matching letters between two box IDs (i.e. two strings). The
    function assumes that the two IDs have the same length.
    
    :param id1: First id to use.
    :type id1: str
    :param id2: Second id to use.
    :type id2: str
    '''
    match = ''
    for a, b in zip(id1, id2):
        if a == b:
            match += a
    return match

def find_matches_common_letters(ids):
    '''Returns the common letters in the two matching IDs, i.e. the box IDs that
    only differ by 1 character (the function assumes that all IDs have the same
    length).
    
    :param ids: List of box IDs to compute the checksum for.
    :type ids: list(str)
    '''
    for id1 in ids:
        for id2 in ids:
            match = ids_match(id1, id2)
            if len(match) == len(id1) - 1: # only differ by 1 character
                return match
    return ''
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert compute_checksum([ 'abcdef', 'bababc', 'abbcde', 'abcccd',
        'aabcdd', 'abcdee', 'ababab' ]) == 12
    ### PART II
    assert find_matches_common_letters([ 'abcde', 'fghij', 'klmno', 'pqrst',
        'fguij', 'axcye', 'wvxyz' ]) == 'fgij'

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day2.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = compute_checksum(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_matches_common_letters(inputs)
    print('PART II: solution = {}'.format(solution))

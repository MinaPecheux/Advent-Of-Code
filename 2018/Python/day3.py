### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 3: No Matter How You Slice It
### =============================================
import re
from collections import Counter

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    regex = r'\#(\d+)\s\@\s(\d+),(\d+):\s(\d+)x(\d+)'
    inputs = []
    for claim in data.split('\n'):
        if claim == '': continue
        matches = re.match(regex, claim)
        inputs.append(tuple(( int(matches.group(m)) for m in range(1, 6) )))
    return inputs

# [ Computation functions ]
# -------------------------
### PART I
def find_overlapping_claims(claims):
    '''Computes how many square inches of fabric are within two or more claims.
    
    :param claims: List of claims (with tuple components: (id, x, y, w, h)).
    :type claims: list(tuple(int))
    '''
    claim_squares = []
    for _, x, y, w, h in claims:
        for xx in range(x, x + w): # range is [x, x+w[ i.e. it has length w
            for yy in range(y, y + h):
                claim_squares.append((xx, yy))
    overlaps = [ sq for sq, count in Counter(claim_squares).items() if count > 1 ]
    return len(set(overlaps))
    
### PART II
def find_non_overlapping_claim(claims):
    '''Finds the single claim that remains after all the overlapping ones have
    been removed.
    
    :param claims: List of claims (with tuple components: (id, x, y, w, h)).
    :type claims: list(tuple(int))
    '''
    claim_squares = {}
    claim_ids = set()
    for id, x, y, w, h in claims:
        claim_ids.add(id)
        for xx in range(x, x + w):
            for yy in range(y, y + h):
                sq = (xx, yy)
                if sq in claim_squares:
                    claim_squares[sq].append(id)
                else:
                    claim_squares[sq] = [ id ]
    overlaps = [ sq for sq, claims in claim_squares.items() if len(claims) > 1 ]
    forbidden_claims = []
    for overlap in overlaps:
        forbidden_claims.extend(claim_squares[overlap])
    forbidden_claims = set(forbidden_claims)
    return set(claim_ids).difference(forbidden_claims).pop()
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert find_overlapping_claims([ (1, 1, 3, 4, 4), (2, 3, 1, 4, 4),
        (3, 5, 5, 2, 2) ]) == 4
    ### PART II
    assert find_non_overlapping_claim([ (1, 1, 3, 4, 4), (2, 3, 1, 4, 4),
        (3, 5, 5, 2, 2) ]) == 3

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day3.txt'
    inputs = parse_input(open(data_path, 'r').read())

    ### PART I
    solution = find_overlapping_claims(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_non_overlapping_claim(inputs)
    print('PART II: solution = {}'.format(solution))

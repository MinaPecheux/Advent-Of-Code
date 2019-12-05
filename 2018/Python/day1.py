### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 1: Frequency changes
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    inputs = []
    for x in data.split('\n'):
        if x == '': continue
        if x.startswith('+'): inputs.append(int(x))
        else: inputs.append(-int(x[1:]))
    return inputs

# [ Computation functions ]
# -------------------------
### PART I
def compute_final_frequency(changes):
    '''Computes the final frequency, starting from 0 and applying all the changes
    one after the other.
    
    :param changes: Frequency changes to apply.
    :type changes: list(int)
    '''
    return sum(changes)
    
### PART II
def compute_first_cycle(changes):
    '''Returns the first frequency the device reaches twice (it might loop back
    if necessary).
    
    :param changes: Frequency changes to apply.
    :type changes: list(int)
    '''
    prev_freqs = set([ 0 ])
    freq = 0
    while True:
        i = 0
        while i < len(changes):
            freq += changes[i]
            if freq in prev_freqs:
                return freq
            else:
                prev_freqs.add(freq)
            i = i + 1 if i < len(changes) - 1 else 0
    return None
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert compute_final_frequency([ 1,1,1 ]) == 3
    assert compute_final_frequency([ 1,1,-2 ]) == 0
    assert compute_final_frequency([ -1,-2,-3 ]) == -6
    ### PART II
    assert compute_first_cycle([ 1, -1 ]) == 0
    assert compute_first_cycle([ 3, 3, 4, -2, -4 ]) == 10
    assert compute_first_cycle([ -6, 3, 8, 5, -6 ]) == 5
    assert compute_first_cycle([ 7, 7, -2, -7, -4 ]) == 14

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day1.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = compute_final_frequency(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = compute_first_cycle(inputs)
    print('PART II: solution = {}'.format(solution))

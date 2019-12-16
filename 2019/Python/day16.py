### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 16: Flawed Frequency Transmission
### =============================================
from tqdm import tqdm

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: list(int)
    '''
    return [ int(x) for x in data.strip() ]

# [ Computation functions ]
# -------------------------
### Part I
def compute_phase(inputs, skip_digits=None):
    '''Computes the next phase by applying the pattern to the given inputs.
    
    :param inputs: Current inputs to apply the pattern to.
    :type inputs: list(int)
    :param skip_digits: Number of digits to skip in the computation. The
        function assumes that if this variable is not None, then it is greater
        than or equal to half of the length of inputs.
    :type skip_digits: int
    :return: New phase state.
    :rtype: list(int)
    '''
    n = len(inputs)
    # compute the full result
    if skip_digits is None:
        output = []
        for idx in range(n):
            s = 0
            l = idx+1
            # apply the pattern on the inputs: either positive (+1) or negative (-1)
            # contribution from some parts of the inputs
            i = idx
            while i < n:
                s += sum(inputs[i:i+l]) - sum(inputs[i+2*l:i+3*l])
                i += 4*l
            # keep only ones digit
            d = int(str(s)[-1])
            output.append(d)
    # or skip ahead to only compute the end (assumes that the skip index is
    # greather than or equal to half of the inputs length)
    else:
        output = [0] * n
        output[-1] = inputs[-1]
        i = n - 2
        for idx in range(n-2, skip_digits - 1, -1):
            output[idx] = (output[idx+1] + inputs[i]) % 10
            i -= 1
    return output

### Part I
def compute_phases(n_phases, inputs, only_eight_digits=False, debug=False):
    '''Process the inputs phase by phase until the required number of phases
    has been reached.
    
    :param n_phases: Number of phases to compute.
    :type n_phases: int
    :param inputs: Initial problem input to process.
    :type inputs: list(int)
    :param only_eight_digits: Whether or not to return only the first eight
        digits of the result (as a string) or the full result (as a list of
        inputs).
    :type only_eight_digits: bool
    :param debug: Whether or not to display a progress bar during the
        computation.
    :type debug: bool
    :return: Final state of the inputs after all the phases have been computed.
    :rtype: str or list(int)
    '''
    iterator = range(n_phases)
    if debug:
        iterator = tqdm(iterator, total=n_phases)
    # compute iterations
    current = inputs
    for _ in iterator:
        current = compute_phase(current)
    # return full output or just the first eight digits as a string
    if only_eight_digits:
        return ''.join([ str(x) for x in current[:8] ])
    return current

### Part II
def compute_phases_nohead(n_phases, inputs, skip_digits, only_eight_digits=False,
    debug=False):
    '''Process the inputs phase by phase until the required number of phases
    has been reached and returns only a part of it while skipping a given
    number of digits from the start. It assumes that the number of passed digits
    is greater than or equal to half of the length of initial inputs.
    
    :param n_phases: Number of phases to compute.
    :type n_phases: int
    :param inputs: Initial problem input to process.
    :type inputs: list(int)
    :param skip_digits: Number of digits to skip in the final result.
    :type skip_digits: int
    :param only_eight_digits: Whether or not to return only the first eight
        digits of the result (as a string) or the full result (as a list of
        inputs).
    :type only_eight_digits: bool
    :param debug: Whether or not to display a progress bar during the
        computation.
    :type debug: bool
    :return: Final state of the inputs after all the phases have been computed.
    :rtype: str or list(int)
    '''
    iterator = range(n_phases)
    if debug:
        iterator = tqdm(iterator, total=n_phases)
    # compute iterations
    current = inputs
    for _ in iterator:
        current = compute_phase(current, skip_digits=skip_digits)
    # return full output or just the first eight digits as a string
    if only_eight_digits:
        return ''.join([ str(x) for x in current[skip_digits:skip_digits+8] ])
    return current

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    assert compute_phases(4, [ 1,2,3,4,5,6,7,8 ]) == [ 0,1,0,2,9,4,9,8 ]
    p = compute_phases(100, [ 8,0,8,7,1,2,2,4,5,8,5,9,1,4,5,4,6,6,1,9,0,8,3,2,1,
        8,6,4,5,5,9,5 ])
    assert ''.join([ str(x) for x in p ]).startswith('24176176')
    p = compute_phases(100, [ 1,9,6,1,7,8,0,4,2,0,7,2,0,2,2,0,9,1,4,4,9,1,6,0,4,
        4,1,8,9,9,1,7 ])
    assert ''.join([ str(x) for x in p ]).startswith('73745418')
    assert compute_phases(100, [ 6,9,3,1,7,1,6,3,4,9,2,9,4,8,6,0,6,3,3,5,9,9,5,
        9,2,4,3,1,9,8,7,3 ], only_eight_digits=True) == '52432133'
    
if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day16.txt'
    data = open(data_path, 'r').read()
    inputs = parse_input(data)
    
    ### PART I
    solution = compute_phases(100, inputs, only_eight_digits=True, debug=True)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    inp = [ item for _ in range(10000) for item in inputs ]
    solution = compute_phases_nohead(100, inp, only_eight_digits=True,
        skip_digits=int(data[:7]), debug=True)
    print('PART II: solution = {}'.format(solution))
    

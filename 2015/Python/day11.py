### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 11: Corporate Policy
### =============================================

# [ Computation functions ]
# -------------------------
def create_generator(syms, rolls, start):
    '''Creates a new generator that works like an odometer.
    
    :param syms: List of possible symbols on each "gear".
    :type syms: list(int) or list(str)
    :param rolls: Number of "gears".
    :type rolls: int
    :param start: Initial value of the odometer (as an int).
    :type start: int
    :return: Generator of all configurations of the odometer.
    :rtype: generator
    '''
    base = len(syms)
    combinations = base ** rolls

    # The odometer is to be reversed on delivery.
    odo = [ syms[0] for i in range(rolls) ]

    # Odometer start setting:
    curval = start
    for i in range(rolls):
        j = curval % base
        odo[i] = syms[j]
        curval = curval // base

    curval = start
    while curval < combinations:
        # Consider roll 0 to be rightmost.
        yield odo[-1::-1]
        for roll, sym in enumerate(odo[:]):
            i = syms.index(sym)
            if i < base - 1:
                odo[roll] = syms[i + 1]
                # Could roll the roll w/o roll-over, next value:
                break
            else:
                odo[roll] = syms[0]
                # There was a roll-over, next roll.
        curval += 1

### PART I
ALPHABET = [ chr(i) for i in range(ord('a'), ord('z')+1) ]
PAIRS = [ c * 2 for c in ALPHABET ]
INCREASING_TRIPLES = [
    'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij', 'ijk',
    'jkl', 'klm', 'lmn', 'mno', 'nop', 'opq', 'pqr', 'qrs', 'rst',
    'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz'
]
def pwd_is_ok(pwd):
    '''Checks if a test password meets the following criteria:
        - include one increasing straight of at least three letters, like abc,
        bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't
        count.
        - not contain the letters i, o, or l
        - must contain at least two different, non-overlapping pairs of letters,
        like aa, bb, or zz
    
    :param pwd: Password to test.
    :type pwd: str
    :return: Password validity.
    :rtype: bool
    '''
    if not any(triple in pwd for triple in INCREASING_TRIPLES):
        return False
    n_pairs = 0
    for pair in PAIRS:
        if pair in pwd:
            n_pairs += 1
    return n_pairs >= 2

def get_new_password(input):
    '''Searches for the new password based on the previous one (the input).
    
    :param input: Old password to start from.
    :type input: str
    :return: New password.
    :rtype: str
    '''
    start = 0
    roll = 1
    for i, c in enumerate(input[::-1]):
        start += (ord(c) - ord('a')) * roll
        roll *= len(ALPHABET)
    valid = False
    generator = create_generator(ALPHABET, len(input), start + 1)
    pwd = input
    for test in generator:
        if 'i' in test or 'o' in test or 'l' in test:
            continue
        pwd = ''.join(test)
        if pwd_is_ok(pwd):
            break
    return pwd

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert pwd_is_ok('hijklmmn') == False
    assert pwd_is_ok('abbceffg') == False
    assert pwd_is_ok('abbcegjk') == False
    assert get_new_password('abcdefgh') == 'abcdffaa'
    assert get_new_password('ghijklmn') == 'ghjaabcc'

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    print('(Finished tests)')
    
    # get input data
    input = 'hepxcrrq'
    
    ### PART I
    solution = get_new_password(input)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = get_new_password(solution)
    print('PART II: solution = {}'.format(solution))

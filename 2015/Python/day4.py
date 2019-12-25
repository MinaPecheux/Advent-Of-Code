### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 4: The Ideal Stocking Stuffer
### =============================================
import hashlib

# [ Computation functions ]
# -------------------------

### PART I + II
def find_hash(secret, leading_zeroes):
    '''Computes the lowest positive integer that should be concatening to the
    secret key in order to get a MD5 hash that starts with a given number of
    zeroes.
    
    :param secret: Secret key for the MD5 hash.
    :type secret: str
    :param leading_zeroes: Number of leading zeroes to search for in the hash.
    :type leading_zeroes: int
    :return: Smallest positive integer that matches the criterion.
    :rtype: int
    '''
    prefix = '0' * leading_zeroes
    i = 1
    while True:
        str = '{}{}'.format(secret, i)
        hex = hashlib.md5(str.encode('utf-8')).hexdigest()
        if hex.startswith(prefix):
            return i
        i += 1
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert find_hash('abcdef', 5) == 609043
    assert find_hash('pqrstuv', 5) == 1048970

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    secret = 'ckczppom'
    
    ### PART I
    solution = find_hash(secret, 5)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_hash(secret, 6)
    print('PART II: solution = {}'.format(solution))

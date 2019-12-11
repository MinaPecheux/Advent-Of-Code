### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 4: Secure Container
### =============================================
from collections import Counter

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: tuple(int, int)
    '''
    tmp = data.split('-')
    return int(tmp[0]), int(tmp[1])

# [ Computation functions ]
# -------------------------
### PART I
def number_is_ok_p1(number):
    '''Checks if a number meets the password criteria of Part I:
        - length of 6 digits
        - two adjacent digits are the same
        - going left from right, digits never decrease (i.e. they increase or
        stay the same)
        
    :param number: Number to check.
    :type number: int
    :return: Number validity.
    :rtype: bool
    '''
    n_str = str(number)
    if len(n_str) != 6:
        return False
    prev_c = -1
    has_duplicate = False
    for c_str in n_str:
        c = int(c_str)
        if c < prev_c:
            return False
        if c == prev_c:
            has_duplicate = True
        prev_c = c
    return has_duplicate

### PART II
def number_is_ok_p2(number):
    '''Checks if a number meets the password criteria of Part II:
        - same as criteria for Part I
        - plus the two adjacent digits are not part of a larger group of matching
        digits (i.e. they are just a double, not a longer sequence of same digit)
        
    :param number: Number to check.
    :type number: int
    :return: Number validity.
    :rtype: bool
    '''
    n_str = str(number)
    if len(n_str) != 6:
        return False
    prev_c = -1
    for c_str in n_str:
        c = int(c_str)
        if c < prev_c:
            return False
        prev_c = c
    counts = Counter(list(n_str))
    return 2 in counts.values()

def get_count_of_valid_numbers(inputs, check):
    '''Finds all the valid numbers (that meet the given password criteria) in
    the range given by the inputs.
        
    :param inputs: Minimum and maximum value (inclusive) for the numbers to check.
    :type inputs: list(int)
    :param check: Validity function to pass.
    :type check: func
    :return: Count of numbers in the range that pass the test.
    :rtype: int
    '''
    min, max = inputs
    count = 0
    for n in range(min, max+1):
        if check(n):
            count += 1
    return count

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert number_is_ok_p1(111111) == True
    assert number_is_ok_p1(223450) == False
    assert number_is_ok_p1(123789) == False
    
    ### PART II
    assert number_is_ok_p2(112233) == True
    assert number_is_ok_p2(123444) == False
    assert number_is_ok_p2(111122) == True

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data = '248345-746315'
    inputs = parse_input(data)

    ### PART I
    solution = get_count_of_valid_numbers(inputs, number_is_ok_p1)
    print('PART I: solution = {}'.format(solution))

    ### PART II
    solution = get_count_of_valid_numbers(inputs, number_is_ok_p2)
    print('PART II: solution = {}'.format(solution))
    

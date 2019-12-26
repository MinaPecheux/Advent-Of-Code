### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 5: Doesn't He Have Intern-Elves For This?
### =============================================
import re

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of strings to check.
    :rtype: list(str)
    '''
    return data.strip().split('\n')

# [ Computation functions ]
# -------------------------

VOWELS = 'aeiou'
def is_nice_p1(str):
    '''Checks if the string is nice, given the criteria:
        - contains at least three vowels
        - at least one letter appears twice in a row
        - does NOT contain the strings: ab, cd, pq, xy (supersedes other
        requirements)
    
    :param str: String to check.
    :type str: str
    :return: "Niceness" of the string.
    :rtype: bool
    '''
    # check for forbidden substrings
    if 'ab' in str or 'cd' in str or 'pq' in str or 'xy' in str:
        return False
    # check for number of vowels
    vowels_count = sum([ 1 if char in VOWELS else 0 for char in str ])
    if vowels_count < 3:
        return False
    # check for repeated letter
    for i in range(1, len(str)):
        if str[i-1] == str[i]:
            return True
    return False

MIDDLE_CHAR_REGEX = r'(\w)\w(\1)'
def is_nice_p2(str):
    '''Checks if the string is nice, given the new criteria:
        - contains a pair of any two letters that appears at least twice in the
        string without overlapping
        - contains at least one letter which repeats with exactly one letter
        between them
    
    :param str: String to check.
    :type str: str
    :return: "Niceness" of the string.
    :rtype: bool
    '''
    # check for letter repetition with one letter in the middle (through regex)
    if re.search(MIDDLE_CHAR_REGEX, str) is None:
        return False
    # check for non-overlapping pair
    pairs = {}
    for i in range(len(str) - 1):
        pair = str[i:i+2]
        if pair in pairs:
            if i >= pairs[pair] + 2:
                return True
        else:
            pairs[pair] = i
    return False

### PART I + II
def get_n_nice_strings(strings, check):
    '''Finds out the number of strings that are "nice".
    
    :param strings: List of strings to check.
    :type strings: list(str)
    :param check: Check function to use for "niceness".
    :type check: func
    :return: Number of "nice" strings.
    :rtype: int
    '''
    return sum([ 1 if check(s) else 0 for s in strings ])
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    assert is_nice_p1('ugknbfddgicrmopn') == True
    assert is_nice_p1('aaa') == True
    assert is_nice_p1('jchzalrnumimnmhp') == False
    assert is_nice_p1('haegwjzuvuyypxyu') == False
    assert is_nice_p1('dvszwmarrgswjxmb') == False
    ### Part II
    assert is_nice_p2('qjhvhtzxzqqjkmpb') == True
    assert is_nice_p2('xxyxx') == True
    assert is_nice_p2('uurcxstgmygtbstg') == False
    assert is_nice_p2('ieodomkazucvgmuy') == False

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day5.txt'
    strings = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = get_n_nice_strings(strings, is_nice_p1)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = get_n_nice_strings(strings, is_nice_p2) # 27: wrong
    print('PART II: solution = {}'.format(solution))

### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 8: Matchsticks
### =============================================
import codecs
import re

# [ Input parsing functions ]
# ---------------------------
def parse_input(file):
    '''Parses the incoming file data into processable inputs.
    
    :param file: Open file pointer with the problem data.
    :type file: io.Stream
    :return: List of strings to check.
    :rtype: list(str)
    '''
    return [ line.strip() for line in file ]

# [ Computation functions ]
# -------------------------

### PART I
def decode_string(encoded):
    '''Decodes a string from its internal representation to the evaluated form.
    
    :param encoded: Encoded string (internal representation).
    :type encoded: str
    :return: Decoded version.
    :rtype: str
    '''
    return eval(encoded)

def get_decoding_diff(strings):
    '''Computes the total difference of length between the initial and the
    decoded (i.e. evaluated) strings.
    
    :param strings: List of strings to check.
    :type strings: list(str)
    :return: Difference of length between initial and decoded strings.
    :rtype: int
    '''
    s1 = 0
    s2 = 0
    for string in strings:
        decoded = decode_string(string)
        s1 += len(string)
        s2 += len(decoded)
    return s1 - s2

### PART II
def encode_string(decoded):
    '''Encodes a string from its classic representation to the escaped version.
    
    :param decoded: Decoded string.
    :type decoded: str
    :return: Escaped version of the string.
    :rtype: str
    '''
    return '"{}"'.format(re.escape(decoded))
    
def get_encoding_diff(strings):
    '''Computes the total difference of length between the encoded (i.e.
    escaped) and the initial strings.
    
    :param strings: List of strings to check.
    :type strings: list(str)
    :return: Difference of length between encoded and initial strings.
    :rtype: int
    '''
    s1 = 0
    s2 = 0
    for string in strings:
        encoded = encode_string(string)
        s1 += len(encoded)
        s2 += len(string)
    return s1 - s2
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    assert decode_string('""') == ''
    assert decode_string('"abc"') == 'abc'
    assert decode_string('"aaa\\"aaa"') == 'aaa"aaa'
    assert decode_string('"\\x27"') == '\''
    
    ### Part II
    assert encode_string('""') == '"\\"\\""'
    assert encode_string('"abc"') == '"\\"abc\\""'
    assert encode_string('"aaa\\"aaa"') == '"\\"aaa\\\\\\"aaa\\""'
    assert encode_string('"\\x27"') == '"\\"\\\\x27\\""'
    
if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    # get input data
    data_path = '../data/day8.txt'
    strings = parse_input(codecs.open(data_path, encoding='utf-8'))
    
    ### PART I
    solution = get_decoding_diff(strings)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = get_encoding_diff(strings)
    print('PART II: solution = {}'.format(solution))

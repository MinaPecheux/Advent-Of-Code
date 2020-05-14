### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2016 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 3: Squares With Three Sides
### =============================================

import re

# [ Input parsing functions ]
# ---------------------------
def parse_input_per_row(data):
    '''Parses the incoming data into processable inputs.

    Each row is inferred to represent one triangle.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of triangles candidates.
    :rtype: list(int)
    '''
    triangles = []
    PARSE_REGEX = r'\s*(\d+)\s*(\d+)\s*(\d+)\n'
    matches = re.findall(PARSE_REGEX, data, re.MULTILINE)
    triangles = [ (int(m[0]), int(m[1]), int(m[2])) for m in matches ]
    return triangles

def parse_input_per_block(data):
    '''Parses the incoming data into processable inputs.

    Triangles are inferred to be defined by columns of 3 numbers,
    one per row through 3 rows.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of triangles candidates.
    :rtype: list(int)
    '''
    triangles = []
    lines = data.split('\n')
    PARSE_REGEX = r'\s*(\d+)\s*(\d+)\s*(\d+)'
    cur_triangles = [ [], [], [] ]
    for i, line in enumerate(lines):
        if i > 0 and i % 3 == 0:
            triangles.extend(cur_triangles)
            cur_triangles = [ [], [], [] ]
        match = re.search(PARSE_REGEX, line)
        if match:
            cur_triangles[0].append(int(match.group(1)))
            cur_triangles[1].append(int(match.group(2)))
            cur_triangles[2].append(int(match.group(3)))
    triangles.extend(cur_triangles)
    return triangles

# [ Computation functions ]
# -------------------------

### PART I + II
def num_of_possible_triangles(inputs):
    '''Computes the number of possible triangles in the list.
    A triangle is possible if the sum of any two sides is
    larger than the remaining side.
    
    :param inputs: List of triangles candidates.
    :type inputs: list(tuple(int, int, int))
    :return: Number of possible triangles.
    :rtype: int
    '''
    num_possible = 0
    for triangle in inputs:
        s1, s2, s3 = triangle
        if s1 + s2 > s3 and s1 + s3 > s2 and s2 + s3 > s1:
            num_possible += 1
    return num_possible

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    triangles = [(5, 10, 25)]
    assert num_of_possible_triangles(triangles) == 0
    ### PART II
    data = '101 301 501\n102 302 502\n103 303 503\n201 401 601\n202 402 602\n203 403 603'
    triangles = parse_input_per_block(data)
    # (convert to tuples to make assertions easier)
    triangles = [ tuple(t) for t in triangles ]
    assert (101, 102, 103) in triangles
    assert (201, 202, 203) in triangles
    assert (301, 302, 303) in triangles
    assert (401, 402, 403) in triangles
    assert (501, 502, 503) in triangles
    assert (601, 602, 603) in triangles

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day3.txt'
    
    ### PART I
    inputs = parse_input_per_row(open(data_path, 'r').read())
    solution = num_of_possible_triangles(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    inputs = parse_input_per_block(open(data_path, 'r').read())
    solution = num_of_possible_triangles(inputs)
    print('PART II: solution = {}'.format(solution))

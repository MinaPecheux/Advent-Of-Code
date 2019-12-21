### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 5: Sunny with a Chance of Asteroids
### =============================================
from intcode import IntcodeProgram

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: list(int)
    '''
    return [ int(x) for x in data.split(',') if x != '' ]

# [ Computation functions ]
# -------------------------
def process_inputs(inputs, input):
    '''Executes the Intcode program on the provided inputs and computes the final
    result.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param input: Specific input for the program execution.
    :type input: int
    :return: Final output of the program.
    :rtype: int
    '''
    # create program
    program = IntcodeProgram(inputs)
    # insert input in memory
    program.push_memory(input)
    # execute program
    program.run()
    # return last output
    return program.output[-1]

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert process_inputs([ 3,0,4,0,99 ], 1) == 1
    assert process_inputs([ 3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 ], 0) == 0
    assert process_inputs([ 3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 ], 1) == 1
    assert process_inputs([ 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,
        1000,1,20,4,20,1105,1,46,98,99 ], 1) == 999
    assert process_inputs([ 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,
        1000,1,20,4,20,1105,1,46,98,99 ], 8) == 1000
    assert process_inputs([ 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,
        1000,1,20,4,20,1105,1,46,98,99 ], 12) == 1001
        
if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day5.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = process_inputs(inputs, input=1)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = process_inputs(inputs, input=5)
    print('PART II: solution = {}'.format(solution))

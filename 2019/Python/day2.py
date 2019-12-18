### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 2: 1202 Program Alarm
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
def process_inputs(inputs, restore_gravity_assist=False):
    '''Executes the Intcode program on the provided inputs and computes the final
    result.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param restore_gravity_assist: Whether or not to restore the gravity assist
        by modifying the input program.
    :type restore_gravity_assist: bool
    :return: Final output of the program.
    :rtype: int
    '''
    # restore gravity assist?
    if restore_gravity_assist:
        inputs[1] = 12
        inputs[2] = 2
    # create and execute program
    program = IntcodeProgram(inputs)
    program.run()
    # isolate final result
    return program.program[0]
    
### PART II
def find_pair(inputs, wanted_output):
    '''A brute-force algorithm to systematically try all possible input pairs
    until we find the one that gave the desired output (we can determine a
    finished set of possible candidates since we know that each number is in the
    [0, 99] range).
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param wanted_output: Desired output of the program.
    :type wanted_output: int
    :return: Specific checksum that matches the desired output.
    :rtype: int
    '''
    # prepare program
    program = IntcodeProgram(inputs)
    for noun in range(0, 100): # range is [0, 100[ = [0, 99]
        for verb in range(0, 100):
            # reset program to initial state
            program.reset()
            # set up noun and verb
            program.program[1] = noun
            program.program[2] = verb
            # run and compare result
            program.run()
            if program.program[0] == wanted_output:
                return 100 * noun + verb

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert process_inputs([ 1,9,10,3,2,3,11,0,99,30,40,50 ]) == 3500
    assert process_inputs([ 1,0,0,0,99 ]) == 2
    assert process_inputs([ 2,3,0,3,99 ]) == 2
    assert process_inputs([ 2,4,4,5,99,0 ]) == 2
    assert process_inputs([ 1,1,1,4,99,5,6,0,99 ]) == 30

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day2.txt'
    
    ### PART I
    inputs = parse_input(open(data_path, 'r').read())
    solution = process_inputs(inputs, restore_gravity_assist=True)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    # (reparse inputs to get back original data)
    inputs = parse_input(open(data_path, 'r').read())
    solution = find_pair(inputs, 19690720)
    print('PART II: solution = {}'.format(solution))
    

### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 9: Sensor Boost
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
### Part I + II
def process_inputs(inputs, input=None, debug=False):
    '''Executes the Intcode program on the provided inputs and computes the final
    result.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param input: Integer to provide as input to the program.
    :type input: int
    :param debug: Whether or not the IntcodeProgram should debug its
        execution at each instruction processing.
    :type debug: bool
    :return: Last output of the program.
    :rtype: int
    '''
    # create program
    program = IntcodeProgram(inputs, debug=debug)
    # insert input in memory if need be
    if input is not None:
        program.push_memory(input)
    # run program
    program.run()
    # get final result
    return program.output[-1]

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    # test new instructions
    ref = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    program = IntcodeProgram([
        109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
    ])
    program.run()
    assert ','.join([ str(x) for x in program.output ]) == ref
    
    # Part I + II
    assert len(str(process_inputs([ 1102,34915192,34915192,7,4,7,99,0 ]))) == 16
    assert process_inputs([ 104,1125899906842624,99 ]) == 1125899906842624

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day9.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = process_inputs(inputs, input=1)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = process_inputs(inputs, input=2)
    print('PART II: solution = {}'.format(solution))
    

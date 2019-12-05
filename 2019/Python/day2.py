### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 2: Intcode programming
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    return [ int(x) for x in data.split(',') if x != '' ]

# [ Computation functions ]
# -------------------------
OPERATIONS = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b
}

### PART I
def process_opcode(inputs, instruction_ptr):
    '''Process an opcode by using the provided inputs and the current operation
    index.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param instruction_ptr: Current instruction pointer.
    :type instruction_ptr: int
    '''
    code = inputs[instruction_ptr]
    if code == 99:
        return None
    elif code == 1 or code == 2:
        op = OPERATIONS[code]
        a, b, c = inputs[instruction_ptr+1:instruction_ptr+4]
        inputs[c] = op(inputs[a], inputs[b])
        return instruction_ptr + 4
    else:
        return -1

def process_inputs(inputs, restore_gravity_assist=False):
    '''Executes the Intcode program on the provided inputs and computes the final
    result.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param restore_gravity_assist: Whether or not to restore the gravity assist
        by modifying the input program.
    :type restore_gravity_assist: bool
    '''
    # restore gravity assist?
    if restore_gravity_assist:
        inputs[1] = 12
        inputs[2] = 2
    # execute program (modifies the inputs in-place)
    instruction_ptr = 0
    while instruction_ptr is not None:
        instruction_ptr = process_opcode(inputs, instruction_ptr)
        if instruction_ptr == -1:
            return None
    # isolate final result
    return inputs[0]
    
### PART II
def find_pair(inputs, wanted_output):
    '''A brute-force algorithm to systematically try all possible input pairs
    until we find the one that gave the desired output (we can determine a
    finished set of possible candidates since we know that each number is in the
    [0, 99] range).
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param wanted_output: Desired outut of the program.
    :type wanted_output: int
    '''
    for noun in range(0, 100): # range is [0, 100[ = [0, 99]
        for verb in range(0, 100):
            # copy original data to avoid overwrite
            test_inputs = [ i for i in inputs ]
            # restore gravity assist
            test_inputs[1] = noun
            test_inputs[2] = verb
            if process_inputs(test_inputs) == wanted_output:
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

    ### PART II
    # .

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
    

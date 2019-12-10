### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 5: Sunny with a Chance of Asteroids
### =============================================
import io, sys

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    return [ int(x) for x in data.split(',') if x != '' ]

# [ Util class ]
# --------------
STREAM = None
class Debugger(object):
    
    '''Util class to print the Intcode program output to a specific stream and
    get back the result easily from it at the end of the execution.'''
    
    def __init__(self):
        self.stream = io.StringIO()
        global STREAM
        STREAM = self.stream
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.stream.close()
        global STREAM
        STREAM = None
        
    def full_output(self):
        return self.stream.getvalue()
        
    def last_output(self, separator='\n'):
        output = self.full_output()
        contents = [ c for c in output.split(separator) if len(c) > 0 ]
        return contents[-1]

# [ Computation functions ]
# -------------------------
INPUT = None # specific value for the input instruction
OPERATIONS = {
    1: (lambda a, b: a + b, 3),
    2: (lambda a, b: a * b, 3),
    3: (lambda: INPUT, 1),
    4: (None, 1),
    5: (None, 2),
    6: (None, 2),
    7: (lambda a, b: a < b, 3),
    8: (lambda a, b: a == b, 3)
}

def get_value(inputs, data, mode):
    '''Gets the "address" or "immediate value" for a given set of inputs and
    data.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param data: Data to execute.
    :type data: int
    :param mode: Execution mode (either 0, "address mode"; or 1, "immediate
        value mode").
    :type mode: int
    '''
    return inputs[data] if mode == 0 else data

def process_opcode(inputs, instruction_ptr):
    '''Process an opcode by using the provided inputs and the current operation
    index.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param instruction_ptr: Current instruction pointer.
    :type instruction_ptr: int
    '''
    instruction = str(inputs[instruction_ptr])
    code = int(instruction[-2:])
    if code == 99:
        return None

    op, n_inputs = OPERATIONS[code]
    modes = instruction[:-2]
    op_modes = [ int(m) for m in modes[::-1] ] + [ 0 ] * (n_inputs - len(modes))
    
    if code == 1 or code == 2: # add or multiply
        a, b, c = inputs[instruction_ptr+1:instruction_ptr+n_inputs+1]
        inputs[c] = op(
            get_value(inputs, a, op_modes[0]), get_value(inputs, b, op_modes[1])
        )
        return instruction_ptr + n_inputs + 1
    elif code == 3: # read input
        a = inputs[instruction_ptr+1]
        inputs[a] = op()
        return instruction_ptr + n_inputs + 1
    elif code == 4: # print output
        a = inputs[instruction_ptr+1]
        v = get_value(inputs, a, op_modes[0])
        if STREAM is None:
            print(v)
        else:
            STREAM.write('{}\n'.format(v))
        return instruction_ptr + n_inputs + 1
    elif code == 5: # jump-true
        a, b = inputs[instruction_ptr+1:instruction_ptr+n_inputs+1]
        if get_value(inputs, a, op_modes[0]) != 0:
            return get_value(inputs, b, op_modes[1])
        else:
            return instruction_ptr + n_inputs + 1
    elif code == 6: # jump-false
        a, b = inputs[instruction_ptr+1:instruction_ptr+n_inputs+1]
        if get_value(inputs, a, op_modes[0]) == 0:
            return get_value(inputs, b, op_modes[1])
        else:
            return instruction_ptr + n_inputs + 1
    elif code == 7 or code == 8: # less than or equal
        a, b, c = inputs[instruction_ptr+1:instruction_ptr+n_inputs+1]
        if op(get_value(inputs, a, op_modes[0]), get_value(inputs, b, op_modes[1])):
            inputs[c] = 1
        else:
            inputs[c] = 0
        return instruction_ptr + n_inputs + 1
    else:
        return -1

def process_inputs(inputs):
    '''Executes the Intcode program on the provided inputs and computes the final
    result.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    '''
    # execute program (modifies the inputs in-place)
    instruction_ptr = 0
    while instruction_ptr is not None:
        instruction_ptr = process_opcode(inputs, instruction_ptr)
        if instruction_ptr == -1:
            return None

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    global INPUT
    with Debugger() as debugger:
        ### PART I
        INPUT = 1
        process_inputs([ 3,0,4,0,99 ])
        assert debugger.last_output() == '1'
    
        ### PART II
        INPUT = 0
        process_inputs([ 3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 ])
        assert debugger.last_output() == '0'
        INPUT = 1
        process_inputs([ 3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 ])
        assert debugger.last_output() == '1'
        
        INPUT = 1
        process_inputs([ 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
            1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,
            1101,1000,1,20,4,20,1105,1,46,98,99 ])
        assert debugger.last_output() == '999'
        INPUT = 8
        process_inputs([ 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
            1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,
            1101,1000,1,20,4,20,1105,1,46,98,99 ])
        assert debugger.last_output() == '1000'
        INPUT = 12
        process_inputs([ 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
            1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,
            1101,1000,1,20,4,20,1105,1,46,98,99 ])
        assert debugger.last_output() == '1001'

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day5.txt'
    
    ### PART I
    INPUT = 1
    inputs = parse_input(open(data_path, 'r').read())
    with Debugger() as debugger:
        process_inputs(inputs)
        print('PART I: solution = {}'.format(debugger.last_output()))
    
    ### PART II
    INPUT = 5
    # (reparse inputs to get back original data)
    inputs = parse_input(open(data_path, 'r').read())
    with Debugger() as debugger:
        process_inputs(inputs)
        print('PART II: solution = {}'.format(debugger.last_output()))
    

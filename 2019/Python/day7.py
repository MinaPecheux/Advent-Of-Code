### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 7: Amplification Circuit
### =============================================
import itertools

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
    1: (lambda a, b: a + b, 3),
    2: (lambda a, b: a * b, 3),
    3: (None, 1),
    4: (None, 1),
    5: (None, 2),
    6: (None, 2),
    7: (lambda a, b: a < b, 3),
    8: (lambda a, b: a == b, 3)
}

class ProgramInstance(object):
    
    '''Util class to represent a program instance with its own instructions,
    memory, run state and instruction pointer. Allows for multiple instances
    in parallel to interact without overwriting data.'''
    
    INSTANCE_ID = 0 # class variable that is common to all instances
    
    def __init__(self, program):
        '''Initialization function for the instance.
        
        :param program: Original Intcode program to execute (will be copied to
            avoid in-place modification).
        :type program: list(int)
        '''
        self.id = ProgramInstance.INSTANCE_ID
        ProgramInstance.INSTANCE_ID += 1
        self.program = [ instruction for instruction in program ]
        self.memory = []
        self.is_running = False
        self.instruction_ptr = 0
    
    def memory_insert(self, data):
        '''Inserts a value in the instance's memory, in first position.
        
        :param data: Value to insert.
        :type data: int
        '''
        self.memory = [ data ] + self.memory
        
    def check_running(self, phase):
        '''Checks if the instance is already running or if it should be
        initialized with its phase setting.
        
        :param phase: Phase setting for this instance.
        :type phase: int
        '''
        if not self.is_running:
            self.memory_insert(phase)
            self.is_running = True
        
    def run(self, instances):
        '''Runs the instance by executing its Intcode program either from
        scratch or from where it last stopped.
        
        :param instances: List of all program instances in the circuit.
        :type instances: list(ProgramInstance)
        '''
        # if we stopped just before halting, we simply terminate the program
        # and go to the next amplifier
        if self.instruction_ptr is None:
            next_amp = (self.id + 1) % len(instances)
            output = self.memory[-1]
            instances[next_amp].memory_insert(output)
            return next_amp
        # else we continue running the program from where we stopped
        while self.instruction_ptr is not None:
            self.instruction_ptr, pause = process_opcode(self.program,
                self.instruction_ptr, self.memory)
            # if we reached the halt op for the last amplifier
            if self.instruction_ptr is None and self.id == 4:
                return -1
            # else if we need to temporary pause the execution of this
            # amplifier
            if pause or self.instruction_ptr is None:
                next_amp = (self.id + 1) % len(instances)
                output = self.memory[-1]
                instances[next_amp].memory_insert(output)
                return next_amp
            # else if we errored
            if self.instruction_ptr == -1:
                return None

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
    if mode == 0: return inputs[data]
    else: return data

def process_opcode(inputs, instruction_ptr, memory):
    '''Process an opcode by using the provided inputs and the current operation
    index.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :param instruction_ptr: Current instruction pointer of the program instance.
    :type instruction_ptr: int
    :param memory: Current memory of the program instance.
    :type memory: list(int)
    '''
    instruction = str(inputs[instruction_ptr])
    code = int(instruction[-2:])
    if code == 99:
        return None, False

    op, n_inputs = OPERATIONS[code]
    modes = instruction[:-2]
    op_modes = [ int(m) for m in modes[::-1] ] + [ 0 ] * (n_inputs - len(modes))

    if code == 1 or code == 2: # add or multiply
        a, b, c = inputs[instruction_ptr+1:instruction_ptr+n_inputs+1]
        inputs[c] = op(
            get_value(inputs, a, op_modes[0]),
            get_value(inputs, b, op_modes[1]))
        return instruction_ptr + n_inputs + 1, False
    elif code == 3: # read input
        a = inputs[instruction_ptr+1]
        inputs[a] = memory.pop(0)
        return instruction_ptr + n_inputs + 1, False
    elif code == 4: # print output
        a = inputs[instruction_ptr+1]
        v = get_value(inputs, a, op_modes[0])
        memory.append(v)
        return instruction_ptr + n_inputs + 1, True
    elif code == 5: # jump-true
        a, b = inputs[instruction_ptr+1:instruction_ptr+n_inputs+1]
        if get_value(inputs, a, op_modes[0]) != 0:
            return get_value(inputs, b, op_modes[1]), False
        else:
            return instruction_ptr + n_inputs + 1, False
    elif code == 6: # jump-false
        a, b = inputs[instruction_ptr+1:instruction_ptr+n_inputs+1]
        if get_value(inputs, a, op_modes[0]) == 0:
            return get_value(inputs, b, op_modes[1]), False
        else:
            return instruction_ptr + n_inputs + 1, False
    elif code == 7 or code == 8: # less than or equal
        a, b, c = inputs[instruction_ptr+1:instruction_ptr+n_inputs+1]
        if op(get_value(inputs, a, op_modes[0]),
            get_value(inputs, b, op_modes[1])):
            inputs[c] = 1
        else:
            inputs[c] = 0
        return instruction_ptr + n_inputs + 1, False
    else:
        return -1, False

### Part I
def process_inputs(inputs):
    '''Executes the Intcode program on the provided inputs and computes the final
    result. Here, we use the [0, 4] phase settings range and no feedback loop
    (so we only go through the amplifiers chain once).
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    '''
    # prepare all possible permutations for phase settings:
    # we have X possibilities for the first one, X-1 for the second one,
    # X-2 for the third one... (no replacement)
    n_amplifiers = 5
    candidate_phase_settings = itertools.permutations(range(5), n_amplifiers)
    
    thrusts = []
    for phase_settings in candidate_phase_settings:
        ProgramInstance.INSTANCE_ID = 0 # reset global instances IDs
        amplifiers = [ ProgramInstance(inputs) for _ in range(n_amplifiers) ]
        amplifiers[0].memory_insert(0)
        for current_amplifier in range(n_amplifiers):
            phase = phase_settings[current_amplifier]
            amplifiers[current_amplifier].check_running(phase)
            # execute program
            amplifiers[current_amplifier].run(amplifiers)
        # remember the power sent to the thrusters
        output = amplifiers[current_amplifier].memory[-1]
        thrusts.append(output)
    return max(thrusts)

### Part II    
def process_inputs_feedback(inputs):
    '''Executes the Intcode program on the provided inputs and computes the final
    result. Here, we use the [5, 9] phase settings range and a feedback loop to
    pass through the amplifiers multiple times.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    '''
    # prepare all possible permutations for phase settings:
    # we have X possibilities for the first one, X-1 for the second one,
    # X-2 for the third one... (no replacement)
    n_amplifiers = 5
    candidate_phase_settings = itertools.permutations(range(5, 10), n_amplifiers)
    
    thrusts = []
    for phase_settings in candidate_phase_settings:
        ProgramInstance.INSTANCE_ID = 0 # reset global instances IDs
        amplifiers = [ ProgramInstance(inputs) for _ in range(n_amplifiers) ]
        amplifiers[0].memory_insert(0)
        current_amplifier = 0
        running = True
        while running:
            # if necessary, initialize amplifier
            phase = phase_settings[current_amplifier]
            amplifiers[current_amplifier].check_running(phase)
            # run amplifier (either from scratch or from where it last
            # stopped)
            next_amp = amplifiers[current_amplifier].run(amplifiers)
            # . if we errored somewhere
            if next_amp is None:
                return None
            # . else if amplifiers loop has halted
            elif next_amp == -1:
                running = False
            # . else reassign the current amplifier index for next iteration
            else:
                current_amplifier = next_amp
        # remember the power sent to the thrusters
        output = amplifiers[current_amplifier].memory[-1]
        thrusts.append(output)
    return max(thrusts)

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert process_inputs([
        3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0 ]) == 43210

    ### PART II
    assert process_inputs_feedback([ 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,
        26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5 ]) == 139629729
    assert process_inputs_feedback([ 3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,
        5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,
        1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10 ]) == 18216

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day7.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = process_inputs(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = process_inputs_feedback(inputs)
    print('PART II: solution = {}'.format(solution))
    

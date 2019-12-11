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
        self.program = { i: inst for i, inst in enumerate(program) }
        self.memory = []
        self.output = []
        self.modes = []
        self.instruction_ptr = 0
        self.is_running = False

        self._initial_program = { i: inst for i, inst in enumerate(program) }
    
    def reset(self):
        '''Resets the program instance in case you want to re-run the same
        program with a fresh start.'''
        self.instruction_ptr = 0
        self.output = []
        self.memory = []
        self.is_running = False
        self.program = { k: v for k, v in self._initial_program.items() }
    
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

    def program_get_data(self, index):
        '''Gets a value in the instance's program at a given position (if the
        position is out of range, returns 0).
        
        :param index: Position to get.
        :type index: int
        :return: Program data value.
        :rtype: int
        '''
        return self.program.get(index, 0)
        
    def program_set_data(self, index, data):
        '''Sets a value in the instance's program at a given position.
        
        :param index: Position to insert at.
        :type index: int
        :param data: Value to insert.
        :type data: int
        '''
        self.program[index] = data
                
    def run(self):
        '''Runs the instance by executing its Intcode program from start to
        finish (until it halts).'''
        # process while operation is not "halt"
        while self.instruction_ptr is not None:
            self.process_opcode()
            # abort if we errored
            if self.instruction_ptr == -1:
                return None
        
    def run_multiple(self, instances):
        '''Runs the instance by executing its Intcode program either from
        scratch or from where it last stopped, as part of a pool of instances
        that feed each other with output to input connection.
        
        :param instances: List of all program instances in the pool.
        :type instances: list(ProgramInstance)
        :return: Index of the next instance in the pool to run, if any.
        :rtype: int
        '''
        # if we stopped just before halting, we simply terminate the program
        # and go to the next instance
        if len(self.output) > 0 and self.instruction_ptr is None:
            next_instance = (self.id + 1) % len(instances)
            output = self.output[-1]
            instances[next_instance].memory_insert(output)
            return next_instance
        # else we continue running the program from where we stopped
        while self.instruction_ptr is not None:
            pause = self.process_opcode()
            # if we reached the halt op for the last instance
            if self.instruction_ptr is None and self.id == len(instances) - 1:
                return -1
            # else if we need to temporary pause the execution of this
            # instance
            if pause or self.instruction_ptr is None:
                next_instance = (self.id + 1) % len(instances)
                output = self.output[-1]
                instances[next_instance].memory_insert(output)
                return next_instance
            # else if we errored
            if self.instruction_ptr == -1:
                return None

    def get_index(self):
        '''Gets the index corresponding to the cell pointed by the current
        instruction pointer plus the current input (in "address" or "immediate
        value").
        
        :return: Index and mode of the next input.
        :rtype: tuple(int, int)
        '''
        # check if there are no more inputs for this instruction; if so: abort
        if len(self.modes) == 0:
            return None, None
        # extract the mode for this input
        mode = self.modes.pop(0)
        # process the index depending on the mode
        if mode == 0:
            val = self.program_get_data(self.instruction_ptr)
        else:
            val = self.instruction_ptr
        # increase the current instruction pointer
        self.instruction_ptr += 1
        return val, mode

    def get_value(self, keep_index=False):
        '''Gets the "address" or "immediate value" for a given set of inputs and
        data.
        
        :param keep_index: Whether or not the function should keep the index as
            is, or interpret it as an address in the program.
        :type keep_index: bool
        :return: Program data value.
        :rtype: int
        '''
        # get the index and mode
        idx, mode = self.get_index()
        if idx is None: return None
        # if necessary, apply the index as an address in the program code
        if not keep_index:
            val = self.program_get_data(idx)
        else:
            val = idx
        return val

    def process_opcode(self):
        '''Processes the next instruction in the program with the current memory
        and instruction pointer.
        
        :return: Whether or not the program should pause (if pause is activated).
        :rtype: bool
        '''
        # get the current instruction
        instruction = str(self.program[self.instruction_ptr])
        # extract the operation code (opcode) and check for halt or error
        opcode = int(instruction[-2:])
        if opcode == 99:
            self.instruction_ptr = None
            return False
        if opcode not in OPERATIONS:
            self.instruction_ptr = -1
            return False
        # get the information on this operation for further process
        op, n_inputs = OPERATIONS[opcode]
        m = instruction[:-2]
        self.modes = [ int(m) for m in m[::-1] ] + [ 0 ] * (n_inputs - len(m))
        # prepare the pause mode as False (could be modified by some operations)
        pause = False
        # execute the right operation depending on the opcode
        self.instruction_ptr += 1
        if opcode == 1 or opcode == 2: # add, multiply
            va = self.get_value()
            vb = self.get_value()
            vc = self.get_value(True)
            self.program_set_data(vc, op(va, vb))
        elif opcode == 3: # read
            if len(self.memory) == 0:
                return False
            va = self.get_value(True)
            vm = self.memory.pop(0)
            self.program_set_data(va, vm)
        elif opcode == 4: # write
            v = self.get_value()
            self.output.append(v)
            pause = True
        elif opcode == 5: # jump if true
            va = self.get_value()
            vb = self.get_value()
            if va != 0:
                self.instruction_ptr = vb
        elif opcode == 6: # jump if false
            va = self.get_value()
            vb = self.get_value()
            if va == 0:
                self.instruction_ptr = vb
        elif opcode == 7 or opcode == 8: # set if less than, set if equal
            va = self.get_value()
            vb = self.get_value()
            vc = self.get_value(True)
            if op(va, vb):
                self.program_set_data(vc, 1)
            else:
                self.program_set_data(vc, 0)
        else:
            pass
        
        return pause

### Part I
def process_inputs(inputs):
    '''Executes the Intcode program on the provided inputs and computes the final
    result. Here, we use the [0, 4] phase settings range and no feedback loop
    (so we only go through the amplifiers chain once).
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :return: Maximum input to the thrusters.
    :rtype: int
    '''
    # prepare all possible permutations for phase settings:
    # we have X possibilities for the first one, X-1 for the second one,
    # X-2 for the third one... (no replacement)
    n_amplifiers = 5
    candidate_phase_settings = itertools.permutations(range(5), n_amplifiers)
    thrusts = []
    
    ProgramInstance.INSTANCE_ID = 0 # reset global instances IDs
    amplifiers = [ ProgramInstance(inputs) for _ in range(n_amplifiers) ]    
    for phase_settings in candidate_phase_settings:
        # reset all amplifiers
        for amp in amplifiers:
            amp.reset()
        # prepare input for first amplifier
        amplifiers[0].memory_insert(0)
        for current_amplifier in range(n_amplifiers):
            phase = phase_settings[current_amplifier]
            amplifiers[current_amplifier].check_running(phase)
            # execute program
            amplifiers[current_amplifier].run_multiple(amplifiers)
        # remember the power sent to the thrusters with these settings
        output = amplifiers[current_amplifier].output[-1]
        thrusts.append(output)
    return max(thrusts)

### Part II    
def process_inputs_feedback(inputs):
    '''Executes the Intcode program on the provided inputs and computes the final
    result. Here, we use the [5, 9] phase settings range and a feedback loop to
    pass through the amplifiers multiple times.
    
    :param inputs: List of integers to execute as an Intcode program.
    :type inputs: list(int)
    :return: Maximum input to the thrusters.
    :rtype: int
    '''
    # prepare all possible permutations for phase settings:
    # we have X possibilities for the first one, X-1 for the second one,
    # X-2 for the third one... (no replacement)
    n_amplifiers = 5
    candidate_phase_settings = itertools.permutations(range(5, 10), n_amplifiers)
    thrusts = []
    
    ProgramInstance.INSTANCE_ID = 0 # reset global instances IDs
    amplifiers = [ ProgramInstance(inputs) for _ in range(n_amplifiers) ]    
    for phase_settings in candidate_phase_settings:
        # reset all amplifiers
        for amp in amplifiers:
            amp.reset()
        # prepare input for first amplifier
        amplifiers[0].memory_insert(0)
        current_amplifier = 0
        running = True
        while running:
            # if necessary, initialize amplifier
            phase = phase_settings[current_amplifier]
            amplifiers[current_amplifier].check_running(phase)
            # run amplifier (either from scratch or from where it last
            # stopped)
            next_amp = amplifiers[current_amplifier].run_multiple(amplifiers)
            # . if we errored somewhere
            if next_amp is None:
                return None
            # . else if amplifiers loop has halted
            elif next_amp == -1:
                running = False
            # . else reassign the current amplifier index for next iteration
            else:
                current_amplifier = next_amp
        # remember the power sent to the thrusters with these settings
        output = amplifiers[current_amplifier].output[-1]
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
    

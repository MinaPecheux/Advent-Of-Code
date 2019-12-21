### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 7: Amplification Circuit
### =============================================
import itertools

from intcode import IntcodeProgram

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
    
    IntcodeProgram.INSTANCE_ID = 0 # reset global instances IDs
    amplifiers = [ IntcodeProgram(inputs) for _ in range(n_amplifiers) ]    
    for phase_settings in candidate_phase_settings:
        # reset all amplifiers
        for amp in amplifiers:
            amp.reset()
        # prepare input for first amplifier
        amplifiers[0].push_memory(0)
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
    
    IntcodeProgram.INSTANCE_ID = 0 # reset global instances IDs
    amplifiers = [ IntcodeProgram(inputs) for _ in range(n_amplifiers) ]    
    for phase_settings in candidate_phase_settings:
        # reset all amplifiers
        for amp in amplifiers:
            amp.reset()
        # prepare input for first amplifier
        amplifiers[0].push_memory(0)
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
    

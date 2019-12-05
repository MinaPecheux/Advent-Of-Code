### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 4: Repose Record
### =============================================
import re
from collections import Counter

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    regex = r'\[(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2})\]\s(.+)'
    inputs = []
    for claim in data.split('\n'):
        if claim == '': continue
        matches = re.match(regex, claim)
        inputs.append(tuple([ int(matches.group(m)) for m in range(1, 6) ] + [ matches.group(6) ]))
    return inputs
    
# Action codes:
# 0 - falls asleep
# 1 - wakes up
def prepare_inputs(inputs):
    '''Prepares the inputs by sorting them in chronological order, isolating the
    guard ID and encoding the action.
    
    :param inputs: List of inputs to prepare.
    :type inputs: list(tuple(int))
    '''
    # sorted in chronological order
    inputs = sorted(inputs, key=lambda x: tuple(x[:-1]))
    # extract guard id and remove the now useless information (year, month,
    # day and hour)
    processed_inputs = []
    guard_id = -1
    for _, _, _, _, min, action in inputs:
        if 'shift' in action:
            guard_id = int(re.search(r'\#(\d+)', action).group(1))
        elif 'falls asleep' in action:
            processed_inputs.append((min, guard_id, 0))
        else:
            processed_inputs.append((min, guard_id, 1))
    return processed_inputs

# [ Computation functions ]
# -------------------------
### PART I
def strategy1(inputs):
    '''Applies the first strategy - computes which guard spends the longest time
    asleep and the minute he is asleep the most.
    
    :param claims: List of event inputs.
    :type claims: list(tuple(int))
    '''
    guards = {}
    time = -1
    for (min, guard_id, action) in inputs:
        if action == 0:
            time = min
        else:
            time_range = list(range(time, min))
            if guard_id in guards:
                guards[guard_id][0].extend(time_range)
                guards[guard_id][1] += min - time
            else:
                guards[guard_id] = [ time_range, min - time ]
    sortable_guards = [ (guard, r, t) for guard, [ r, t ] in guards.items() ]
    sortable_guards = sorted(sortable_guards, key=lambda x: x[2], reverse=True)
    most_asleep_guard = sortable_guards[0]
    asleep_min_counts = Counter(most_asleep_guard[1])
    most_asleep_min = asleep_min_counts.most_common()[0][0]
    return most_asleep_guard[0] * most_asleep_min
    
### PART II
def strategy2(inputs):
    '''Applies the second strategy - computes which guard is most frequently
    asleep on the same minute.
    
    :param claims: List of event inputs.
    :type claims: list(tuple(int))
    '''
    guards = {}
    time = -1
    for (min, guard_id, action) in inputs:
        if action == 0:
            time = min
        else:
            time_range = list(range(time, min))
            if guard_id in guards:
                guards[guard_id].extend(time_range)
            else:
                guards[guard_id] = time_range
    sortable_guards = [ (guard, Counter(r).most_common()[0]) \
        for guard, r in guards.items() ]
    sortable_guards = sorted(sortable_guards, key=lambda x: x[1][1], reverse=True)
    most_asleep_guard = sortable_guards[0]
    most_asleep_min = most_asleep_guard[1][0]
    return most_asleep_guard[0] * most_asleep_min
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert strategy1([ (5, 10, 0), (25, 10, 1), (30, 10, 0),
        (55, 10, 1), (40, 99, 0), (50, 99, 1), (24, 10, 0), (29, 10, 1),
        (36, 99, 0), (46, 99, 1), (45, 99, 0), (55, 99, 1) ]) == 240
    ### PART II
    assert strategy2([ (5, 10, 0), (25, 10, 1), (30, 10, 0),
        (55, 10, 1), (40, 99, 0), (50, 99, 1), (24, 10, 0), (29, 10, 1),
        (36, 99, 0), (46, 99, 1), (45, 99, 0), (55, 99, 1) ]) == 4455

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day4.txt'
    inputs = parse_input(open(data_path, 'r').read())
    inputs = prepare_inputs(inputs)

    ### PART I
    solution = strategy1(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = strategy2(inputs)
    print('PART II: solution = {}'.format(solution))

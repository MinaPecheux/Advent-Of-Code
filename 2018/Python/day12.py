### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 12: Subterranean Sustainability
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    lines = data.split('\n')
    initial_state = lines[0].replace('initial state: ', '')
    rules = {}
    for line in lines[2:]:
        if line == '': continue
        tmp = line.split(' => ')
        rules[tmp[0]] = tmp[1]
    return initial_state, rules

# [ Computation functions ]
# -------------------------
def display_pots(generations):
    '''Displays the evolution of the pots, generation per generation.
    
    :param generations: List of pots for each generation.
    :type generations: list(tuple(int, str))
    '''
    # compute the overall bounds of the generations to align the displays
    leftmost, rightmost = None, None
    for gen in generations:
        positions = [ pos for pos, _ in gen ]
        l, r = min(positions), max(positions)
        if leftmost is None or l < leftmost: leftmost = l
        if rightmost is None or r > rightmost: rightmost = r
    # iterate through the history to print each generation
    for i, gen in enumerate(generations):
        chars = [ d[1] for d in sorted(gen, key=lambda x: x[0]) ]
        positions = [ pos for pos, _ in gen ]
        l, r = min(positions), max(positions)
        if l >= leftmost:
            pad_start = '.' * abs(leftmost - l)
        else:
            pad_start = ''
            chars = chars[leftmost:]
        if r <= rightmost:
            pad_end = '.' * abs(rightmost - r)
        else:
            pad_end = ''
            chars = chars[:rightmost]
        print('[%2d]' % i, pad_start + ''.join(chars) + pad_end)    

def padding_buffers(rules):
    '''Computes the padding size that should be added to the state each
    generation to prepare the next one.
    
    :param rules: Evolution rules for the pots (i.e. patterns that impact
        whether or not their is a plant in the pot).
    :type rules: dict
    '''
    buffers = [ 0, 0 ]
    for rule, replacement in rules.items():
        if replacement == '#':
            l = len(rule)
            for i in range(l):
                if rule[i] == '#': break
                buffers[0] = max([ buffers[0], i+1 ])
            for i in range(l - 1, -1, -1):
                if rule[i] == '#': break
                buffers[1] = max([ buffers[1], l - i ])
    return buffers

def compute_pots_evolution(n_evolutions, initial_state, rules,
    display_progress=False, display_final=False):
    '''
    Computes the evolution of the pots for a given number of generation,
    starting from a given initial state.
    
    The algorithm speeds up the computation based on a specificity of the
    inputs: after a while, the pots state remains the same and simply shifts of
    one position each iteration (i.e. its the exact same pattern but one
    position further on the right).
    
    :param n_evolutions: Number of evolutions to compute.
    :type n_evolutions: int
    :param initial_state: Initial state for the pots (in the form of '.' and
        '#', starting from pot 0).
    :type initial_state: str
    :param rules: Evolution rules for the pots (i.e. patterns that impact
        whether or not their is a plant in the pot).
    :type rules: dict
    :param display_final: If true, then the final state is displayed.
    :type display_final: bool
    '''
    # prepare the state buffers depending on the evolution rules
    pad_start, pad_end = padding_buffers(rules)
    generations = [ [ (i, c) for i, c in enumerate(initial_state) ] ]
    # prepare previous patterns cache: it will hold the previously seen patterns
    # with their starting position
    prev_patterns = {}
    prev_patterns[initial_state] = 0
    # compute evolutions
    for n in range(n_evolutions):
        # . get back the old generation
        prev_generation = generations[n]
        # . compute the new generation
        new_generation = []
        for plant in prev_generation:
            pos, active = plant
            # .. get the pattern around the pot
            pattern = ''
            for p in range(pos-2, pos+3):
                a = '.'
                for prev in prev_generation:
                    if prev[0] == p:
                        a = prev[1]
                        break
                pattern += a
            # .. check if the pattern matches a rule
            new_active = rules[pattern] if pattern in rules else '.'
            # .. store the pot with its new state
            new_generation.append((pos, new_active))

        # . add the start and end paddings
        for i in range(1, pad_start + 1):
            first_pos = new_generation[0][0]
            new_generation.insert(0, (first_pos-1, '.'))
        for i in range(1, pad_end + 1):
            last_pos = new_generation[-1][0]
            new_generation.append((last_pos + 1, '.'))
        # . add the generation to the evolution list
        generations.append(new_generation)
        
        # . compute the pattern and store it in the cache with its position
        tmp = ''.join([ d[1] for d in new_generation ])
        full_pattern = tmp.strip('.')
        full_pattern_start = 0
        while tmp[full_pattern_start] != '#':
            full_pattern_start += 1
        full_pattern_start += min([ pos for pos, _ in new_generation ])
        
        # . if the pattern was already found, early-stop the loop!
        if full_pattern in prev_patterns:
            break
        prev_patterns[full_pattern] = full_pattern_start
        
    # if the computation was stopped early, infer the rest by simply adding
    # the offset the pots would have taken with the remaining iterations
    if n != n_evolutions - 1:
        for i, pot in enumerate(generations[-1]):
            pos, active = pot
            generations[-1][i] = (pos + (n_evolutions - n - 1), active)

    # finalize execution
    if display_final: display_pots(generations)
    return sum([ pos for pos, active in generations[-1] if active == '#' ])

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    initial_state, rules = ('#..#.#..##......###...###', {
        '...##': '#', '..#..': '#', '.#...': '#', '.#.#.': '#', '.#.##': '#',
        '.##..': '#', '.####': '#', '#.#.#': '#', '#.###': '#', '##.#.': '#',
        '##.##': '#', '###..': '#', '###.#': '#', '####.': '#'
    })
    assert compute_pots_evolution(20, initial_state, rules) == 325
        
if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    # get input data
    data_path = '../data/day12.txt'
    initial_state, rules = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = compute_pots_evolution(20, initial_state, rules)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = compute_pots_evolution(50000000000, initial_state, rules)
    print('PART II: solution = {}'.format(solution))

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    return [ int(x) for x in data.split('\n') if x != '' ]

# [ Computation functions ]
# -------------------------
### PART I
def compute_fuel(mass):
    '''Computes the required fuel for a module of given mass.
    
    :param mass: The mass of the module to compute the fuel consumption for.
    :type mass: int
    '''
    return (mass // 3) - 2

### PART II
def compute_total_fuel(mass):
    '''Computes the total required fuel for a module of given mass and the
    added fuel, and so on. It works recursively until the computed amount of
    fuel is zero or negative.
    
    :param mass: The mass of the module to compute the fuel consumption for.
    :type mass: int
    '''
    f = (mass // 3) - 2
    if f <= 0:
        return 0
    else:
        return f + compute_total_fuel(f)
    
# [ Base tests ]
# --------------
### PART I
assert compute_fuel(12) == 2
assert compute_fuel(14) == 2
assert compute_fuel(1969) == 654
assert compute_fuel(100756) == 33583

### PART II
assert compute_total_fuel(14) == 2
assert compute_total_fuel(1969) == 966
assert compute_total_fuel(100756) == 50346

if __name__ == '__main__':
    data_path = '../data/day1.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = sum([ compute_fuel(i) for i in inputs ])
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = sum([ compute_total_fuel(i) for i in inputs ])
    print('PART II: solution = {}'.format(solution))

### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 1: The Tyranny of the Rocket Equation
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: list(int)
    '''
    return [ int(x) for x in data.split('\n') if x != '' ]

# [ Computation functions ]
# -------------------------
### PART I
def compute_fuel(mass):
    '''Computes the required fuel for a module of given mass.
    
    :param mass: The mass of the module to compute the fuel consumption for.
    :type mass: int
    :return: Required amount of fuel.
    :rtype: int
    '''
    return (mass // 3) - 2

### PART II
def compute_total_fuel(mass):
    '''Computes the total required fuel for a module of given mass and the
    added fuel, and so on. It works recursively until the computed amount of
    fuel is zero or negative.
    
    :param mass: The mass of the module to compute the fuel consumption for.
    :type mass: int
    :return: Required amount of fuel.
    :rtype: int
    '''
    f = compute_fuel(mass)
    if f <= 0:
        return 0
    return f + compute_total_fuel(f)
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
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
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day1.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = sum([ compute_fuel(i) for i in inputs ])
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = sum([ compute_total_fuel(i) for i in inputs ])
    print('PART II: solution = {}'.format(solution))

### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 12: The N-Body Problem
### =============================================
import re
from itertools import combinations
                    
# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: list(tuple(int, int, int))
    '''
    reg = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'
    points = []
    for line in data.split('\n'):
        if line == '': continue
        match = re.match(reg, line)
        points.append((int(match.group(1)), int(match.group(2)),
            int(match.group(3))))
    return points

# [ Computation functions ]
# -------------------------
### Part I
def compute_total_energy(moon):
    '''Computes the total energy of a moon based on its current position and
    velocity.
    
    :param moon: Current position and velocity of the moon.
    :type moon: tuple(int, int, int, int, int, int)
    '''
    x, y, z, vx, vy, vz = moon
    potential_energy = abs(x) + abs(y) + abs(z)
    kinetic_energy = abs(vx) + abs(vy) + abs(vz)
    return potential_energy * kinetic_energy

def simulate_moons(moons, timesteps):
    '''Simulates the moons' movement over a given number of time steps and
    computes the final total energy of the entire system (i.e. the sum of the
    final total energies of each moon).
    
    :param moons: Initial positions of the moons to process.
    :type moons: list(tuple(int, int, int))
    :param timesteps: Number of time steps to simulate.
    :type timesteps: int
    :return: Total energy of the entire system at the end of the simulation.
    :rtype: int
    '''
    # prepare moons with their velocities
    moons = [ [ x, y, z, 0., 0., 0. ] for x, y, z in moons ]
    # prepare all the unique moon pairs
    moon_pairs = list(combinations(range(len(moons)), 2))

    for time in range(timesteps):
        # apply gravity
        for i1, i2 in moon_pairs:
            x1, y1, z1, vx1, vy1, vz1 = moons[i1]
            x2, y2, z2, vx2, vy2, vz2 = moons[i2]
            if x1 > x2:
                moons[i1][3] -= 1; moons[i2][3] += 1
            elif x1 < x2:
                moons[i1][3] += 1; moons[i2][3] -= 1
            if y1 > y2:
                moons[i1][4] -= 1; moons[i2][4] += 1
            elif y1 < y2:
                moons[i1][4] += 1; moons[i2][4] -= 1
            if z1 > z2:
                moons[i1][5] -= 1; moons[i2][5] += 1
            elif z1 < z2:
                moons[i1][5] += 1; moons[i2][5] -= 1
        # apply velocity
        for moon in moons:
            moon[0] += moon[3]
            moon[1] += moon[4]
            moon[2] += moon[5]

    return int(sum([ compute_total_energy(m) for m in moons ]))

### Part II
def GCD(x, y):
   '''Computes the greatest common divisor (GCD) of two numbers.
   
   :param x: First number to process.
   :type x: int
   :param y: Second number to process.
   :type y: int
   :return: GCD of the two numbers.
   :rtype: int
   '''
   while y:
       x, y = y, x % y
   return x
   
def LCM(x, y):
   '''Computes the least common multiple (LCM) of two numbers.
   
   :param x: First number to process.
   :type x: int
   :param y: Second number to process.
   :type y: int
   :return: LCM of the two numbers.
   :rtype: int
   '''
   lcm = (x * y) // GCD(x, y)
   return lcm

def find_first_repetition(moons):
    '''Simulates the moons' movement until they repeat a previous state.
    
    :param moons: Initial positions of the moons to process.
    :type moons: list(tuple(int, int, int))
    :return: Number of steps until the first repetition.
    :rtype: int
    '''
    # prepare moons with their velocities
    moons = [ [ x, y, z, 0., 0., 0. ] for x, y, z in moons ]
    # prepare all the unique moon pairs
    moon_pairs = list(combinations(range(len(moons)), 2))

    history_x, history_y, history_z = {}, {}, {}
    period_x, period_y, period_z = None, None, None
    time = 0
    while True:
        # apply gravity
        for i1, i2 in moon_pairs:
            x1, y1, z1, vx1, vy1, vz1 = moons[i1]
            x2, y2, z2, vx2, vy2, vz2 = moons[i2]
            if x1 > x2:
                moons[i1][3] -= 1; moons[i2][3] += 1
            elif x1 < x2:
                moons[i1][3] += 1; moons[i2][3] -= 1
            if y1 > y2:
                moons[i1][4] -= 1; moons[i2][4] += 1
            elif y1 < y2:
                moons[i1][4] += 1; moons[i2][4] -= 1
            if z1 > z2:
                moons[i1][5] -= 1; moons[i2][5] += 1
            elif z1 < z2:
                moons[i1][5] += 1; moons[i2][5] -= 1
        # apply velocity
        for moon in moons:
            moon[0] += moon[3]
            moon[1] += moon[4]
            moon[2] += moon[5]
        # hash state:
        # . hash each axis
        # . check the matching dict for a repetition
        # . store the hash with the current time for further checks
        state_x = hash(str([ (x, vx) for x, _, _, vx, _, _ in moons ]))
        if state_x in history_x:
            period_x = time - history_x[state_x]
        history_x[state_x] = time
        state_y = hash(str([ (y, vy) for _, y, _, _, vy, _ in moons ]))
        if state_y in history_y:
            period_y = time - history_y[state_y]
        history_y[state_y] = time
        state_z = hash(str([ (z, vz) for _, _, z, _, _, vz in moons ]))
        if state_z in history_z:
            period_z = time - history_z[state_z]
        history_z[state_z] = time
        if period_x is not None and period_y is not None and period_z is not None:
            break
        time += 1

    # find the total repetition period by getting the LCM of the three subperiods
    return LCM(LCM(period_x, period_y), LCM(period_y, period_z))

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert compute_total_energy((2, 1, -3, -3, -2, 1)) == 36
    assert compute_total_energy((1, -8, 0, -1, 1, 3)) == 45
    assert compute_total_energy((3, -6, 1, 3, 2, -3)) == 80
    assert compute_total_energy((2, 0, 4, 1, -1, -1)) == 18
    
    ### PART I
    assert simulate_moons([
        (-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)
    ], 10) == 179

    ### PART II
    assert find_first_repetition([
        (-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)
    ]) == 2772
    assert find_first_repetition([
        (-8, -10, 0), (5, 5, 10), (2, -7, 3), (9, -8, -3)
    ]) == 4686774924

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day12.txt'
    moons = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = simulate_moons(moons, 1000)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_first_repetition(moons)
    print('PART II: solution = {}'.format(solution))
    

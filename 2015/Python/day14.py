### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 14: Reindeer Olympics
### =============================================
import re

class Reindeer(object):
    
    '''Util class to represent a reindeer with a name, a speed, a fly time
    and a rest time.'''
    
    def __init__(self, name, speed, fly_time, rest_time):
        '''Initialization function for a new Reindeer.
        
        :param name: Name of the reindeer.
        :type name: str
        :param speed: Speed of the reindeer (in km/s).
        :type speed: int
        :param fly_time: Amount of seconds in a row the reindeer can fly.
        :type fly_time: int
        :param rest_time: Amount of seconds in a row the reindeer must rest.
        :type rest_time: int
        '''
        self.name = name
        self.speed = speed
        self.fly_time = fly_time
        self.rest_time = rest_time
        self.reset()
        
    def __str__(self):
        '''Specific string representation for a Reindeer.
        
        :return: Specific representation.
        :rtype: str
        '''
        state = 'fly' if self.is_flying else 'rest'
        out = '{} ({} pts): total dist = {}'.format(self.name, self.score,
            self.distance)
        out += ' - current state: "{}"'.format(state)
        return out
        
    def reset(self):
        '''Resets a Reindeer to its initial state (for a new race, for
        example.).'''
        self.is_flying = True
        self.time_before_switch = self.fly_time
        self.distance = 0
        self.score = 0
        
    def travel_one(self):
        '''Makes the Reindeer travel during one second.'''
        if self.time_before_switch == 0:
            self.is_flying = not self.is_flying
            self.time_before_switch = (
                self.fly_time
                if self.is_flying
                else self.rest_time
            )
            
        if self.is_flying:
            self.distance += self.speed
            
        self.time_before_switch -= 1
        
    def travel(self, n_seconds, reset=False):
        '''Makes the Reindeer travel during a given amount of seconds.
        
        :param n_seconds: Amount of seconds to travel for.
        :type n_seconds: int
        :param reset: Whether or not to first reset the Reindeer to its initial
            state.
        :type reset: bool
        :return: Total travelled distance.
        :rtype: int
        '''
        if reset:
            self.reset()
        for _ in range(n_seconds):
            self.travel_one()
        return self.distance

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of reindeers.
    :rtype: list(Reindeer)
    '''
    reg = r'(\w+)[^\d]*(\d+)[^\d]*(\d+)[^\d]*(\d+)'
    reindeers = []
    for line in data.strip().split('\n'):
        name, speed, fly_time, rest_time = re.search(reg, line).groups()
        reindeers.append(Reindeer(name, int(speed), int(fly_time),
            int(rest_time)))
    return reindeers

# [ Computation functions ]
# -------------------------
def best_reindeer_no_bonus(reindeers, n_seconds):
    '''Computes the distance each reindeer has travelled in a given number of
    seconds and finds out which one is the best by getting the highest travelled
    distance.
    
    :param reindeers: Dictionary of reindeers.
    :type reindeers: dict(str, tuple(int, int, int))
    :param n_seconds: Number of seconds to compute.
    :type n_seconds: int
    :return: Highest distance travelled by a reindeer.
    :rtype: int
    '''
    return max([ reindeer.travel(n_seconds) for reindeer in reindeers ])

def best_reindeer_with_bonus(reindeers, n_seconds):
    '''Computes the distance each reindeer has travelled in a given number of
    seconds and finds out which one is the best by awarding one point to the
    reindeer in the lead each second and finding the one that has the highest
    number of points in the end.
    
    :param reindeers: Dictionary of reindeers.
    :type reindeers: dict(str, tuple(int, int, int))
    :param n_seconds: Number of seconds to compute.
    :type n_seconds: int
    :return: Highest distance travelled by a reindeer.
    :rtype: int
    '''
    # (take reindeers back to their original state if need be)
    for r in reindeers:
        r.reset()
        
    for _ in range(n_seconds):
        for reindeer in reindeers:
            reindeer.travel_one()
        highest_distance = max(reindeers, key=lambda r: r.distance).distance
        for r in reindeers:
            if r.distance == highest_distance:
                r.score += 1
    return max(reindeers, key=lambda r: r.score).score

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    reindeers = parse_input(
    '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.''')
    ### Part I
    assert reindeers[0].travel(1, reset=True) == 14
    assert reindeers[0].travel(10, reset=True) == 140
    assert reindeers[0].travel(11, reset=True) == 140
    assert reindeers[0].travel(1000, reset=True) == 1120
    assert reindeers[1].travel(1, reset=True) == 16
    assert reindeers[1].travel(10, reset=True) == 160
    assert reindeers[1].travel(11, reset=True) == 176
    assert reindeers[1].travel(1000, reset=True) == 1056
    
    ### Part II
    assert best_reindeer_with_bonus(reindeers, 1000) == 689

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day14.txt'
    reindeers = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = best_reindeer_no_bonus(reindeers, 2503)
    print('PART I: solution = {}'.format(solution))
    
    ### PART I
    solution = best_reindeer_with_bonus(reindeers, 2503)
    print('PART II: solution = {}'.format(solution))
    
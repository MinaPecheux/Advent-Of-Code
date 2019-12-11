### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 10: Monitoring Station
### =============================================
from math import atan2, sqrt, radians, pi

class Map(object):
    
    '''Util class to represent the map of a field of asteroids.'''
    
    def __init__(self, data):
        '''initialization function for a new Map.
        
        :param data: Data to create the map.
        :type data: str
        '''
        self.parse_data(data)
        
    def parse_data(self, data):
        '''Parses the data to get the positions of each asteroids.
        
        :param data: Data to create the map.
        :type data: str
        '''
        self.asteroids = {}
        for y, line in enumerate(data.split('\n')):
            for x, char in enumerate(line):
                if char == '#':
                    self.asteroids[(x,y)] = set()
                    
    def compute_asteroid_sights(self, store_coords=False):
        '''Computes all the other asteroids each asteroid in the map can "see".
        If the coordinates are not stores, then the function will overlap
        asteroids in the same line of sight (same angle); else, each asteroid
        will be stored with its angle, its distance to the reference asteroid
        and its position.
        
        :param store_coords: Whether or not to store the coordinates of the
            other asteroids.
        :type store_coords: bool
        '''
        sights = {}
        for ast1 in self.asteroids:
            if store_coords:
                sights[ast1] = []
                for ast2 in self.asteroids:
                    # ignore same location
                    if ast1 == ast2:
                        continue
                    # else compute angle and distance, and add asteroid
                    a = angle(ast1, ast2)
                    d = dist(ast1, ast2)
                    sights[ast1].append((a, d, ast2))
            else:
                sights[ast1] = set()
                for ast2 in self.asteroids:
                    # ignore same location
                    if ast1 == ast2:
                        continue
                    # else compute angle and add asteroid to list
                    sights[ast1].add(angle(ast1, ast2))
        return sights
                    
# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: Map
    '''
    return Map(data.strip())

# [ Computation functions ]
# -------------------------
def dist(ast1, ast2):
    '''Computes the Euclidean distance between two 2D points.
    
    :param ast1: Coordinates of the first point.
    :type ast1: tuple(int, int)
    :param ast2: Coordinates of the second point.
    :type ast2: tuple(int, int)
    :return: Euclidean distance between the two 2D points.
    :rtype: float
    '''
    x1, y1 = ast1
    x2, y2 = ast2
    return sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
                    
def angle(ast1, ast2):
    '''Computes the angle between two 2D points using the atan2 and rotates the
    result by 90° counterclockwise.
    
    :param ast1: Coordinates of the first point.
    :type ast1: tuple(int, int)
    :param ast2: Coordinates of the second point.
    :type ast2: tuple(int, int)
    :return: Angle between the two 2D points.
    :rtype: float
    '''
    x1, y1 = ast1
    x2, y2 = ast2
    return (atan2(y1 - y2, x1 - x2) - radians(90)) % (pi*2.0)

### Part I
def find_best_asteroid(map):
    '''Finds the asteroid from which the station would see the greatest number
    of asteroids.
    
    :param map: Map of the asteroids in the neighborhood.
    :type map: Map
    :return: Coordinates and number of asteroids visible from the "best"
        asteroid.
    :rtype: tuple(tuple(int, int), int)
    '''
    # compute each asteroid sight (and overwrite the ones that are in the same
    # angle)
    sights = map.compute_asteroid_sights()
    # associate the number of visible asteroids to the asteroid position
    n_visible = [ (k, len(v)) for k, v in sights.items() ]
    # return the best one, i.e. the position that "sees" the most asteroids
    return sorted(n_visible, key=lambda x: x[1], reverse=True)[0]

### Part II
def process_laser_vaporization(map, station):
    '''Computes the whole laser vaporization process given some coordinates have
    been picked for the monitoring station.
    
    :param map: Map of the asteroids in the neighborhood.
    :type map: Map
    :param station: Coordinates of the monitoring station.
    :type station: tuple(int, int)
    :return: Checksum of the laser vaporization process.
    :rtype: int
    '''
    # compute each asteroid sight (keep track of asteroids angle, distance and
    # position)
    sights = map.compute_asteroid_sights(store_coords=True)[station]
    # sort the sights per angle, then per distance
    sorted_sights = sorted(sorted(sights, key=lambda x: x[1]), key=lambda x: x[0])
    # roll the laser until 200 asteroids have been destroyed
    i = 0
    last_angle = -1.0
    target_coords = None
    for i in range(200):
        idx = 0
        a = sorted_sights[idx][0]
        while a <= last_angle and idx < len(sorted_sights):
            a = sorted_sights[idx][0]
            if a <= last_angle:
                idx += 1
        a, d, p = sorted_sights.pop(idx)
        last_angle = a % (2.0*pi)
    # compute the checksum for the position of the 200th destroyed asteroid
    target_x, target_y = p
    return target_x * 100 + target_y

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    map = parse_input('''.#..#
.....
#####
....#
...##''')
    _, c = find_best_asteroid(map)
    assert c == 8
    map = parse_input('''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####''')
    _, c = find_best_asteroid(map)
    assert c == 33
    map = parse_input('''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.''')
    _, c = find_best_asteroid(map)
    assert c == 35
    map = parse_input('''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..''')
    _, c = find_best_asteroid(map)
    assert c == 41
    map = parse_input('''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##''')
    _, c = find_best_asteroid(map)
    assert c == 210

    ### Part II
    map = parse_input('''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##''')
    coords, _ = find_best_asteroid(map)
    assert process_laser_vaporization(map, coords) == 802

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day10.txt'
    map = parse_input(open(data_path, 'r').read())
    
    ### PART I
    station_coords, solution = find_best_asteroid(map)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = process_laser_vaporization(map, station_coords)
    print('PART II: solution = {}'.format(solution))
    

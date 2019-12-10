### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 3: Crossed Wires
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    return [ p.split(',') for p in data.split('\n') if p != '' ]

# [ Computation functions ]
# -------------------------
def manhattan_distance(x1, y1, x2, y2):
    '''Computes the Manhattan distance between two 2D points.
    
    :param x1: Horizontal coordinate of the first point.
    :type x1: int
    :param y1: Vertical coordinate of the first point.
    :type y1: int
    :param x2: Horizontal coordinate of the second point.
    :type x2: int
    :param y1: Vertical coordinate of the second point.
    :type y1: int
    '''
    return abs(x2 - x1) + abs(y2 - y1)
    
def find_path_points(path):
    '''Computes all the points a path goes through.
    
    :param path: Path to walk, as a list of moves to take (with a direction and
        an integer pace).
    :type path: list(str)
    '''
    cx = 0; cy = 0; d = 1
    points = {}
    for move in path:
        dir = move[0]
        pace = int(move[1:])
        if dir == 'R':
            for x in range(cx + 1, cx + pace + 1):
                points[(x,cy)] = d
                d += 1
            cx += pace
        elif dir == 'L':
            for x in range(cx - 1, cx - pace - 1, -1):
                points[(x,cy)] = d
                d += 1
            cx -= pace
        elif dir == 'U':
            for y in range(cy - 1, cy - pace - 1, -1):
                points[(cx,y)] = d
                d += 1
            cy -= pace
        elif dir == 'D':
            for y in range(cy + 1, cy + pace + 1):
                points[(cx,y)] = d
                d += 1
            cy += pace
    return points

### PART I
def find_closest_intersection_with_dist(paths):
    '''Finds the intersection of given paths that is closest to the central port,
    considering the Manhattan distance.
    
    :param paths: Paths to process.
    :type paths: list(list(str))
    '''
    # compute all activated points on the grid
    path_points = [ find_path_points(path) for path in paths ]
    # extract the intersections of all the paths
    intersections = set(path_points[0]).intersection(set(path_points[1]))
    print(intersections)
    # find the one closest to the central port (compute its Manhattan distance)
    dists = [ manhattan_distance(pos[0], pos[1], 0, 0) for pos in intersections ]
    return min(dists)

### PART II
def find_closest_intersection_with_steps(paths):
    '''Finds the intersection of given paths that is closest to the central port,
    considering the combined number of steps to the chosen intersection.
    
    :param paths: Paths to process.
    :type paths: list(list(str))
    '''
    # compute all activated points on the grid
    path_points = [ find_path_points(path) for path in paths ]
    # extract the intersections of all the paths
    intersections = set(path_points[0]).intersection(set(path_points[1]))
    # find the smallest sum of combined steps
    return min([ sum([ p[i] for p in path_points ]) for i in intersections ])

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert find_closest_intersection_with_dist([
        ['R8','U5','L5','D3'],
        ['U7','R6','D4','L4']
    ]) == 6
    assert find_closest_intersection_with_dist([
        ['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
        ['U62','R66','U55','R34','D71','R55','D58','R83']
    ]) == 159
    assert find_closest_intersection_with_dist([
        ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
        ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
    ]) == 135
    
    ### PART II
    assert find_closest_intersection_with_steps([
        ['R8','U5','L5','D3'],
        ['U7','R6','D4','L4']
    ]) == 30
    assert find_closest_intersection_with_steps([
        ['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
        ['U62','R66','U55','R34','D71','R55','D58','R83']
    ]) == 610
    assert find_closest_intersection_with_steps([
        ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
        ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
    ]) == 410

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day3.txt'
    inputs = parse_input(open(data_path, 'r').read())

    ### PART I
    solution = find_closest_intersection_with_dist(inputs)
    print('PART I: solution = {}'.format(solution))

    ### PART II
    solution = find_closest_intersection_with_steps(inputs)
    print('PART II: solution = {}'.format(solution))
    

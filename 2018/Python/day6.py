### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 6: Chronal Coordinates
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    inputs = []
    for line in data.split('\n'):
        if line == '': continue
        x, y = line.split(', ')
        inputs.append((int(x), int(y)))
    return inputs

# [ Computation functions ]
# -------------------------
### PART I
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

def find_largest_finite_area(markers):
    '''Finds the largest area between the given markers that is not infinite.
    
    :param markers: Positions of the marked spots.
    :type markers: list(tuple(int))
    '''
    x, y = zip(*markers)
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)
    grid = {}
    for xx in range(min_x, max_x+1):
        for yy in range(min_y, max_y+1):
            closest = None
            dist = None
            abort_point = False
            for i, marker in enumerate(markers):
                d = manhattan_distance(marker[0], marker[1], xx, yy)
                if dist is None or d < dist:
                    dist = d
                    closest = i
                    abort_point = False
                elif dist == d and closest != i:
                    abort_point = True
            if abort_point: continue
            if closest in grid: grid[closest].append((xx, yy))
            else: grid[closest] = [ (xx, yy) ]
    finite_areas = []
    for marker, points in grid.items():
        invalid_area = False
        pts = []
        for point in points:
            if (point[0] == min_x or point[0] == max_x) or \
                (point[1] == min_y or point[1] == max_y):
                invalid_area = True
                break
            pts.append(point)
        if not invalid_area:
            finite_areas.append((marker, len(pts)))
    sorted_areas = sorted(finite_areas, key=lambda x: x[1], reverse=True)
    return sorted_areas[0][1]

### Part II
def find_area_below_threshold(markers, threshold):
    '''Finds the size of the area containing all the points that have a total
    Manhattan distance to all markers combined below the given threshold.
    
    :param markers: Positions of the marked spots.
    :type markers: list(tuple(int))
    :param threshold: Maximum value for the sum of Manhattan distances to each
        marker for a point in the desired region.
    :type threshold: int
    '''
    x, y = zip(*markers)
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)
    area_size = 0
    for xx in range(min_x, max_x+1):
        for yy in range(min_y, max_y+1):
            dist = 0
            for i, marker in enumerate(markers):
                dist += manhattan_distance(marker[0], marker[1], xx, yy)
            if dist < threshold: area_size += 1
    return area_size
        
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    assert find_largest_finite_area([ (1, 1), (1, 6), (8, 3), (3, 4), (5, 5),
        (8, 9) ]) == 17
    ### PART II
    assert find_area_below_threshold([ (1, 1), (1, 6), (8, 3), (3, 4), (5, 5),
        (8, 9) ], 32) == 16

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day6.txt'
    inputs = parse_input(open(data_path, 'r').read())

    ### PART I
    solution = find_largest_finite_area(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_area_below_threshold(inputs, 10000)
    print('PART II: solution = {}'.format(solution))

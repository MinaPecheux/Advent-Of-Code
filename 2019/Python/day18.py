### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 18: Many-Worlds Interpretation
### =============================================
from queue import Queue

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: Map
    '''
    return Map(data)

# [ Computation functions ]
# -------------------------

class Map(object):
    
    '''Util class to represent the map of entrances, doors and keys.'''
    
    KEYS = 'abcdefghijklmnopqrstuvwxyz'
    
    def __init__(self, data):
        '''initialization function for a new Map.
        
        :param data: Provided problem data.
        :type data: str
        '''
        self.parse_data(data)
            
    def parse_data(self, data):
        '''Parses the incoming data into a map board and interesting points.
        
        :param data: Provided problem data.
        :type data: str
        '''
        self.board = {}
        self.start_positions = []
        entrance_id = 1
        for y, line in enumerate(data.split('\n')):
            for x, char in enumerate(line):
                if char == '.': # normal path
                    self.board[(x,y)] = 0
                elif char == '@': # start pos
                    self.board[(x,y)] = 0
                    self.start_positions.append((x, y))
                    entrance_id += 1
                elif 65 <= ord(char) <= 90: # door
                    self.board[(x,y)] = char
                elif 97 <= ord(char) <= 122: # key
                    self.board[(x,y)] = char

        self.compute_all_routes()

    def compute_routes(self, source):
        '''Computes all the routes on the map between a source and all other
        points of interest (entrances, doors, keys). It uses a BFS approach.
        
        :param source: Source of the routes.
        :type source: tuple(int, int)
        :return: All relevant routes in the board.
        :rtype: dict(dict)
        '''    
        sx, sy = source
        visited = set([ (sx, sy) ])
        queue = Queue()
        queue.put((source, 0, ''))
        routes = {}
        
        while not queue.empty():
            (x, y), dist, route = queue.get()
            data = self.board.get((x, y), None)
            if data is not None and isinstance(data, str) and dist > 0:
                routes[data] = (dist, route)
                route = route + data
            visited.add((x, y))
            
            for dir in [ (1,0), (0,1), (-1,0), (0,-1) ]:
                neighbor_x, neighbor_y = x + dir[0], y + dir[1]
                neighbor_data = self.board.get((neighbor_x, neighbor_y), None)
                if neighbor_data is not None \
                    and (neighbor_x, neighbor_y) not in visited:
                    queue.put(((neighbor_x, neighbor_y), dist + 1, route))
        return routes

    def compute_all_routes(self):
        '''Computes all the routes on the map between points of interest
        (entrances, doors, keys).'''    
        self.routes = {}
        # treat start positions (one or many depending on Part I or Part II)
        if len(self.start_positions) == 1:
            self.routes['@'] = self.compute_routes(self.start_positions[0])
        else:
            for i, pos in enumerate(self.start_positions):
                self.routes[i+1] = self.compute_routes(pos)
        # process the rest of the markers
        for (x, y), marker in self.board.items():
            if marker == 0:
                continue
            self.routes[marker] = self.compute_routes((x, y))

### Part I + II
def get_number_of_steps(map, n_agents=1):
    '''Finds the optimal way of collecting all the keys on the board to get a
    minimal number of moves.
    
    :param map: Map to process.
    :type map: Map
    :return: Optimal number of steps to get all the keys on the map.
    :rtype: int
    '''
    keys = set([ k for k in map.routes.keys() \
        if isinstance(k, str) and k in Map.KEYS ])
    
    n = len(keys)
    # keep current information as dict: (current pos, current keys) -> distance
    start = ('@',) if n_agents == 1 else tuple([ a+1 for a in range(n_agents) ])
    cur_info = { (start, frozenset()): 0 }
    for _ in range(n):
        new_info = {}
        for (cur_markers, cur_keys), cur_dist in cur_info.items():
            for key in keys:
                if key not in cur_keys:
                    for agent in range(n_agents):
                        if key in map.routes[cur_markers[agent]]:
                            dist, route = map.routes[cur_markers[agent]][key]
                            reachable = all( (c in cur_keys or c.lower() in cur_keys) \
                                for c in route )
                            if reachable:
                                new_dist = cur_dist + dist
                                new_keys = frozenset(cur_keys | set((key,)))
                                new_markers = list(cur_markers)
                                new_markers[agent] = key
                                new_markers = tuple(new_markers)
                                k = (new_markers, new_keys)
                                if k not in new_info or new_dist < new_info[k]:
                                    new_info[k] = new_dist
        cur_info = new_info
    return min(cur_info.values())
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    map = parse_input('''#########
#b.A.@.a#
#########''')
    assert get_number_of_steps(map) == 8
    map = parse_input('''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################''')
    assert get_number_of_steps(map) == 86
    map = parse_input('''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################''')
    assert get_number_of_steps(map) == 132
    map = parse_input('''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################''')
    assert get_number_of_steps(map) == 136
    map = parse_input('''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################''')
    assert get_number_of_steps(map) == 81
    
if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    ### PART I
    # get input data
    data_path = '../data/day18.txt'
    data = open(data_path, 'r').read()
    map = parse_input(data)
    # solve
    solution = get_number_of_steps(map)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    # get input data
    data_path = '../data/day18_2.txt'
    data = open(data_path, 'r').read()
    map = parse_input(data)
    # solve
    solution = get_number_of_steps(map, n_agents=4)
    print('PART II: solution = {}'.format(solution))
    

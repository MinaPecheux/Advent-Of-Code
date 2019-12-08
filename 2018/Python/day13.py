### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 13: Mine Cart Madness
### =============================================

class ShellColors(object):
    
    '''Enumeration of ANSI codes for shell special formatting.'''
    
    HEADER = '\033[95m'
    BLUE = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Cart(object):
    
    '''Class to represent a cart in the mine (with a current position and
    direction).'''
    
    DIRECTIONS = {
        'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)
    }
    DISPLAYS = { 'up': '^', 'down': 'v', 'left': '<', 'right': '>' }
    
    def __init__(self, x, y, dir):
        '''Initialization function for a new Cart.
        
        :param x: Initial horizontal coordinate.
        :type x: int
        :param y: Initial vertical coordinate.
        :type y: int
        :param dir: Initial direction.
        :type dir: str
        '''
        self.x = x
        self.y = y
        self.dir = dir
        self.crossing = 0
        
    def __str__(self):
        '''Special string formatting for a Cart: automatically finds the right
        display given the current direction and adds some red color for shell
        output (with ANSI codes).'''
        disp = Cart.DISPLAYS[self.dir]
        return ShellColors.RED + ShellColors.BOLD + disp + ShellColors.ENDC
        
    def move(self, mine):
        '''Moves the Cart in the mine given its current position and direction.
        
        :param mine: Mine map to move the Cart on.
        :type mine: Mine
        '''
        mx, my = Cart.DIRECTIONS[self.dir]
        self.x += mx
        self.y += my
        tile = mine.get(self.x, self.y)
        if tile == 2:
            if self.dir == 'up' or self.dir == 'down':
                self.turn_right()
            else:
                self.turn_left()
        elif tile == 3:
            if self.dir == 'up' or self.dir == 'down':
                self.turn_left()
            else:
                self.turn_right()
        elif tile == 4:
            self.cross_intersection()
            
    def turn_right(self):
        '''Turns the Cart to the right (modifies its current direction).'''
        if self.dir == 'up':
            self.dir = 'right'
        elif self.dir == 'right':
            self.dir = 'down'
        elif self.dir == 'down':
            self.dir = 'left'
        elif self.dir == 'left':
            self.dir = 'up'
            
    def turn_left(self):
        '''Turns the Cart to the left (modifies its current direction).'''
        if self.dir == 'up':
            self.dir = 'left'
        elif self.dir == 'right':
            self.dir = 'up'
        elif self.dir == 'down':
            self.dir = 'right'
        elif self.dir == 'left':
            self.dir = 'down'
            
    def cross_intersection(self):
        '''Makes the Cart cross an intersection (it might modify its current
        direction according to the given cycling algorithm).'''
        if self.crossing == 0:
            self.turn_left()
        elif self.crossing == 1:
            pass
        elif self.crossing == 2:
            self.turn_right()
        self.crossing = (self.crossing + 1) % 3

class Mine(object):
    
    '''Class to represent the mine map (ensemble of tiles and carts).'''
    
    # dict to convert string tiles to int codes
    TILE_MAP = { '|': 0, '-': 1, '/': 2, '\\': 3, '+': 4, ' ': 99 }
    # dict to convert int codes to string tiles
    TILE_REVERSE_MAP = { 0: '|', 1: '-', 2: '/', 3: '\\', 4: '+', 99: ' ' }
    
    def __init__(self, data):
        '''Initialization function for a new Mine object.
        
        :param data: Input data as lines of characters that represent the
            initial state of the mine.
        :type data: list(str)
        '''
        self.parse_data(data)
        
    def parse_data(self, data):
        '''Parses the given data into a map of tiles and carts.
        
        :param data: Input data as data of characters that represent the
            initial state of the mine.
        :type data: list(str)
        '''
        self.width, self.height = len(data[0]), len(data)
        self.tiles = {}
        self.carts = []
        for y in range(self.height):
            for x in range(self.width):
                try:
                    tile_str = data[y][x]
                except IndexError:
                    tile_str = ' '
                if tile_str in Mine.TILE_MAP:
                    tile_type = Mine.TILE_MAP[tile_str]
                else:
                    if tile_str == '^':
                        self.carts.append(Cart(x, y, 'up'))
                        tile_type = Mine.TILE_MAP['|']
                    elif tile_str == 'v':
                        self.carts.append(Cart(x, y, 'down'))
                        tile_type = Mine.TILE_MAP['|']
                    elif tile_str == '<':
                        self.carts.append(Cart(x, y, 'left'))
                        tile_type = Mine.TILE_MAP['-']
                    elif tile_str == '>':
                        self.carts.append(Cart(x, y, 'right'))
                        tile_type = Mine.TILE_MAP['-']
                self.tiles['{},{}'.format(x, y)] = tile_type

    def get(self, x, y):
        '''Gets the int code of a tile on the Map (at some given (x,y)
        coordinates).
        
        :param x: Horizontal coordinate of the tile.
        :type x: int
        :param y: Vertical coordinate of the tile.
        :type y: int
        '''
        return self.tiles['{},{}'.format(x, y)]
        
    def get_last_cart(self):
        '''Gets the position of the last Cart in the list of carts on the Map
        (i.e. after all crashes, when there is only one Cart remaining).'''
        cart = self.carts[0]
        return (cart.x, cart.y)
        
    def tick(self):
        '''Performs a tick on the Map to move the carts and check for crashes.'''
        # sort carts based on their position
        sorted_carts = sorted(self.carts, key=lambda cart: (cart.y, cart.x))
        # move all the sorted carts and check for crashes (to remove carts if
        # need be before processing the rest)
        crashed = []
        for cart in sorted_carts:
            cart.move(self)
            crash = self.test_crash()
            if crash is not None: crashed.append(crash)
        return crashed if len(crashed) > 0 else None
            
    def display(self):
        '''Displays the Map (with its tiles and carts).'''
        cart_positions = [ (cart.x, cart.y) for cart in self.carts ]
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                tile = Mine.TILE_REVERSE_MAP[self.get(x, y)]
                for cart in self.carts:
                    if cart.x == x and cart.y == y:
                        tile = str(cart)
                row += tile
            print(row)

    def test_crash(self):
        '''Tests for crashes between two carts on the current Map (i.e. checks
        whether two carts have the exact same position on the Map).'''
        cart_positions = [ (i, cart.x, cart.y) for i, cart in enumerate(self.carts) ]
        removed_carts = set()
        crash = None
        for i1, x1, y1 in cart_positions:
            for i2, x2, y2 in cart_positions:
                if i1 == i2: continue
                if x1 == x2 and y1 == y2:
                    crash = (x1, y1)
                    removed_carts.add(i1)
                    removed_carts.add(i2)
                    break
        self.carts = [ cart for i, cart in enumerate(self.carts) \
            if i not in removed_carts ]
        return crash
        
    def update(self, display=True):
        '''Updates the Map: performs a tick, optionally displays the Map in its
        current state, and returns crashes (if any) and the number of remaining
        carts.
        
        :param display: If true, the Map is displayed at the end of the tick.
        :type display: bool
        '''
        crash = self.tick()
        if display:
            self.display()
        return crash, len(self.carts)

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    lines = data.strip('\n').split('\n')
    return Mine(lines)

# [ Computation functions ]
# -------------------------
### Part I
def predict_first_crash(mine, display=False):
    '''Predicts the (x, y) position of the first carts crash on the given mine
    map.
    
    :param mine: Mine map to process.
    :type mine: Mine
    :param display: If true, the map is displayed at the end of each tick.
    :type display: bool
    '''
    crash = None
    while crash is None:
        crash, _ = mine.update(display=display)
    return crash[0]
    
### Part II
def find_last_cart(mine, display=False):
    '''Finds the position of the cart that will be the last one remaining after
    all possible crashes have occurred.
    
    :param mine: Mine map to process.
    :type mine: Mine
    :param display: If true, the map is displayed at the end of each tick.
    :type display: bool
    '''
    n_carts = None
    i = 0
    while n_carts is None or n_carts > 1:
        _, n_carts = mine.update(display=display)
    return mine.get_last_cart()

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    data = '''/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/   '''
    mine = parse_input(data)
    assert predict_first_crash(mine) == (7, 3)

    ### Part II
    data2 = '''/>-<\\  
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/'''
    mine = parse_input(data2)
    assert find_last_cart(mine) == (6, 4)
        
if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    # get input data
    data_path = '../data/day13.txt'
    data = open(data_path, 'r').read()
    
    ### PART I
    mine = parse_input(data)
    solution = predict_first_crash(mine)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    mine = parse_input(data)
    solution = find_last_cart(mine)
    print('PART II: solution = {}'.format(solution))

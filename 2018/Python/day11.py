### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 11: Chronal Charge
### =============================================
import numpy as np
from scipy.signal import convolve2d
from tqdm import tqdm

# [ Computation functions ]
# -------------------------
GRID_W, GRID_H = 300, 300

def cell_power(grid_serial_number):
    def _cell_power(data):
        '''Computes the power of a cell with the given algorithm.
        
        :param grid_serial_number: Serial number for the grid (problem input).
        :type grid_serial_number: int
        :param data: Coordinte of the cell in the 'x,y' string format.
        :type data: str
        '''
        x, y = data.split(',')
        x = int(x)
        y = int(y)
        rack_id = x + 10
        power = rack_id * y
        power += grid_serial_number
        power *= rack_id
        if power < 100:
            power = 0
        else:
            power = int(str(power)[-3])
        return power - 5
    return _cell_power
    
### Part I
def compute_best_square_3x3(grid_serial_number):
    '''Computes the top-left coordinates of the 3x3 square that has the highest
    cell power sum value.
    
    :param grid_serial_number: Serial number for the grid (problem input).
    :type grid_serial_number: int
    '''
    # make a GRID_W x GRID_H grid where each cell contains its coordinates in
    # 'x,y' string format
    coords = [ '{},{}'.format(x+1, y+1) for x in range(GRID_W) \
        for y in range(GRID_H) ]
    grid = np.array(coords)
    # compute the corresponding power grid by computing the cell power value
    # for each cell (vectorizing speeds up the process)
    power_grid = np.vectorize(cell_power(grid_serial_number))(grid)
    # reshape and convolve the power grid with a 3x3 kernel
    power_grid = power_grid.reshape((GRID_W, GRID_H))
    summed_grid = convolve2d(power_grid, np.ones((3, 3)), 'same')
    # extract the position of the best (i.e. maximal) value
    best_square_coord = np.unravel_index(np.argmax(summed_grid), (GRID_W, GRID_H))
    return best_square_coord
    
### Part II
def compute_auxiliary_matrix(grid):
    '''Computes the auxiliary matrix of the given grid that contains the
    cumulative sums (i.e. aux[i][j] contains the sum of all cells of the initial
    grid values from (0,0) to (i,j)).
    
    :param grid: Initial grid values.
    :type grid: np.ndarray
    '''
    aux = grid.copy()
    aux = np.cumsum(aux, axis=0)
    aux = np.cumsum(aux, axis=1)
    return aux
    
def get_sum_square(aux, coord, size):
    '''Computes the total sum of cells in the rectangle that has its top-left
    corner at the given coordinates, of given size (using the previously
    computed auxiliary matrix).
    
    :param aux: Previously computed auxiliary matrix.
    :type aux: np.ndarray
    :param coord: Top-left coordinates of the rectangle to sum.
    :type coord: tuple(int, int)
    :param size: Width and height of the rectangle to sum.
    :type size: tuple(int, int)
    '''
    tli, tlj = coord
    rbi, rbj = coord[0] + size[0], coord[1] + size[1]
    res = aux[rbi][rbj]
    if tli > 0:
        res -= aux[tli-1][rbj]
    if tlj > 0:
        res -= aux[rbi][tlj-1]
    if tli > 0 and tlj > 0:
        res += aux[tli-1][tlj-1]
    return res
    
def compute_best_square_nxn(grid_serial_number, display_progress=True):
    '''Computes the top-left coordinates and the size of the NxN square that has
    the highest cell power sum value. This algorithm takes the problem as a
    submatrix sum queries problem.
    
    :param grid_serial_number: Serial number for the grid (problem input).
    :type grid_serial_number: int
    :param display_progress: If true, then progress bar are shown during the
        computation (using the tqdm module).
    :type display_progress: bool
    '''
    # make a GRID_W x GRID_H grid where each cell contains its coordinates in
    # 'x,y' string format
    coords = [ '{},{}'.format(x+1, y+1) for x in range(GRID_W) \
        for y in range(GRID_H) ]
    grid = np.array(coords)
    # compute the corresponding power grid by computing the cell power value
    # for each cell (vectorizing speeds up the process)
    power_grid = np.vectorize(cell_power(grid_serial_number))(grid)
    # reshape the power grid and compute its auxiliary matrix to speed up sums
    # afterwards
    power_grid = power_grid.reshape((GRID_W, GRID_H))
    aux_grid = compute_auxiliary_matrix(power_grid)
    # for each possible size, get the sum square and look for the maximal value
    # (and its corresponding coordinates)
    best_square_value, best_square_coord = -1, None
    iterator = range(300)
    if display_progress:
        iterator = tqdm(iterator, total=300)
    for size in iterator:
        for x in range(0, GRID_W-size):
            for y in range(0, GRID_H-size):
                v = get_sum_square(aux_grid, (x, y), (size, size))
                if v > best_square_value:
                    best_square_value = v
                    best_square_coord = (x+1, y+1, size+1)
    return best_square_coord

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert cell_power(8)('3,5') == 4
    assert cell_power(57)('122,79') == -5
    assert cell_power(39)('217,196') == 0
    assert cell_power(71)('101,153') == 4
    
    ### Part I
    assert compute_best_square_3x3(18) == (33, 45)
    assert compute_best_square_3x3(42) == (21, 61)

    ### Part II
    assert compute_best_square_nxn(18, True) == (90, 269, 16)
    assert compute_best_square_nxn(42, True) == (232, 251, 12)
        
if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    ### PART I
    solution = compute_best_square_3x3(1308)
    print('PART I: solution = {}'.format(solution))

    ### PART II
    solution = compute_best_square_nxn(1308)
    print('PART II: solution = {}'.format(solution))

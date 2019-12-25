### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 2: I Was Told There Would Be No Math
### =============================================

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of boxes to wrap.
    :rtype: list(tuple(int, int, int))
    '''
    boxes = []
    for line in data.strip().split('\n'):
        l, w, h = line.split('x')
        boxes.append((int(l), int(w), int(h)))
    return boxes

# [ Computation functions ]
# -------------------------
def box_surface(box):
    '''Computes the total surface of the box.
    
    :param box: Box to compute the surface for.
    :type box: tuple(int, int, int)
    :return: Box surface.
    :rtype: int
    '''
    l, w, h = box
    return 2*l*w + 2*w*h + 2*h*l
    
def smallest_surface(box):
    '''Computes the smallest surface of the box.
    
    :param box: Box to compute the surface for.
    :type box: tuple(int, int, int)
    :return: Box smallest surface.
    :rtype: int
    '''
    l, w, h = box
    return min([ l*w, w*h, h*l ])
    
def box_smallest_perimeter(box):
    '''Computes the smallest perimeter of the box.
    
    :param box: Box to compute the perimeter for.
    :type box: tuple(int, int, int)
    :return: Box smallest perimeter.
    :rtype: int
    '''
    l, w, h = box
    return min([ 2*l+2*w, 2*w+2*h, 2*h+2*l ])
    
def box_volume(box):
    '''Computes the volume of the box.
    
    :param box: Box to compute the volume for.
    :type box: tuple(int, int, int)
    :return: Box volume.
    :rtype: int
    '''
    l, w, h = box
    return l*w*h

### PART I
def total_wrapping_paper(boxes):
    '''Computes the total amount of wrapping paper that is required to wrap all
    of the boxes.
    
    :param boxes: List of boxes to wrap.
    :type boxes: list(tuple(int, int, int))
    :return: Total amount of wrapping paper.
    :rtype: int
    '''
    return sum([ box_surface(b) + smallest_surface(b) for b in boxes ])
    
### PART II
def total_ribbon(boxes):
    '''Computes the total amount of ribbon that is required to wrap all of the
    boxes.
    
    :param boxes: List of boxes to wrap.
    :type boxes: list(tuple(int, int, int))
    :return: Total amount of ribbon.
    :rtype: int
    '''
    return sum([ box_smallest_perimeter(b) + box_volume(b) for b in boxes ])
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert box_surface(( 2, 3, 4 )) == 52
    assert box_surface(( 1, 1, 10 )) == 42
    assert smallest_surface(( 2, 3, 4 )) == 6
    assert smallest_surface(( 1, 1, 10 )) == 1
    assert box_smallest_perimeter(( 2, 3, 4 )) == 10
    assert box_smallest_perimeter(( 1, 1, 10 )) == 4
    assert box_volume(( 2, 3, 4 )) == 24
    assert box_volume(( 1, 1, 10 )) == 10
    ### PART I
    assert total_wrapping_paper([ ( 2, 3, 4 ), ( 1, 1, 10 ) ]) == 101
    ### PART II
    assert total_ribbon([ ( 2, 3, 4 ), ( 1, 1, 10 ) ]) == 48

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day2.txt'
    boxes = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = total_wrapping_paper(boxes)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = total_ribbon(boxes)
    print('PART II: solution = {}'.format(solution))

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
    l, w, h = box
    return 2*l*w + 2*w*h + 2*h*l
    
def smallest_surface(box):
    l, w, h = box
    return min([ l*w, w*h, h*l ])
    
def ribbon_amount(box):
    l, w, h = box
    return min([ 2*l+2*w, 2*w+2*h, 2*h+2*l ])
    
def bow_amount(box):
    l, w, h = box
    return l*w*h

### PART I
def total_wrapping_paper(boxes):
    '''Computes the total amount of wrapping paper that is required to wrap all
    of the boxes.
    
    :param boxes: List of boxes to wrap.
    :type boxes: list(tuple(int, int, int))
    '''
    return sum([ box_surface(b) + smallest_surface(b) for b in boxes ])
    
### PART II
def total_ribbon(boxes):
    '''Computes the total amount of ribbon that is required to wrap all of the
    boxes.
    
    :param boxes: List of boxes to wrap.
    :type boxes: list(tuple(int, int, int))
    '''
    return sum([ ribbon_amount(b) + bow_amount(b) for b in boxes ])
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert box_surface(( 2, 3, 4 )) == 52
    assert box_surface(( 1, 1, 10 )) == 42
    assert smallest_surface(( 2, 3, 4 )) == 6
    assert smallest_surface(( 1, 1, 10 )) == 1
    assert ribbon_amount(( 2, 3, 4 )) == 10
    assert ribbon_amount(( 1, 1, 10 )) == 4
    assert bow_amount(( 2, 3, 4 )) == 24
    assert bow_amount(( 1, 1, 10 )) == 10
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

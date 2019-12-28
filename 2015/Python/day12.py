### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 12: JSAbacusFramework.io
### =============================================
import re
import json

# [ Computation functions ]
# -------------------------
NUMBERS_REGEX = r'(-?\d+)'
def get_numbers_sum(input):
    '''Gets the sum of all the numbers in the text input.
    
    :param input: Text to analyze.
    :type input: str
    :return: Sum of all the numbers.
    :rtype: int
    '''
    numbers = re.findall(NUMBERS_REGEX, input)
    return sum([ int(x) for x in numbers ])

def ignore_reds(obj):
    '''Removes all the (sub)objects in the JSON data that contain the value
    "red". It works recursively by checking the type of value and getting rid of
    the items that match this criterion.
    
    :param obj: JSON data to transform.
    :type obj: dict or list
    :return: Transformed data.
    :rtype: dict or list
    '''
    if isinstance(obj, dict):
        if 'red' in obj.values():
            return None
        new_obj = {}
        for k, v in obj.items():
            val = ignore_reds(v)
            if val is not None:
                new_obj[k] = val
        return new_obj
    elif isinstance(obj, list):
        new_list = []
        for item in obj:
            v = ignore_reds(item)
            if v is not None:
                new_list.append(v)
        return new_list
    else:
        return obj

def get_sum_no_reds(input):
    '''Gets the sum of all the numbers in the text input after the (sub)objects
    containing the value "red" have been removed.
    
    :param input: Text to analyze.
    :type input: str
    :return: Sum of all the numbers.
    :rtype: int
    '''
    # turn to object
    content = json.loads(input)
    # remove all content that has 'red' in it (recursively)
    content = ignore_reds(content)
    # reconvert back to text and get sum
    return get_numbers_sum(json.dumps(content))

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    assert get_numbers_sum('[1,2,3]') == 6
    assert get_numbers_sum('{"a":2,"b":4}') == 6
    assert get_numbers_sum('[[[3]]]') == 3
    assert get_numbers_sum('{"a":{"b":4},"c":-1}') == 3
    assert get_numbers_sum('{"a":[-1,1]}') == 0
    assert get_numbers_sum('[-1,{"a":1}]') == 0
    assert get_numbers_sum('[]') == 0
    assert get_numbers_sum('{}') == 0
    
    ### Part II
    assert get_sum_no_reds('[1,2,3]') == 6
    assert get_sum_no_reds('[1,{"c":"red","b":2},3]') == 4
    assert get_sum_no_reds('{"d":"red","e":[1,2,3,4],"f":5}') == 0
    assert get_sum_no_reds('[1,"red",5]') == 6

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day12.txt'
    input = open(data_path, 'r').read()
    
    ### PART I
    solution = get_numbers_sum(input)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = get_sum_no_reds(input)
    print('PART II: solution = {}'.format(solution))

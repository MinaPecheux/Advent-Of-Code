### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 16: Aunt Sue
### =============================================
import re

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: All the information on the 'Sue' aunts.
    :rtype: dict(int, dict(str, int))
    '''
    aunts = {}
    reg = r'Sue (\d+): (.*)'
    for line in data.strip().split('\n'):
        number, info = re.search(reg, line).groups()
        number = int(number)
        info = info.split(', ')
        data = {}
        for i in info:
            k, v = i.split(': ')
            data[k] = int(v)
        aunts[number] = data
    return aunts

# [ Computation functions ]
# -------------------------
GREATER_THAN_KEYS = [ 'cats', 'trees' ]
FEWER_THAN_KEYS = [ 'pomeranians', 'goldfish' ]
def aunt_matches_info(aunt, info, with_ranges):
    '''Checks if the aunt info match the reference information. We can only
    check the keys that are provided (and ignore the rest). If there are
    ranges, we check for specific inequalities. Else, we check for equalities.
    
    :param aunt: Info on the aunt to check.
    :type aunt: dict(str, int)
    :param info: Reference info to use.
    :type info: dict(str, int)
    :param with_ranges: Whether or not the given ints or exact values or ranges
        (more/fewer depending on the key).
    :type with_ranges: bool
    :return: Whether or not this aunt matches the criteria.
    :rtype: bool
    '''
    if not with_ranges:
        for k, v in aunt.items():
            if info[k] != v:
                return False
    else:
        for k, v in aunt.items():
            if k in GREATER_THAN_KEYS:
                if info[k] > v:
                    return False
            elif k in FEWER_THAN_KEYS:
                if info[k] < v:
                    return False
            elif info[k] != v:
                return False            
    return True

def find_matching_ids(aunts, info, with_ranges):
    '''Finds out which aunt sent out the present by comparing the available info
    on all the aunts and the info on the one that sent the present.
    
    :param aunts: All the information on the 'Sue' aunts.
    :type aunts: dict(int, dict(str, int))
    :param info: Info on the gift sender.
    :type info: dict(str, int)
    :param with_ranges: Whether or not the given ints or exact values or ranges
        (more/fewer depending on the key).
    :type with_ranges: bool
    :return: Number of the aunt that sent the present.
    :rtype: int
    '''
    matches = { k: v for k, v in aunts.items() \
        if aunt_matches_info(v, info, with_ranges) }
    return list(matches.keys())

if __name__ == '__main__':
    # get input data
    data_path = '../data/day16.txt'
    aunts = parse_input(open(data_path, 'r').read())
    aunt_info = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }
    
    ### PART I
    solution = find_matching_ids(aunts, aunt_info, False)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = find_matching_ids(aunts, aunt_info, True)
    print('PART II: solution = {}'.format(solution))
    
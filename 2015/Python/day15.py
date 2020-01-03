### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 15: Science for Hungry People
### =============================================
import re

import numpy as np
from tqdm import tqdm

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: All available ingredients.
    :rtype: dict(str, dict(str, int))
    '''
    ingredients = {}
    reg = r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)'
    for line in data.strip().split('\n'):
        name, capacity, durability, flavor, texture, calories = re.search(reg,
            line).groups()
        ingredients[name] = [ int(capacity), int(durability), int(flavor),
            int(texture), int(calories) ]
    return ingredients

# [ Computation functions ]
# -------------------------
def compute_recipe_value(proportions, ref_amounts, check_calories=None):
    '''Computes the best recipe, i.e. the mix of ingredients that gives the
    highest cookie value, and returns its value.
    
    :param proportions: Amount of ingredients to take.
    :type proportions: list(int)
    :param ref_amounts: Ingredients properties.
    :type ref_amounts: numpy.ndarray
    :param check_calories: If not null, specific number of calories to match
        for the valid recipes.
    :type check_calories: None or int
    :return: Cookie recipe value.
    :rtype: int
    '''
    # compute proportions
    ings_prop_sum = sum([
        np.outer(proportions[i], ref_amounts[i,:]) \
        for i in range(len(proportions))
    ])
    # isolate calories column
    calories = ings_prop_sum[:, -1]
    ings_prop_sum = ings_prop_sum[:, :-1]
    # replace negative values with zeros
    ings_prop_sum[ings_prop_sum < 0] = 0

    if check_calories is not None and isinstance(check_calories, int):
        ings_prop_sum = ings_prop_sum[calories == check_calories]
        if len(ings_prop_sum) == 0:
            return -1
    return np.prod(ings_prop_sum, axis=1).max()

def best_recipe_value(ingredients, check_calories=None):
    '''Computes the best recipe, i.e. the mix of ingredients that gives the
    highest cookie value, and returns its value.
    
    :param ingredients: All available ingredients.
    :type ingredients: dict(str, dict(str, int))
    :param check_calories: If not null, specific number of calories to match
        for the valid recipes.
    :type check_calories: None or int
    :return: Highest cookie value.
    :rtype: int
    '''
    # get list of ingredients and extract ingredients properties
    ings = list(ingredients.keys())
    amounts = np.array([ ingredients[i] for i in ings ])
    
    # process is adapted to the ingredients, so we must check the total number
    # of available ingredients
    highest_cookie_value = -1
    if len(ings) == 2:
        for c0 in tqdm(range(101), total=100):
            c1 = 100 - c0
            highest_cookie_value = max(
                compute_recipe_value([ c0, c1 ], amounts, check_calories),
                highest_cookie_value)
    elif len(ings) == 4:
        for c0 in tqdm(range(101), total=100):
            for c1 in range(101 - c0):
                for c2 in range(101 - c0 - c1):
                    c3 = 100 - c0 - c1 - c2
                    highest_cookie_value = max(
                        compute_recipe_value([ c0, c1, c2, c3 ], amounts,
                            check_calories),
                        highest_cookie_value)
                        
    return highest_cookie_value

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ingredients = parse_input(
    '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3''')
    assert best_recipe_value(ingredients) == 62842880

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day15.txt'
    ingredients = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = best_recipe_value(ingredients)
    print('PART I: solution = {}'.format(solution))
    
    ### PART I
    solution = best_recipe_value(ingredients, check_calories=500)
    print('PART II: solution = {}'.format(solution))
    
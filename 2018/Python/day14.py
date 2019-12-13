### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 14: Chocolate Charts
### =============================================

# [ Computation functions ]
# -------------------------
### Part I
def compute_recipes_p1(prediction):
    '''Computes the 10 recipes that come after N recipes, where N is the
    prediction the elves make on the required number of recipe tests.
    
    :param prediction: Predicted required number of recipes to test.
    :type prediction: int
    :return: Scores of the 10 recipes after the prediction.
    :rtype: str
    '''
    recipes = [ 3, 7 ]
    r1, r2 = 0, 1
    while len(recipes) < prediction + 10:
        new_recipe = str(recipes[r1] + recipes[r2])
        recipes.extend([ int(x) for x in new_recipe ])
        r1 = (1 + r1 + recipes[r1]) % len(recipes)
        r2 = (1 + r2 + recipes[r2]) % len(recipes)
    return ''.join([ str(x) for x in recipes[prediction:prediction+10] ])

def compute_recipes_p2(target):
    '''Computes the number of recipes that come before the target recipes
    scores.
    
    :param target: Target recipes scores.
    :type target: int
    :return: Number of previous recipes.
    :rtype: int
    '''
    recipes = [ 3, 7 ]
    r1, r2 = 0, 1
    recipe_str = ''.join([ str(x) for x in recipes ])
    new_recipe = ''
    while target not in recipe_str[-(len(target)+len(new_recipe)):]:
        new_recipe = str(int(recipe_str[r1]) + int(recipe_str[r2]))
        recipe_str += new_recipe
        r1 = (1 + r1 + int(recipe_str[r1])) % len(recipe_str)
        r2 = (1 + r2 + int(recipe_str[r2])) % len(recipe_str)
    return recipe_str.index(target)

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    assert compute_recipes_p1(5) == '0124515891'
    assert compute_recipes_p1(9) == '5158916779'
    assert compute_recipes_p1(18) == '9251071085'
    assert compute_recipes_p1(2018) == '5941429882'
        
    ### Part II
    assert compute_recipes_p2('01245') == 5
    assert compute_recipes_p2('51589') == 9
    assert compute_recipes_p2('92510') == 18
    assert compute_recipes_p2('59414') == 2018
        
import time
if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    ### PART I
    solution = compute_recipes_p1(110201)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    st = time.time()
    solution = compute_recipes_p2('110201')
    print('PART II: solution = {}'.format(solution))

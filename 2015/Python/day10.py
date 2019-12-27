### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 10: Elves Look, Elves Say
### =============================================
from itertools import groupby

# [ Computation functions ]
# -------------------------
### PART I
def look_and_say(input, rounds):
    '''Plays the "look-and-say" game for a given number of rounds. Each round,
    we take the input, read it aloud and write down the result as the input for
    the next round.
    
    :param input: Initial input to start the game.
    :type input: str
    :param rounds: Number of rounds to play.
    :type rounds: int
    :return: Final input.
    :rtype: str
    '''
    current = input
    for _ in range(rounds):
        says = [ (k, len(list(g))) for k, g in groupby(list(current)) ]
        current = ''.join([ '{}{}'.format(count, char) for char, count in says ])
    return current

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert look_and_say('1', 1) == '11'
    assert look_and_say('11', 1) == '21'
    assert look_and_say('21', 1) == '1211'
    assert look_and_say('1211', 1) == '111221'
    assert look_and_say('111221', 1) == '312211'

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    input = '1113222113'
    
    ### PART I
    round_40 = look_and_say(input, 40)
    solution = len(round_40)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = len(look_and_say(round_40, 10))
    print('PART II: solution = {}'.format(solution))

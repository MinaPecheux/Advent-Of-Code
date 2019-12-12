### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 8: Space Image Format
### =============================================

# [ Computation functions ]
# -------------------------
### PART I
def decode_layers(inputs, width, height):
    '''Decodes the image layers by splitting it in even chunks.
    
    :param inputs: Content of the image (as a string).
    :type inputs: str
    :param width: Width of each layer in the image.
    :type width: int
    :param height: Height of each layer in the image.
    :type height: int
    :return: Layers in the image.
    :rtype: list(str)
    '''
    layer_size = width * height
    n_layers = len(inputs) // layer_size
    return [ inputs[l*layer_size:(l+1)*layer_size] for l in range(n_layers) ]
    
def compute_checksum(inputs, width, height):
    '''Computes a basic checksum to verify the image is intact by finding the
    layer that has the fewest layer and computing the product of its number of
    1s and 2s.
    
    :param inputs: Content of the image (as a string).
    :type inputs: str
    :param width: Width of each layer in the image.
    :type width: int
    :param height: Height of each layer in the image.
    :type height: int
    :return: Checksum to verify the image validity.
    :rtype: int
    '''
    layers = decode_layers(inputs, width, height)
    best_n_zeros, best_value = None, None
    for layer in layers:
        n_zeros = layer.count('0')
        if best_n_zeros is None or n_zeros < best_n_zeros:
            n_ones = layer.count('1')
            n_twos = layer.count('2')
            best_n_zeros = n_zeros
            best_value = n_ones * n_twos
    return best_value, layers
    
### Part II
def display_message(layers, width, height):
    '''Displays the message that was sent (and has previously been divided into
    even layers).
    
    :param layers: Layers of the image.
    :type layers: list(str)
    :param width: Width of each layer in the image.
    :type width: int
    :param height: Height of each layer in the image.
    :type height: int
    '''
    marker = '█'
    # iterate through layers in reverse order to have the right depht overwrite
    img = [ [ ' ' for _ in range(width) ] for _ in range(height) ]
    for layer in layers[::-1]:
        # go through grid
        for y in range(height):
            for x in range(width):
                # and turn on/off pixels depending on the value (transparent has
                # no impact)
                if layer[x + y*width] == '1':
                    img[y][x] = marker
                elif layer[x + y*width] == '0':
                    img[y][x] = ' '
    # display the message
    print('')
    for y in range(height):
        print(''.join(img[y]))
    print('')
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert decode_layers('123456789012', 3, 2) == [ '123456', '789012' ]
    assert decode_layers('210012011212', 3, 2) == [ '210012', '011212' ]

    ### PART I
    c, _ = compute_checksum('123456789012', 3, 2)
    assert c == 1
    c, _ = compute_checksum('210012011212', 3, 2)
    assert c == 6

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day8.txt'
    inputs = open(data_path, 'r').read().strip()
    
    ### PART I
    solution, layers = compute_checksum(inputs, 25, 6)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    display_message(layers, 25, 6)
    print('PART II (see the shell)')
    

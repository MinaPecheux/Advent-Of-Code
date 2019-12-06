### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 8: Memory Maneuver
### =============================================
import itertools

# [ Input parsing functions ]
# ---------------------------
def parse_rec(id_generator, data):
    '''Util recursive function for the parsing of the inputs. It creates a new
    node in the tree and recursively calls itself to produce all the children
    nodes as well.
    
    :param id_generator: Auto-incremented IDs generator.
    :type id_generator: iterator
    :param data: Digits to work on and parse into a node (can be a subset of the
        entire original input where the beginning has been removed up to the
        header of the new node to create).
    :type data: list(int)
    '''
    # base case
    if len(data) == 0:
        return {}, 0, None
    # generate a new auto-incremented ID (automatically moves the counter to
    # its next slot for next time)
    id = next(id_generator)
    # extract information from the header
    n_children, n_metadata = data[:2]
    # compute children nodes and store the nodes + their indices
    offset = 0
    children = {}
    children_idx = []
    for _ in range(n_children):
        nodes, off, i = parse_rec(id_generator, data[2+offset:])
        children.update(nodes)
        children_idx.append(i)
        offset += off
    # extract metadata
    metadata = data[2+offset:2+offset+n_metadata]
    # build the new node
    node = tuple([ children_idx, metadata ])
    # take the full list of nodes and add the new one to it
    nodes = children
    nodes[id] = node
    return nodes, 2+offset+n_metadata, id

def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    digits = [ int(x) for x in data.split() ]
    nodes, _, _ = parse_rec(itertools.count(), digits)
    return nodes

# [ Computation functions ]
# -------------------------
### Part I
def compute_metadata_checksum(nodes):
    '''Computes a basic checksum by adding all the metadata from all nodes.
    
    :param nodes: List of nodes to compute with.
    :type nodes: dict(int, tuple)
    '''
    return sum([ sum(node[1]) for node in nodes.values() ])
    
### Part II
def compute_node_value(nodes, node):
    '''Computes the value of a node depending on whether or not it has children.
    The function works recursively.
    
    :param nodes: List of nodes to compute with.
    :type nodes: dict(int, tuple)
    :param node: Id of the node to compute the value for.
    :type node: int
    '''
    if node not in nodes: return 0 # skip invalid reference
    children, metadata = nodes[node]
    # if no children: the value is the sum of the metadata
    if len(children) == 0:
        return sum(metadata)
    # else: metadata becomes a table of addresses for the children
    s = 0
    for meta in metadata:
        # extract reference if possible (else skip to the next item)
        try:
            child_ref = children[meta - 1]
        except IndexError:
            continue
        # skip root node (avoid infinite cycling)
        if child_ref == 0:
            continue
        # recursively compute the child's value
        s += compute_node_value(nodes, child_ref)
    return s

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    # check correct parsing
    parsed = parse_input('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2')
    correct = { 0: ([1, 2], [1,1,2]), 1: ([], [10,11,12]),
        2: ([3], [2]), 3: ([], [99]) }
    assert len(parsed) == len(correct) and sorted(parsed) == sorted(correct)
    
    parsed2 = parse_input(
        '3 4 0 3 1 2 5 2 2 1 1 0 2 3 3 1 0 3 1 2 4 1 2 1 2 0 1 2 1 2 1 1 2 3')
    correct2 = { 0: ([1, 2, 6], [1,1,2,3]), 1: ([], [1,2,5]),
        2: ([3,5], [1,2]), 3: ([4], [1]), 4: ([], [3,3]), 5: ([], [1,2,4]),
        6: ([7], [1,2]), 7: ([], [2]) }
    assert len(parsed2) == len(correct2) and sorted(parsed2) == sorted(correct2)
    
    ### PART I
    assert compute_metadata_checksum(parsed) == 138
    assert compute_metadata_checksum(parsed2) == 37
    
    ### PART II
    assert compute_node_value(parsed, 0) == 66
    assert compute_node_value(parsed2, 0) == 31

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day8.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = compute_metadata_checksum(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = compute_node_value(inputs, 0) #4766: too low
    print('PART II: solution = {}'.format(solution))

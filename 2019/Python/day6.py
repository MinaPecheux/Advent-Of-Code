### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 6: Universal Orbit Map
### =============================================
import networkx as nx

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    return [ line.split(')') for line in data.split('\n') if line != '' ]

# [ Computation functions ]
# -------------------------
### PART I
def count_orbits(orbits):
    '''Finds the number of direct and indirect orbits from the given list of
    orbits.
    
    :param orbits: List of orbit pairs in the form (object at the center of the
        orbit, revolving object).
    :type orbits: list(tuple(str))
    '''
    G = nx.DiGraph()
    G.add_edges_from(orbits)
    return G, sum([
        len(list(nx.edge_dfs(G, node, orientation='reverse'))) for node in G
    ])

### Part II
def find_min_moves(graph):
    '''Finds the minimal number of orbital moves that have to be executed to
    reach Santa! (The graph passed as parameter should probably be undirected
    to allow for path search in any direction...)
    
    :param graph: Already computed graph to compute the orbital moves on.
    :type graph: nx.Graph
    '''
    # remove 2 because we exclude the final nodes (that are include by NetworkX)
    # and the move from our current position to the object we are revoving around
    return len(nx.algorithms.shortest_path(graph, 'YOU', 'SAN')) - 3

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    _, n_orbits = count_orbits([ ('COM', 'B'), ('C', 'D'), ('B', 'C'),
        ('D', 'E'), ('E', 'F'), ('B', 'G'), ('G', 'H'), ('D', 'I'),
        ('E', 'J'), ('J', 'K'), ('K', 'L') ])
    assert n_orbits == 42
        
    ### PART II
    graph = nx.Graph()
    graph.add_edges_from([ ('COM', 'B'), ('C', 'D'), ('B', 'C'),
        ('D', 'E'), ('E', 'F'), ('B', 'G'), ('G', 'H'), ('D', 'I'),
        ('E', 'J'), ('J', 'K'), ('K', 'L'), ('K', 'YOU'), ('I', 'SAN') ])
    assert find_min_moves(graph) == 4

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day6.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    directed_graph, solution = count_orbits(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    # (transform the graph in an undirected one to allow path search in any
    # direction)
    undirected_graph = nx.Graph(directed_graph)
    solution = find_min_moves(undirected_graph)
    print('PART II: solution = {}'.format(solution))

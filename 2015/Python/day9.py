### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 9: All in a Single Night
### =============================================
from networkx import Graph, all_simple_paths

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of connections in the graph.
    :rtype: list(tuple(str, str, dict))
    '''
    connections = []
    for line in data.strip().split('\n'):
        points, dist = line.split(' = ')
        dist = int(dist)
        entry, exit = points.split(' to ')
        connections.append((entry, exit, { 'weight': dist }))
    return connections

# [ Computation functions ]
# -------------------------
### PART I + II
def compute_route_lengths(graph):
    '''Computes all the possible paths in the graph and stores the length of
    each. The given graph represents the map with cities modeled as nodes and
    connections between cities modeled as edges weighted by the distance.
    
    :param graph: Graph that represents the map.
    :type graph: nx.Graph
    :return: Lengths of all the paths.
    :rtype: list(int)
    '''
    lengths = []
    for source in graph.nodes:
        for target in graph.nodes:
            if source == target: # ignore same node
                continue
            for path in all_simple_paths(graph, source, target):
                if len(set(path)) != len(graph.nodes):
                    continue
                length = 0
                for i in range(len(path) - 1):
                    length += graph.get_edge_data(path[i], path[i+1])['weight']
                lengths.append(length)
    return lengths
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    graph = Graph()
    graph.add_edges_from(parse_input(
    '''London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141'''))
    route_lengths = compute_route_lengths(graph)
    assert min(route_lengths) == 605
    assert max(route_lengths) == 982
    
if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    # get input data
    data_path = '../data/day9.txt'
    connections = parse_input(open(data_path, 'r').read())
    
    # prepare graph and path lengths
    graph = Graph()
    graph.add_edges_from(connections)
    route_lengths = compute_route_lengths(graph)
    
    ### PART I
    solution = min(route_lengths)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = max(route_lengths)
    print('PART II: solution = {}'.format(solution))

### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 7: The Sum of Its Parts
### =============================================
import re

import networkx as nx

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    '''
    step_regex = r'Step ([A-Z])[\w\s]+([A-Z])'
    inputs = []
    for line in data.split('\n'):
        if line == '': continue
        match = re.match(step_regex, line)
        inputs.append((match.group(1), match.group(2)))
    return inputs

# [ Computation functions ]
# -------------------------
### PART I
def sort_instructions(instructions):
    '''Finds the correct execution order for the given instructions.
    
    :param instructions: List of conditional relations for instruction steps
        pairs.
    :type instructions: list(tuple(int))
    '''
    # compute dependency tree
    G = nx.DiGraph()
    G.add_edges_from(instructions)
    dependencies, deps_copy = {}, {}
    for node in G:
        values = list(nx.edge_dfs(G, node, orientation='reverse'))
        dependencies[node] = set([ t[0] for t in values ])
        deps_copy[node] = set([ t[0] for t in values ])
    # step order computation
    order = ''
    while len(dependencies) > 0:
        next_node = sorted(dependencies.keys(),
            key=lambda x: (len(dependencies[x]), x))[0]
        for n, children in dependencies.items():
            children.discard(next_node)
        del dependencies[next_node]
        order += next_node
    return deps_copy, order

### Part II
def step_is_queued(queue, step):
    '''Checks if a step is currently in the execution queue.
    
    :param queue: List of currently processed steps.
    :type queue: list(tuple(str, int))
    :param step: Step to check.
    :type step: str
    '''
    for exec in queue:
        if exec is not None and exec[0] == step:
            return True
    return False

def step_is_locked(dependencies, done, step):
    '''Checks if a step is currently locked because its dependencies haven't
    been completed yet.
    
    :param dependencies: Already computed dependencies to compute the
        instructions execution with.
    :type dependencies: dict
    :param done: Set of already processed steps.
    :type done: set(str)
    :param step: Step to check.
    :type step: str
    '''
    return len(dependencies[step]) > 0 and not done.issuperset(dependencies[step])

def compute_execution_time(dependencies, n_workers, base_duration):
    '''Finds the correct execution order for the given instructions.
    
    :param dependencies: Already computed dependencies to compute the
        instructions execution with.
    :type dependencies: dict
    :param n_workers: Number of workers for the execution.
    :type n_workers: int
    :param base_duration: Minimal duration of a step.
    :type base_duration: int
    '''
    time = 0
    exec_queue = [ None ] * n_workers
    done = set()
    while len(dependencies) > 0:
        # . check if any steps are completed, else simply reduce the execution
        # time by 1 for all the remaining ones in the queue
        new_exec_queue = [ None ] * n_workers
        for i, task in enumerate(exec_queue):
            if task is None: continue
            step, exec = task
            e = exec - 1
            if e != 0:
                new_exec_queue[i] = (step, e)
            else:
                for n, children in dependencies.items():
                    children.discard(step)
                del dependencies[step]
                done.add(step)
        exec_queue = new_exec_queue
        
        # . find all possible tasks for this step (filter out the ones that are
        # already in the queue or are locked by not-yet-completed dependencies)
        sorted_nodes = sorted(dependencies.keys(),
            key=lambda x: (len(dependencies[x]), x))
        sorted_nodes = [ n for n in sorted_nodes if not \
            (step_is_locked(dependencies, done, n) or \
            step_is_queued(exec_queue, n)) ]

        # . foreach worker, if he doesn't have a job yet, assign him to a step
        for worker_id in range(n_workers):
            if len(sorted_nodes) == 0: break
            if exec_queue[worker_id] is not None: continue
            next_node = sorted_nodes.pop(0)
            exec_time = base_duration + 1 + (ord(next_node) - ord('A'))
            exec_queue[worker_id] = (next_node, exec_time)
        time += 1
    return time - 1

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### PART I
    deps, order = sort_instructions([ ('C', 'A'), ('C', 'F'), ('A', 'B'),
        ('A', 'D'), ('B', 'E'), ('D', 'E'), ('F', 'E') ])
    assert order == 'CABDFE'
    _, order = sort_instructions([ ('B', 'C'), ('A', 'B'), ('J', 'B'),
        ('E', 'C') ])
    assert order == 'AEJBC'
    _, order = sort_instructions([ ('A', 'F'), ('A', 'G'), ('F', 'Y'),
        ('G', 'Y'), ('Y', 'Z') ])
    assert order == 'AFGYZ'
        
    ### PART II
    assert compute_execution_time(deps, 2, 0) == 15

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day7.txt'
    inputs = parse_input(open(data_path, 'r').read())
    
    ### PART I
    dependencies, solution = sort_instructions(inputs)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = compute_execution_time(dependencies, 5, 60)
    print('PART II: solution = {}'.format(solution))

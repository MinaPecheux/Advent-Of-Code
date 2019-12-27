### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2015 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 7: Some Assembly Required
### =============================================

class CircuitPiece(object):
    
    '''Util class to represent a piece in the circuit. It is define by its
    label and type, and has a list of inputs that can either be the label of
    another piece in the circuit or a direct integer input.'''
    
    OPERATIONS = {
        None: lambda a: a,
        'AND': lambda a, b: a & b,
        'OR': lambda a, b: a | b,
        'LSHIFT': lambda a, b: a << b,
        'RSHIFT': lambda a, b: a >> b,
        'NOT': lambda a: ~a
    }
    
    def __init__(self, label, type, inputs):
        '''Initialization function to create a new CircuitPiece.
        
        :param label: Label of the piece.
        :type label: str
        :param type: Type of piece: if None, then the piece assumes direct
            inputs; else it can have one or two inputs.
        :type type: None or str
        :param inputs: Inputs of the piece.
        :type inputs: list(str) or list(int)
        '''
        self.label = label
        self.type = type
        self.inputs = inputs
        self.value = None
        
    def __str__(self):
        '''Specific representation of the CircuitPiece for debug.
        
        :return: String representation.
        :rtype: str
        '''
        out = '[{}] - {}: '.format(self.label, self.type)
        out += str(self.inputs)
        return out
        
    def compute(self, pieces):
        '''Computes the value of a piece in the circuit by applying the correct
        operations to its inputs (and recursively computing the value of these
        inputs if need be).
        
        :param pieces: Complete circuit to compute with.
        :type pieces: dict(str, CircuitPiece)
        :return: Value of the piece.
        :rtype: int
        '''
        if self.value is None:
            inputs = []
            for i in self.inputs:
                if isinstance(i, int):
                    inputs.append(i)
                elif i.isdigit():
                    inputs.append(int(i))
                else:
                    inputs.append(pieces[i].compute(pieces))
            self.value = CircuitPiece.OPERATIONS[self.type](*inputs)
            if self.value < 0:
                self.value += 65536
        return self.value

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: List of strings to check.
    :rtype: dict(str, CircuitPiece)
    '''
    pieces = {}
    for line in data.strip().split('\n'):
        if line == '': continue
        inputs, output = line.split(' -> ')
        found_op = False
        for op in CircuitPiece.OPERATIONS:
            if op is None: continue # (invalid op for parsing)
            if op in inputs:
                found_op = True
                if op == 'NOT': # only 1 operand
                    operand = inputs.replace('NOT ', '')
                    pieces[output] = CircuitPiece(output, op, [ operand ])
                else: # 2 operands
                    operands = inputs.split(' {} '.format(op))
                    pieces[output] = CircuitPiece(output, op, operands)
                break
        if not found_op:
            if inputs.isdigit():
                pieces[output] = CircuitPiece(output, None, [ int(inputs) ])
            else:
                pieces[output] = CircuitPiece(output, None, [ inputs ])
    return pieces

# [ Computation functions ]
# -------------------------

### PART I
def compute_circuit(circuit, test_wire):
    '''Computes the value of a piece in the given circuit (found by its label).
    
    :param circuit: Complete circuit to compute with.
    :type circuit: dict(str, CircuitPiece)
    :return: Value of the piece.
    :rtype: int
    '''
    return circuit[test_wire].compute(circuit)

### PART II
    
# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    circuit = parse_input('''123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i''')
    assert compute_circuit(circuit, 'd') == 72
    assert compute_circuit(circuit, 'e') == 507
    assert compute_circuit(circuit, 'f') == 492
    assert compute_circuit(circuit, 'g') == 114
    assert compute_circuit(circuit, 'h') == 65412
    assert compute_circuit(circuit, 'i') == 65079
    assert compute_circuit(circuit, 'x') == 123
    assert compute_circuit(circuit, 'y') == 456
    
if __name__ == '__main__':
    # check function results on example cases
    make_tests()

    # get input data
    data_path = '../data/day7.txt'
    circuit = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = compute_circuit(circuit, 'a')
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    # . reset all pieces
    for piece in circuit.values():
        piece.value = None
    # . override wire b
    circuit['b'].inputs = [ solution ]
    solution = compute_circuit(circuit, 'a')
    print('PART II: solution = {}'.format(solution))

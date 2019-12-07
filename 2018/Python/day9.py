### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2018 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 9: Marble Mania
### =============================================
import itertools
from tqdm import tqdm

# [ Computation functions ]
# -------------------------
class DoubleLinkedListNode(object):
    
    '''Util class to represent an item in a double linked list. An item has
    a value (its data), a previous node in the list and a next node in the list.
    If either is None, then there is no connection in this direction.'''
    
    def __init__(self, data, prev=None, next=None):
        '''Initialization function for a double linked list node.
        
        :param data: Value of the node.
        :type data: int
        :param prev: If not None, reference to the previous node in the list.
        :type prev: DoubleLinkedListNode
        :param next: If not None, reference to the next node in the list.
        :type next: DoubleLinkedListNode
        '''
        self.data = data
        self.prev = prev
        self.next = next    
        
class DoubleLinkedList(object):
    
    '''Util class to implement a double linked list, i.e. a linked list where
    items both have a connection to the previous and the next node. The list
    is circular, meaning that the successor of the last node is the first node
    in the list.
    
    The list has a "head" pointer to the first item in the list (arbitrarily
    chosen in the cycle as the first one added) and a "current" pointer to the
    currently selected node.'''
    
    def __init__(self, head):
        '''Initialization function for a double linked list.
        
        :param head: Reference to the first node in the list.
        :type head: DoubleLinkedListNode
        '''
        self.head = head
        self.current = head
        self.length = 1
                
    def print(self):
        '''Util function to display the double linked list, starting from the
        head (and stopping at the end of the first cycle).'''
        iter = self.head
        output = []
        in_loop = False
        while iter is not None:
            if in_loop and iter == self.head:
                break
            if iter == self.current:
                output.append('(%s)' % iter.data)
            else:
                output.append(str(iter.data))
            iter = iter.next
            if not in_loop:
                in_loop = True
        print(' '.join(output))
                
    def add(self, data, set_ptr=False):
        '''Adds a node at the end of the double linked list.
        
        :param data: Value of the node to add.
        :type data: int
        :param set_ptr: If true, then the "current" pointer of the list will be
            assigned to the newly created node.
        :type set_ptr: bool
        '''
        if self.length == 1:
            node = DoubleLinkedListNode(data, self.head, self.head)
            self.head.next = node
            self.head.prev = node
        else:
            prev = self.head.prev
            node = DoubleLinkedListNode(data, prev, self.head)
            if prev is not None:
                prev.next = node
            self.head.prev = node
        self.length += 1
        if set_ptr: self.current = node
                
    def insert(self, offset, data, set_ptr=False):
        '''Inserts a node in the double linked list with a given offset from the
        currently selected node.
        
        :param offset: Offset from the currently selected node: if positive, the
            node will be inserted in the successors, else it will be inserted in
            the predecessors.
        :type offset: int
        :param data: Value of the node to insert.
        :type data: int
        :param set_ptr: If true, then the "current" pointer of the list will be
            assigned to the newly created node.
        :type set_ptr: bool
        '''
        iter = self.current
        pace = 0
        if offset > 0:
            while iter.next is not None and pace < offset-1:
                iter = iter.next
                pace += 1
            node = DoubleLinkedListNode(data, iter, iter.next)
            iter.next.prev = node
            iter.next = node
            self.length += 1
        elif offset < 0:
            while iter.prev is not None and pace < -offset-1:
                iter = iter.prev
                pace += 1
            node = DoubleLinkedListNode(data, iter.prev, iter)
            iter.prev.next = node
            iter.prev = node
            self.length += 1
        else:
            self.current.data = data
            
        if set_ptr: self.current = node
        
    def remove(self, offset, set_ptr=False):
        '''Removes a node in the double linked list with a given offset from the
        currently selected node.
        
        :param offset: Offset from the currently selected node: if positive, the
            node will be removed from the successors, else it will be removed
            from the predecessors.
        :type offset: int
        :param set_ptr: If true, then the "current" pointer of the list will be
            assigned to the successor of the removed node.
        :type set_ptr: bool
        '''
        iter = self.current
        pace = 0
        if offset > 0:
            while iter.next is not None and pace < offset:
                iter = iter.next
                pace += 1
        elif offset < 0:
            while iter.prev is not None and pace < -offset:
                iter = iter.prev
                pace += 1

        d = iter.data
        p, n = iter.prev, iter.next
        iter.prev.next = n
        iter.next.prev = p
            
        self.length -= 1
        if iter == self.head: self.head = iter.next
        if set_ptr: self.current = iter.next
        return d

### Part I
def compute_highscore(inputs, display_progress=True):
    '''Computes the highscore for the winning Elf given the number of players
    and the last marble's value (equivalent to the number of turns).
    
    :param inputs: Tuple containing the game information (number of players and
        last marble's value).
    :type inputs: tuple(int, int)
    :param display_progress: If true, then progress bar are shown during the
        computation (using the tqdm module).
    :type display_progress: bool
    '''
    n_players, n_turns = inputs
    scores = [ 0 ] * n_players
    board = DoubleLinkedList(DoubleLinkedListNode(0))
    # make iterator (remember to include the last turn)
    iterator = range(1, n_turns + 1)
    if display_progress:
        iterator = tqdm(iterator, total=n_turns)
    for turn in iterator:
        # check for special case
        if turn % 23 == 0:
            player = (turn - 1) % n_players
            removed = board.remove(-7, set_ptr=True)
            scores[player] += turn + removed
        # else add the marble in the circle
        else:
            if board.length < 2:
                board.add(turn, set_ptr=True)
            else:
                board.insert(2, turn, set_ptr=True)
    return max(scores)

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    assert compute_highscore((9, 25), False) == 32
    assert compute_highscore((10, 1618), False) == 8317
    assert compute_highscore((13, 7999), False) == 146373
    assert compute_highscore((17, 1104), False) == 2764
    assert compute_highscore((21, 6111), False) == 54718
    assert compute_highscore((30, 5807), False) == 37305
    
if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    ### PART I
    solution = compute_highscore((459, 71320))
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = compute_highscore((459, 7132000))
    print('PART II: solution = {}'.format(solution))

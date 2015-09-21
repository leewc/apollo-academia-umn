import queue
import copy
import pdb
"""This is where the problem is defined. Initial state, goal state and other information that can be got from the problem"""


def collapse(node):
    """Return a list of states for a potential soln."""
    x = list()
    while node.parent is not None:
        x.insert(0, node.state)
        node = node.parent
    return x

class Problem(object):

    """
        My notes:
        - each 0 in the list is an empty node that needs to be solved.
        - need a build initial tree function of nodes that is called by init.
        - since each level is based on numbers, create nodes with value 1 -> length
        - goal test needs to check if the constraints are obeyed.
        - perhaps add a separate flag to enable pruning? (later)
    """

    def __init__(self, representation, goal=None):
        """This is the constructor for the Problem class. It specifies the initial state, and possibly a goal state, if there is a unique goal.  You can add other arguments if the need arises"""

        """
            Based on the set up initial is of type node. A Tree of Nodes.
            Goal is also a node tree.
        """
        self.representation = representation
        self.initial = 0
        self.goal = goal
        self.numberOfUnknowns = 0
        self.dimension = len(representation)  # dimension of sudoku
        self.indexValues = list()  # a tuple of indexes to avoid deepcopy

        for row in range(len(self.representation)):
            # 0 represents an unknown number
            self.numberOfUnknowns += self.representation[row].count(0)
            for cell in range(len(self.representation[0])):
                value = self.representation[row][cell]
                if value is 0:
                    self.indexValues.append((row, cell))   # append index tuple to list

    def actions(self, state, depth):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        # if state == 0:  #First Node in tree with no child
        if depth != self.numberOfUnknowns:
            return [x for x in range(1, self.dimension + 1)]
        else:
            return []

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        return action  # since we want a bunch of nodes, this doesn't do much, just return what needs to be returned.

    def make_soln(self, states):
        """Swaps in potential solutions into the board"""
        for index in self.indexValues:
            self.representation[index[0]][index[1]] = states.pop(0)

    def checkRow(self,row):
        for i in range(1, self.dimension + 1):
            if row.count(i) > 1:
                return False
        return True

    def getColumn(self, index):
        return [row[index] for row in self.representation]

    def checkSubGrid(self,row,col,step):
        subGrid = list()
        for i in range(row, row + step):
            for j in range(col, col + step):
                subGrid.append(self.representation[i][j])
        # print(subGrid)
        return self.checkRow(subGrid)

    def checkSubSquares(self):
        if self.dimension is 4:
            for x in range(0,4,2):
                for y in range(0,4,2):
                    if not self.checkSubGrid(x,y,2):
                        return False
            return True

    def check_soln(self, board):
        # print(board)
        for i in range(0, self.dimension):
            if not (self.checkRow(board[i])):
                return False
            if not (self.checkRow(self.getColumn(i))):
                return False
        if(self.checkSubSquares()):
            return True
        return False

    def goal_test(self, node):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        if node.depth != self.numberOfUnknowns:
            return False
        else:
            w = collapse(node)
            self.make_soln(w)
            return self.check_soln(self.representation)
            # print(self.representation)


class Node:

    """A node in a search tree. Contains:
        - a pointer to the parent (the node that this is a successor of, up one level) 
        - a pointer to the actual state for this node. 
        - the action that got us to this state

    If a state is arrived at by two paths, then there are two nodes with
    the same state.

    """

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action.
        Update the node parameters based on constructor values"""
        # update(self, state=state, parent=parent, action=action, depth=0)
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        # If depth is specified then depth of node will be 1 more than the
        # depth of parent
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        # List the nodes reachable in one step from this node.
        return [self.child_node(problem, action)
                for action in problem.actions(self.state, self.depth)]

    # Makes a child node
    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        return Node(next, self, action)

    def __str__(self):
        return "Node %i - Depth %i" % (self.state, self.depth)

# def printTree(parentNode):
#     print(parentNode)
#     print("|", end="")
#     for parentNode.child


def breadth_first_search(problem):
    printTree = False
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node):
        return nodes
    # Create a Queue to store all nodes of a particular level. Import
    # QueueClass()
    frontier = queue.Queue()
    frontier.put(node)

    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test
    # criteria are met
    while not frontier.empty():
        # Remove from frontier, for analysis
        node = frontier.get()
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes
        # here
        if printTree: print(node)
        for child in node.expand(problem):
            if printTree: print(" |--", child, "--", end="")
            # If child node meets Goal_Test criteria
            if problem.goal_test(child):
                # pdb.set_trace()
                return child
            # Add every new child to the frontier
            frontier.put(child)
            if printTree: print("")
    # printTree(node)
    return None


def runApp():
    """
    sudoku = [
        [1, 5, 0, 0, 4, 0],
        [2, 0, 0, 0, 5, 6],
        [4, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 4],
        [6, 3, 0, 0, 2, 0],
        [0, 2, 0, 0, 3, 1],
    ]
    """
    sudoku = [
        [0, 1, 0, 4],
        [4, 0, 0, 0],
        [0, 0, 0, 3],
        [3, 0, 2, 0],
    ]

    expectedSoln = [
        [2, 1, 3, 4],
        [4, 3, 1, 2],
        [1, 2, 4, 3],
        [3, 4, 2, 1],
    ]

    print("Original Sudoku is: ", sudoku)
    # problemStartNode = Node(sudoku) -- This is done by BFS
    solutionNode = breadth_first_search(Problem(sudoku))

    print("From top to bottom", collapse(solutionNode))

    assert(sudoku, expectedSoln)
    print("Final Solved Sudoku is", sudoku)
            


if(__name__ == '__main__'):
    runApp()

"""
sudoku = [
        [0, 1, 0, 4],
        [4, 0, 0, 0],
        [0, 0, 0, 3],
        [3, 0, 2, 0],
    ]

soln = [
    [2, 1, 3, 4],
    [4, 3, 1, 2],
    [1, 2, 4, 3],
    [3, 4, 2, 1],
]
"""

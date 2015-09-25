import queue
import pdb
import time


class Problem(object):

    """This is where the problem is defined. Initial state, goal state and other information 
    that can be got from the problem

    - Each 0 in the list is an empty node that needs to be solved.
    - since each level is based on numbers, create nodes with value 1 -> length
    - goal test needs to check if the constraints are obeyed.
    """

    def __init__(self, representation, goal=None, prune=True):
        """This is the constructor for the Problem class.
        It specifies the initial state, and possibly a goal state,
        if there is a unique goal.
        You can add other arguments if the need arises

        Based on the set up initial is of type node. A Tree of Nodes.
        Goal is also a node tree.
        """
        self.PRUNE = prune
        self.representation = representation
        self.initial = 0
        self.goal = goal
        self.numberOfUnknowns = 0
        self.dimension = len(representation)  # dimension of sudoku
        self.indexValues = list()  # tuples of indexes (of 0) to avoid deepcopy

        for row in range(len(self.representation)):
            # 0 represents an unknown number
            for cell in range(len(self.representation[0])):
                value = self.representation[row][cell]
                if value is 0:
                    # append index tuple to List
                    self.indexValues.append((row, cell))
                    self.numberOfUnknowns += 1

    def actions(self, state, depth):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        if depth != self.numberOfUnknowns:
            return [x for x in range(1, self.dimension + 1)]
        else:
            return []

    def result(self, parentNode, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        if not self.PRUNE:
            # since we want a bunch of nodes, without pruning, just return
            # the value of action to be made into a possible soln.
            return action
        else:
            # get index based on depth, since each depth level is an unknown
            # pdb.set_trace()
            index = self.indexValues[parentNode.depth]

            # # update board with new values
            self.representation[index[0]][index[1]] = action

            # # load in whatever previous value we have
            ptrNode = parentNode
            while ptrNode.depth is not 0:
                # -1 because if not offset it is overwritten -> took too long
                idx = self.indexValues[ptrNode.depth - 1]
                self.representation[idx[0]][idx[1]] = ptrNode.state
                ptrNode = ptrNode.parent

            # count of 'action' value is must be =1 on row and col
            isPossibleValue = False
            if self.representation[index[0]].count(action) == 1:
                if self.getColumn(index[1]).count(action) == 1:
                    # check subGrid where unknown is located at
                    if self.checkSubSquares(index[0], index[1]):
                        isPossibleValue = True

            # Clean up so we can try next soln set - BFS switches branches
            for indexTuple in self.indexValues:
                self.representation[indexTuple[0]][indexTuple[1]] = 0

            if isPossibleValue:
                return action

    # #### Begin Board Checking Functions #### #
    def checkRow(self, row):
        for i in range(1, self.dimension + 1):
            if row.count(i) != 1:
                return False
        return True

    def getColumn(self, index):
        return [row[index] for row in self.representation]

    def checkSubGrid(self, row, col, stepRow, stepCol, zeroOK=False):
        """Different step values needed for rectangle subGrids e.g: 6x6"""
        subGrid = list()
        for i in range(row, row + stepCol):
            for j in range(col, col + stepRow):
                subGrid.append(self.representation[i][j])

        # short-circuit for pruning, no need to check if incomplete grid
        if zeroOK and subGrid.count(0) > 0:
            return True
        else:
            return self.checkRow(subGrid)

    def checkSubSquares(self, row=None, col=None):
        # Hard coded boundaries based on dimension of sudoku, remember range is upperbounded.
        if row is None or col is None:
            if self.dimension is 4:
                for x in range(0, 4, 2):
                    for y in range(0, 4, 2):
                        if not self.checkSubGrid(x, y, 2, 2):
                            return False
            if self.dimension is 6:
                for x in range(0, 6, 2):
                    for y in range(0, 6, 3):
                        if not self.checkSubGrid(x, y, 3, 2):
                            return False
            if self.dimension is 9:
                for x in range(0, 7, 3):
                    for y in range(0, 7, 3):
                        if not self.checkSubGrid(x, y, 3, 3):
                            return False
            return True
        else:
            # Individual grid checking (for pruning)
            if self.dimension is 6:
                if col <= 2 and row <= 1:  # First subgrid
                    return self.checkSubGrid(0, 0, 3, 2, True)
                elif (3 <= col <= 5) and row <= 1:
                    return self.checkSubGrid(0, 3, 3, 2, True)
                elif col <= 2 and (2 <= row <= 3):
                    return self.checkSubGrid(2, 0, 3, 2, True)
                elif (3 <= col <= 5) and (2 <= row <= 3):
                    return self.checkSubGrid(2, 3, 3, 2, True)
                elif col <= 2 and (4 <= row <= 5):
                    return self.checkSubGrid(4, 0, 3, 2, True)
                else:
                    return self.checkSubGrid(4, 3, 3, 2, True)

            elif self.dimension is 9:
                if col <= 3 and row <= 2:  # First subgrid
                    return self.checkSubGrid(0, 0, 3, 3, True)
                elif (4 <= col <= 6) and row <= 2:  # Second
                    return self.checkSubGrid(0, 3, 3, 3, True)
                elif (7 <= col <= 9) and row <= 2:  # Third
                    return self.checkSubGrid(0, 6, 3, 3, True)

                elif col <= 3 and (3 <= row <= 6):  # Fourth
                    return self.checkSubGrid(3, 0, 3, 3, True)
                elif (4 <= col <= 6) and (3 <= row <= 6):  # Fifth
                    return self.checkSubGrid(3, 3, 3, 3, True)
                elif (7 <= col <= 9) and (3 <= row <= 6):  # Sixth
                    return self.checkSubGrid(3, 6, 3, 3, True)

                elif col <= 3 and (7 <= row <= 9):  # Seventh
                    return self.checkSubGrid(6, 0, 3, 3, True)
                elif (4 <= col <= 6) and (7 <= row <= 9):  # Eighth
                    return self.checkSubGrid(6, 3, 3, 3, True)
                elif (7 <= col <= 9) and (7 <= row <= 9):  # Ninth
                    return self.checkSubGrid(6, 6, 3, 3, True)
            else:
                return True
                # Individual checking for 4x4 and other dimensions
                # not implemented, return True to keep possible values
                # board will still be checked later when board is complete.

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

    # #### End Board Checking Functions #### #

    def goal_test(self, node):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        if node.depth != self.numberOfUnknowns:
            return False
        else:
            ptrNode = node
            while ptrNode.state is not 0:
                idx = self.indexValues[ptrNode.depth-1]
                self.representation[idx[0]][idx[1]] = ptrNode.state
                ptrNode = ptrNode.parent

            return self.check_soln(self.representation)


class Node:

    """
    A node in a search tree. Contains:
        - a pointer to the parent (successor node, up one level)
        - a pointer to the actual state for this node.
        - the action that got us to this state

    If a state is arrived at by two paths, then there are two nodes with
    the same state.
    """

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action.
        Update the node parameters based on constructor values"""

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
        # NoneType is returned when pruning occurs
        return list(filter(None.__ne__,
                           [self.child_node(problem, action)
                            for action in problem.actions(self.state, self.depth)]))

        # Alternative return without NoneType method
        # return [self.child_node(problem, action)
        #         for action in problem.actions(self.state, self.depth)
        #         if self.child_node(problem, action) is not None]

    def child_node(self, problem, action):
        """Makes a child node"""
        next = problem.result(self, action)
        if next is not None:
            return Node(next, self, action)

    def __str__(self):
        return "Node %i - Depth %i" % (self.state, self.depth)


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
        if printTree:
            print(node)
        for child in node.expand(problem):
            if printTree:
                print(" |--", child, "--", end="")
            # If child node meets Goal_Test criteria
            if problem.goal_test(child):
                # pdb.set_trace()
                return child
            # Add every new child to the frontier
            frontier.put(child)
            if printTree:
                print("")
    # printTree(node)
    return None


def printNestedList(lol):
    string = ""
    for l in lol:
        string += str(l) + "\n"
    return string


def sudoku_driver(sudoku, expectedSoln=None):
    """
    Driver method that runs the solver, input: unsolved sudoku.
    Optional: expectedSoln, a solution for correctness
    Prints the Original, then the Solution, and Elapsed process_time.
    Raises a ValueError if no solution can be found.
    Note:
        Add a False as an argument for Problem constructor if you
        do not want pruning. e.g Problem(sudoku, False)
    """

    t = time.process_time()

    print("Original Sudoku:\n%s" % printNestedList(sudoku))

    solutionNode = breadth_first_search(Problem(sudoku))

    if solutionNode is None:
        raise(ValueError("No valid soln found."))

    print("Final Solved Sudoku:\n%s" % printNestedList(sudoku))
    print("Elapsed time for soln: ", time.process_time() - t)
    if expectedSoln is not None:
        assert(sudoku == expectedSoln)
        print("Solution Matches Expected Solution! \n")


def runApp():
    """
    Put in any sudoku to be solved, represented as List of Lists.
    I've included the test puzzles, as well as 'easier' versions that
    have less unknowns to speed up my testing.
    I've also included expected solutions for test puzzles
    """

    fourByFour = [
        [0, 1, 0, 4],
        [4, 0, 0, 0],
        [0, 0, 0, 3],
        [3, 0, 2, 0],
    ]

    solnFourByFour = [
        [2, 1, 3, 4],
        [4, 3, 1, 2],
        [1, 2, 4, 3],
        [3, 4, 2, 1],
    ]

    sixBySixFirst = [
        [1, 5, 0, 0, 4, 0],
        [2, 0, 0, 0, 5, 6],
        [4, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 4],
        [6, 3, 0, 0, 2, 0],
        [0, 2, 0, 0, 3, 1],
    ]

    sixBySixFirstEasy = [
        [1, 5, 6, 3, 4, 0],
        [2, 4, 3, 1, 5, 6],
        [4, 0, 2, 0, 0, 3],
        [3, 6, 5, 0, 0, 4],
        [6, 3, 0, 0, 2, 0],
        [5, 2, 0, 0, 3, 1],
    ]

    solnSixBySixFirst = [
        [1, 5, 6, 3, 4, 2],
        [2, 4, 3, 1, 5, 6],
        [4, 1, 2, 5, 6, 3],
        [3, 6, 5, 2, 1, 4],
        [6, 3, 1, 4, 2, 5],
        [5, 2, 4, 6, 3, 1],
    ]

    sixBySixSecond = [
        [0, 0, 0, 0, 4, 0],
        [5, 6, 0, 0, 0, 0],
        [3, 0, 2, 6, 5, 4],
        [0, 4, 0, 2, 0, 3],
        [4, 0, 0, 0, 6, 5],
        [1, 5, 6, 0, 0, 0],
    ]

    solnSixBySixSecond = [
        [2, 3, 1, 5, 4, 6],
        [5, 6, 4, 3, 2, 1],
        [3, 1, 2, 6, 5, 4],
        [6, 4, 5, 2, 1, 3],
        [4, 2, 3, 1, 6, 5],
        [1, 5, 6, 4, 3, 2],
    ]

    nineByNine = [
        [0, 0, 0, 8, 4, 0, 6, 5, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 5, 2, 0, 1],
        [0, 3, 4, 0, 7, 0, 5, 0, 6],
        [0, 6, 0, 2, 5, 1, 0, 3, 0],
        [5, 0, 9, 0, 6, 0, 7, 2, 0],
        [1, 0, 8, 5, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 4, 0],
        [0, 5, 2, 0, 8, 6, 0, 0, 0],
    ]

    nineBynineEasy = [
        [7, 2, 1, 8, 0, 9, 6, 0, 3],
        [3, 8, 5, 0, 1, 2, 4, 7, 9],
        [9, 4, 6, 7, 3, 5, 2, 8, 1],
        [2, 3, 4, 9, 7, 8, 5, 1, 6],
        [8, 6, 7, 0, 5, 1, 9, 3, 4],
        [5, 1, 9, 4, 6, 3, 7, 2, 8],
        [1, 7, 0, 5, 9, 4, 3, 6, 2],
        [6, 9, 3, 1, 2, 7, 8, 4, 5],
        [4, 5, 2, 3, 0, 6, 1, 9, 7],
    ]

    nineBynineSoln = [
        [7, 2, 1, 8, 4, 9, 6, 5, 3],
        [3, 8, 5, 6, 1, 2, 4, 7, 9],
        [9, 4, 6, 7, 3, 5, 2, 8, 1],
        [2, 3, 4, 9, 7, 8, 5, 1, 6],
        [8, 6, 7, 2, 5, 1, 9, 3, 4],
        [5, 1, 9, 4, 6, 3, 7, 2, 8],
        [1, 7, 8, 5, 9, 4, 3, 6, 2],
        [6, 9, 3, 1, 2, 7, 8, 4, 5],
        [4, 5, 2, 3, 8, 6, 1, 9, 7],
    ]

    sudoku_driver(fourByFour, solnFourByFour)
    sudoku_driver(sixBySixFirst, solnSixBySixFirst)
    sudoku_driver(sixBySixSecond, solnSixBySixSecond)
    sudoku_driver(nineByNine, nineBynineSoln)


if(__name__ == '__main__'):
    runApp()

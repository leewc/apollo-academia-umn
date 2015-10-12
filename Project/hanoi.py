from queue import Queue
import pdb 

"""This is where the problem is defined. Initial state, goal state and other information that can be got from the problem"""


class Problem(object):

    def __init__(self, initial, goal=None):
        """This is the constructor for the Problem class. It specifies the initial state, and possibly a goal state, if there is a unique goal.  You can add other arguments if the need arises"""
        self.initial = initial  # Lists of Lists
        
        if goal is not None:
            self.goal = goal
        else: 
            # goal state is the initial state 1st peg on another peg, sort it just in case
            self.goal = sorted(self.initial[0], reverse=True) 

        assert(len(initial) == 3)  # Can't have more than 3 pegs
        self.pegs = [i for i in range(0, len(initial))]
        # Get number of disks
        self.numberOfDisks = len(self.initial[0])
        # Add sentinel value
        self.sentinel = self.initial[0][0] + 1

        for peg in self.initial:
            peg.insert(0, self.sentinel)

        self.goal.insert(0, self.sentinel)

    def printHanoi(self):
        for peg in self.initial:
            print(peg, end=" ")
        print("","Sentinel Value:", self.sentinel)

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        actions = []
        tops = [peg[-1] for peg in state]
        idxSmallest = tops.index(1) #Since smallest(1) is always on top, this will always be true
        moveSmallTo = list(self.pegs) 
        moveSmallTo.remove(idxSmallest) #Empty move if move to itself

        nextSmall = min(tops[moveSmallTo[0]], tops[moveSmallTo[1]])
        idxNextSmall = tops.index(nextSmall)
        for move in moveSmallTo:
                actions.append(Action(idxSmallest, move, 1))

        if nextSmall is self.sentinel:
            # 1 disk to move only (cannot move sentinel)
            return actions
        else:
            moveSmallTo.remove(idxNextSmall)
            assert(len(move) == 1)
            actions.append(Action(idxNextSmall, move[0], nextSmall))
            return actions


    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        result = state[:]   # Make a copy
        value = result[action.src].pop()
        print(value, " vs ", action.value)
        assert(value == action.value)
        if value is self.sentinel:
            raise(ValueError,"Attempted to Move Sentinel Value")
        result[action.dest].append(value)
        return result


    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        if state[0][0] is not self.sentinel:
            return False
        elif state[1] is not self.goal and state[2] is not self.goal:
            return False
        return True


class Action:
    def __init__(self, src, dest, value):
        self.src = src
        self.dest = dest
        self.value = value

    def __str__(self):
        return "Move " + self.value + " from peg " + self.src + " to peg " + self.dest


class Node:

    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state"""

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action.
        Update the node parameters based on constructor values"""
        # update(self, state=state, parent=parent, action=action, depth=0)
        # If depth is specified then depth of node will be 1 more than the
        # depth of parent
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        # List the nodes reachable in one step from this node.
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        return Node(next, self, action)


def breadth_first_search(problem):
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node.state):
        return node
    # Create a Queue to store all nodes of a particular level.
    frontier = Queue()
    frontier.put(node)

    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test
    # criteria are met
    while frontier:
        # Remove from frontier, for analysis
        node = frontier.get()
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes
        # here
        for child in node.expand(problem):
            # If child node meets Goal_Test criteria
            if problem.goal_test(child.state):
                return child
            # Add every new child to the frontier
            frontier.put(child)
    return None

x = Problem([[3,2,1],[],[]])
x.printHanoi()

y = breadth_first_search(x)
print(y.state)
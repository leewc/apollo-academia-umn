from queue import Queue
import time
import pdb 

import itertools # for bidirectional

"""     BEGIN DEFINITION FOR PROBLEM FRAMEWORKS         """
class Problem(object):
    """This is where the problem is defined. Initial state, goal state and other information that can be got from the problem"""

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
        # Make sentinel value
        self.sentinel = self.initial[0][0] + 1

        for peg in self.initial:
            peg.insert(0, self.sentinel)

        self.goal.insert(0, self.sentinel)
        self.nodesTouched = 0

        self.visited = dict() #keep visited states

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        def check(action):
            """Check to see if we'll end up in a loop by applying the action.
            """
            result = [peg[:] for peg in state]
            value = result[action.src].pop()
            # if value < result[action.dest][-1] or result[action.dest] == self.sentinel:
            #     return True
            result[action.dest].append(value)
            if str(result) in self.visited:
                return False
            return True

        actions = []
        tops = [peg[-1] for peg in state]
        idxSmallest = tops.index(1) #Since smallest(1) is always on top, this will always be true
        moveSmallTo = list(self.pegs) 
        moveSmallTo.remove(idxSmallest) #Empty move if move to itself

        nextSmall = min(tops[moveSmallTo[0]], tops[moveSmallTo[1]])
        idxNextSmall = tops.index(nextSmall)
        for move in moveSmallTo:
            action = Action(idxSmallest, move, 1)
            if check(action):
                actions.append(action)

        if nextSmall is self.sentinel:
            # 1 disk to move only (cannot move sentinel)
            return actions
        else:
            moveSmallTo.remove(idxNextSmall)
            assert(len(moveSmallTo) == 1)
            action = Action(idxNextSmall, moveSmallTo[0], nextSmall)
            if check(action):
                actions.append(action)
            return actions        

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        result = [peg[:] for peg in state]   # Make a copy - fixed
        value = result[action.src].pop()
        assert(value == action.value)
        if value is self.sentinel:
            raise(ValueError("Attempted to Move Sentinel Value"))
        result[action.dest].append(value)
        # print(action, end=" ")
        # print(result)
        return result

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        if state[0][-1] != self.sentinel:
            return False
        # if state[1] == self.goal or state[2] == self.goal: # nah just one is goal
        if state[2] == self.goal:
            return True
        return False

class BiDirectionalProblem(Problem):
    """Similar Problem to the original class, but handles which side to arrange disks to.
    Inherits from Problem other than Actions, goal_test is not used as the goal is when 2 identical states are found
    Note 2 visited dictionaries are needed else can not test for membership in the another set
    """

    def __init__(self, initial, goal=None):
        """This is the constructor for the Problem class. It specifies the initial state, and possibly a goal state, if there is a unique goal.  You can add other arguments if the need arises"""
        super().__init__(initial)

        if goal is not None:
            self.goal = goal
        else: 
            # goal state is the initial state 1st peg on another peg, sort it just in case
             self.goal = [peg[:] for peg in self.initial]
             self.goal.reverse() # in place hence the copy

        self.StartVisited = dict()
        self.GoalVisited = dict()

    def actions(self, state, fromStart):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.

        FromEnd is a boolean that will perform a separate action if starting from the end
        Exact code other than use of fromState routines. 
        Makes code more efficient without having to check for fromStart existence even on BFS.
        """

        def check(action):
            """Check to see if we'll end up in a loop by applying the action.
            """
            result = [peg[:] for peg in state]
            value = result[action.src].pop()
            result[action.dest].append(value)
            if fromStart:
                if self.StartVisited.get(str(result), None) is not None:
                    return False
            else:
                if self.GoalVisited.get(str(result), None) is not None:
                    return False
            return True

        actions = []
        tops = [peg[-1] for peg in state]
        idxSmallest = tops.index(1) #Since smallest(1) is always on top, this will always be true
        moveSmallTo = list(self.pegs) 
        moveSmallTo.remove(idxSmallest) #Empty move if move to itself

        nextSmall = min(tops[moveSmallTo[0]], tops[moveSmallTo[1]])
        idxNextSmall = tops.index(nextSmall)
        for move in moveSmallTo:
            action = Action(idxSmallest, move, 1)
            if check(action):
                actions.append(action)

        if nextSmall is self.sentinel:
            # 1 disk to move only (cannot move sentinel)
            return actions
        else:
            moveSmallTo.remove(idxNextSmall)
            assert(len(moveSmallTo) == 1)
            action = Action(idxNextSmall, moveSmallTo[0], nextSmall)
            if check(action):
                actions.append(action)
            return actions

"""     END DEFINITION FOR PROBLEM FRAMEWORKS           """

class Action:
    def __init__(self, src, dest, value):
        self.src = src
        self.dest = dest
        self.value = value # TODO: Can also remove this one dev is stable.

    def __str__(self):
        return "Move " + str(self.value) + " from peg " + str(self.src) + " to peg " + str(self.dest)

    def __cmp__(self, other): # not used
        return (self.src == other.src) and (self.dest == other.dest) and (self.value and other.value)

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

    def expand(self, problem, fromStart=None):
        # List the nodes reachable in one step from this node.
        if fromStart is None:
            return [self.child_node(problem, action)
                    for action in problem.actions(self.state)]
        else:
            return [self.child_node(problem, action)
                    for action in problem.actions(self.state, fromStart)]

    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        # print("Depth ", self.depth)
        return Node(next, self, action)

"""     BEGIN ALGORITHMS                                """
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
    while not frontier.empty():
        # Remove from frontier, for analysis
        node = frontier.get()
        problem.nodesTouched +=1
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes
        # here
        problem.visited[str(node.state)] = 1 # add to visited nodes
        for child in node.expand(problem):
            # If child node meets Goal_Test criteria
            if problem.goal_test(child.state):
                return child
            # Add every new child to the frontier
            frontier.put(child)
    return None


def bidirectional_BFS(problem): # where problem is biDirectionalProblem instance 

    def stitch(nodeS, nodeG):
        # NodeG has a bunch of nodes that point to GoalNode
        # NodeS has a bunch of nodes that point to InitialNode
        # Change direction of parent refs in NodeG group to point to NodeS
        # nodeS.state == nodeG.state
        newParent = nodeS
        current = nodeG.parent # snip off the same state
        while current.parent is not None:
            nextNode = current.parent # hold on to parent refs
            current.depth = newParent.depth + 1 # this line updates the depth correctly
            current.parent = newParent #flip refs

            newParent = current # shift down
            current = nextNode
        #Finally, point current (last node to the right parent)
        current.parent = newParent
        return current #at the end this is the last node

    startNode = Node(problem.initial)
    goalNode = Node(problem.goal)

    if startNode.state == goalNode.state:
        return startNode # same thing, unlikely but an edge case 

    frontierFromStart = []
    frontierFromGoal = []

    frontierFromStart.append(startNode)
    frontierFromGoal.append(goalNode)

    while frontierFromStart and frontierFromGoal: # Both must not be empty
        nodeFromStart = frontierFromStart.pop(0)
        nodeFromGoal = frontierFromGoal.pop(0)
        problem.nodesTouched +=2
        # print("Node from start ", nodeFromStart.state, end="")
        # print(" Node from goal ", nodeFromGoal.state)

        #Hold references so we can grab it out in O(1)
        problem.StartVisited[str(nodeFromStart.state)] = nodeFromStart
        problem.GoalVisited[str(nodeFromGoal.state)] = nodeFromGoal

        listFromStart = nodeFromStart.expand(problem, True)
        listFromGoal = nodeFromGoal.expand(problem, False)

        for childFromStart in listFromStart:
            # Previously had a bunch of for-loop and if-conditionals in attempt 
            # to short circuit the checking in frontier and expanded nodes,
            # turns out that makes runtime worse as the frontier gets bigger 
            # since it's always O(n) everytime, just remove it all and check at the end.
            # (On 8 disks it went from 27.76 to 3.5s)
            connectorNode = problem.GoalVisited.get(str(childFromStart.state), None) 
            if connectorNode is not None:
                return stitch(childFromStart, connectorNode)

        frontierFromStart += listFromStart
        frontierFromGoal += listFromGoal

    return None

def depth_first_search(problem):
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = []
    frontier.append(node)

    while frontier:
        node = frontier.pop() # get last item, stack
        problem.visited[str(node.state)] = 1 # add to visited nodes
        problem.nodesTouched +=1
        for child in node.expand(problem):
            # If child node meets Goal_Test criteria
            if problem.goal_test(child.state):
                return child
            # Add every new child to the frontier
            frontier.append (child)
    return None        

def iterative_deepening_DFS(problem):
    # http://web.stanford.edu/~msirota/soco/inter.html
    MAX_DEPTH = 0
    node = Node(problem.initial)

    frontier = []
    frontier.append(node)

    while frontier:
        currentNode = frontier.pop() # get last item, stack
        if currentNode.depth <= MAX_DEPTH:
            problem.visited[str(currentNode.state)] = 1 # add to visited nodes
            problem.nodesTouched +=1

            if problem.goal_test(currentNode.state):
                return currentNode

            for child in currentNode.expand(problem):
                frontier.append (child)
        else:
            # Reached max depth, start over
            frontier.clear()
            problem.visited.clear()
            frontier.append(node)
            MAX_DEPTH += 1
    return None        

class Hanoi:
    """Hanoi object based on number of disks. Makes Problem object with a list of lists"""
    def __init__(self,numberOfDisks):
        self.problem = Problem([ [i for i in range(numberOfDisks, 0, -1)], list(), list() ])
        self.bidirectionalProblem = BiDirectionalProblem([ [i for i in range(numberOfDisks, 0, -1)], list(), list() ])
        self.minSteps = 2**numberOfDisks - 1
        self.sentinel = numberOfDisks + 1
        self.numberOfDisks = numberOfDisks
        self.solnNode = None

    def stripSentinel(self, board):
        return [[i for i in peg 
                    if i != self.sentinel] 
                    for peg in board]

    def printHanoi(self, board, strip=False):
        if strip: 
            board = self.stripSentinel(board)
        for peg in board:
            print(peg, end=" ")
        if self.sentinel in peg:
            print("","Sentinel Value:", self.sentinel)
        else:
            print("")

    def printProblem(self):
        self.printHanoi(self.problem.initial, True)

    def solveProblem(self,alg):
        if alg is "Bidirectional_BFS":
            self.bidirectionalProblem.StartVisited.clear()
            self.bidirectionalProblem.GoalVisited.clear() #reset
        else:
            self.problem.visited.clear() #reset
        self.problem.nodesTouched = 0
        # print('Solving Hanoi Puzzle with ', self.numberOfDisks, ' disks using ', alg)

        if alg is "Breadth_First_Search":
            self.solnNode = breadth_first_search(self.problem)
        elif alg is "Depth_First_Search":
            self.solnNode = depth_first_search(self.problem)
        elif alg is "Iterative_Deepening_DFS":
            self.solnNode = iterative_deepening_DFS(self.problem)
        elif alg is "Bidirectional_BFS":
            self.solnNode = bidirectional_BFS(self.bidirectionalProblem)
            # have to transfer this over since we have a different instance, so it prints
            self.problem.nodesTouched = self.bidirectionalProblem.nodesTouched
        else:
            print("Parameter Not Recognized, please try again.")
            return

        if self.solnNode is not None:
            print("Solving Complete, number of touched nodes", self.problem.nodesTouched)
            return self.solnNode
        else:
            raise(ValueError("Solution Not Found -- This should not happen."))

   
    def printSolution(self):
        if self.solnNode is None:
            print("Please run solve functions first.")
        else:
            print("Solution: \t")
            self.printHanoi(self.solnNode.state, True)

    def printSolutionPath(self):
        currentNode = self.solnNode
        print("Path: \n <END>", end="")
        while currentNode.parent is not None:
            print(self.stripSentinel(currentNode.state), "<- ", end="")
            currentNode = currentNode.parent
        print(self.stripSentinel(currentNode.state), "<-<START>")

    
def runTests():
    x = Hanoi(8)
    x.printProblem()
    
    print("START BFS SOLVE")
    t = time.process_time()
    x.solveProblem("Breadth_First_Search")
    print("Elapsed time for soln: ", time.process_time() - t)
    # print("COMPLETE BFS SOLVE: Solution is: ")
    # x.printSolution()
    # # x.printSolutionPath()

    print("START Bidirectional BFS Solve")
    t = time.process_time()
    x.solveProblem("Bidirectional_BFS")
    print("Elapsed time for soln: ", time.process_time() - t)
    # print("COMPLETE Bidirectional BFS SOLVE: Solution is: ")
    # x.printSolution()
    # x.printSolutionPath()

    print("START DFS Solve")
    t = time.process_time()
    x.solveProblem("Depth_First_Search")
    print("Elapsed time for soln: ", time.process_time() - t)
    # print("COMPLETE DFS SOLVE: Solution is: ")
    # x.printSolution()

    print("START IDDFS Solve")
    t = time.process_time()
    x.solveProblem("Iterative_Deepening_DFS")
    print("Elapsed time for soln: ", time.process_time() - t)
    # print("COMPLETE DFS SOLVE: Solution is: ")
    # x.printSolution()

if(__name__ == '__main__'):
    runTests()
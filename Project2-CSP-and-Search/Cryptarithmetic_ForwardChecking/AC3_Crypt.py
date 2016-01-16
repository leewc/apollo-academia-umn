__author__ = 'Sean'
from random import randrange
# Sean Lin
# Problem : Cryptarithmetic

import time
import sys
import functools
import queue
from testRead import *
# The primary problem set-up consists of "variables" and "constraints":
#   "variables" are a dictionary of constraint variables (of type ConstraintVar), example variables['A1']
#   "constraints" are a set of binary constraints (of type BinaryConstraint)

# First, Node Consistency is achieved by passing each UnaryConstraint of each variable to nodeConsistent().
# Arc Consistency is achieved by passing "constraints" to Revise().
# AC3 is not fully implemented, Revise() needs to be repeatedly called until all domains are reduced to a single value

class ConstraintVar:
    # instantiation example: ConstraintVar( [1,2,3],'A1' )
    # MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain
    def __init__( self, d, n ):
        self.domain = [ v for v in d ]
        self.name = n
        self.neighbors = []

class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__( self, v, fn ):
        self.var = v
        self.func = fn

class BinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y )
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn

class TernaryConstraint:
    # v1, v2 and v3 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, A3 lambda x,y,z: x != y != z )
    def __init__(self, v1, v2, v3, fn):
        self.var1 = v1
        self.var2 = v2
        self.var3 = v3
        self.func = fn

def allDiff( constraints, v ):
    # generate a list of constraints that implement the allDiff constraint for all variable combinations in v
    # constraints is a preconstructed list. v is a list of ConstraintVar instances.
    # call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y: x != y
    for i in range( len( v ) ):
        for j in range( len( v ) ):
            if ( i != j ) :
                constraints.append( BinaryConstraint( v[ i ], v[ j ], fn ) )
                if not ( v[i] in v[j].neighbors ):
                    v[j].neighbors.append(v[i])
                if not ( v[j] in v[i].neighbors ):
                    v[i].neighbors.append(v[j])

# Set up cryptarithmetic constraints
def setUpCrypt(variables, constraints, words, letters, op):
    # A variable represents a different letter
    domain = [i for i in range(10)]

    for l in letters:
        variables[l] = ConstraintVar(domain, l)

    allCons = []
    for k in variables.keys():
        allCons.append( variables[k] )

    # Constrain all letters to different digits
    allDiff( constraints, allCons )

    # Set max word length, constrain all first letters to not 0
    maxWordLength = 0
    maxVarLength = 0
    for w in range(len(words)):
        constraints.append(UnaryConstraint( variables[words[w][0]], lambda x: x != 0 ))

        if len(words[w]) > maxWordLength:
            maxWordLength = len(words[w])
        if len(words[w]) > maxVarLength and w < len(words)-1:
            maxVarLength = len(words[w])
    prevNumVars = 1

    # Constrain columns to add up
    for i in range(maxWordLength):
        varLetters = {}
        numVars = 0
        # Count number of times each letter to be added appears in column
        for j in range(len(words)-1):
            index = len(words[j]) - i - 1
            if i < len(words[j]):
                numVars +=1
                vlKeys = list(varLetters.keys())
                if (vlKeys.count(words[j][index]) == 0):
                    varLetters[words[j][index]] = 1
                else:
                    varLetters[words[j][index]] += 1

        # Take the letters in solution to account
        j = len(words)-1
        index = len(words[j]) - i - 1
        if i < len(words[j]):
            vlKeys = list(varLetters.keys())
            if (vlKeys.count(words[j][index]) == 0):
                if len(vlKeys) == 0:
                    #print(prevNumVars)
                    constraints.append(UnaryConstraint( variables[words[j][index]], lambda x, p = prevNumVars: x < p ))
                else:
                    varLetters[words[j][index]] = -1
            else:
                varLetters[words[j][index]] -= 1
        #print(varLetters)

        vlKeys = list(varLetters.keys())


        # Constraint the letters. In each column, the sum of each letter to be added, minus the letter in the answer
        # Must be a multiple of 10, or slightly less than a multiple of 10 if carrying digits are taken into account
        # if 3 letters in a column, ternary constraint
        if len(vlKeys) == 3:
            if not ( variables[vlKeys[1]] in variables[vlKeys[2]].neighbors ):
                variables[vlKeys[2]].neighbors( variables[vlKeys[1]])
            if not ( variables[vlKeys[0]] in variables[vlKeys[2]].neighbors ):
                variables[vlKeys[2]].neighbors( variables[vlKeys[0]])
            if not ( variables[vlKeys[1]] in variables[vlKeys[0]].neighbors ):
                variables[vlKeys[0]].neighbors( variables[vlKeys[1]])
            if not ( variables[vlKeys[2]] in variables[vlKeys[0]].neighbors ):
                variables[vlKeys[0]].neighbors( variables[vlKeys[2]])
            if not ( variables[vlKeys[0]] in variables[vlKeys[1]].neighbors ):
                variables[vlKeys[1]].neighbors( variables[vlKeys[0]])
            if not ( variables[vlKeys[2]] in variables[vlKeys[1]].neighbors ):
                variables[vlKeys[1]].neighbors( variables[vlKeys[2]])

            #print(vlKeys[0],varLetters[vlKeys[0]],vlKeys[1],varLetters[vlKeys[1]],vlKeys[2],varLetters[vlKeys[2]])
            constraints.append(TernaryConstraint( variables[vlKeys[0]], variables[vlKeys[1]], variables[vlKeys[2]],
                                lambda x,y,z,xv=varLetters[vlKeys[0]],yv=varLetters[vlKeys[1]],
                                       zv=varLetters[vlKeys[2]], p = prevNumVars:
                                              (x*xv + y*yv + z*zv)%10 == 0 or
                                              (x*xv + y*yv + z*zv)%10 >= 10-(p-1)))
            constraints.append(TernaryConstraint( variables[vlKeys[2]], variables[vlKeys[1]], variables[vlKeys[0]],
                                lambda x,y,z,xv=varLetters[vlKeys[2]],yv=varLetters[vlKeys[1]],
                                       zv=varLetters[vlKeys[0]], p = prevNumVars:
                                              (x*xv + y*yv + z*zv)%10 == 0 or
                                              (x*xv + y*yv + z*zv)%10 >= 10-(p-1)))
            constraints.append(TernaryConstraint( variables[vlKeys[1]], variables[vlKeys[0]], variables[vlKeys[2]],
                                lambda x,y,z,xv=varLetters[vlKeys[1]],yv=varLetters[vlKeys[0]],
                                       zv=varLetters[vlKeys[2]], p = prevNumVars:
                                              (x*xv + y*yv + z*zv)%10 == 0 or
                                              (x*xv + y*yv + z*zv)%10 >= 10-(p-1)))

        # binary constraint
        elif len(vlKeys) == 2:

            if not ( variables[vlKeys[0]] in variables[vlKeys[1]].neighbors ):
                variables[vlKeys[1]].neighbors( variables[vlKeys[0]])
            if not ( variables[vlKeys[1]] in variables[vlKeys[0]].neighbors ):
                variables[vlKeys[0]].neighbors( variables[vlKeys[1]])

            #print(vlKeys[0],varLetters[vlKeys[0]],vlKeys[1],varLetters[vlKeys[1]])
            constraints.append(BinaryConstraint( variables[vlKeys[0]], variables[vlKeys[1]],
                                lambda x,y,xv=varLetters[vlKeys[0]],yv=varLetters[vlKeys[1]], p = prevNumVars:
                                              (x*xv + y*yv)%10 == 0 or
                                              (x*xv + y*yv)%10 >= 10-(p-1)))
            constraints.append(BinaryConstraint( variables[vlKeys[1]], variables[vlKeys[0]],
                                lambda x,y,xv=varLetters[vlKeys[1]],yv=varLetters[vlKeys[0]], p = prevNumVars:
                                              (x*xv + y*yv)%10 == 0 or
                                              (x*xv + y*yv)%10 >= 10-(p-1)))

        #unary
        elif len(vlKeys) == 1:
            #print(vlKeys[0],varLetters[vlKeys[0]])
            constraints.append(UnaryConstraint( variables[vlKeys[0]],
                                lambda x,xv=varLetters[vlKeys[0]], p = prevNumVars:
                                              (x*xv)%10 == 0 or
                                              (x*xv)%10 >= 10-(p-1)))


        prevNumVars = numVars

def Revise( cv , variables):
    revised = False
    domain_list = []
    if ( type( cv ) == TernaryConstraint ):

        if not ( cv.var2 in cv.var1.neighbors ):
            cv.var1.neighbors.append( cv.var2 )
        if not ( cv.var3 in cv.var1.neighbors ):
            cv.var1.neighbors.append( cv.var3 )
        if not ( cv.var1 in cv.var2.neighbors ):
            cv.var1.neighbors.append( cv.var1 )
        if not ( cv.var3 in cv.var2.neighbors ):
            cv.var1.neighbors.append( cv.var3 )
        if not ( cv.var1 in cv.var3.neighbors ):
            cv.var1.neighbors.append( cv.var1 )
        if not ( cv.var2 in cv.var3.neighbors ):
            cv.var1.neighbors.append( cv.var2 )

        dom1 = list( variables[cv.var1.name].domain )
        dom2 = list( variables[cv.var2.name].domain )
        dom3 = list( variables[cv.var3.name].domain )
        # for each value in the domain of variable 1
        for x in dom1:
            check = 0
            # for each value in the domain of variable 2
            for y in dom2:
                # for each value in the domain of variable 3
                for z in dom3:
                # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x
                    if ( cv.func( x, y, z ) == False ):
                        check += 1
                    if ( check == len( dom2 ) * len( dom3 ) ):
                        variables[cv.var1.name].domain.remove( x )
                        revised = True

    elif ( type( cv ) == BinaryConstraint ):
        if not ( cv.var2 in cv.var1.neighbors ):
            cv.var1.neighbors.append( cv.var2 )
        if not ( cv.var1 in cv.var2.neighbors ):
            cv.var1.neighbors.append( cv.var1 )

        dom1 = list( variables[cv.var1.name].domain)
        dom2 = list( variables[cv.var2.name].domain)
        # for each value in the domain of variable 1
        for x in dom1:
            check = 0
            # for each value in the domain of variable 2
            for y in dom2:
            # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x

                if ( cv.func( x, y ) == False):
                    check += 1
                if ( check == len( dom2 ) ):

                    variables[cv.var1.name].domain.remove( x )
                    revised = True

    elif ( type( cv ) == UnaryConstraint ):
        dom = list( variables[cv.var.name].domain)
        # for each value in the domain of variable
        for x in dom:
            if ( cv.func( x ) == False ):
                variables[cv.var.name].domain.remove( x )
                revised = True

    return revised

def nodeConsistent( uc ):
    domain = list(uc.var.domain)
    for x in domain:
        if ( False == uc.func(x) ):
            uc.var.domain.remove(x)

def printDomains( vars, n=3 ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % n ):
            print(' ')

# Sets up the Problem
def setupProblem():
    # create a dictionary of ConstraintVars keyed by names in VarNames.
    constraints = []
    variables = dict()

    op, words, letters = readCrypt()
    # t = time.time()
    setUpCrypt(variables, constraints, words, letters, op)

    print("Initial Domains")
    printDomains( variables )
    return variables, constraints, words

# Runs ac3 again. Only ques neighbors of var, unless var is none
def AC3(constraints, variables, var = None):
    #transferConstraint( cons, constraints, variables )
    que = queue.LifoQueue()

    # Initialize the queue by putting all the constraint variables in the queue

    if var != None:
        for c in constraints:
            if type(c) == TernaryConstraint:
                if c.var2.name == var.name or c.var3.name == var.name:
                    que.put(c)
            elif type(c) == BinaryConstraint:
                if c.var2.name == var.name:
                    que.put(c)
    else:
        for c in constraints:
            que.put(c)


    while not( que.empty() ):
        constr = que.get()
        if Revise( constr, variables ):
            que.put(constr)

    #print("\nFinal Domains")
    #printDomains( variables )
    rInt = randrange(1,6)
    dString = ("."*rInt) + (" " * (6-rInt))
    #print(dString)
    print("\rSolving" + dString, end ="")

    # returns whether all domains reduced to 1, or has an empty domain
    for k in list(variables.keys()):
        if len(variables[k].domain) == 0:
            return -1
        elif len(variables[k].domain) > 1:
            return 0
    return 1

# const = []
# vars = dict()
# setupAC3(const, vars)
# AC3(const, vars)






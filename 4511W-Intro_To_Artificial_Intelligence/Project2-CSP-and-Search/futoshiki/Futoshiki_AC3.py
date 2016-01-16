# Wen Chuan Lee (4927941)
# Project Part 2 : Comparison of CSP and Search Algorithms
# Problem : Futoshiki

# Code base provided by Sihan Chen (thanks!)

import sys
import functools
import queue
from functools import reduce
from testRead import *
import math
import pdb

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
        self.var1 = v
        self.func = fn

class BinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y )
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
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

class CSP():

    def __init__( self, size ):
        self.variables, self.constraints = self.SetupCSP( size )

    def setUpNeighbor(self, varname, variables, size ):
        # Helper function for SetupCSP to make the neighbors
        # Add other elements in one element's row to its neighbor
        for i in range( 0, size ):
            for j in range( 0, size ):
                for k in range( 0, size ):
                    if k != j:
                        variables[ varname[ i ][ j ] ].neighbors.append( variables[ varname[ i ][ k ] ] )

        # Add other elements in one element's column to its neighbor
        for j in range( 0, size ):
            for i in range( 0, size ):
                for k in range( 0, size ):
                    if k != i:
                        variables[ varname[ i ][ j ] ].neighbors.append( variables[ varname[ k ][ j ] ] )

    def SetupCSP( self, size ):
        ''' This function is used to set up variables and their initial domain. '''
        if size <= 1:
            print( "Unsolvable Futoshiki")
            sys.exit()
        rows = []
        cols = []
        domain = []

        variables = dict()
        constraints = []
        
        # BEGIN Set up the Problem Framework

        # Create a list with upper case character in alphabetical order 
        for c in ( chr( i ) for i in range( 65, 65 + size ) ):
            rows.append( c )
            
        # Create a list with increasing integer from 1 to size 
        for i in range( 1, size+1 ):
            cols.append( str( i ) )

        # Create a list with initial domain of each variables.
        for i in range( 1, size+1 ):
            domain.append( i )
            
        # Create name for all the variables, such as A1, A2, A3..... 
        varNames = [ x + y for x in rows for y in cols ]

        for var in varNames:
            variables[ var ] = ConstraintVar( domain, var )

        # END Set up Problem Framework 
        # varname is a 2 dimensional list used in setUpNeighbor function 
        varname = []
        k = 0
        for i in range( 0, size ):
            new = []
            for j in range( 0, size ):
                new.append( varNames[ k ] )
                k = k + 1
            varname.append( new )

        self.setUpNeighbor(varname, variables, size )    
        
        """ Set up AllDiff Constraints Here. """
        for r in rows:
            aRow = []
            for k in variables.keys():
                if ( str(k).startswith(r) ):
                    # Accumulate all ConstraintVars contained in row 'r'
                    aRow.append( variables[k] )
            # Add the allDiff constraints among those row elements
            allDiff( constraints, aRow )
        
        # For example, for cols 1,2,3 (with keys A1,B1,C1 ...) generate A1!=B1!=C1, A2!=B2 ...
        for c in cols:
            aCol = []
            for k in variables.keys():
                key = str(k)
                # The column is indicated in the 2nd character of the key string
                if ( key[1] == c ):
                    # Accumulate all ConstraintVars contained in column 'c'
                    aCol.append( variables[k] )
            allDiff( constraints, aCol )
   
        return variables, constraints

def transferConstraint( cons, csp ):
    for c in cons:
        ctype = c[ 0 ]
        # When ctype = 0, constraints are either x < y or x > y 
        if ctype == 0:
            # lvar and rvar are variables on the left side and right side of the comparison operator respectively.
            lvar = c[ 1 ]
            rvar = c[ 2 ]
            bc = BinaryConstraint( csp.variables[ lvar ], csp.variables[ rvar ], c[ 3 ] )
            csp.constraints.append( bc )

        # When ctype = 1, constraints are assignment.
        elif ctype == 1:
            var = c[ 1 ]
            # print("MAKING", c[2])
            uc = UnaryConstraint( csp.variables[ var ], c[ 2 ] )
            csp.constraints.append( uc )
                     
def Revise( cv ):
    revised = False 
    if ( type( cv ) == BinaryConstraint ):
        if not ( cv.var2 in cv.var1.neighbors ):
            cv.var1.neighbors.append( cv.var2 )
        if not ( cv.var1 in cv.var2.neighbors ):
            cv.var1.neighbors.append( cv.var1 )
                                                                     
        dom1 = list( cv.var1.domain )
        dom2 = list( cv.var2.domain )
        # for each value in the domain of variable 1
        for x in dom1:
            check = False
            # for each value in the domain of variable 2
            for y in dom2:
                if y != x:
                # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x      
                    if not ( cv.func( x, y ) == False):
                        check = True
                        break     
            if ( check == False ):
                # print("Removing Domain: ", x, " in BC with vars: ", cv.var1.name, cv.var2.name, "of Func ", inspect.getsource(cv.func))
                cv.var1.domain.remove( x )
                revised = True   

    elif ( type( cv ) == UnaryConstraint ):                                                                              
        dom = list( cv.var1.domain )
        # for each value in the domain of variable
        for x in dom:
            # print("val ", x, cv.func(x), cv.var1.name)
            if ( cv.func( x ) == False ):
                # print("Removing Domain: ", x, " in UC with var: " ,cv.var1.name, "of Func ", inspect.getsource(cv.func))
                cv.var1.domain.remove( x )
                revised = True
    return revised


def printDomains( vars, size ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % size ):
            print(' ')


def AC3():
    # Load data from file
    size, cons = readFutoshiki()
    # Set up the Problem with AllDiff Constraints
    csp = CSP (size)
    # Copy over constraints into the Problem
    transferConstraint( cons, csp )

    # Print Initial Domains
    print("Initial Domains:")
    printDomains(csp.variables, size)

    que = queue.LifoQueue()

    # Initialize the queue by putting all the constraint variables in the queue
    for constraint in csp.constraints:
        que.put( constraint )

    while not( que.empty() ):
        # print(que.qsize())
        constr = que.get()

        if Revise( constr ):
            if constr.var1.domain == []:
                print("Empty domain.")
                return False
            
            if type( constr ) == BinaryConstraint:
                for constraint in csp.constraints:
                    if type( constraint ) == BinaryConstraint and \
                        constraint.var1 != constr.var1 and \
                        constraint.var1 != constr.var2 and \
                        constraint.var2 == constr.var1:
                        que.put( constraint )
        # else:
            # print("Not revised")
    print("\nHere are the domains after AC3:")                       
    printDomains( csp.variables, size )


AC3()
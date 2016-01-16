# Wen Chuan Lee
# Project Part 2 : Comparison of CSP and Search Algorithms
# Problem : Cryptarithmetic

import sys
import functools
import queue
from functools import reduce
from testRead import *
import AC3_Crypt
import math
import copy
import pdb
############################################################

class ConstraintVar:
    # instantiation example: ConstraintVar( [1,2,3],'A1' )
    # MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain
    def __init__( self, d, n ):
        self.domain = [ v for v in d ]
        self.name = n
        
class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__( self, v1, fn ):
        self.var1 = v1
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

    def __init__( self ):
        self.variables, self.constraints, self.words = self.setupCSP()

    def setupCSP( self ):
        ''' This function is used to set up variables and their initial domain. '''
        return AC3_Crypt.setupProblem()

    def reset( self, var, value, assignment, csp ):
        for variable in assignment[ var ][ 1 ]:
            for l in assignment[ var ][ 1 ][ variable ]:
                csp.variables[ variable ].domain.append( l )
        assignment[ var ][ 0 ] = 0        


def MRV( csp, assignment ):
    # Select the variable with fewest possible value, that is fewest value in its domain.
    domainLen = []
    for var in csp.variables:
        # Only select from unassigned variables
        if ( assignment[ var ][0] == 0 ):
            dlen = len( csp.variables[ var ].domain )
            domainLen.append( ( var, dlen ) )
            
    # Determine the minimum domain value

    minVar = domainLen[ 0 ]
    for index in range( 0, len( domainLen ) ):
        if domainLen[ index ][ 1 ] < minVar[ 1 ]:
            minVar = domainLen[ index ]
    return minVar[ 0 ]     


def completeTest( assignment, csp ):
    # Calculate and add up variable values 
        sum = 0
        for i in range(len(csp.words) - 1):
            word = csp.words[i]
            if csp.variables[word[0]].domain[0]== 0:
                return False
            wordLen = len(word)
            for j in range(wordLen):
                sum += (10**j) * csp.variables[word[wordLen - j - 1]].domain[0]

        # Calculate and add up solution value
        solution = 0
        word = csp.words[len(csp.words) - 1]
        if csp.variables[word[0]].domain[0]== 0:
            return False
        wordLen = len(word)
        for j in range(wordLen):
            solution += (10**j) * csp.variables[word[wordLen - j - 1]].domain[0]

        # Return whether solution true or false
        if (solution == sum):
            return True
        else:
            return False
    
def consistentTest( var, value, csp ):
    check = False
    for c in csp.constraints:
        if ( type( c ) == AC3_Crypt.UnaryConstraint ) and c.var.name == var and c.func( value ) == False:
                return False    
        elif ( type( c ) == BinaryConstraint ):
            # Consider var's neighbor
            if c.var2.name == var:
                domain = list( c.var1.domain )
                for x in domain:
                    if c.func( x, value ):
                        check = True
                        break
            elif c.var1.name == var:
                domain = list( c.var2.domain )
                for x in domain:
                    if c.func( value, x ):
                        check = True
                        break
    return True        
            

        
def forward_checking( csp, var, assignment ):

    ''' Check all the binary constraint with var as its second variable, that is, establishing
        arc consistency for it.'''
    # pdb.set_trace()
    consist = True
    for c in csp.constraints:
        if ( type( c ) == AC3_Crypt.BinaryConstraint ):
            # Consider var's neighbor
            if c.var2.name == var:
                if c.var1.name not in assignment[ var ][ 1 ]:
                    assignment[ var ][ 1 ][ c.var1.name ] = []
                value = assignment[ var ][ 0 ]
                domain = list( c.var1.domain )
                # For each value in the domain of variable 2
                for x in domain:
                    if c.func( x, value ) == False:
                        c.var1.domain.remove( x )
                        assignment[ var ][ 1 ][ c.var1.name ].append( x )
                if not( c.var1.domain ):
                    consist = False
                    break               
    return consist
    
        
def backtracking_search( csp ):
    assignment = dict()
    # Initialize assignment
    for var in csp.variables:
        assignment[ var ] = ( 0, {} )
    return backtrack( assignment, csp )


def backtrack( assignment, csp ):
    #print(assignment)
    if completeTest( assignment, csp ):
        return assignment    
    var = MRV( csp, assignment )
    dom = copy.copy( csp.variables[ var ].domain )
    for value in dom:
        inferences = dict()
        if consistentTest( var, value, csp ):
            assignment[ var ] = [ value, inferences ]
            assignment[ var ][ 1 ][ var ] = []
            varDomain = copy.copy( csp.variables[ var ].domain )
            for val in varDomain:
                if val != value:
                    csp.variables[ var ].domain.remove( val )
                    assignment[ var ][ 1 ][ var ].append( val )
            #### THIS IS WHERE FORWARD CHECKING IS ####
            check = forward_checking( csp, var, assignment )
            if check:
                result = backtrack( assignment, csp )
                if result != False:
                    return result 
            csp.reset( var, value, assignment, csp )
    return False         
            

def printDomains( vars, size ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % size ):
            print(' ')    
                

def FC_Crypt():
    csp = CSP()
    assignment = backtracking_search( csp )
    printDomains( csp.variables, size )

        

FC_Crypt()




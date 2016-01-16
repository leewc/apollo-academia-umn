import re
import operator

# Thanks StackOverflow: http://stackoverflow.com/questions/1740726/python-turn-string-into-operator
ops = {'+': operator.add,
       '-': operator.sub,
       '*': operator.mul,
       '/': operator.truediv,
       '==': operator.eq,
       '!=': operator.ne,
       '<': operator.lt,
       '<=': operator.le,
       '>': operator.gt,
       '>=': operator.ge,
       'abs': operator.abs,
       '^': operator.pow
       }


def readFutoshiki():
    def generateLambda(value):
      return lambda x: x == value

    def generateInequalityLambda(op):
      # op is a string that maps to the dictionary of op, x and y are values
      return lambda x,y: ops[op](x,y)

    # start a dictionary of variables and a list of constraints
    vars = {}
    Cons = []
    
    # read in the file with constraints for KenKen puzzles (1 line per puzzle)
    lines = open('testFutoshiki.txt').readlines()
    testLine = 0 # test this line in file
    l = lines[testLine]
    #remove white space
    l = re.sub('[ ]','',l)
    # print('l ',l)
    
    # size of puzzle is first number on the line
    n = eval(re.findall('^\d+',l)[0])
    l = re.sub('^\d+','',l)
    print('size ',n)
    
    # find all "x Op y" 
    cs=re.findall('\w+\W+\w+',l)
    print('constraints ',cs)

    # for each, separate apart the variables, operator, and values
    for c in cs:  
        # these are x < y OR x > y
        if re.findall('\w+\d+<\w+\d+',c) or re.findall('\w+\d+>\w+\d+',c):
  
            lvar = re.findall('^\w+\d+',c)[0]
            rvar = re.findall('\w+\d+$',c)[0]
            op = re.findall('\W',c)[0]
            
            # Make a Constraint, 0 stand for situation when x < y or x > y
            # print("Making Constraint: ", op, "lvar :", lvar, "rvar :", rvar)
            #convert inequalities to lambda fn
            # Make the opposite constraint as well for CSP
            if op == '<':
              Cons.append( ( 0, rvar, lvar, generateInequalityLambda('>') ) )
            if op == '>':
              Cons.append( ( 0, rvar, lvar, generateInequalityLambda('<') ) )
            if op == '>=':
              Cons.append( ( 0, rvar, lvar, generateInequalityLambda('<=') ) )
            if op == '<=':
              Cons.append( ( 0, rvar, lvar, generateInequalityLambda('<=') ) )

            # else just add the original inequality.
            Cons.append( ( 0, lvar, rvar, generateInequalityLambda(op) ) )
            
            
        else:
            # find x = value
            if re.findall('\w+\d+=\d+',c):
                var = re.findall('^\w+\d+',c)[0]
                value = re.findall('\d+$',c)[0]
            # find value = x
            elif re.findall('\d+=\w+\d+',c):
                var = re.findall('\w+\d+$',c)[0]
                value = re.findall('^\d+$',c)[0]
            # conver equalities to lambda fn
            ## We need to use differed execution else only one lambda is selected

            # Make a Constraint, 1 stand for situation when x < y or x > y
            # print("Making Constraint: =", value, "var :", var)
            Cons.append( ( 1, var, generateLambda(eval(value))))
            
    return n, Cons 


if __name__ == "__main__":
    readFutoshiki()
    

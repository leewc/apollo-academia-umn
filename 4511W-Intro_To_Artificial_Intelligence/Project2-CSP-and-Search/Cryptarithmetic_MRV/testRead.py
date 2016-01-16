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

#class struct a bit overkill for this, can use dict[varname]=domain if this is all it needs 
class MakeVar:
    def __init__(self,n,d=[1,2,3,4]):
        self.name = n
        self.domain = d
        
# create a constraint for KenKen specific to number of vars involved
class Constraint:
    def __init__(self,vs,op,a):
        self.nvars = len(vs)
        self.vlist = vs
        self.op = op
        if ( 1 == self.nvars ):
            self.fn = lambda x: x == eval(a)
        elif (2 == self.nvars ):
            self.fn = lambda x,y: ops[op](x,y) == eval(a)
        elif (3 == self.nvars ):
            self.fn = lambda x,y,z: ops[op](ops[op](x,y),z) == eval(a)
        else:
            print('num vars not right')

def readCrypt():

    # read in the file with constraints for KenKen puzzles (1 line per puzzle)
    lines = open('testCrypt.txt').readlines()
    testLine = 0 # test this line in file
    l = lines[testLine]
    #remove white space
    l=re.sub('[ ]','',l)
    print('l ',l)

    # determine operator and remove, find "answer"
    op = re.findall('^\W',l)
    print('op ',op)
    l = re.sub('^\W,','',l)
    answer = re.findall('=\w+',l)
    answer = re.sub('=','',answer[0])
    print('l ',l,'answer ',answer)

    # start a dictionary of variables and a list of constraints
    Cons = []

    vars = []
    # separate values
    words = re.findall('\w+',l)
    print(words)
    for w in words:
        letters = re.findall('\w',w)
        for letter in letters:
            if letter not in vars: vars.append(letter)
    print('vars ',vars)
    return op,words,vars

if __name__ == "__main__":
    #readKenKen()
    readCrypt()
    #readFutoshiki()
    #readCrossMath()
    

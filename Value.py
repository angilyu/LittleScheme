#### Value Types ####
class Values:
    BOOLEAN = 1
    STRING = 2
    NUMBER = 3
    SYMBOL = 4
    PAIR = 5
    PROCEDURE = 6

#### Value Representation ####
class Value:
    def __init__(self, valueType, val):
        self.valueType = valueType
        self.val = val

class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

class Procedure:
    def __init__(self, proc, isUserDefined = True):
        self.proc = proc
        self.isUserDefined = isUserDefined

#### Value Constructors ####
def makeString(val):
    """ val should be python's string """
    return Value(Values.STRING, val)
def makeNumber(val):
    """ val should be python's floating number """
    return Value(Values.NUMBER, val)
def makeBoolean(val):
    """ val can be either python's True/False """
    return Value(Values.BOOLEAN, val)

def makeSymbol(val):
    """ val should be python's string """
    return Value(Values.SYMBOL, val)
def makePair(first, second):
    """ val should be python's binary tuple """
    val = Pair(first, second)
    return Value(Values.PAIR, val)
def makeProcedure(proc, isUserDefined = True):
    val = Procedure(proc, isUserDefined)
    return Value(Values.PROCEDURE, val)


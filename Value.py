class Values:
    BOOLEAN = 1
    STRING = 2
    NUMBER = 3
    SYMBOL = 4
    PAIR = 5
    PROCEDURE = 6

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
def makePair(val):
    """ val should be python's binary tuple """
    return Value(Values.PAIR, val)
def makePrecedure(val):
    return Values(Values.PROCEDURE, (True, val))

class Value:
    def __init__(self, valueType, val):
        self.valueType = valueType
        self.val = val


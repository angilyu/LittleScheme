from Token import *

#### Value Types ####
class Values:
    BOOLEAN = 1
    STRING = 2
    NUMBER = 3
    SYMBOL = 4
    PAIR = 5
    PROCEDURE = 6
    LIST = 7
    KEYWORD = 8

_BUILDIN_OPERATORS = set([Tokens.DEFINE, Tokens.COND, Tokens.IF,
                         Tokens.ELSE, Tokens.ASSIGNMENT, Tokens.LAMBDA])

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
    def __init__(self, body, params, env, isUserDefined = True):
        self.body = body
        self.params = params
        self.env = env
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
def makeList(val):
    return Value(Values.LIST, val)
def makePair(first, second):
    """ val should be python's binary tuple """
    val = Pair(first, second)
    return Value(Values.PAIR, val)
def makeProcedure(body, params, env, isUserDefined = True):
    val = Procedure(body, params, env, isUserDefined)
    return Value(Values.PROCEDURE, val)

def makeFromToken(token):
    if token.tokenType == Tokens.NUMBER:
        return makeNumber(token.literal)
    elif token.tokenType == Tokens.STRING:
        return makeSymbol(token.literal)
    elif token.tokenType == Tokens.TRUE or token.tokenType == Tokens.FALSE:
        return makeBoolean(token.tokenType == Tokens.TRUE)
    elif token.tokenType == Tokens.VARIABLE:
        return makeSymbol(token.literal)
    elif token.tokenType in _BUILDIN_OPERATORS:
        return Value(Values.KEYWORD, token.tokenType)
    else:
        assert False

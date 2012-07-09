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
    NULL = 8
    KEYWORD = 9
    LITERAL = 10 # expression after quote

_BUILDIN_OPERATORS = set([Tokens.DEFINE, Tokens.COND, Tokens.IF,
                         Tokens.ELSE, Tokens.ASSIGNMENT, Tokens.LAMBDA])

#### Value Representation ####
class Value:
    # Used for __str__
    toStringHandlers = {
        Values.NUMBER: lambda val: str(val),
        Values.STRING: lambda val: '"%s"' % val,
        Values.BOOLEAN: lambda val: '#t' if val else '#f',
        Values.SYMBOL: lambda val: "'%s" % val,
        Values.PAIR: lambda val: "%s . %s" % (str(val.first), str(val.second)),
        Values.PROCEDURE: lambda val: "<function>",
        Values.LIST: lambda val: "(%s)" % " ".join(str(item) for item in val),
        Values.NULL: lambda val: "null",
        Values.KEYWORD: lambda val: Tokens.tokenNames[val],
        Values.LITERAL: lambda val: "<literal>",
    }
    def __init__(self, valueType, val):
        """ initialize things """
        self.valueType = valueType
        self.val = val
    def __eq__(self, other):
        return self.valueType == other.valueType and \
               self.val == other.val
    def __str__(self):
        return Value.toStringHandlers[self.valueType](self.val)
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
def makeKeyword(tokenType):
    return Value(Values.KEYWORD, tokenType)
def makeNULL():
    return Value(Values.NULL, None)
def makeLiteral(val):
    return Value(Values.LITERAL, val)
def makeProcedure(body, params, env, isUserDefined = True):
    val = Procedure(body, params, env, isUserDefined)
    return Value(Values.PROCEDURE, val)
def makeFromToken(token):
    if token.tokenType == Tokens.NUMBER:
        return makeNumber(token.literal)
    elif token.tokenType == Tokens.STRING:
        return makeString(token.literal)
    elif token.tokenType == Tokens.TRUE or token.tokenType == Tokens.FALSE:
        return makeBoolean(token.tokenType == Tokens.TRUE)
    elif token.tokenType == Tokens.VARIABLE:
        return makeSymbol(token.literal)
    elif token.tokenType in _BUILDIN_OPERATORS:
        return makeKeyword(token.tokenType)
    elif token.tokenType == Tokens.NULL:
        return makeNULL()
    else:
        assert False


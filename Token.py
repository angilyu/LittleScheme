
# Constants for Tokens
class Tokens:
    ##### TOKEN IDs #####
    # -- Characters
    LPAREN = 1 # "("
    RPAREN = 2 # ")"
    QUOTE = 3 # "'"

    # -- Primitives
    STRING = 10 # "example"
    TRUE = 11 # #t
    FALSE = 12 # #f
    NUMBER = 13
    VARIABLE = 14

    # -- Keywords
    DEFINE = 20 # define
    COND = 21 # cond
    IF = 22 # if
    ELSE = 23 # else
    ASSIGNMENT = 24 # set!
    NULL = 25 # NULL
    LAMBDA = 26 # lambda

    # -- Undefined
    UNDEFINED = 30

    ##### TOKEN Names #####
    tokenNames = {
        # Basic characters
        LPAREN: "(",
        RPAREN: ")",
        QUOTE: "'",

        # Primitives
        STRING: "string",
        NUMBER: "number",
        VARIABLE: "variable",

        # Keywords
        DEFINE: "define",
        COND: "cond",
        IF: "if",
        ELSE: "else",
        ASSIGNMENT: "set!",
        NULL: "null",
        TRUE: "#t",
        FALSE: "#f",
        LAMBDA: "lambda",
    }

    specialCharacters = [LPAREN, RPAREN, QUOTE]
    primitives = [STRING, NUMBER, VARIABLE]
    keywords = [DEFINE, COND, IF, ELSE, ASSIGNMENT, NULL, TRUE, FALSE, LAMBDA]
    keywordStrings = {"define":DEFINE, "cond":COND, "if":IF, "else":ELSE,\
                      "set!":ASSIGNMENT, "null":NULL, "lambda":LAMBDA}

class Token:
    def __init__(self, tokenType, pos, literal = None):
        """ the Token instance has the follow fields:
             @params tokenType indicats the type of this token
             @params pos indicates the start position in the original file
             @params literal is optional, contains the literal of the token
         """
        self.tokenType = tokenType
        self.pos = pos
        self.literal = literal

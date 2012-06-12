
# Constants for Tokens
class Tokens:
    # -- Characters
    LPAREN = 1 # "("
    RPAREN = 2 # ")"
    QUOTE = 3 # "'"

    # -- Primitives
    # text enclosed by ", can use \" to escape internal `double quote`
    STRING = 10 # "example"
    TRUE = 11 # #t
    FALSE = 12 # #f
    # ------
    NUMBER = 13
    # variable could be composed by alphabets (a-z, A-Z) and digits (0~9)
    # or special characters: ! $ % & * + - . / : < = > ? @ ^ _ ~
    VARIABLE = 14

    # -- Keywords
    DEFINE = 20 # define
    COND = 21 # cond
    IF = 22 # if
    ELSE = 23 # else
    ASSIGNMENT = 24 # set!
    NULL = 25 # NULL

    # -- Undefined
    UNDEFINED = 30

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

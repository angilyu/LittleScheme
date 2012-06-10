import string

# Constants for Tokens
class Tokens:
    # -- Characters
    LPAREN = 1 # "("
    RPAREN = 2 # ")"
    QUOTE = 3 # "'"

    # -- Primitives
    # text enclosed by ", can use \" to escape internal `double quote`
    STRING = 10
    # either #t or #f
    NUMBER = 11
    # variable could be composed by alphabets (a-z, A-Z) and digits (0~9)
    # or special characters: ! $ % & * + - . / : < = > ? @ ^ _ ~
    VARIABLE = 12
    TRUE = 13 # #t
    FALSE = 14 # #f

    # -- Keywords
    DEFINE = 20
    COND = 21
    IF = 22
    SET = 22

    # -- Undefined
    UNDEFINED = 30


def getToken(text, pos):
    # TODO: can use the "trie" to do the fast detection
    # right now we just use some linear
    tokenType, pos = exactMatch(text, pos)
    if tokenType != Tokens.UNDEFINED:
        return (tokenType, pos)

    # try match number/string
    possibleToken = fastDispatch(text, pos)
    if possibleToken == Tokens.NUMBER:
        tokenType, pos = extractNumber(text, pos)
    elif possibleToken == Tokens.STRING:
        tokenType, pos = extractNumber(text, pos)

    if tokenType != Tokens.UNDEFINED:
        return (tokenType, pos)

    # try match variable
    tokenType, pos = extractVariable(text, pos)

# Utilities functions
_COMMENT_START_ = '"'
def _skipWhitespace(text, pos):
    while pos != len(text):
        if text[pos] in string.whitespace:
            pos += 1
        else:
            break
    return pos

def _skipToNextLine(text, pos):
    # TODO: WHAT if the new line is not represented by '\n'?
    while pos != len(text):
        if text[pos] == '\n':
            return pos + 1
        else:
            pos += 1

    assert pos == len(text)
    return pos

def _skip(text, pos):
    while pos != len(text):
        pos = _skipWhitespace(text, pos)

        if pos != len(text) and text[pos] == _COMMENT_START_:
            pos = _skipToNextLine(text, pos)
        else:
            return pos
    return pos

def _fetchToken(text, pos):
    pass

def tokenize(text):
    """ tokenize() is a generator that takes the text as the input and returns
        a token every time.
    """
    pos = 0
    while pos != len(text):
        # skip white spaces and the comments
        pos = _skip(text, pos)
        token, pos = _fetchToken(text, pos)
        yield token


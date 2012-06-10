import string

# Constants for Tokens
class Tokens:
    # Characters
    LPAREN = 1
    RPAREN = 2
    QUOTE = 3

    # Primitives
    STRING = 10
    BOOLEAN = 11
    VARIABLE = 12

    # Keywords
    DEFINE = 21
    COND = 22
    IF = 24
    SET = 23

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


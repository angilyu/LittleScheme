import string
from Token import *

######## CONSTANTS ########
_COMMENT_STARTER_ = ';'
SPECIAL_CHARS = {"(": Tokens.LPAREN, ")": Tokens.RPAREN, "'": Tokens.QUOTE}
_PRIMITIVES = ["#t","#f"]
_LEGAL_VAR_CHARS = string.letters + string.digits + "!$%&*+-./:<=>?@^_~"
_ESCAPED_CHARS = {"\\":"\\", "\"":"\"", "a":"\a", "b":"\b", "f":"\f", "n":"\n",
                  "r":"\r", "t":"\t"}
_DOUBLE_QUOTE = '"'
_BACK_SLASH = '\\'

######## SKIP ########
def _skipToNextLine(text, pos):
    while pos < len(text):
        if text[pos] == '\n':
            return pos + 1;
        else:
            pos += 1;
    return pos;
def _skipComments(text, pos):
    if text[pos] == _COMMENT_STARTER_:
        pos = _skipToNextLine(text, pos)
    return pos
def _skipWhitespaces(text, pos):
    while pos < len(text):
        if text[pos] in string.whitespace:
            pos += 1
        else:
            break
    return pos
def _skip(text, pos):
    while pos < len(text):
        pos = _skipWhitespaces(text, pos)
        if pos < len(text):
            newPos = _skipComments(text, pos)
            if newPos == pos:
                break
            else:
                pos = newPos
    return pos

######## EXTRACT TOKENS ########
def _extractSpectialChar(text, pos):
    if text[pos] in SPECIAL_CHARS:
        return Token(SPECIAL_CHARS[text[pos]], pos), pos + 1

    return None

def _extractString(text, pos):
    originalPos = pos
    # check the leading double quote
    if text[pos] != _DOUBLE_QUOTE:
        return None

    pos += 1
    parsedString = ""
    while True:
        if text[pos] == _DOUBLE_QUOTE:
            break
        if text[pos] != _BACK_SLASH:
            parsedString += text[pos]
            pos += 1
        else:
            if text[pos + 1] in _ESCAPED_CHARS:
                parsedString += _ESCAPED_CHARS[text[pos + 1]]
                pos += 2
            else:
                assert False
    return Token(Tokens.STRING, originalPos, parsedString), pos + 1

def _extractBoolean(text, pos):
    # check if there's enough space for them
    if len(text) - pos < 2:
        return None

    prefix = text[pos: pos + 2]
    if prefix not in _PRIMITIVES:
        return None

    if len(text) - pos >= 3 and text[pos + 2] in _LEGAL_VAR_CHARS:
        return None

    tokenType = Tokens.TRUE if prefix[1] == "t" else Tokens.FALSE
    return Token(tokenType, pos), pos + 2

def _isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def _isKeywords(s):
    return s in Tokens.keywordStrings

def _extractVariable(text, pos):
    originalPos = pos
    variable = ""
    while pos < len(text):
        if text[pos] in _LEGAL_VAR_CHARS:
            variable += text[pos]
            pos += 1
        else:
            break
    if pos == originalPos:
        return None
    else:
        literal = None
        if _isNumber(variable):
            tokenType = Tokens.NUMBER
            literal = float(variable)
        elif _isKeywords(variable):
            tokenType = Tokens.keywordStrings[variable]
            literal = None
        else:
            tokenType = Tokens.VARIABLE
            literal = variable
        return Token(tokenType, originalPos, literal), pos

def _extractToken(text, pos):
    """ @return A Pair, the first element is a Token, the second element is the start position of the token """
    result = _extractSpectialChar(text, pos)

    # extract string
    if result is None:
        result = _extractString(text, pos)

    # extract boolean
    if result is None:
        result = _extractBoolean(text, pos)

    #extract variable
    if result is None:
        result = _extractVariable(text, pos)

    return result

###### tokenize() ######
def tokenize(text, pos):
    """ tokenize() is a generator that takes the text as the input and returns
        one token at a time.
    """
    while pos < len(text):
        pos = _skip(text, pos)
        if pos < len(text):
            result = _extractToken(text, pos)
            if result is None:
                break
            else:
                token, pos = result
                yield token


import string
from Token import *


_COMMENT_START_ = ';'
def _skipToNextLine(text, pos):
    while pos < len(text):
        if text[pos] == '\n':
            return pos + 1;
        else:
            pos += 1;
    return pos;
def _skipComments(text, pos):
    if text[pos] == _COMMENT_START_:
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
characters = {"(": Tokens.LPAREN, ")": Tokens.RPAREN, "'": Tokens.QUOTE}
primitives = ["#t","#f"]
legalCharacters = string.letters + string.digits + "!$%&*+-./:<=>?@^_~"
keywords = ["define", "cond", "if", "else", "set!", "null"]

def checkCharacters(text, pos):
    if text[pos] in characters:
        return True, pos + 1, Token(characters[text[pos]], pos, text[pos])
    else:
        return False, pos, None

escapedCharacters = {"\\":"\\", "\"":"\"", "a":"\a", "b":"\b", "f":"\f", "n":"\n", "r":"\r", "t":"\t"}
def checkString(text, pos):
    originalPos = pos
    if text[pos] != "\"":
        return False, pos, None
    pos += 1
    parsedString = ""
    while True:
        if text[pos] == "\"":
            break
        if text[pos] != "\\":
            parsedString += text[pos]
            pos += 1
        else:
            if text[pos + 1] in escapedCharacters:
                parsedString += escapedCharacters[text[pos + 1]]
                pos += 2
            else:
                assert False
    token = Token(Tokens.STRING, originalPos, parsedString)
    return True, pos + 1, token
def checkTrueFalse(text, pos):
    if text[pos:pos + 2] == "#t":
        return True, pos + 2, Token(Tokens.TRUE, pos, "#t")
    elif text[pos:pos + 2] == "#f":
        return True, pos + 2, Token(Tokens.FALSE, pos, "#f")
    else:
        return False, pos, None
def getToken(text, pos):
    exist, pos, token = checkCharacters(text, pos)
    if False == exist:
        exist, pos, token = checkString(text, pos)
    if False == exist:
        exist, pos, token = checkTrueFalse(text, pos)
    return exist, pos, token

def tokenize(text, pos):
    while pos < len(text):
        pos = _skip(text, pos)
        if pos < len(text):
            exist, pos, token = getToken(text, pos)
        if exist:
            exist = False
            yield token
    return

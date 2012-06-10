import string
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
def tokenize(text):
    return

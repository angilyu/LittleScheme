from Token import *
from Exp import *

####### Error code #######
# TODO: the error code should be public
_OK = 0 # Expression has been extracted
_CE_ENDS = 1 # compound expression ends
_EXPECT_LPAREN = 2 # expect left parenthesis but didn't get it.
_EMPTY_EXPRESSION = 3 # EMPTY EXPRESSION
_NOT_AN_EXPRESSION = 4

BUILDIN_OPERATORS = set([ Tokens.DEFINE, Tokens.COND, Tokens.IF,
                          Tokens.ELSE, Tokens.ASSIGNMENT, Tokens.LAMBDA])
def _isBuildin(exp):
    return not exp.isCompound() and exp.tokenType in BUILDIN_OPERATORS

def _parse(tokenIter):
    """ _parse() recursively extract the expression from the given
        token iterator
        \param tokenIter is the token iterator that represents the
               stream of tokens
        \return a pair, where the first parameter reports the error code
                occurs while parsing (_OK indicates no error happens);
                the second parameter is the extracted expression, which will
                be None if error occurs.
    """
    token = tokenIter.next()

    # All tokens, except the special characters, are considered
    # to be "atom"
    if not token.tokenType in Tokens.specialCharacters:
        return _OK, AtomExp(token)

    # check if this is the start of an compound expression
    if token.tokenType == Tokens.RPAREN:
        return (_CE_ENDS, token), None

    # If the token either indicates the atomic expression nor teh end of
    # compoun expression, then it must be the "beginning" of a compound
    # expression.
    if token.tokenType != Tokens.LPAREN:
        return (_EXPECT_LPAREN, token), None

    # -- Read operator
    error, op = _parse(tokenIter)
    if error != _OK:
        return _EMPTY_EXPRESSION, result
    # check if the operator is a buildin operator
    if _isBuildin(op):
        op = op.tokenType
    exp = CompoundExp(op)

    # Read parameters
    while True:
        error, param = _parse(tokenIter)

        if error != _OK:
            # reach the end the this compound expression?
            if error[0] == _CE_ENDS:
                break
            # or real error occurs
            else:
                return error, param

        if _isBuildin(param):
            return _NOT_AN_EXPRESSION, param

        exp.addParameter(param)

    return _OK, exp

def parse(tokenIter):
    while True:
        yield _parse(tokenIter)

from Token import *
import Value

####### Parse Errors #######
class ParseError:
    OK = 0 # Expression has been extracted
    CE_ENDS = 1 # compound expression ends
    EXPECT_LPAREN = 2 # expect left parenthesis but didn't get it.
    EMPTY_EXPRESSION = 3 # EMPTY EXPRESSION
    NOT_AN_EXPRESSION = 4

def _parse(tokenIter):
    """ _parse() recursively extract the expression from the given
        token iterator
        //param tokenIter is the token iterator that represents the
               stream of tokens
        //return a pair, where the first parameter reports the error code
                occurs while parsing (OK indicates no error happens);
                the second parameter is the extracted expression, which will
                be None if error occurs.
    """
    token = tokenIter.next()

    # All tokens, except the special characters, are considered
    if not token.tokenType in Tokens.specialCharacters:
        return ParseError.OK, Value.makeFromToken(token)

    # check if this is the end of an expression
    if token.tokenType == Tokens.RPAREN:
        return (ParseError.CE_ENDS, token), None

    # If the token either indicates the expression element
    # (operator, parameters)nor the end of expression, then it
    # must be the "beginning" of a expression.
    if token.tokenType != Tokens.LPAREN:
        return (_EXPECT_LPAREN, token), None

    sList = []
    # Read parameters, operator is placed together with parameter as the first element of the list
    while True:
        error, param = _parse(tokenIter)

        if error != ParseError.OK:
            # reach the end the this expression?
            if error[0] == ParseError.CE_ENDS:
                break
            # or real error occurs
            else:
                return error, param

        sList.append(param)

    return ParseError.OK, Value.makeList(sList)

def parse(tokenIter):
    while True:
        yield _parse(tokenIter)

from Token import *
import Value

####### Parse Errors #######
class ParseError:
    OK = 0 # Expression has been extracted
    CE_ENDS = 1 # compound expression ends
    EXPECT_LPAREN = 2 # expect left parenthesis but didn't get it.
    EMPTY_EXPRESSION = 3 # EMPTY EXPRESSION
    NOT_AN_EXPRESSION = 4
    TOKENIZE_ERROR = 5
    TOKEN_NORMALLY_ENDS = 6
    TOKEN_UNEXPECTED_ENDS = 7

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
    try:
        token = tokenIter.next()
    except StopIteration:
        return ParseError.TOKEN_NORMALLY_ENDS, None
    # Token type is ERROR
    if token.tokenType == Tokens.ERROR:
        return (ParseError.TOKENIZE_ERROR, token), None

    # All tokens, except the special characters, are considered. special char are: ( ) '
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
        print error
        print param

        if error != ParseError.OK:
            # reach the end the this expression?
            if error[0] == ParseError.CE_ENDS:
                break
            elif error[0] == ParseError.TOKEN_NORMALLY_ENDS:
                return ParseError.TOKEN_UNEXPECTED_ENDS, None
            # or real error occurs
            else:
                print "No right )"
                return error, param

        sList.append(param)
        print sList

    print "out of while"
    return ParseError.OK, Value.makeList(sList)

def parse(tokenIter):
    while True:
        error, param = _parse(tokenIter)
        # ends normally
        if error == ParseError.TOKEN_NORMALLY_ENDS:
            break

        yield error, param
        if error != ParseError.OK:
            break

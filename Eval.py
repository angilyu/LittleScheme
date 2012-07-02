from Token import *
from Value import *

#### Eval Errors ####
class EvalError:
    OK = 0,
    INCORRECT_PARAM_NUMBER = 1
    UNEXPECTED_TYPE = 2
    INVALID_PARAM_LIST = 3
    UNMATCH_PARAM_NUMBER = 4
    EMPTY_LIST = 5

#### Evaluating the build-in operations ####
def _evalDefine(params, env):
    """
    Evaluate define expression
    """
    # Check the correctness of define expression
    if len(params) != 2:
        return INCORRECT_PARAM_NUMBER, 2, len(params)

    # for example: "define size (+ 3 5)", params[0] is size
    symb = params[0]
    if symb.valueType != Values.SYMBOL:
        return UNEXPECTED_TYPE, Values.SYMBOL, 0

    # TODO: should add error report here
    # for example: "define size (+ 3 5)", params[1] is (+ 3 5)
    result = eval(params[1], env)
    if result[0] != EvalError.OK:
        return result

    # result[1] is the eval result of (+ 3 5)
    env[symb.val] = result[1]
    return EvalError.OK, None

def _evalLambda(params, env):
    """
    Evaluate lambda expression
    """
    # lambda expression should have at least 2 parameters
    assert len(params) >= 2

    # extract lambda expression's param list
    paramList = params[0].val

    if any(param.valueType != Values.SYMBOL for param in paramList):
        return EvalError.INVALID_PARAM_LIST, None

    # extract body
    body = params[1:]

    return EvalError.OK, makeProcedure(body, paramList, env)

_keywordEvalTable = {
    Tokens.DEFINE: _evalDefine,
    Tokens.COND: None,
    Tokens.ELSE: None,
    Tokens.IF: None,
    Tokens.ASSIGNMENT: None,
    Tokens.LAMBDA: _evalLambda,
}

def _evalParams(params, env):
    """
    Evaluate all the parameters
    """
    parameters = []
    for param in params:
        result = eval(param, env)
        if result[0] != EvalError.OK:
            return result
        parameters.append(result[1])

    return EvalError.OK, parameters

def _evalExpSeq(exps, env):
    """
    Evaluate expression sequences and return the result of the last expression
    """
    for exp in exps:
        result = eval(exp, env)
        if result[0] != EvalError.OK:
            return result
    return result

def _evalList(slist, env):
    """
        Evaluate the expression list. The list contains operator and parameters
        @params slist is the combination of operator and parameters of expression. operator is the first element.
        @params evn is the environment varibles
    """
    if len(slist) == 0:
        return EvalError.EMPTY_LIST,

    op = slist[0]
    if op.val in Tokens.keywords:
        return _keywordEvalTable[op.val](slist[1:], env)
    else:
        opResult = eval(op, env)
        if opResult[0] != EvalError.OK:
            return opResult

        op = opResult[1]
        paramResult = _evalParams(slist[1:], env)
        if paramResult[0] != EvalError.OK:
            return paramResult

        return apply(op.val, paramResult[1])

############## Public Interface ##############
def eval(exp, env):
    if exp.valueType == Values.LIST:
        return _evalList(exp.val, env)
    else:
        return EvalError.OK, \
               env[exp.val] if exp.valueType == Values.SYMBOL else exp

def apply(proc, args):
    # builtin functions
    # TODO: what if the build-in function return some errors.
    if proc.isUserDefined == False:
        return EvalError.OK, proc.body(args)
    else:
        # setup environment
        assert len(args) == len(proc.params)

        # generate a new environment dict for new procedure. The new env's parent is the old env
        env = proc.env.spawn(proc.params, args)

        # Evaluate Sequence
        return _evalExpSeq(proc.body, env)

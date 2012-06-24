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

#### Eval atom expressions ####

#### Evaluating the build-in operations ####
def _evalDefine(params, env):
    # Check correctness
    if len(params) != 2:
        return INCORRECT_PARAM_NUMBER, 2, len(params)

    symb = params[0]
    if symb.valueType != Values.SYMBOL:
        return UNEXPECTED_TYPE, Values.SYMBOL, 0

    # TODO: should add error report here
    result = seval(params[1], env)
    if result[0] != EvalError.OK:
        return result

    env[symb.val] = result[1]
    return EvalError.OK, None

def _evalLambda(params, env):
    # TODO
    assert len(params) >= 2

    # extract the param list
    paramList = params[0].val

    if any(param.valueType != Values.SYMBOL for param in paramList):
        return EvalError.INVALID_PARAM_LIST, None

    # extract body
    body = params[1:]

    return EvalError.OK, makeProcedure(body, params[1:], env)


_keywordEvalTable = {
    Tokens.DEFINE: _evalDefine,
    Tokens.COND: None,
    Tokens.ELSE: None,
    Tokens.IF: None,
    Tokens.ASSIGNMENT: None,
    Tokens.LAMBDA: _evalLambda,
}

def _evalParams(params, env):
    parameters = []
    for param in params:
        result = seval(param, env)
        if result[0] != EvalError.OK:
            return result
        parameters.append(result[1])

    return EvalError.OK, parameters

def _evalList(slist, env):
    if len(slist) == 0:
        return EvalError.EMPTY_LIST,
    op = slist[0]

    if op.val in Tokens.keywords:
        return _keywordEvalTable[op.val](slist[1:], env)
    else:
        result = seval(op, env)
        if result[0] != EvalError.OK:
            return result

        op = result[1]
        result = _evalParams(slist[1:], env)
        if result[0] != EvalError.OK:
            return result

        return sapply(op.val, result[1])

############## Public Interface ##############
def seval(exp, env):
    if exp.valueType == Values.LIST:
        return _evalList(exp.val, env)
    else:
        return EvalError.OK, \
               env[exp.val] if exp.valueType == Values.SYMBOL else exp

def sapply(proc, params):
    # builtin functions 
    if proc.isUserDefined == False:
        return EvalError.OK, proc.body(params)
    else:
        paramList = proc.params
        newEnv = proc.env.spawn()
        # setup environment
        assert len(params) == len(paramList)

        for index in xrange(len(params)):
            newEnv[paramList[index]] = params[index]

        for exp in proc.body:
            result = seval(exp, newEnv)
            if result[0] != EvalError.OK:
                return result
        return result


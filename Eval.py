from Token import *
from Value import *

#### Eval Errors ####
class EvalError:
    OK = 0,
    INCORRECT_PARAM_NUMBER = 1
    UNEXPECTED_TYPE = 2
    INVALID_PARAM_LIST = 3
    UNMATCH_PARAM_NUMBER = 4

#### Eval atom expressions ####
_atomProcessors = {
    Tokens.STRING: makeString,
    Tokens.NUMBER: makeNumber,
}

#### Evaluating the build-in operations ####
def _evalDefine(params, env):
    # Check correctness
    if len(params) != 2:
        return INCORRECT_PARAM_NUMBER, 2, len(params)

    symb = params[0]
    if symb.isCompound() or symb.tokenType != Tokens.VARIABLE:
        return UNEXPECTED_TYPE, Tokens.VARIABLE, 0

    # TODO: should add error report here
    result = seval(params[1], env)
    if result[0] != EvalError.OK:
        return result

    env[symb.literal] = result[1]
    return EvalError.OK, None

def _evalLambda(params, env):
    # TODO
    assert len(params) >= 2

    # extract the param list
    paramList = [params[0].operator]
    paramList.extend(params[0].parameters)

    if any(param.isCompound() or param.tokenType != Tokens.VARIABLE \
            for param in paramList):
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

def _evalCompound(compound, env):
    if compound.isKeyword():
        return _keywordEvalTable[compound.operator](compound.parameters, env)
    else:
        result = seval(compound.operator, env)
        if result[0] != EvalError.OK:
            return result

        op = result[1]
        result = _evalParams(compound.parameters, env)
        if result[0] != EvalError.OK:
            return result

        return sapply(op.val, result[1])

def _evalAtom(atom, env):
    if atom.tokenType in _atomProcessors:
        return EvalError.OK, _atomProcessors[atom.tokenType](atom.literal)
    elif atom.tokenType == Tokens.TRUE or atom.tokenType == Tokens.FALSE:
        return EvalError.OK, makeBoolean(atom.tokenType == Tokens.TRUE)
    elif atom.tokenType == Tokens.VARIABLE:
        return EvalError.OK, env[atom.literal]
    else:
        assert False

############## Public Interface ##############
def seval(exp, env):
    if not exp.isCompound():
        return _evalAtom(exp, env)
    else:
        return _evalCompound(exp, env)

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


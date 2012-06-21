from Token import *
from Value import *

#### Eval Errors ####
class EvalError:
    OK = 0,
    INCORRECT_PARAM_NUMBER = 1
    UNEXPECTED_TYPE = 2

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
    if result[0] != Eval.OK:
        return result

    env[symb.literal] = result[1]
    return EvalError.OK, None

# TODO: this function has a lot of duplication
def _assignmentEval(params, env):
    # Check correctness
    if len(params) != 2:
        return INCORRECT_PARAM_NUMBER, 2, len(params)

    symb = params[0]
    if symb.isCompound() or symb.tokenType != Tokens.VARIABLE:
        return UNEXPECTED_TYPE, Tokens.VARIABLE, 0

    # TODO: should add error report here
    result = seval(params[1], env)
    if result[0] != Eval.OK:
        return result

    env[symb.literal] = result[1]
    return EvalError.OK, None

_keywordEvalTable = {
    Tokens.DEFINE: _evalDefine,
    Tokens.COND: None,
    Tokens.ELSE: None,
    Tokens.IF: None,
    Tokens.ASSIGNMENT: None,
    Tokens.LAMBDA: None,
}

def _evalCompound(compound, env):
    if compound.isKeyword():
        return _keywordEvalTable[compound.operator](compound.parameters, env)
    else:
        result = seval(compound.operator, env)
        if result[0] != EvalError.OK:
            return result

        op = result[1]
        parameters = []
        for param in compound.parameters:
            result = seval(param, env)
            if result[0] != EvalError.OK:
                return result
            parameters.append(result[1])

        return sapply(op, parameters, env)

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
    return _evalCompound(exp, env) if exp.isCompound() else \
           _evalAtom(exp, env)

def sapply(op, params, env):
    # builtin functions 
    if op[0] == False:
        return EvalError.OK, op[1](params)
    else:
        env = setupEnv(env, params)
        return seval(op, env)

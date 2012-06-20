from Token import *
from Value import *

_atomProcessors = {
    Tokens.STRING: makeString,
    Tokens.NUMBER: makeNumber,
}
_keywordEvalTable = {
    Tokens.DEFINE: None,
    Tokens.COND: None,
    Tokens.IF: None,
    Tokens.ELSE: None,
    Tokens.ASSIGNMENT: None,
    Tokens.LAMBDA: None,
}

def _evalOp(compound, env):
    # Get the operator, the operator could be either 'keywords' or procedure.
    if compound.operator in Tokens.keywords:
        return True, compound.operator.tokenType
    return False, seval(compound.operator, env)

def _evalCompound(compound, env):
    # Get operator
    isKeyword, op = _evalOp(compound, env)

    # Apply
    if isKeyword:
        return keywordEvalTable[op](compound.parameters, env)
    else:
        parameters = [seval(param, env) for param in compound.parameters]
        return sapply(op, parameters, env)

def _evalAtom(atom, env):
    if atom.tokenType in _atomProcessors:
        return _atomProcessors[atom.tokenType](atom.literal)
    elif atom.tokenType == Tokens.TRUE or atom.tokenType == Tokens.FALSE:
        return makeBoolean(atom.tokenType == Tokens.TRUE)
    elif atom.tokenType == Tokens.VARIABLE:
        return env[atom.literal]
    else:
        assert False

############## Public Interface ##############
def seval(exp, env):
    return _evalCompound(exp, env) if exp.isCompound() else \
           _evalAtom(exp, env)

def sapply(op, params, env):
    # builtin functions 
    if op[0] == False:
        return op[1](params)
    else:
        env = setupEnv(env, params)
        return seval(op, env)

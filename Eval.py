from Token import *
from Values import *

_atomProcessors = {
    Tokens.STRING: makeString,
    Tokens.NUMBER: makeNumber,
    Tokens.BOOLEAN: makeBoolean,
}

def _evalOp(compound, env):
    # Get the operator, the operator could be either 'keywords' or procedure.
    if compound.operator.tokenType in Tokens.KEYWORDS:
        return True, compound.op.tokenType
    return False, eval(compound.op, env)

def _evalCompound(compound, env):
    # Get operator
    isKeyword, op = _evalOp(compound, env)

    # Apply
    if isKeyword:
        return keywordEvals[op](compound.parameters, env)
    else:
        parameters = [seval(param) for param in compound.parameters]
        return sapply(op, parameters, env)

def _evalAtom(atom, env):
    if atom.tokenType in _atomProcessors:
        _atomProcessors[atom.tokenType](atom.literal)
    elif atom.tokenType == Tokens.VARIABLE:
        return env[atom.literal]
    else:
        assert False

def seval(exp, env):
    if exp.isCompound():
        _evalCompound(exp, env)
    else:
        _evalAtom(exp, env)

def sapply(op, params, env):
    env = setupEnv(env, params)
    return seval(op, env)

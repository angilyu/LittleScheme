from Token import *

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
    if atom.tokenType == Tokens.STRING:
        pass
    elif atom.tokenType == Tokens.NUMBER:
        pass
    elif atom.tokenType == Tokens.VARIABLE:
        return env[atom.literal]
    elif atom.tokenType == NULL:
        pass
    elif atom.tokenType in [Tokens.TRUE, Tokens.FALSE]:
        pass
    else:
        assert False

def seval(exp, env):
    if exp.isCompound():
        _evalCompound(exp, env)
    else:
        _evalAtom(exp, env)


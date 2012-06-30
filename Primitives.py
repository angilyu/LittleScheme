import Value

# TODO: no error checking at this time
def add(params):
    return Value.makeNumber(sum(item.val for item in params))

def minus(params):
    return Value.makeNumber(params[0].val - params[1].val)

BuildIns = {
    # TODO: should pass the param in the future
    "+": Value.makeProcedure(add, None, None, False),
    "-": Value.makeProcedure(minus, None, None, False),
}


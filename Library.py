import Value

# TODO: no error checking at this time
def add(params):
    return Value.makeNumber(sum(item.val for item in params))

def minus(params):
    return Value.makeNumber(params[0].val - params[1].val)

BuildIns = {
    "+": Value.makeProcedure(add, False),
    "-": Value.makeProcedure(minus, False),
}


import Value

def add(params):
    # TODO: no error checking at this time
    return Value.makeNumber(sum(item.val for item in params))

def minus(params):
    return Value.makeNumber(params[0].val - params[1].val)

BuildIns = {
    "+": (False, add),
    "-": (False, minus),
}

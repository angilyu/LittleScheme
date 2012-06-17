from Token import *

class AtomExp:
    def __init__(self, token):
        self.tokenType = token.tokenType
        self.literal = token.literal

    def isCompound(self):
        return False

    def __str__(self):
        if self.tokenType == Tokens.STRING:
            return '"%s"' % self.literal
        elif self.tokenType == Tokens.NUMBER:
            return str(self.literal)
        elif self.tokenType == Tokens.VARIABLE:
            return "'%s" % self.literal
        elif self.tokenType in Tokens.keywords:
            return str(Tokens.tokenNames[self.tokenType])

        assert False

class CompoundExp:
    def __init__(self, operator):
        self.operator = operator
        self.parameters = []

    def addParameter(self, param):
        self.parameters.append(param)

    def isCompound(self):
        return True
    def __str__(self):
        strs = [str(p) for p in self.parameters]
        return "(%s)" % " ".join(strs)


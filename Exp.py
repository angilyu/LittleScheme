from Token import *

class AtomExp:
    def __init__(self, token):
        self.tokenType = token.tokenType
        self.literal = token.literal
    def isCompound(self):
        return False
    def __str__(self):
        if self.tokenType in Tokens.keywords:
            return str(Tokens.tokenNames[self.tokenType])
        else:
            return str(self.literal)

class CompoundExp:
    def __init__(self, operator):
        self.operator = operator
        self.parameters = []

    def addParameter(self, param):
        self.parameters.append(param)

    def isCompound(self):
        return True
    def __str__(self):
        strs = ["(", str(self.operator)]
        strs.extend(str(p) for p in self.parameters)
        strs.append(")")
        return " ".join(strs)


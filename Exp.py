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
        """ \params operator can be either be:
                1. ID of defined buildin operators: such as `define`,
                   `lambda`, etc.
                2. Normal procedure: user defined procedure.
        """
        self.operator = operator
        self.parameters = []

    def addParameter(self, param):
        self.parameters.append(param)

    def isCompound(self):
        return True
    def isKeyword(self):
        return self.operator in Tokens.keywords

    def __str__(self):
        # TODO what if the opeator is the build-in operator?
        strs = [str(p) for p in self.parameters]
        return "(%s)" % " ".join(strs)


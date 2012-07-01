import Env
import Tokenize
import Eval
import Primitives
from Parse import *

def _loadPrimitives(env):
    for symbol, proc in Primitives.BuildIns.items():
        env[symbol] = proc

class Interpreter:
    def __init__(self):
        self.glob = Env.Env()
        _loadPrimitives(self.glob)
    def execute(self, sourceCode):
        tokens = Tokenize.tokenize(sourceCode, 0)
        for status, exp in parse(tokens):
            if status != ParseError.OK:
                print "Error occurs:", status
                return
            return Eval.eval(exp, self.glob)[1]


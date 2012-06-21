import Env
import Tokenize
import Eval
import Library
import Parser

def _loadLibrary(env):
    for symbol, proc in Library.BuildIns.items():
        env[symbol] = proc

class Interpreter:
    def __init__(self):
        self.glob = Env.Env()
        _loadLibrary(self.glob)
    def execute(self, cmd):
        tokens = Tokenize.tokenize(cmd, 0)
        for success, exp in Parser.parse(tokens):
            if success != Parser._OK:
                print "Error occurs:", success
                return
            print Eval.seval(exp, self.glob)[1].val

it = Interpreter()
it.execute("(+ 5 6)")

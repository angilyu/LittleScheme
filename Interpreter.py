import Env
import Tokenize
import Eval
import Library
import Parse

def _loadLibrary(env):
    for symbol, proc in Library.BuildIns.items():
        env[symbol] = proc

class Interpreter:
    def __init__(self):
        self.glob = Env.Env()
        _loadLibrary(self.glob)
    def execute(self, cmd):
        tokens = Tokenize.tokenize(cmd, 0)
        for success, exp in Parse.parse(tokens):
            if success != Parse._OK:
                print "Error occurs:", success
                return
            return Eval.seval(exp, self.glob)[1]

it = Interpreter()
it.execute("(define a 1)")
print it.execute("(+ a 6)").val

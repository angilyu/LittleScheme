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
        for exp in Parser.parse(tokens):
            seval(cmd)

it = Interpreter()


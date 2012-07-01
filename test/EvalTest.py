import TestConfig
import unittest
from Eval import *
import Tokenize
import Env
import Interprete

class EvalTest(unittest.TestCase):
    def test_atom_expression(self):
        sourceCode = "10"
        interpreter = Interprete.Interpreter()
        self.assertEqual(interpreter.execute(sourceCode), makeNumber(10))

        sourceCode = '"hello!"'
        interpreter = Interprete.Interpreter()
        self.assertEqual(interpreter.execute(sourceCode), makeString("hello!"))

    def test_define(self):
        sourceCode = "(define size 5)"
        interpreter = Interprete.Interpreter()
        interpreter.execute(sourceCode)
        self.assertEqual(interpreter.glob["size"], makeNumber(5))

        # Test Symbol atom
        sourceCode = "size"
        self.assertEqual(interpreter.execute(sourceCode), makeNumber(5))

    def test_userDefined_proc(self):
        sourceCode = "(define add (lambda (a b) (+ a b)))"
        interpreter = Interprete.Interpreter()
        interpreter.execute(sourceCode)
        self.assertEqual(interpreter.execute("(add 1 3)"), makeNumber(4))

if __name__ == '__main__':
    unittest.main()

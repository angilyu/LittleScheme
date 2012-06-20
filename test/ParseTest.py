import TestConfig
import unittest
import Parser
import Tokenize
from Token import *
from Exp import *

class ExpressionTest(unittest.TestCase):
    def test_primitive_expression(self):
        # String
        token = Token(Tokens.STRING, 0, "token")
        exp = self._parseAsList(self._asIter(token), 1)[0]
        self._assertExpressionEqual(AtomExp(token), exp)

        # Number
        token = Token(Tokens.NUMBER, 0, 1234)
        exp = self._parseAsList(self._asIter(token), 1)[0]
        self._assertExpressionEqual(AtomExp(token), exp)

        # BOOLEAN
        token = Token(Tokens.TRUE, 0)
        exp = self._parseAsList(self._asIter(token), 1)[0]
        self._assertExpressionEqual(AtomExp(token), exp)

    def test_build_in_operator(self):
        tokens = Tokenize.tokenize("(define a 1)", 0)
        exp = self._parseAsList(tokens, 1)[0]
        self.assertEqual(exp.operator, Tokens.DEFINE)

    def test_one_compound_expression(self):
        tokens, expected = self._makeSampleCompundExpression()
        actual = self._parseAsList(tokens.__iter__(), 1)[0]
        self._assertExpressionEqual(expected, actual)

    def test_several_expression(self):
        tokens, expected = self._makeSampleCompundExpression()
        tokens = tokens * 2
        atom = Token(Tokens.STRING, 0, "token")
        tokens.append(atom)

        results = self._parseAsList(tokens.__iter__(), 3)

        # test the first two compund expression
        self._assertExpressionEqual(expected, results[0])
        self._assertExpressionEqual(expected, results[1])

        # test the last atom expression
        self._assertExpressionEqual(AtomExp(atom), results[2])

    # Helpers
    def _makeSampleCompundExpression(self):
        # a token equivelent to (+(cons "key" variable) 234)
        tokens = [
          Token(Tokens.LPAREN, 0),
              Token(Tokens.VARIABLE, 1, "+"),

              Token(Tokens.LPAREN, 2),
                  Token(Tokens.VARIABLE, 4, "cons"),
                  Token(Tokens.STRING, 9, "key"),
                  Token(Tokens.VARIABLE, 15, "variable"),
              Token(Tokens.RPAREN, 0),

              Token(Tokens.NUMBER, 9, 234),
          Token(Tokens.RPAREN, 0),
         ]

        # making the expected expression
        op = AtomExp(Token(Tokens.VARIABLE, 1, "cons"))
        inner = CompoundExp(op)
        inner.parameters = [
                AtomExp(Token(Tokens.STRING, 9, "key")),
                AtomExp(Token(Tokens.VARIABLE, 15, "variable"))]

        op = AtomExp(Token(Tokens.VARIABLE, 1, "+"))
        expected = CompoundExp(op)
        expected.parameters = [
            inner, AtomExp(Token(Tokens.NUMBER, 9, 234))]

        return tokens, expected

    def _parseAsList(self, tokenIter, expectedLen):
        result = list(Parser.parse(tokenIter))
        self.assertEqual(expectedLen, len(result))

        for item in result:
            self.assertEqual(Parser._OK, item[0])

        return [item[1] for item in result]

    def _asIter(self, token):
        return [token].__iter__()

    # Additional assertions
    def _assertExpressionEqual(self, expected, actual):
        self.assertEqual(expected.isCompound(), actual.isCompound())
        if expected.isCompound():
            self._assertCompoundEqual(expected, actual)
        else:
            self._assertAtomEqual(expected, actual)

    def _assertAtomEqual(self, expected, actual):
        self.assertEqual(expected.tokenType, actual.tokenType)
        self.assertEqual(expected.literal, actual.literal)

    def _assertCompoundEqual(self, expected, actual):
        self._assertExpressionEqual(expected.operator, actual.operator)

        self.assertEqual(len(expected.parameters),
                         len(actual.parameters))

        for index in range(len(expected.parameters)):
            self._assertExpressionEqual(expected.parameters[index],
                                        actual.parameters[index])

if __name__ == '__main__':
    unittest.main()

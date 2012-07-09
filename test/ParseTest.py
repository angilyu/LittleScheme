import TestConfig
import unittest
import Tokenize
from Parse import *
from Token import *
from Value import *

class ParseTest(unittest.TestCase):
    def test_primitive_expression(self):
        tokens = Tokenize.tokenize('"I am a string" 1234 #t #f symbol null', 0)

        expected = [makeString('I am a string'), makeNumber(1234),
                    makeBoolean(True), makeBoolean(False),
                    makeSymbol("symbol"), makeNULL()]

        result = list(parse(tokens))

        self.assertTrue(all(code == ParseError.OK for code, _ in result))
        actual = [item for _, item in result]
        self.assertEqual(expected, actual)

    def test_keywords_expression(self):
        tokens = Tokenize.tokenize("define cond if else set! lambda", 0)

        expected = [makeKeyword(Tokens.DEFINE), makeKeyword(Tokens.COND),
                    makeKeyword(Tokens.IF), makeKeyword(Tokens.ELSE),
                    makeKeyword(Tokens.ASSIGNMENT), makeKeyword(Tokens.LAMBDA)]

        result = list(parse(tokens))

        self.assertTrue(all(code == ParseError.OK for code, _ in result))
        actual = [item for _, item in result]
        self.assertEqual(expected, actual)

    def test_single_expression(self):
        tokens = Tokenize.tokenize("(define size 4)", 0)
        expList = [makeKeyword(Tokens.DEFINE), makeSymbol("size"), makeNumber(4)]
        expected = makeList(expList)

        result = list(parse(tokens))

        self.assertTrue(all(code == ParseError.OK for code, _ in result))
        actual = [item for _, item in result]
        self.assertEqual(1, len(actual))
        self.assertEqual(expected, actual[0])
    def test_multiple_expression(self):
        tokens = Tokenize.tokenize("(define size 4)(+ size 5)", 0)
        expListOne = [makeKeyword(Tokens.DEFINE), makeSymbol("size"), makeNumber(4)]
        expListTwo = [makeSymbol("+"), makeSymbol("size"), makeNumber(5)]
        expectedOne = makeList(expListOne)
        expectedTwo = makeList(expListTwo)

        result = list(parse(tokens))

        self.assertTrue(all(code == ParseError.OK for code, _ in result))
        actual = [item for _, item in result]
        self.assertEqual(2, len(actual))
        self.assertEqual(expectedOne, actual[0])
        self.assertEqual(expectedTwo, actual[1])

    def test_illegal_expression(self):
        tokens = Tokenize.tokenize("(define size 3(cons 3 4)", 0)
        result = list(parse(tokens))
        self.assertEqual(1, len(result))
        self.assertEqual(ParseError.TOKEN_UNEXPECTED_ENDS, result[0][0])

    def test_illegal_token_expression(self):
        tokens = Tokenize.tokenize("(define size #a)", 0)
        result = list(parse(tokens))
        self.assertEqual(1, len(result))
        self.assertEqual(ParseError.TOKENIZE_ERROR, result[0][0])
        self.assertEqual(Token(Tokens.ERROR, 13), result[0][1])

    def test_literal_expression(self):
        tokens = Tokenize.tokenize("'(cons a b) 'c", 0)
        result = list(parse(tokens))

        partialTokens = Tokenize.tokenize("(cons a b)", 0)
        partialResult = list(parse(partialTokens))

        self.assertEqual(result[0][1].valueType, Values.LITERAL)
        self.assertEqual(result[0][1].val, partialResult[0][1])

        self.assertEqual(result[1][1].valueType, Values.LITERAL)
        self.assertEqual(result[1][1].val, makeSymbol("c"))
if __name__ == '__main__':
    unittest.main()

import TestConfig
import unittest
import Tokenize
from Token import *

class SkipFunctionsTest(unittest.TestCase):
    def test_skipWhiteSpaces(self):
        # text with leading spaces
        text = "    \n\r\t    \n\r\t  text"
        pos = Tokenize._skipWhitespaces(text, 0)
        self.assertEqual("text", text[pos:])

        # text with no leading space
        test = "text"
        pos = Tokenize._skipWhitespaces(text, 0)
        self.assertEqual("text", text[pos:])

    def test_skipToNewLine(self):
        textWith3Lines = "line1\nline2\nline3"
        pos = Tokenize._skipToNextLine(textWith3Lines, 0)
        self.assertEqual(textWith3Lines[pos:], "line2\nline3")

        pos = Tokenize._skipToNextLine(textWith3Lines, pos)
        self.assertEqual(textWith3Lines[pos:], "line3")

        pos = Tokenize._skipToNextLine(textWith3Lines, pos)
        self.assertEqual(textWith3Lines[pos:], "")
    def test_skip(self):
        text = "\n  ;This line is leave blank\n  ;code will begin\n  (cons 1 2)"
        pos = Tokenize._skip(text, 0)
        self.assertEqual(text[pos:], "(cons 1 2)")

        #another test case
        text = "Nil"
        pos = Tokenize._skip(text, 0)
        self.assertEqual(text[pos:], "Nil")
    def test_getToken(self):
        text = "(cons 1 2)"
        result = Tokenize._extractToken(text, 0)

        self.assertIsNotNone(result)
        self.assertEqual(result[1], 1)
        self.assertTokenEqual(result[0], Token(Tokens.LPAREN, 0))

        """
        text = "   "
        result = Tokenize._extractToken(text, 0)
        self.assertIsNone(result)
        """
    def test_tokenzie(self):
        text = \
"""("hi, I am Wenjing"  #t  #f result cond 123
"""
        results = list(Tokenize.tokenize(text, 0))
        self.assertEqual(len(results), 7)
        self.assertTokenEqual(results[0], Token(Tokens.LPAREN, 0))
        self.assertTokenEqual(results[1], Token(Tokens.STRING, 1, "hi, I am Wenjing"))
        self.assertTokenEqual(results[2], Token(Tokens.TRUE, 21))
        self.assertTokenEqual(results[3], Token(Tokens.FALSE, 25))
        self.assertTokenEqual(results[4], Token(Tokens.VARIABLE, 28, "result"))
        self.assertTokenEqual(results[5], Token(Tokens.COND, 35, ))
        self.assertTokenEqual(results[6], Token(Tokens.NUMBER, 40, 123))

        text = "(('))"
        results = list(Tokenize.tokenize(text, 0))
        self.assertEqual(len(results), 5)
        self.assertTokenEqual(results[0], Token(Tokens.LPAREN, 0))
        self.assertTokenEqual(results[1], Token(Tokens.LPAREN, 1))
        self.assertTokenEqual(results[2], Token(Tokens.QUOTE, 2))
        self.assertTokenEqual(results[3], Token(Tokens.RPAREN, 3))
        self.assertTokenEqual(results[4], Token(Tokens.RPAREN, 4))

        text = """(cond "hello" 12)"""
        results = list(Tokenize.tokenize(text, 0))
        self.assertEqual(len(results), 5)
        self.assertTokenEqual(results[0], Token(Tokens.LPAREN, 0))
        self.assertTokenEqual(results[1], Token(Tokens.COND, 1))
        self.assertTokenEqual(results[2], Token(Tokens.STRING, 6, "hello"))
        self.assertTokenEqual(results[3], Token(Tokens.NUMBER, 14, 12))
        self.assertTokenEqual(results[4], Token(Tokens.RPAREN, 16))

    def test_tokenize_unidentifiableToken(self):
        text = "#f#k"
        result = list(Tokenize.tokenize(text,0))
        self.assertTokenEqual(result[0], Token(Tokens.FALSE, 0))
        self.assertTokenEqual(result[1], Token(Tokens.ERROR, 2))

    # Helpers
    def assertTokenEqual(self, token1, token2):
        if token1 == None:
            self.assertIsNone(token2)
            return

        self.assertEqual(token1.tokenType, token2.tokenType)
        self.assertEqual(token1.pos, token2.pos)
        self.assertEqual(token1.literal, token2.literal)

if __name__ == '__main__':
    unittest.main()

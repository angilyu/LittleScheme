import TestConfig
import unittest
import Tokenize

class SkipFunctionsTest(unittest.TestCase):

    def setUp(self):
        pass

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

if __name__ == '__main__':
    unittest.main()

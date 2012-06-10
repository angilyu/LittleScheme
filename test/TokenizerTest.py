import TestConfig
import unittest
import Tokenizer

class SkipFunctionsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_skipWhiteSpace(self):
        # text with leading spaces
        text = "    \n\r\t    \n\r\t  text"
        pos = Tokenizer._skipWhitespace(text, 0)
        self.assertEqual("text", text[pos:])

        # text with no leading space
        test = "text"
        pos = Tokenizer._skipWhitespace(text, 0)
        self.assertEqual("text", text[pos:])

    def test_skipToNewLine(self):
        textWith3Lines = "line1\nline2\nline3"
        pos = Tokenizer._skipToNextLine(textWith3Lines, 0)
        self.assertEqual(textWith3Lines[pos:], "line2\nline3")

        pos = Tokenizer._skipToNextLine(textWith3Lines, pos)
        self.assertEqual(textWith3Lines[pos:], "line3")

        pos = Tokenizer._skipToNextLine(textWith3Lines, pos)
        self.assertEqual(textWith3Lines[pos:], "")

if __name__ == '__main__':
    unittest.main()

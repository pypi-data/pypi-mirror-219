"""
test_maps
~~~~~~~~~

Unittests for the yadr.maps module.
"""
import unittest as ut

from tests.common import BaseTests
from yadr import maps
from yadr.model import Token


# Lexing test cases.
class KVDelimiterTestCase(BaseTests.MapLexTokenTestCase):
    token = Token.KV_DELIMITER
    allowed = [
        Token.NEGATIVE_SIGN,
        Token.NUMBER,
        Token.QUALIFIER,
        Token.QUALIFIER_DELIMITER,
        Token.WHITESPACE,
    ]

    def test_kv_delimiter(self):
        """Given a key-value delimiter, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, 1),
            (Token.KV_DELIMITER, ':'),
        )
        yadn = '{"spam"=1:'
        self.lex_test(exp, yadn)

    def test_kv_delimiter_whitespace(self):
        """Given a key-value delimiter, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, 1),
            (Token.KV_DELIMITER, ':'),
        )
        yadn = '{"spam"=1 :'
        self.lex_test(exp, yadn)


class MapCloseTestCase(BaseTests.MapLexTokenTestCase):
    token = Token.MAP_CLOSE
    allowed = []

    def test_map_close(self):
        """Given a map close character, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.MAP_CLOSE, '}'),
        )
        yadn = '{}'
        self.lex_test(exp, yadn)

    def test_map_close_whitespace(self):
        """Given a map close character, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.MAP_CLOSE, '}'),
        )
        yadn = '{ }'
        self.lex_test(exp, yadn)


class MapOpenTestCase(BaseTests.MapLexTokenTestCase):
    token = Token.MAP_OPEN
    allowed = [
        Token.MAP_CLOSE,
        Token.QUALIFIER,
        Token.QUALIFIER_DELIMITER,
        Token.WHITESPACE,
    ]

    def test_map_open(self):
        """Given a map open character, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
        )
        yadn = '{'
        self.lex_test(exp, yadn)


class NameDelimiterTestCase(BaseTests.MapLexTokenTestCase):
    token = Token.NAME_DELIMITER
    allowed = [
        Token.NEGATIVE_SIGN,
        Token.NUMBER,
        Token.WHITESPACE,
    ]

    def test_name_delimiter(self):
        """Given a name delimiter, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '=')
        )
        yadn = '{"spam"='
        self.lex_test(exp, yadn)

    def test_name_delimiter_whitespace(self):
        """Given a name delimiter, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '=')
        )
        yadn = '{"spam" ='
        self.lex_test(exp, yadn)


class NegativeSignTestCase(BaseTests.MapLexTokenTestCase):
    token = Token.NEGATIVE_SIGN
    allowed = [
        Token.NUMBER,
    ]

    def test_negative_sign(self):
        """Given a negative sign, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, -1),
        )
        yadn = '{"spam"=-1'
        self.lex_test(exp, yadn)


class NumberTestCase(BaseTests.MapLexTokenTestCase):
    token = Token.NUMBER
    allowed = [
        Token.KV_DELIMITER,
        Token.MAP_CLOSE,
        Token.PAIR_DELIMITER,
    ]

    def test_number(self):
        """Given a number, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, 1),
        )
        yadn = '{"spam"=1'
        self.lex_test(exp, yadn)

    def test_number_whitespace(self):
        """Given a number, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, 1),
        )
        yadn = '{"spam"= 1'
        self.lex_test(exp, yadn)


class PairDelimiterTestCase(BaseTests.MapLexTokenTestCase):
    token = Token.PAIR_DELIMITER
    allowed = [
        Token.NEGATIVE_SIGN,
        Token.NUMBER,
        Token.WHITESPACE,
    ]

    def test_pair_delimiter(self):
        """Given a pair delimiter, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, 1),
            (Token.KV_DELIMITER, ':'),
            (Token.QUALIFIER, 'value'),
            (Token.PAIR_DELIMITER, ','),
        )
        yadn = '{"spam"=1:"value",'
        self.lex_test(exp, yadn)

    def test_pair_delimiter_whitespace(self):
        """Given a pair delimiter, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, 1),
            (Token.KV_DELIMITER, ':'),
            (Token.QUALIFIER, 'value'),
            (Token.PAIR_DELIMITER, ','),
        )
        yadn = '{"spam"=1:"value" ,'
        self.lex_test(exp, yadn)


class QualifierTestCase(BaseTests.MapLexTokenTestCase):
    token = Token.QUALIFIER
    allowed = [
        Token.MAP_CLOSE,
        Token.NAME_DELIMITER,
        Token.PAIR_DELIMITER,
        Token.WHITESPACE,
    ]

    def test_qualifier(self):
        """Given a qualifier, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam')
        )
        yadn = '{"spam"'
        self.lex_test(exp, yadn)

    def test_qualifier_whitespace(self):
        """Given a qualifier, return the proper tokens."""
        exp = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'spam')
        )
        yadn = '{ "spam"'
        self.lex_test(exp, yadn)


# Parsing test cases.
class ParseTestCase(ut.TestCase):
    def setUp(self):
        self.parser = maps.Parser()

    def tearDown(self):
        self.parser = None

    def parser_test(self, exp, tokens):
        act = self.parser.parse(tokens)
        self.assertEqual(exp, act)

    # Test cases.
    def test_parser(self):
        """A basic dice mapping can be parsed."""
        exp = (
            'name',
            {
                1: "none",
                2: "success",
                3: "success",
                4: "success success",
            }
        )
        tokens = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'name'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, 1),
            (Token.KV_DELIMITER, ':'),
            (Token.QUALIFIER, 'none'),
            (Token.PAIR_DELIMITER, ','),
            (Token.NUMBER, 2),
            (Token.KV_DELIMITER, ':'),
            (Token.QUALIFIER, 'success'),
            (Token.PAIR_DELIMITER, ','),
            (Token.NUMBER, 3),
            (Token.KV_DELIMITER, ':'),
            (Token.QUALIFIER, 'success'),
            (Token.PAIR_DELIMITER, ','),
            (Token.NUMBER, 4),
            (Token.KV_DELIMITER, ':'),
            (Token.QUALIFIER, 'success success'),
            (Token.PAIR_DELIMITER, ','),
            (Token.MAP_CLOSE, '}'),
        )
        self.parser_test(exp, tokens)

    def test_parser_with_numbers(self):
        """A basic dice mapping can be parsed."""
        exp = (
            'name',
            {
                1: -1,
                2: 0,
                3: 1,
            }
        )
        tokens = (
            (Token.MAP_OPEN, '{'),
            (Token.QUALIFIER, 'name'),
            (Token.NAME_DELIMITER, '='),
            (Token.NUMBER, 1),
            (Token.KV_DELIMITER, ':'),
            (Token.NUMBER, -1),
            (Token.PAIR_DELIMITER, ','),
            (Token.NUMBER, 2),
            (Token.KV_DELIMITER, ':'),
            (Token.NUMBER, 0),
            (Token.PAIR_DELIMITER, ','),
            (Token.NUMBER, 3),
            (Token.KV_DELIMITER, ':'),
            (Token.NUMBER, 1),
            (Token.MAP_CLOSE, '}'),
        )
        self.parser_test(exp, tokens)

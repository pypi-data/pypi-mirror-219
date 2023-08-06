"""
test_encoder
~~~~~~~~~~~~

Unit tests for the yadr.encoder module.
"""
import unittest as ut

from yadr import encode as e
from yadr import model as m


# Encoder test case.
class EncoderTestCase(ut.TestCase):
    def setUp(self):
        self.encoder = e.Encoder()

    def tearDown(self):
        self.encoder = None

    def test_boolean(self):
        """An bool becomes a string containing the YADN boolean."""
        exp = 'T'
        data = True
        act = self.encoder.encode(data)
        self.assertEqual(exp, act)

    def test_compound_result(self):
        """A CompoundResult becomes a string of roll delimited
        values.
        """
        exp = '[1, 1, 3, 8]; 3'
        data = m.CompoundResult((
            (1, 1, 3, 8),
            3
        ))
        act = self.encoder.encode(data)
        self.assertEqual(exp, act)

    def test_number(self):
        """An int becomes a string containing the YADN number."""
        exp = '3'
        data = 3
        act = self.encoder.encode(data)
        self.assertEqual(exp, act)

    def test_pool(self):
        """A tuple of integers becomes a string containing the
        YADN pool.
        """
        exp = '[1, 1, 3, 8]'
        data = (1, 1, 3, 8)
        act = self.encoder.encode(data)
        self.assertEqual(exp, act)

    def test_qualifier(self):
        """A string becomes a double-quoted string.
        """
        exp = '"spam"'
        data = 'spam'
        act = self.encoder.encode(data)
        self.assertEqual(exp, act)

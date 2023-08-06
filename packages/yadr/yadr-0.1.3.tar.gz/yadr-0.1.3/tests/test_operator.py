"""
test_operator
~~~~~~~~~~~~~

Dice operators for the `yadr` package.
"""
import unittest as ut
from unittest.mock import patch

from yadr import operator as op


# Choice test cases.
class ChoiceTestCase(ut.TestCase):
    def test_choice_options(self):
        """Generate choice options."""
        # Expected value.
        exp = ('spam', 'eggs')

        # Test data and state.
        a = exp[0]
        b = exp[1]

        # Run test.
        act = op.choice_options(a, b)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_choice(self):
        """Make a choice."""
        # Expected value.
        exp = 'spam'

        # Test data and state.
        boolean = True
        options = ('spam', 'eggs')

        # Run test.
        act = op.choice(boolean, options)

        # Determine test result.
        self.assertEqual(exp, act)


# Dice operation test cases.
class ConcatTestCase(ut.TestCase):
    @patch('random.randint')
    def test_concat(self, mock_randint):
        """Concatenate the least significant digit of the dice."""
        # Expected value.
        exp = 304

        # Test data and state.
        mock_randint.side_effect = (3, 10, 4)
        num = 3
        size = 10

        # Run test.
        act = op.concat(num, size)

        # Determine test result.
        self.assertEqual(exp, act)


class DieTestCase(ut.TestCase):
    def die_test(self, exp, args=None, kwargs=None, seed='spam'):
        """Common test for the die function."""
        if not args:
            args = []
        if not kwargs:
            kwargs = {}
        op._seed(seed)
        act = op.die(*args, **kwargs)
        self.assertEqual(exp, act)

    def test_die(self):
        """Given a number of dice and the size of the die,
        roll that many dice and return the result.
        """
        exp = 4
        kwargs = {
            'num': 1,
            'size': 6,
        }
        seed = 'spam12'
        self.die_test(exp, kwargs=kwargs, seed=seed)


class ExplodingDie(ut.TestCase):
    def exploding_die_test(self, exp, num, size):
        """Common test for the die function."""
        act = op.exploding_die(num, size)
        self.assertEqual(exp, act)

    @patch('random.randint')
    def test_exploding_die(self, mock_randint):
        """Given a number of dice and the size of the die,
        roll that many exploding dice and return the result.
        """
        exp = 25
        mock_randint.side_effect = [2, 1, 4, 4, 3, 1, 4, 4, 2]
        num = 5
        size = 4
        self.exploding_die_test(exp, num, size)


class KeepHighDie(ut.TestCase):
    @patch('random.randint')
    def test_keep_high_die(self, mock_randint):
        # Expected value.
        exp = 18

        # Test data and state.
        mock_randint.side_effect = [15, 3, 6, 18, 10]
        num = 5
        size = 20

        # Run test.
        act = op.keep_high_die(num, size)

        # Determine test result.
        self.assertEqual(exp, act)


class KeepLowDie(ut.TestCase):
    @patch('random.randint')
    def test_keep_high_die(self, mock_randint):
        # Expected value.
        exp = 3

        # Test data and state.
        mock_randint.side_effect = [15, 3, 6, 18, 10]
        num = 5
        size = 20

        # Run test.
        act = op.keep_low_die(num, size)

        # Determine test result.
        self.assertEqual(exp, act)


class WildDie(ut.TestCase):
    @patch('random.randint')
    def test_wild_die(self, mock_randint):
        # Expected value.
        exp = 17

        # Test data and state.
        mock_randint.side_effect = [3, 4, 1, 5, 4]
        num = 5
        size = 6

        # Run test.
        act = op.wild_die(num, size)

        # Determine test result.
        self.assertEqual(exp, act)

    @patch('random.randint')
    def test_wild_die_explodes(self, mock_randint):
        # Expected value.
        exp = 22

        # Test data and state.
        mock_randint.side_effect = [6, 2, 4, 1, 5, 4]
        num = 5
        size = 6

        # Run test.
        act = op.wild_die(num, size)

        # Determine test result.
        self.assertEqual(exp, act)

    @patch('random.randint')
    def test_wild_die_is_one(self, mock_randint):
        # Expected value.
        exp = 0

        # Test data and state.
        mock_randint.side_effect = [1, 4, 1, 5, 4]
        num = 5
        size = 6

        # Run test.
        act = op.wild_die(num, size)

        # Determine test result.
        self.assertEqual(exp, act)


# Pool degeneration test cases.
class PoolConcatenateTestCase(ut.TestCase):
    def test_pool_concatenate(self):
        """Concatenate the members in the pool."""
        exp = 314
        pool = (3, 1, 4)
        act = op.pool_concatenate(pool)
        self.assertEqual(exp, act)


class PoolCountTestCase(ut.TestCase):
    def test_pool_count(self):
        """Count the members in the pool."""
        exp = 3
        pool = (3, 1, 4)
        act = op.pool_count(pool)
        self.assertEqual(exp, act)


class PoolSumTestCase(ut.TestCase):
    def test_pool_count(self):
        """Sum the members in the pool."""
        exp = 8
        pool = (3, 1, 4)
        act = op.pool_sum(pool)
        self.assertEqual(exp, act)


class CountSuccessesTestCase(ut.TestCase):
    def test_count_successes(self):
        """Count the number of values above or equal to a target."""
        # Expected value.
        exp = 5

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        target = 5

        # Run test.
        act = op.count_successes(pool, target)

        # Determine test result.
        self.assertEqual(exp, act)


class CountSuccessesWithBotchesTestCase(ut.TestCase):
    def test_count_successes_with_botch(self):
        """Count the number of values above or equal to a target and
        remove botches.
        """
        # Expected value.
        exp = 3

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        target = 5

        # Run test.
        act = op.count_successes_with_botch(pool, target)

        # Determine test result.
        self.assertEqual(exp, act)


# Pool generation operation test cases.
class DicePoolTestCase(ut.TestCase):
    @patch('random.randint')
    def test_dice_pool(self, mock_randint):
        """Generate a dice pool."""
        # Expected value.
        exp = (3, 5, 1, 10, 8, 4, 3)

        # Test data and state.
        mock_randint.side_effect = exp
        num = 7
        size = 10

        # Run test.
        act = op.dice_pool(num, size)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class ExplodingPoolTestCase(ut.TestCase):
    @patch('random.randint')
    def test_exploding_pool(self, mock_randint):
        """Generate a dice pool."""
        # Expected value.
        exp = (2, 9, 1, 1, 13, 3)

        # Test data and state.
        mock_randint.side_effect = (2, 6, 1, 1, 6, 3, 3, 6, 1)
        num = 6
        size = 6

        # Run test.
        act = op.exploding_pool(num, size)

        # Determine test result.
        self.assertTupleEqual(exp, act)


# Pool operation test cases.
class PoolKeepAbove(ut.TestCase):
    def test_pool_keep_above(self):
        """Keep dice equal to or below above the given value from the
        pool.
        """
        # Expected value.
        exp = (5, 6, 4, 5, 6, 6)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        keep = 4

        # Run test.
        act = op.pool_keep_above(pool, keep)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolKeepBelow(ut.TestCase):
    def test_pool_keep_below(self):
        """Keep dice equal to or below the given value from the pool."""
        # Expected value.
        exp = (1, 2, 4, 1, 3)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        ceiling = 4

        # Run test.
        act = op.pool_keep_below(pool, ceiling)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolCapTestCase(ut.TestCase):
    def test_pool_cap(self):
        """Dice in the pool are capped at the given value."""
        # Expected value.
        exp = (1, 2, 3, 7, 5, 6, 7, 7, 7, 4)

        # Test data and state.
        pool = (1, 2, 3, 10, 5, 6, 7, 8, 9, 4)
        cap = 7

        # Run test.
        act = op.pool_cap(pool, cap)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolFloorTestCase(ut.TestCase):
    def test_pool_floor(self):
        """Dice in the pool are floored at the given value."""
        # Expected value.
        exp = (3, 3, 3, 10, 5, 6, 7, 8, 9, 4)

        # Test data and state.
        pool = (1, 2, 3, 10, 5, 6, 7, 8, 9, 4)
        cap = 3

        # Run test.
        act = op.pool_floor(pool, cap)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolKeepHigh(ut.TestCase):
    def test_pool_keep_high(self):
        """Keep the given number of highest dice from the pool."""
        # Expected value.
        exp = (5, 6, 5, 6, 6)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        keep = 5

        # Run test.
        act = op.pool_keep_high(pool, keep)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolKeepLow(ut.TestCase):
    def test_pool_keep_low(self):
        """Keep the given number of highest dice from the pool."""
        # Expected value.
        exp = (1, 2, 1)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        keep = 3

        # Run test.
        act = op.pool_keep_low(pool, keep)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolModulo(ut.TestCase):
    def test_pool_keep_below(self):
        """Perform a modulo on all members."""
        # Expected value.
        exp = (1, 2, 2, 0, 1, 2, 1, 0, 0, 0)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        divisor = 3

        # Run test.
        act = op.pool_modulo(pool, divisor)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolRemove(ut.TestCase):
    def test_pool_keep_below(self):
        """Keep dice equal to or below the given value from the pool."""
        # Expected value.
        exp = (1, 2, 6, 4, 1, 6, 3, 6)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        cut = 5

        # Run test.
        act = op.pool_remove(pool, cut)

        # Determine test result.
        self.assertTupleEqual(exp, act)

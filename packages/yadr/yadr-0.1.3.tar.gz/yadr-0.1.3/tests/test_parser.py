"""
test_parse
~~~~~~~~~~

Unit tests for the yadr.parse module.
"""
import unittest as ut
from unittest.mock import patch

from yadr import parser as p
from yadr.model import Token
from yadr import operator as yo


# Test cases.
class ParserTestCase(ut.TestCase):
    def setUp(self):
        self.parser = p.Parser()

    def tearDown(self):
        self.parser = None

    def parser_test(self, exp, tokens):
        """Return the expected result for the given tokens."""
        act = self.parser.parse(tokens)
        self.assertEqual(exp, act)

    # Tests.
    # Identities
    def test_boolean(self):
        """Parse a boolean."""
        exp = True
        tokens = (
            (Token.BOOLEAN, True),
        )
        self.parser_test(exp, tokens)

    def test_number(self):
        "Parse a number."
        exp = 5
        tokens = (
            (Token.NUMBER, 5),
        )
        self.parser_test(exp, tokens)

    def test_pool(self):
        "Parse a pool."
        exp = (3, 3, 4)
        tokens = (
            (Token.POOL, (3, 3, 4)),
        )
        self.parser_test(exp, tokens)

    def test_quantifier(self):
        """Parse a qualifier."""
        exp = 'spam'
        tokens = (
            (Token.QUALIFIER, 'spam'),
        )
        self.parser_test(exp, tokens)

    # Basic arithmetic.
    def test_addition(self):
        """Parse basic addition."""
        exp = 5
        tokens = (
            (Token.NUMBER, 3),
            (Token.AS_OPERATOR, '+'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_division(self):
        "Perform basic division."
        exp = 2
        tokens = (
            (Token.NUMBER, 4),
            (Token.MD_OPERATOR, '/'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_division_rounds_down(self):
        "Division rounds down to the nearest integer (floor division)."
        exp = 2
        tokens = (
            (Token.NUMBER, 5),
            (Token.MD_OPERATOR, '/'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_exponentiation(self):
        "Perform basic division."
        exp = 9
        tokens = (
            (Token.NUMBER, 3),
            (Token.EX_OPERATOR, '^'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_modulo(self):
        "Perform basic modulo."
        exp = 1
        tokens = (
            (Token.NUMBER, 3),
            (Token.MD_OPERATOR, '%'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_multiplication(self):
        "Perform basic multiplication."
        exp = 6
        tokens = (
            (Token.NUMBER, 3),
            (Token.MD_OPERATOR, '*'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_subtraction(self):
        "Perform basic subtraction."
        exp = 1
        tokens = (
            (Token.NUMBER, 3),
            (Token.AS_OPERATOR, '-'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    # Choice and related operators.
    def test_choice(self):
        """Perform choice operation."""
        exp = 'eggs'
        tokens = (
            (Token.BOOLEAN, False),
            (Token.CHOICE_OPERATOR, '?'),
            (Token.QUALIFIER, 'spam'),
            (Token.OPTIONS_OPERATOR, ':'),
            (Token.QUALIFIER, 'eggs'),
        )
        self.parser_test(exp, tokens)

    def test_greater_than(self):
        """Perform greater than comparison."""
        exp = True
        tokens = (
            (Token.NUMBER, 3),
            (Token.COMPARISON_OPERATOR, '>'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_greater_than_or_equal(self):
        """Perform greater than or equal comparison."""
        exp = True
        tokens = (
            (Token.NUMBER, 3),
            (Token.COMPARISON_OPERATOR, '>='),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_less_than(self):
        """Perform less than comparison."""
        exp = False
        tokens = (
            (Token.NUMBER, 3),
            (Token.COMPARISON_OPERATOR, '<'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_less_than_or_equal(self):
        """Perform less than comparison."""
        exp = False
        tokens = (
            (Token.NUMBER, 3),
            (Token.COMPARISON_OPERATOR, '<='),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_equal(self):
        """Perform less than comparison."""
        exp = False
        tokens = (
            (Token.NUMBER, 3),
            (Token.COMPARISON_OPERATOR, '=='),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_not_equal(self):
        """Perform less than comparison."""
        exp = True
        tokens = (
            (Token.NUMBER, 3),
            (Token.COMPARISON_OPERATOR, '!='),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_options_operator(self):
        """Create a choice options."""
        exp = ('spam', 'eggs')
        tokens = (
            (Token.QUALIFIER, 'spam'),
            (Token.OPTIONS_OPERATOR, ':'),
            (Token.QUALIFIER, 'eggs'),
        )
        self.parser_test(exp, tokens)

    # Dice operators.
    @patch('random.randint')
    def test_concat(self, mock_randint):
        """Concatenate dice rolls."""
        mock_randint.side_effect = [1, 11, 3]
        exp = 113
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'dc'),
            (Token.NUMBER, 12),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_die(self, mock_randint):
        """Roll a die."""
        mock_randint.side_effect = [1, 2, 2]
        exp = 5
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'd'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_exploding_die(self, mock_randint):
        """Roll an exploding die."""
        mock_randint.side_effect = [1, 2, 4, 2, 2]
        exp = 11
        tokens = (
            (Token.NUMBER, 4),
            (Token.DICE_OPERATOR, 'd!'),
            (Token.NUMBER, 4),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_keep_high_die(self, mock_randint):
        """Roll dice and keep the highest."""
        mock_randint.side_effect = [1, 5, 3]
        exp = 5
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'dh'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_keep_low_die(self, mock_randint):
        """Roll dice and keep the lowest."""
        mock_randint.side_effect = [1, 5, 3]
        exp = 1
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'dl'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_wild_die(self, mock_randint):
        """Roll dice and keep the lowest."""
        mock_randint.side_effect = [4, 2, 1, 6]
        exp = 13
        tokens = (
            (Token.NUMBER, 4),
            (Token.DICE_OPERATOR, 'dw'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    # Pool generation operators.
    @patch('random.randint')
    def test_dice_pool(self, mock_randint):
        """Roll dice and keep the highest."""
        mock_randint.side_effect = [1, 5, 3]
        exp = (1, 5, 3)
        tokens = (
            (Token.NUMBER, 3),
            (Token.POOL_GEN_OPERATOR, 'g'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_exploding_pool(self, mock_randint):
        """Roll an exploding dice pool."""
        mock_randint.side_effect = [1, 5, 3]
        exp = (1, 5, 3)
        tokens = (
            (Token.NUMBER, 3),
            (Token.POOL_GEN_OPERATOR, 'g!'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    # Unary pool degeneration operators.
    @patch('random.randint')
    def test_pool_concatenate(self, mock_randint):
        """Concatenate the dice in a pool."""
        mock_randint.side_effect = [1, 5, 3]
        exp = 153
        tokens = (
            (Token.U_POOL_DEGEN_OPERATOR, 'C'),
            (Token.NUMBER, (1, 5, 3)),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_pool_count(self, mock_randint):
        """Count the dice in a pool."""
        mock_randint.side_effect = [1, 5, 3]
        exp = 3
        tokens = (
            (Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (Token.NUMBER, (1, 5, 3)),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_pool_sum(self, mock_randint):
        """Count the dice in a pool."""
        mock_randint.side_effect = [1, 5, 3]
        exp = 9
        tokens = (
            (Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (Token.NUMBER, (1, 5, 3)),
        )
        self.parser_test(exp, tokens)

    # Pool degeneration operators.
    def test_count_successes(self):
        """Keep a values that aren't a given number in the pool."""
        exp = 2
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_DEGEN_OPERATOR, 'ns'),
            (Token.NUMBER, 8),
        )
        self.parser_test(exp, tokens)

    def test_count_successes_with_botch(self):
        """Keep a values that aren't a given number in the pool."""
        exp = 1
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_DEGEN_OPERATOR, 'nb'),
            (Token.NUMBER, 8),
        )
        self.parser_test(exp, tokens)

    # Pool operators.
    def test_pool_keep_above(self):
        """Keep a values above a given number in the pool."""
        exp = (8, 9)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'pa'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    def test_pool_keep_below(self):
        """Keep a values below a given number in the pool."""
        exp = (5, 1)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'pb'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    def test_pool_cap(self):
        """Cap the values in a pool at a given value."""
        exp = (5, 7, 1, 7)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'pc'),
            (Token.NUMBER, 7),
        )
        self.parser_test(exp, tokens)

    def test_pool_floor(self):
        """Floor the values in a pool at a given value."""
        exp = (8, 8, 8, 9)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'pf'),
            (Token.NUMBER, 8),
        )
        self.parser_test(exp, tokens)

    def test_pool_keep_high(self):
        """Keep a number of highest values from the pool."""
        exp = (8, 9)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'ph'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_pool_keep_low(self):
        """Keep a number of highest values from the pool."""
        exp = (5, 1)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'pl'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_pool_modulo(self):
        """Perform a modulo on each member."""
        exp = (0, 3, 1, 4)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'p%'),
            (Token.NUMBER, 5),
        )
        self.parser_test(exp, tokens)

    def test_pool_remove(self):
        """Keep a values that aren't a given number in the pool."""
        exp = (5, 1, 9)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'pr'),
            (Token.NUMBER, 8),
        )
        self.parser_test(exp, tokens)

    # Dice mapping.
    def test_map(self):
        """Parse and store a dice map."""
        # Expected value.
        exp = 'success'

        # Test data and state.
        tokens = (
            (Token.MAP, ('spam', {1: 'none', 2: 'success'})),
        )
        _ = self.parser.parse(tokens)

        # Run test.
        act = self.parser.dice_map['spam'][2]

        # Determine test result.
        self.assertEqual(exp, act)

    # Mapping operators.
    @patch('random.randint')
    def test_map_result(self, mock_randint):
        """Given a map and a roll with a dice map operator, return the
        correct result.
        """
        # Expected value.
        exp = 'success'

        # Test data and state.
        parser = p.Parser()
        mock_randint.side_effect = (3, )
        parser.dice_map['_test_map_result'] = {
            1: 'none',
            2: 'success',
            3: 'success',
            4: 'success success',
        }
        tokens = (
            (Token.NUMBER, 1),
            (Token.DICE_OPERATOR, 'd'),
            (Token.NUMBER, 4),
            (Token.MAPPING_OPERATOR, 'm'),
            (Token.QUALIFIER, '_test_map_result'),
        )

        # Run test.
        act = parser.parse(tokens)

        # Determine test result.
        self.assertEqual(exp, act)

    @patch('random.randint')
    def test_map_result_pool(self, mock_randint):
        """Given a map and a roll with a dice map operator, return the
        correct result.
        """
        # Expected value.
        exp = ('success', 'none')

        # Test data and state.
        mock_randint.side_effect = (3, 1, )
        self.parser.dice_map['_test_map_result'] = {
            1: 'none',
            2: 'success',
            3: 'success',
            4: 'success success',
        }
        tokens = (
            (Token.NUMBER, 2),
            (Token.DICE_OPERATOR, 'g'),
            (Token.NUMBER, 4),
            (Token.MAPPING_OPERATOR, 'm'),
            (Token.QUALIFIER, '_test_map_result'),
        )

        # Run test.
        act = self.parser.parse(tokens)

        # Determine test result.
        self.assertEqual(exp, act)

    @patch('random.randint')
    # Test rolls and results.
    def test_roll_delimiter(self, mock_randint):
        """Return the result of two rolls."""
        mock_randint.side_effect = (1, 1, 3, 8)
        exp = ((1, 1, 3), 10)
        tokens = (
            (Token.NUMBER, 3),
            (Token.POOL_GEN_OPERATOR, 'g'),
            (Token.NUMBER, 8),
            (Token.ROLL_DELIMITER, ';'),
            (Token.NUMBER, 1),
            (Token.DICE_OPERATOR, 'd'),
            (Token.NUMBER, 10),
            (Token.AS_OPERATOR, '+'),
            (Token.NUMBER, 2)
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_roll_delimiter_remove_none_result(self, mock_randint):
        """Return the result of two rolls."""
        mock_randint.side_effect = (2,)
        exp = 'lose'
        tokens = (
            (Token.MAP, (
                'spam',
                {1: "win", 2: "lose"}
            )),
            (Token.ROLL_DELIMITER, ';'),
            (Token.NUMBER, 1),
            (Token.DICE_OPERATOR, 'd'),
            (Token.NUMBER, 2),
            (Token.MAPPING_OPERATOR, 'm'),
            (Token.QUALIFIER, 'spam')
        )
        self.parser_test(exp, tokens)

    # Test order of precedence.
    def test_can_perform_multiple_operations(self):
        """The parser can parse statements with multiple operators."""
        exp = 9
        tokens = (
            (Token.NUMBER, 3),
            (Token.AS_OPERATOR, '+'),
            (Token.NUMBER, 2),
            (Token.AS_OPERATOR, '+'),
            (Token.NUMBER, 4),
        )
        self.parser_test(exp, tokens)

    def test_exponentiation_before_multiplication(self):
        """Multiplication should occur before addition."""
        exp = 48
        tokens = (
            (Token.NUMBER, 3),
            (Token.MD_OPERATOR, '*'),
            (Token.NUMBER, 2),
            (Token.EX_OPERATOR, '^'),
            (Token.NUMBER, 4),
        )
        self.parser_test(exp, tokens)

    def test_multiplication_before_addition(self):
        """Multiplication should occur before addition."""
        exp = 11
        tokens = (
            (Token.NUMBER, 3),
            (Token.AS_OPERATOR, '+'),
            (Token.NUMBER, 2),
            (Token.MD_OPERATOR, '*'),
            (Token.NUMBER, 4),
        )
        self.parser_test(exp, tokens)

    def test_parens_before_multiplication(self):
        """Parentheses should occur before multiplication."""
        exp = 18
        tokens = (
            (Token.NUMBER, 3),
            (Token.MD_OPERATOR, '*'),
            (Token.GROUP_OPEN, '('),
            (Token.NUMBER, 2),
            (Token.AS_OPERATOR, '+'),
            (Token.NUMBER, 4),
            (Token.GROUP_CLOSE, ')'),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_pool_generation_happens_before_pool_degeneration(self, mock_ri):
        """Pool generation should happen before pool degeneration
        in order of operations.
        """
        # Expected value.
        exp = 20

        # Test data and state.
        rand_results = [5, 4, 6, 2, 3]
        mock_ri.side_effect = rand_results
        tokens = (
            (Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (Token.NUMBER, 5),
            (Token.POOL_GEN_OPERATOR, 'g'),
            (Token.NUMBER, 6),
        )

        # Run test.
        act = self.parser.parse(tokens)

        # Determine test result.
        self.assertEqual(exp, act)

    @patch('random.randint')
    def test_unary_pool_degeneration_happens_before_operators(self, mock_ri):
        """Unary pool degeneration should happen before operators
        in order of operations.
        """
        # Expected value.
        exp = 25

        # Test data and state.
        rand_results = [5, 4, 6, 2, 3]
        mock_ri.side_effect = rand_results
        tokens = (
            (Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (Token.NUMBER, 5),
            (Token.POOL_GEN_OPERATOR, 'g'),
            (Token.NUMBER, 6),
            (Token.AS_OPERATOR, '+'),
            (Token.NUMBER, 5),
        )

        # Run test.
        act = self.parser.parse(tokens)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_pool_operation_happens_before_pool_degeneration(self):
        """Pool operations should happen before pool degeneration
        in order of operations.
        """
        # Expected value.
        exp = 1

        # Test data and state.
        tokens = (
            (Token.POOL, (5, 4, 6, 2, 3)),
            (Token.POOL_OPERATOR, 'pb'),
            (Token.NUMBER, 5),
            (Token.POOL_DEGEN_OPERATOR, 'ns'),
            (Token.NUMBER, 5),
        )

        # Run test.
        act = self.parser.parse(tokens)

        # Determine test result.
        self.assertEqual(exp, act)

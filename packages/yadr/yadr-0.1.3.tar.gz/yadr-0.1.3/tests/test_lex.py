"""
test_lex
~~~~~~~~

Unit tests for the dice notation lexer.
"""
import unittest as ut

from tests.common import BaseTests
from yadr import lex
from yadr import model as m


# Symbol test cases.
class ASOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.AS_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_addition(self):
        """Given a basic addition equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 15),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, 3),
        )
        data = '15+3'
        self.lex_test(exp, data)

    def test_basic_addition_with_spaces(self):
        """Given a basic addition equation containing whitespace,
        return the tokens that represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 15),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, 3),
        )
        data = ' 15 + 3 '
        self.lex_test(exp, data)

    def test_basic_subtraction(self):
        """Given a basic subtraction equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 200),
            (lex.Token.AS_OPERATOR, '-'),
            (lex.Token.NUMBER, 10),
        )
        data = '200-10'
        self.lex_test(exp, data)


class BooleanTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.BOOLEAN
    allowed = [
        m.Token.CHOICE_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_boolean_true(self):
        """Lex a boolean."""
        exp = (
            (lex.Token.BOOLEAN, True),
        )
        data = 'T'
        self.lex_test(exp, data)

    def test_boolean_false(self):
        """Lex a boolean."""
        exp = (
            (lex.Token.BOOLEAN, True),
        )
        data = 'T'
        self.lex_test(exp, data)


class ChoiceTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.CHOICE_OPERATOR
    allowed = [
        m.Token.QUALIFIER,
        m.Token.QUALIFIER_DELIMITER,
        m.Token.WHITESPACE,
    ]

    def test_choice(self):
        """Lex a choice operator."""
        exp = (
            (lex.Token.BOOLEAN, True),
            (lex.Token.CHOICE_OPERATOR, '?'),
            (lex.Token.QUALIFIER, 'spam'),
            (lex.Token.OPTIONS_OPERATOR, ':'),
            (lex.Token.QUALIFIER, 'eggs'),
        )
        data = 'T?"spam":"eggs"'
        self.lex_test(exp, data)


class ComparisonOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.COMPARISON_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_equal(self):
        """Lex equal."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '=='),
            (lex.Token.NUMBER, 20),
        )
        data = '21==20'
        self.lex_test(exp, data)

    def test_basic_greater_than(self):
        """Lex greater than."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '>'),
            (lex.Token.NUMBER, 20),
        )
        data = '21>20'
        self.lex_test(exp, data)

    def test_basic_greater_than_or_equal(self):
        """Lex greater than or equal."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '>='),
            (lex.Token.NUMBER, 20),
        )
        data = '21>=20'
        self.lex_test(exp, data)

    def test_basic_greater_than_whitspace(self):
        """Lex greater than."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '>'),
            (lex.Token.NUMBER, 20),
        )
        data = '21 > 20'
        self.lex_test(exp, data)

    def test_basic_less_than(self):
        """Lex greater than."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '<'),
            (lex.Token.NUMBER, 20),
        )
        data = '21<20'
        self.lex_test(exp, data)

    def test_basic_less_than_or_equal(self):
        """Lex less than or equal."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '<='),
            (lex.Token.NUMBER, 20),
        )
        data = '21<=20'
        self.lex_test(exp, data)

    def test_basic_not_equal(self):
        """Lex not equal."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '!='),
            (lex.Token.NUMBER, 20),
        )
        data = '21!=20'
        self.lex_test(exp, data)


class DiceOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.DICE_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_concat(self):
        """Given a basic concat equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dc'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dc10'
        self.lex_test(exp, data)

    def test_basic_die(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '20d10'
        self.lex_test(exp, data)

    def test_basic_exploding_die(self):
        """Given a basic exploding die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'd!'),
            (lex.Token.NUMBER, 10),
        )
        data = '20d!10'
        self.lex_test(exp, data)

    def test_basic_keep_high_die(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dh'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dh10'
        self.lex_test(exp, data)

    def test_basic_keep_low_die(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dl'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dl10'
        self.lex_test(exp, data)

    def test_basic_wild_die(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dw'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dw10'
        self.lex_test(exp, data)


class ExOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.EX_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_exponentiation(self):
        """Given a basic exponentiation equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.EX_OPERATOR, '^'),
            (lex.Token.NUMBER, 10),
        )
        data = '20^10'
        self.lex_test(exp, data)


class GroupingTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.GROUP_CLOSE
    allowed = [
        m.Token.AS_OPERATOR,
        m.Token.MD_OPERATOR,
        m.Token.EX_OPERATOR,
        m.Token.DICE_OPERATOR,
        m.Token.GROUP_CLOSE,
        m.Token.POOL_OPERATOR,
        m.Token.ROLL_DELIMITER,
        m.Token.POOL_GEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_parentheses(self):
        """Given a statement containing parenthesis, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 32),
            (lex.Token.AS_OPERATOR, '-'),
            (lex.Token.NUMBER, 5),
            (lex.Token.GROUP_CLOSE, ')'),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 21),
        )
        data = '(32-5)*21'
        self.lex_test(exp, data)

    def test_parentheses_with_whitespace(self):
        """Given a statement containing parenthesis and whitespace,
        return the tokenized equation.
        """
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 32),
            (lex.Token.AS_OPERATOR, '-'),
            (lex.Token.NUMBER, 5),
            (lex.Token.GROUP_CLOSE, ')'),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 21),
        )
        data = '( 32 - 5 ) * 21'
        self.lex_test(exp, data)


class GroupOpenTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.GROUP_OPEN
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.POOL,
        m.Token.POOL_OPEN,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]


class MapTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.MAP
    allowed = [
        m.Token.ROLL_DELIMITER,
        m.Token.WHITESPACE,
    ]

    def test_map(self):
        """Given a statement containing a map, return the tokenized
        dice mapping.
        """
        exp = ((
            m.Token.MAP,
            (
                'name',
                {
                    1: "none",
                    2: "success",
                    3: "success",
                    4: "success success",
                }
            )
        ),)
        yadn = '{"name"=1:"none",2:"success",3:"success",4:"success success"}'
        self.lex_test(exp, yadn)


class MappingOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.MAPPING_OPERATOR
    allowed = [
        m.Token.QUALIFIER,
        m.Token.QUALIFIER_DELIMITER,
        m.Token.WHITESPACE,
    ]

    def test_mapping_operator(self):
        """Lex a mapping operator."""
        exp = (
            (lex.Token.NUMBER, 3),
            (lex.Token.MAPPING_OPERATOR, 'm'),
            (lex.Token.QUALIFIER, 'spam'),
        )
        data = '3m"spam"'
        self.lex_test(exp, data)


class MDOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.MD_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_division(self):
        """Given a basic division equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.MD_OPERATOR, '/'),
            (lex.Token.NUMBER, 10),
        )
        data = '20/10'
        self.lex_test(exp, data)

    def test_basic_exponentiation(self):
        """Given a basic exponentiation equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.EX_OPERATOR, '^'),
            (lex.Token.NUMBER, 10),
        )
        data = '20^10'
        self.lex_test(exp, data)

    def test_basic_modulo(self):
        """Given a basic modulo equation, return the tokens
        that represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.MD_OPERATOR, '%'),
            (lex.Token.NUMBER, 10),
        )
        data = '2%10'
        self.lex_test(exp, data)

    def test_basic_multiplication(self):
        """Given a basic multiplication equation, return the tokens
        that represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 10),
        )
        data = '2*10'
        self.lex_test(exp, data)


class NumberTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.NUMBER
    allowed = [
        m.Token.AS_OPERATOR,
        m.Token.COMPARISON_OPERATOR,
        m.Token.EX_OPERATOR,
        m.Token.DICE_OPERATOR,
        m.Token.GROUP_CLOSE,
        m.Token.MAPPING_OPERATOR,
        m.Token.MD_OPERATOR,
        m.Token.POOL_GEN_OPERATOR,
        m.Token.ROLL_DELIMITER,
        m.Token.WHITESPACE,
    ]

    # Allowed next symbol.
    def test_number_cannot_follow_number(self):
        """Numbers cannot follow numbers."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '4 cannot follow a NUMBER.'

        # Test data and state.
        data = '3 4'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)


class OptionsOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.OPTIONS_OPERATOR
    allowed = [
        m.Token.QUALIFIER,
        m.Token.QUALIFIER_DELIMITER,
        m.Token.WHITESPACE,
    ]

    def test_basic_options_operator(self):
        """Lex choice options."""
        exp = (
            (lex.Token.QUALIFIER, 'spam'),
            (lex.Token.OPTIONS_OPERATOR, ':'),
            (lex.Token.QUALIFIER, 'eggs'),
        )
        data = '"spam":"eggs"'
        self.lex_test(exp, data)


class PoolDegenerationOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.POOL_DEGEN_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_count_successes(self):
        """Given a basic count successes statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.NUMBER, 5),
        )
        data = '[5,1,9]ns5'
        self.lex_test(exp, data)

    def test_basic_count_successes_with_botch(self):
        """Given a basic count successes with botches statement, return
        the tokens in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'nb'),
            (lex.Token.NUMBER, 5),
        )
        data = '[5,1,9]nb5'
        self.lex_test(exp, data)

    def test_count_successes_before_group(self):
        """Groups can follow pool degeneration operators."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 3),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, 2),
            (lex.Token.GROUP_CLOSE, ')'),
        )
        data = '[5,1,9]ns(3+2)'
        self.lex_test(exp, data)

    def test_count_successes_before_unary_pool_degen(self):
        """Unary pool degens can follow pool degeneration operators."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (5, 1, 9)),
        )
        data = '[5,1,9]nsN[5,1,9]'
        self.lex_test(exp, data)

    def test_count_successes_before_operator(self):
        """Operators cannot occur after pool degen operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow a POOL_DEGEN_OPERATOR.'

        # Test data and state.
        data = '[5,1,9]ns+'
        lexer = lex.Lexer()

        # Run test and determine results.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)


class PoolGenerationOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.POOL_GEN_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_dice_pool(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.POOL_GEN_OPERATOR, 'g'),
            (lex.Token.NUMBER, 10),
        )
        data = '20g10'
        self.lex_test(exp, data)

    def test_basic_expolding_pool(self):
        """Given a basic pool generation, return the tokens that
        represent the generation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.POOL_GEN_OPERATOR, 'g!'),
            (lex.Token.NUMBER, 10),
        )
        data = '20g!10'
        self.lex_test(exp, data)


class PoolOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.POOL_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_pool_keep_above(self):
        """Given a basic pool keep above statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pa'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]pa2'
        self.lex_test(exp, data)

    def test_basic_pool_keep_below(self):
        """Given a basic pool keep below statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pb'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]pb2'
        self.lex_test(exp, data)

    def test_basic_pool_cap(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pc'),
            (lex.Token.NUMBER, 7),
        )
        data = '[5,1,9]pc7'
        self.lex_test(exp, data)

    def test_basic_pool_floor(self):
        """Floor the minimum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pf'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]pf2'
        self.lex_test(exp, data)

    def test_basic_pool_keep_high(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'ph'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]ph2'
        self.lex_test(exp, data)

    def test_basic_pool_keep_low(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pl'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]pl2'
        self.lex_test(exp, data)

    def test_basic_pool_modulo(self):
        """Given a basic pool modulo statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'p%'),
            (lex.Token.NUMBER, 5),
        )
        data = '[5,1,9]p%5'
        self.lex_test(exp, data)

    def test_basic_pool_remove(self):
        """Given a basic pool remove statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pr'),
            (lex.Token.NUMBER, 5),
        )
        data = '[5,1,9]pr5'
        self.lex_test(exp, data)


class PoolTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.POOL
    allowed = [
        m.Token.GROUP_CLOSE,
        m.Token.POOL_OPERATOR,
        m.Token.POOL_DEGEN_OPERATOR,
        m.Token.ROLL_DELIMITER,
        m.Token.WHITESPACE,
    ]

    def test_pool(self):
        """A pool of dice."""
        exp = ((
            lex.Token.POOL,
            (5, 1, 9),
        ),)
        data = '[5,1,9]'
        self.lex_test(exp, data)

    def test_pool_with_whitespace(self):
        """A pool of dice that has whitespace."""
        exp = ((
            lex.Token.POOL,
            (5, 1, 9),
        ),)
        data = '[ 5 , 1 , 9 ]'
        self.lex_test(exp, data)


class QualifierTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.QUALIFIER
    allowed = [
        m.Token.OPTIONS_OPERATOR,
        m.Token.ROLL_DELIMITER,
        m.Token.WHITESPACE,
    ]

    def test_quotation_marks(self):
        """Given a statement containing quotation marks, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.QUALIFIER, 'spam'),
        )
        data = '"spam"'
        self.lex_test(exp, data)


class ResultsRollTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.ROLL_DELIMITER
    allowed = [
        m.Token.BOOLEAN,
        m.Token.GROUP_OPEN,
        m.Token.MAP_OPEN,
        m.Token.MAP,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.POOL,
        m.Token.POOL_OPEN,
        m.Token.QUALIFIER,
        m.Token.QUALIFIER_DELIMITER,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_roll_delimiter(self):
        """Given a statement containing parenthesis, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
            (lex.Token.ROLL_DELIMITER, ';'),
            (lex.Token.NUMBER, 5),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '2d10;5d10'
        self.lex_test(exp, data)

    def test_roll_delimiter_whitespace(self):
        """Given a statement containing parenthesis, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
            (lex.Token.ROLL_DELIMITER, ';'),
            (lex.Token.NUMBER, 5),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '2d10 ; 5d10'
        self.lex_test(exp, data)


class UnaryPoolDegenerationOperatorTestCase(BaseTests.LexTokenTestCase):
    token = m.Token.U_POOL_DEGEN_OPERATOR
    allowed = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.POOL,
        m.Token.POOL_OPEN,
        m.Token.U_POOL_DEGEN_OPERATOR,
        m.Token.WHITESPACE,
    ]

    def test_basic_pool_concatente(self):
        """Given a basic pool concatenate statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'C'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'C[3,1,7]'
        self.lex_test(exp, data)

    def test_basic_pool_count(self):
        """Given a basic pool count statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'N[3,1,7]'
        self.lex_test(exp, data)

    def test_basic_pool_count_with_space(self):
        """Given a basic pool count statement with white space, return
        the tokens in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'N [3,1,7]'
        self.lex_test(exp, data)

    def test_basic_pool_sum(self):
        """Given a basic pool count statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'S[3,1,7]'
        self.lex_test(exp, data)


# Roll test case.
class StartRollTestCase(BaseTests.LexTestCase):
    def test_operator_cannot_start_roll(self):
        """An operator cannot start an expression."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = 'Cannot start with \\+.'

        # Test data and state.
        data = '+2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_operator_cannot_start_roll_whitespace(self):
        """An operator cannot start an expression."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = 'Cannot start with \\+.'

        # Test data and state.
        data = ' +2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)


# Order of operations test case.
class OrderOfOperationsTestCase(BaseTests.LexTestCase):
    def test_negative_number(self):
        """Tokenize a number that starts with a negative sign."""
        exp = ((lex.Token.NUMBER, -24),)
        data = '-24'
        self.lex_test(exp, data)

    def test_negative_number_after_operator(self):
        """Tokenize a number that starts with a negative sign."""
        exp = (
            (lex.Token.NUMBER, 3),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, -24),
        )
        data = '3+-24'
        self.lex_test(exp, data)

    def test_negative_number_after_operator_with_whitespace(self):
        """Tokenize a number that starts with a negative sign."""
        exp = (
            (lex.Token.NUMBER, 3),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, -24),
        )
        data = '3 + -24'
        self.lex_test(exp, data)

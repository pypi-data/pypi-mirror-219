"""
parse
~~~~~

Parse dice notation.
"""
from collections.abc import Callable, Sequence
from functools import wraps
import operator
from typing import Any, Optional

from yadr import operator as yo
from yadr.model import (
    CompoundResult,
    DiceMapping,
    Result,
    Token,
    TokenInfo,
    op_tokens,
    id_tokens
)


# The dice map.
# This needs to not be a global value, but it will require a very large
# change to this module to get that to work. This will work for now.
dice_map: dict[str, DiceMapping] = {}


# Parser specific operations.
def map_result(
    result: int | tuple[int, ...],
    key: str
) -> str | int | tuple[str, ...]:
    """Map a roll result to a dice map."""
    if isinstance(result, int):
        return dice_map[key][result]
    new_result = [map_result(n, key) for n in result]
    str_result = tuple(str(item) for item in new_result)
    return str_result


# Exceptons
class IsMap(Exception):
    """Raised to tell the parser not to expect results from the
    current roll because the roll is a dice mapping.
    """


class NoResult(Exception):
    """Raised to tell the parser no result was returned for the
    passed :ref:`YADN` tokens.
    """


# Utility classes and functions.
def _bad_type(side: str, need: str, got: Any) -> None:
    """Raise a TypeError."""
    name = type(got).__name__
    msg = f'{side.title()} operand must be {need}. Was {name}.'
    raise ValueError(msg)


class Tree:
    """A binary tree used to execute parsed :ref:`YADN`.

    :param kind: The type of token to be executed.
    :param value: The specific value of the token for execution.
    :param left: (Optional.) The branch of tokens to be executed first.
    :param right: (Optional.) The branch of tokens to be executed last.
    :param dice_map: (Optional.) Dice maps to use during execution.
    :return: None.
    :rtype: :class:`NoneType`
    """
    def __init__(
        self,
        kind: Token,
        value: Result,
        left: Optional['Tree'] = None,
        right: Optional['Tree'] = None,
        dice_map: Optional[dict[str, DiceMapping]] = None
    ) -> None:
        self.kind = kind
        self.value = value
        self.left = left
        self.right = right
        if dice_map is None:
            dice_map = {}
        self.dice_map = dice_map

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}(kind={self.kind}, value={self.value})'

    def compute(self):
        """Execute the tree.

        :return: The result of the identity or operation token.
        :rtype: Result

        .. warning::
            The return here is too complex to type check. At least
            it's too complex for me to type check at this point. I'll
            keep trying, but for now it's not annotated.
        """
        # Simple identities do not need any computation.
        if self.kind in id_tokens:
            return self.value

        # The only tokens that should make it into Trees are identity
        # or operation tokens. If a different type of token is here,
        # there is a problem that can't be easily resolved.
        if self.kind not in op_tokens:
            msg = f'Unknown token {self.kind}'
            raise TypeError(msg)

        # Compute the value of the tokens that are higher in the
        # order of operations than this tree and on the left-side
        # of this expression.
        left = self.left.compute()

        # Compute the value of the tokens that are higher in the
        # order of operations than this tree and on the right-side
        # of this expression.
        right = self.right.compute()

        # Determine the operation to run.
        try:
            op = yo.ops[self.value]
        except KeyError:
            if self.value != 'm':
                msg = f'Operator not recognized: {self.value}.'
                raise ValueError(msg)
            op = self._map_result

        # Perform the operation on the left and right values,
        # returning the result.
        return op(left, right)

    def _map_result(
        self, result: int | tuple[int, ...],
        key: str
    ) -> str | int | tuple[str, ...]:
        """Map a roll result to a dice map."""
        if isinstance(result, int):
            return self.dice_map[key][result]
        new_result = [self._map_result(n, key) for n in result]
        str_result = tuple(str(item) for item in new_result)
        return str_result


class Unary(Tree):
    """A unary tree used to execute parsed :ref:`YADN`.

    :param kind: The type of token to be executed.
    :param value: The specific value of the token for execution.
    :param child: (Optional.) The branch of tokens to be executed first.
    :return: None.
    :rtype: :class:`NoneType`
    """
    def __init__(
        self,
        kind: Token,
        value: Result,
        child: Optional['Tree'] = None
    ) -> None:
        self.kind = kind
        self.value = value
        self.child = child

    def compute(self):
        """Execute the tree.

        :return: The result of the identity or operation token.
        :rtype: Result

        .. warning::
            This is not type annotated to remain consistent with
            :meth:`yadr.parser.Tree.compute`. See the docstring there
            for why.
        """
        # Simple identities do not need any computation.
        if self.kind in id_tokens:
            return self.value

        # Compute the result of any children.
        child = self.child.compute()

        # Determine the operation to perform.
        if self.kind in op_tokens:
            op = yo.ops[self.value]

        # Perform the operation and return the result.
        return op(child)


# Parser class.
class Parser:
    """A state machine for parsing :ref:`YADN`.

    How Parsing Works
    =================
    Essentially, parsing turns an ordered list of tokens into a
    tree structure for execution. For example, let's say we have
    the :ref:`YADN` expression::

        3 * ( 4 - 2 )

    That is lexed into the tokens::

        Token(NUMBER, 3)
        Token(MD_OPERATOR, '*')
        Token(GROUP_OPEN, '(')
        Token(NUMBER, 4)
        Token(AS_OPERATOR, '-')
        Token(NUMBER, 2)
        Token(GROUP_CLOSE, ')')

    Which is then parsed into the tree::

            *
           / \\
          -   3
         / \\
        4   2

    Where each token ends up in each tree is dependent on the
    :ref:`ops_order` defined by :ref:`YADN`.

    """
    def __init__(self) -> None:
        self.dice_map: dict[str, DiceMapping] = dict()
        self.top_rule = self._map_operator

    # Public method.
    def parse(
        self,
        tokens: Sequence[TokenInfo]
    ) -> None | Result | CompoundResult:
        """Parse one or more die rolls.

        :param tokens: A sequence of lexed :ref:`YADN` tokens to parse.
        :return: A class defined in either :class:`yadr.model.Result` or
            :class:`yadr.model.CompoundResult`.
        :rtype: Result | CompoundResult
        """
        # Split tokens into rolls for parsing.
        rolls = []
        while (Token.ROLL_DELIMITER, ';') in tokens:
            index = tokens.index((Token.ROLL_DELIMITER, ';'))
            roll = tokens[0:index]
            rolls.append(roll)
            tokens = tokens[index + 1:]
        else:
            rolls.append(tokens)

        # Parse each roll.
        results: list[Result] = []
        for roll in rolls:
            try:
                results.append(self._parse_roll(roll))
            except IsMap:
                continue
            except NoResult:
                continue

        # Return the results of the rolls.
        if len(results) > 1:
            return CompoundResult(results)
        elif results:
            return results[0]
        return None

    def _make_tree(self, kind: Token, value: Result) -> Tree:
        """Tranform tokens into trees for execution."""
        return Tree(kind, value, dice_map=self.dice_map)

    def _parse_roll(self, tokens: Sequence[TokenInfo]) -> Result:
        """Parse a sequence of YADN tokens."""
        # Parse the tokens into a tree.
        trees = [self._make_tree(kind, value) for kind, value in tokens]
        trees = trees[::-1]
        parsed = self.top_rule(trees)

        # Execute the parsed tree.
        if not parsed:
            raise NoResult('The parsed string did not create a Tree.')
        return parsed.compute()

    # Parsing rules.
    def _identity(self, trees: list[Tree]) -> Tree:
        """Parse an identity."""
        identity_tokens = [
            Token.BOOLEAN,
            Token.NUMBER,
            Token.POOL,
            Token.QUALIFIER,
        ]
        tree = trees.pop()

        # If the tree is an identity, return it.
        if tree.kind in identity_tokens:
            return tree

        # If the tree is a dice map, add it to the dice map and raise
        # IsMap to prevent the parse from trying to return it as a
        # result. The asserts in here are to keep mypy happy. They
        # probably mean I need to rework how dice maps are handled to
        # keep them out of this parser.
        elif tree.kind == Token.MAP:
            assert isinstance(tree.value, tuple)
            name, map_ = tree.value
            assert isinstance(name, str)
            assert isinstance(map_, dict)
            self.dice_map[name] = map_
            raise IsMap('Roll is a map.')

        # If the tree is starting a group, parse through that group.
        elif tree.kind == Token.GROUP_OPEN:
            expression = self.top_rule(trees)
            if trees[-1].kind == Token.GROUP_CLOSE:
                _ = trees.pop()
            return expression

        # Handle anything unexpected that got here.
        else:
            msg = f'Unrecognized token {tree.kind}'
            raise TypeError(msg)

    def _pool_gen_operator(self, trees: list[Tree]) -> Tree:
        """Parse pool generation operator."""
        rule = self._binary_operator
        rule_affects = Token.POOL_GEN_OPERATOR
        next_rule = self._identity
        return rule(rule_affects, next_rule, trees)

    def _pool_operator(self, trees: list[Tree]) -> Tree:
        """Parse pool operator."""
        rule = self._binary_operator
        rule_affects = Token.POOL_OPERATOR
        next_rule = self._pool_gen_operator
        return rule(rule_affects, next_rule, trees)

    def _u_pool_degen_operator(self, trees: list[Tree]) -> Tree:
        """Parse unary pool degeneration."""
        rule = self._unary_operator
        rule_affects = Token.U_POOL_DEGEN_OPERATOR
        next_rule = self._pool_operator
        return rule(rule_affects, next_rule, trees)

    def _pool_degen_operator(self, trees: list[Tree]) -> Tree:
        """Parse unary pool degeneration."""
        rule = self._binary_operator
        rule_affects = Token.POOL_DEGEN_OPERATOR
        next_rule = self._u_pool_degen_operator
        return rule(rule_affects, next_rule, trees)

    def _dice_operator(self, trees: list[Tree]) -> Tree:
        """Parse dice operators."""
        rule = self._binary_operator
        rule_affects = Token.DICE_OPERATOR
        next_rule = self._pool_degen_operator
        return rule(rule_affects, next_rule, trees)

    def _ex_operator(self, trees: list[Tree]) -> Tree:
        """Parse exponentiation."""
        rule = self._binary_operator
        rule_affects = Token.EX_OPERATOR
        next_rule = self._dice_operator
        return rule(rule_affects, next_rule, trees)

    def _md_operator(self, trees: list[Tree]) -> Tree:
        """Parse addition and subtraction."""
        rule = self._binary_operator
        rule_affects = Token.MD_OPERATOR
        next_rule = self._ex_operator
        return rule(rule_affects, next_rule, trees)

    def _as_operator(self, trees: list[Tree]) -> Tree:
        """Parse addition and subtraction."""
        rule = self._binary_operator
        rule_affects = Token.AS_OPERATOR
        next_rule = self._md_operator
        return rule(rule_affects, next_rule, trees)

    def _comparison_operator(self, trees: list[Tree]) -> Tree:
        """Parse comparisons."""
        rule = self._binary_operator
        rule_affects = Token.COMPARISON_OPERATOR
        next_rule = self._as_operator
        return rule(rule_affects, next_rule, trees)

    def _options_operator(self, trees: list[Tree]) -> Tree:
        """Parse comparisons."""
        rule = self._binary_operator
        rule_affects = Token.OPTIONS_OPERATOR
        next_rule = self._comparison_operator
        return rule(rule_affects, next_rule, trees)

    def _choice_operator(self, trees: list[Tree]) -> Tree:
        """Parse chocies."""
        rule = self._binary_operator
        rule_affects = Token.CHOICE_OPERATOR
        next_rule = self._options_operator
        return rule(rule_affects, next_rule, trees)

    def _map_operator(self, trees: list[Tree]) -> Tree:
        """Parse dice mapping operators."""
        rule = self._binary_operator
        rule_affects = Token.MAPPING_OPERATOR
        next_rule = self._choice_operator
        return rule(rule_affects, next_rule, trees)

    # Base rules.
    def _binary_operator(
        self, rule_affects: Token,
        next_rule: Callable[[list[Tree]], Tree],
        trees: list[Tree]
    ) -> Tree:
        """Parse a binary operator."""
        left = next_rule(trees)
        while trees and trees[-1].kind == rule_affects:
            tree = trees.pop()
            tree.left = left
            tree.right = next_rule(trees)
            left = tree
        return left

    def _unary_operator(
        self, rule_affects: Token,
        next_rule: Callable[[list[Tree]], Tree],
        trees: list[Tree]
    ) -> Tree:
        """Parse an unary operator."""
        if trees[-1].kind == rule_affects:
            tree = trees.pop()
            unary = Unary(tree.kind, tree.value)
            unary.child = next_rule(trees)
            return unary
        return next_rule(trees)

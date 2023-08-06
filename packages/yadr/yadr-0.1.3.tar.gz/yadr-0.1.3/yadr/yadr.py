"""
yadr
~~~~

The core of the :mod:`yadr` package.
"""
from argparse import ArgumentParser
from importlib.resources import open_text
from pathlib import Path
from typing import Optional

from yadr import maps as m
from yadr.encode import Encoder
from yadr.lex import Lexer
from yadr.model import CompoundResult, DiceMapping, Result, TokenInfo
from yadr.parser import dice_map, Parser


# Execute YADN.
def roll(
    yadn: str,
    yadn_out: bool = False,
    dice_map: Optional[dict[str, DiceMapping]] = None
) -> None | Result | CompoundResult:
    """Execute a string of :ref:`YADN` to roll dice.

    :param yadn: A string of :ref:`YADN` that defines the die roll to
        execute.
    :param yadn_out: (Optional.) Whether the output should be in native
        Python objects or :ref:`YADN` notation. The default is native
        Python objects.
    :param dice_map: (Optional.) A dictionary of maps for transforming
        the value rolled. See :ref:`dice_maps` for details.
    :return: The result depends on the details of the die roll.
    :rtype: None, Result, or CompoundResult

    Usage::

        >>> import yadr
        >>>
        >>> yadr.roll('3d6')                        # doctest: +SKIP
        16

    The specific result will depend on the :ref:`YADN` being executed.
    In the example above, it will be an integer in the range of three to
    eighteen that is created by generating three random integers in the
    range of one to six.
    """
    # Get the default dice maps and add any passed into the roll.
    if not dice_map:
        dice_map = {}
    default_maps = get_default_maps()
    default_maps.update(dice_map)

    # Lex the YADN into tokens for parsing.
    lexer = Lexer()
    tokens = lexer.lex(yadn)

    # Parse and execute the YADN tokens.
    parser = Parser()
    parser.dice_map = default_maps
    result: None | Result | CompoundResult = parser.parse(tokens)

    # If needed, encode the result into YADN and return the result.
    if yadn_out:
        encoder = Encoder()
        result = encoder.encode(result)
    return result


# Utility.
def read_file(loc: str | Path) -> str:
    """Read test from a file.

    :param loc: The file system location of the file.
    :return: A :class:str object.
    :rtype: str
    """
    path = Path(loc)
    with open(path) as fh:
        contents = fh.read()
    return contents


def parse_map(yadn: str) -> dict[str, DiceMapping]:
    """Parse the contents of a dice mapping file."""
    if ';' in yadn:
        yadn_parts = yadn.split(';')
        dice_map = {}
        for part in yadn_parts:
            assert ';' not in part
            dice_map.update(parse_map(part))
        return dice_map

    mlexer = m.Lexer()
    mparser = m.Parser()
    tokens = mlexer.lex(yadn)
    name, value = mparser.parse(tokens)
    return {name: value, }


# Command parsing.
def add_dice_map(loc: str) -> dict[str, DiceMapping]:
    """Load the dice-maps from a given file.

    :param loc: The location of the file of dice mappings to load.
    :return: None.
    :rtype: NoneType

    Usage::

        >>> from yadr import add_dice_map
        >>>
        >>> path = 'tests/data/__test_dice_map.txt'
        >>> add_dice_map(path)              # doctest: +NORMALIZE_WHITESPACE
        {'spam': {1: 'eggs', 2: 'bacon', 3: 'eggs', 4: 'tomato'}, 'fudge':
        {1: '-', 2: '', 3: '+'}}
    """
    yadn = read_file(loc)
    return parse_map(yadn)


def get_default_maps() -> dict[str, DiceMapping]:
    """Get the default dice maps.

    :return: The default dice maps as a :class:`dict` of :class:`dict`
        objects.
    :rtype: dict

    Usage::

        >>> from yadr.yadr import get_default_maps
        >>>
        >>> get_default_maps()              # doctest: +ELLIPSIS
        {'sweote boost': {1: '',...
    """
    default_file = open_text('yadr.data', 'dice_maps.yadn')
    default_maps_yadn = default_file.read()
    default_file.close()
    return parse_map(default_maps_yadn)


def list_dice_maps() -> str:
    """Get the list of the default dice maps.

    :return: A :class:`str` object.
    :rtype: str

    Usage::

        >>> from yadr import list_dice_maps
        >>>
        >>> list_dice_maps()                # doctest: +ELLIPSIS
        'sweote boost...
    """
    dice_map = get_default_maps()
    maps_ = '\n'.join(dice_map)
    return maps_


def parse_cli() -> None:
    """Parse command line options."""
    # Stand up the parser.
    p = ArgumentParser(
        description='Execute YADN syntax to roll dice.',
        prog='yadr'
    )

    # Define the command line arguments.
    p.add_argument(
        'yadn',
        help='A string of YADN describing the die roll.',
        action='store',
        nargs='?',
        type=str
    )
    p.add_argument(
        '--list_dice_maps', '-l',
        help='List the names of the default dice maps.',
        action='store_true'
    )
    p.add_argument(
        '--add_dice_map', '-m',
        help='Load the dice mappings at the given file location.',
        nargs=1,
        action='store',
        type=str
    )

    # Parse and execute the command.
    args = p.parse_args()
    result = ''
    dice_map = {}
    if args.add_dice_map:
        dice_map = add_dice_map(args.add_dice_map[0])
    elif args.list_dice_maps:
        result = list_dice_maps()
    if args.yadn:
        raw_result = roll(args.yadn, True, dice_map)
        result = str(raw_result)
    print(result)

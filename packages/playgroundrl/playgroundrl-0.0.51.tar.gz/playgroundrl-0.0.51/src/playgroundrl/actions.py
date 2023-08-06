from typing import TypeAlias, List
import attrs
from enum import Enum


SnakeAction: TypeAlias = str


GoAction: TypeAlias = int

TicTacToeAction: TypeAlias = int


## These are actions that have a Key - Value type schema
class DictLikeAction:
    pass


@attrs.define
class ChessAction(DictLikeAction):
    uci: str


class PokerActionType(Enum):
    CHECK = "CHECK"
    CALL = "CALL"
    RAISE = "RAISE"
    FOLD = "FOLD"


@attrs.define
class PokerAction(DictLikeAction):
    action_type: PokerActionType
    ""

    total: int = 0
    """ If action is raise, this is the new betting total"""


@attrs.define
class CodenamesGuesserAction(DictLikeAction):
    # Strictly speaking, you can also specify a single guess at a time
    # but this is the preferred way for bots

    guesses: List[str]
    """List of words to guess, in order. """


@attrs.define
class CodenamesSpymasterAction(DictLikeAction):
    word: str
    """ The clue word (must be English, a single word, and not on the board)"""

    count: int
    """ The number of words the clue word applies to 0 - 9"""


CodenamesAction: TypeAlias = CodenamesGuesserAction | CodenamesSpymasterAction


@attrs.define
class MiningDecarbonizationAction(DictLikeAction):
    mining: List[float]
    exploration: List[float]
    research_budget: List[float]

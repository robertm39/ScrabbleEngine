from typing import Literal, Mapping, Collection
from dataclasses import dataclass

# A playable letter.
LETTER = Literal[
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

# A playable word.
WORD = str


# A tile with a letter on it.
@dataclass
class BasicTile:
    letter: LETTER
    points: int


# A tile with nothing on it.
@dataclass
class BlankTile:
    points: int


# Any tile.
TILE = BasicTile | BlankTile


# A position on the Scrabble board.
@dataclass
class BoardPosition:
    x: int  # Starting from 0, going from left to right.
    y: int  # Starting from 0, going from top to bottom.


# A multiplier on the board for a word.
@dataclass
class WordMultiplier:
    multiplier: int


# A multiplier on the board for a tile.
@dataclass
class TileMultiplier:
    multiplier: int


# Any multiplier on the board.
MULTIPLIER = WordMultiplier | TileMultiplier


# The configuration of the board.
@dataclass
class BoardConfig:
    width: int
    height: int
    tile_to_multiplier: Mapping[BoardPosition, MULTIPLIER]


# The configuration of a Scrabble game.
@dataclass
class ScrabbleConfig:
    board_config: BoardConfig
    playable_words: Collection[WORD]
    tiles: Collection[TILE]
    max_tiles_in_hand: int
    min_tiles_for_bingo: int
    bingo_points: int
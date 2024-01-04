from typing import Literal
from enum import Enum

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# The string containing the multipliers for Scrabble.
SCRABBLE_MULTIPLIER_STRING = (
    "3  A   3   A  3\n"
    " 2   B   B   2 \n"
    "  2   A A   2  \n"
    "A  2   A   2  A\n"
    "    2     2    \n"
    " B   B   B   B \n"
    "  A   A A   A  \n"
    "3  A   2   A  3\n"
    "  A   A A   A  \n"
    " B   B   B   B \n"
    "    2     2    \n"
    "A  2   A   2  A\n"
    "  2   A A   2  \n"
    " 2   B   B   2 \n"
    "3  A   3   A  3"
)
# The mapping from letter to points in Scrabble.
SCRABBLE_LETTER_TO_POINTS = {
    "A": 1,
    "E": 1,
    "I": 1,
    "O": 1,
    "N": 1,
    "R": 1,
    "T": 1,
    "L": 1,
    "S": 1,
    "U": 1,
    "D": 2,
    "G": 2,
    "B": 3,
    "C": 3,
    "M": 3,
    "P": 3,
    "F": 4,
    "H": 4,
    "V": 4,
    "W": 4,
    "Y": 4,
    "K": 5,
    "J": 8,
    "X": 8,
    "Q": 10,
    "Z": 10,
}

# The tiles in a Scrabble game.
SCRABBLE_INITIAL_TILES_STR = (
    "E" * 12
    + "AI" * 9
    + "O" * 8
    + "NRT" * 6
    + "LSUD" * 4
    + "G" * 3
    + "BCMPFHVWY" * 2
    + "KJXQZ"
    + "**"
)

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


class Direction(Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"


# A playable word.
WORD = str

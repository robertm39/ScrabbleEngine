from typing import Generator
from random import shuffle

from game_state import *
from rules import *
import get_words

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


# Returns a list containing the tiles in a Scrabble game.
def get_scrabble_tiles() -> list[Tile]:
    tiles = get_tiles_from_string(
        tile_string=SCRABBLE_INITIAL_TILES_STR,
        letter_to_points=SCRABBLE_LETTER_TO_POINTS,
    )
    shuffle(tiles)
    return tiles

SCRABBLE_RACK_SIZE = 7

# Return the game-config for Scrabble.
def get_scrabble_config() -> GameConfig:
    return GameConfig(
        playable_words=get_words.get_all_words(),
        min_tiles_for_turn_in=SCRABBLE_RACK_SIZE,
        max_tiles_in_hand=SCRABBLE_RACK_SIZE,
        min_tiles_for_bonus=SCRABBLE_RACK_SIZE,
        bonus_points=50,
        scoreless_turns_to_end_game=6
    )

# Return the dimensions of the board contained withing the given string.
def get_dimensions_from_string(s) -> tuple[int, int]:
    if len(s) == 0:
        return 0, 0

    lines = s.split("\n")
    if len(lines) == 0:
        return 0, 0

    return len(lines[0]), len(lines)


# Walk through the characters in the given string, giving the coordinates.
def get_coords_from_string(
    s: str | None,
) -> Generator[tuple[tuple[int, int], str], None, None]:
    if s is None:
        return
    for y, line in enumerate(s.split("\n")):
        for x, c in enumerate(line):
            yield (x, y), c


BLANK_TILE_NO_LETTER = "*"


# Return the tile specified by the given character.
def get_tile_from_char(c: str, letter_to_points: Mapping[str, int]) -> Tile:
    # Check if it's supposed to be a blank tile with no letter.
    if c == BLANK_TILE_NO_LETTER:
        return BlankTile()

    # An uppercase letter means a normal tile of that letter.
    # A lowercase letter means a blank tile placed as that letter.
    if c.isupper():
        points = letter_to_points.get(c, 0)
        return LetterTile(letter=c, points=points)  # type: ignore

    return BlankTile(letter=c.upper())  # type: ignore


# Return the position-to-tile mapping contained in the given string.
def get_position_to_tile_from_string(
    tile_string: str | None,
    letter_to_points: Mapping[str, int] | None = None,
) -> Mapping[BoardPosition, Tile]:
    letter_to_points = dict() if letter_to_points is None else letter_to_points

    # Get the layout of the tiles.
    position_to_tile = dict[BoardPosition, Tile]()
    for pos, c in get_coords_from_string(tile_string):
        # Ignore all non-letters.
        if not c.isalpha():
            continue

        # if c.isupper():
        #     points = letter_to_points.get(c, 0)
        #     tile = LetterTile(letter=c, points=points)  # type: ignore
        # else:
        #     tile = BlankTile(letter=c.upper())  # type: ignore
        tile = get_tile_from_char(c=c, letter_to_points=letter_to_points)
        position_to_tile[pos] = tile
    return position_to_tile


# Return the position-to-multiplier mapping contained in the given string.
def get_position_to_multiplier_from_string(
    multiplier_string: str | None,
) -> Mapping[BoardPosition, Multiplier]:
    position_to_multiplier = dict[BoardPosition, Multiplier]()
    for pos, c in get_coords_from_string(multiplier_string):
        if c.isnumeric():
            multiplier = WordMultiplier(multiplier=int(c))
            position_to_multiplier[pos] = multiplier
        elif c.isalpha():
            mul = ord(c) - ord("A") + 2
            multiplier = TileMultiplier(multiplier=mul)
            position_to_multiplier[pos] = multiplier
    return position_to_multiplier


# Return the board specified by the given strings.
def get_board_from_strings(
    multiplier_string: str | None = None,
    tile_string: str | None = None,
    letter_to_points: Mapping[str, int] | None = None,
) -> Board:
    if multiplier_string is None and tile_string is None:
        return Board(
            width=0, height=0, position_to_tile=dict(), position_to_multiplier=dict()
        )
    letter_to_points = dict() if letter_to_points is None else letter_to_points

    # Figure out the dimensions.
    if multiplier_string is not None:
        width, height = get_dimensions_from_string(multiplier_string)
    else:
        width, height = get_dimensions_from_string(tile_string)

    # Get the layout of the tiles.
    position_to_tile = get_position_to_tile_from_string(
        tile_string=tile_string, letter_to_points=letter_to_points
    )

    # Get the layout of the multipliers.
    position_to_multiplier = get_position_to_multiplier_from_string(
        multiplier_string=multiplier_string
    )

    return Board(
        width=width,
        height=height,
        position_to_tile=position_to_tile,
        position_to_multiplier=position_to_multiplier,
    )


# Return the on-board word contained in the given string.
def get_word_on_board_from_string(tile_string: str) -> WordOnBoard:
    position_to_tile = get_position_to_tile_from_string(tile_string=tile_string)
    return WordOnBoard(position_to_tile=position_to_tile)


# Return the tile-placing move contained in the given string.
def get_place_tiles_move_from_string(
    tile_string: str, letter_to_points: Mapping[str, int] | None = None
) -> PlaceTilesMove:
    letter_to_points = dict() if letter_to_points is None else letter_to_points

    position_to_placing = dict[BoardPosition, TilePlacing]()
    position_to_tile = get_position_to_tile_from_string(tile_string=tile_string)
    for position, tile in position_to_tile.items():
        if isinstance(tile, LetterTile):
            points = letter_to_points.get(tile.letter, 0)
            position_to_placing[position] = LetterTilePlacing(
                tile=LetterTile(letter=tile.letter, points=points)
            )
            continue
        if isinstance(tile, BlankTile):
            position_to_placing[position] = BlankTilePlacing(tile=BlankTile(), letter=tile.letter)  # type: ignore
            continue
    return PlaceTilesMove(position_to_placing=position_to_placing)


# Return a list of the tiles specified by the given string.
def get_tiles_from_string(
    tile_string: str, letter_to_points: Mapping[str, int] | None = None
) -> list[Tile]:
    letter_to_points = dict() if letter_to_points is None else letter_to_points
    result = list[Tile]()
    for c in tile_string:
        tile = get_tile_from_char(c=c, letter_to_points=letter_to_points)
        result.append(tile)

    return result

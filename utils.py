from typing import Generator

from game_state import *
from rules import *


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


# Return the position-to-tile mapping contained in the given string.
def get_position_to_tile_from_string(
    tile_string: str | None,
) -> Mapping[BoardPosition, Tile]:
    # Get the layout of the tiles.
    position_to_tile = dict[BoardPosition, Tile]()
    for pos, c in get_coords_from_string(tile_string):
        # Ignore all non-letters.
        if not c.isalpha():
            continue

        # An uppercase letter means a normal tile of that letter.
        # A lowercase letter means a blank tile placed as that letter.
        if c.isupper():
            tile = LetterTile(letter=c)  # type: ignore
        else:
            tile = BlankTile(letter=c.upper())  # type: ignore
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
    multiplier_string: str | None = None, tile_string: str | None = None
) -> Board:
    if multiplier_string is None and tile_string is None:
        return Board(
            width=0, height=0, position_to_tile=dict(), position_to_multiplier=dict()
        )

    # Figure out the dimensions.
    if multiplier_string is not None:
        width, height = get_dimensions_from_string(multiplier_string)
    else:
        width, height = get_dimensions_from_string(tile_string)

    # Get the layout of the tiles.
    position_to_tile = get_position_to_tile_from_string(tile_string=tile_string)

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
def get_place_tiles_move_from_string(tile_string: str) -> PlaceTilesMove:
    position_to_placing = dict[BoardPosition, TilePlacing]()
    position_to_tile = get_position_to_tile_from_string(tile_string=tile_string)
    for position, tile in position_to_tile.items():
        if isinstance(tile, LetterTile):
            position_to_placing[position] = LetterTilePlacing(tile=tile)
            continue
        if isinstance(tile, BlankTile):
            position_to_placing[position] = BlankTilePlacing(tile=BlankTile(), letter=tile.letter)  # type: ignore
            continue
    return PlaceTilesMove(position_to_placing=position_to_placing)


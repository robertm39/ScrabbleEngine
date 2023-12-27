from typing import Generator

from game_state import *


# Return the dimensions of the board contained withing the given string.
def get_dimensions_from_string(s) -> tuple[int, int]:
    # if s[-1] == "\n":
    #     s = s[:-1]

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


# Return the board specified by the given strings.
def get_board_from_strings(
    multiplier_string: str | None = None, tile_string: str | None = None
) -> Board | None:
    if multiplier_string is None and tile_string is None:
        return None

    # Figure out the dimensions.
    if multiplier_string is not None:
        width, height = get_dimensions_from_string(multiplier_string)
    else:
        width, height = get_dimensions_from_string(tile_string)

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

    # Get the layout of the multipliers.
    position_to_multiplier = dict[BoardPosition, Multiplier]()
    for pos, c in get_coords_from_string(multiplier_string):
        if c.isnumeric():
            multiplier = WordMultiplier(multiplier=int(c))
            position_to_multiplier[pos] = multiplier
        elif c.isalpha():
            mul = ord(c) - ord("A") + 2
            multiplier = TileMultiplier(multiplier=mul)
            position_to_multiplier[pos] = multiplier

    return Board(
        width=width,
        height=height,
        position_to_tile=position_to_tile,
        position_to_multiplier=position_to_multiplier,
    )

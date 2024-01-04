from typing import Any, Generator
from random import shuffle
from colorama import Fore, Back, Style

from game_state import *
from rules import *
import get_words



# Return an empty Scrabble board.
def get_scrabble_board() -> Board:
    board = get_board_from_strings(multiplier_string=SCRABBLE_MULTIPLIER_STRING)
    board.starting_position = 7, 7
    return board

# Returns a list containing the tiles in a Scrabble game.
def get_scrabble_tiles() -> list[Tile]:
    tiles = get_tiles_from_string(
        tile_string=SCRABBLE_INITIAL_TILES_STR,
        letter_to_points=SCRABBLE_LETTER_TO_POINTS,
    )
    shuffle(tiles)
    return tiles


SCRABBLE_RACK_SIZE = 7
SCRABBLE_CONFIG_NAME = "Scrabble"


# Return the game-config for Scrabble.
def get_scrabble_config() -> GameConfig:
    return GameConfig(
        playable_words=get_words.get_all_words(),
        min_tiles_for_turn_in=SCRABBLE_RACK_SIZE,
        max_tiles_in_hand=SCRABBLE_RACK_SIZE,
        min_tiles_for_bonus=SCRABBLE_RACK_SIZE,
        bonus_points=50,
        scoreless_turns_to_end_game=6,
        config_name=SCRABBLE_CONFIG_NAME,
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


# Return the player with the highest score.
def get_highest_score_player(state: GameState) -> Player:
    return max(state.player_order, key=lambda p: state.player_to_state[p].score)


# ┌─┬─┐
# │ │ │
# ├─┼─┤
# │ │ │
# └─┴─┘


@dataclass
class PrintInfo:
    pos_to_char: dict[tuple[int, int], str]
    pos_to_info: dict[tuple[int, int], list]

    def __init__(self) -> None:
        self.pos_to_char = dict()
        self.pos_to_info = dict()

    def add_format(self, pos: tuple[int, int], f: Any) -> None:
        if not pos in self.pos_to_info:
            self.pos_to_info[pos] = list()
        self.pos_to_info[pos].append(f)

        if not pos in self.pos_to_char:
            self.pos_to_char[pos] = " "

    def print(self, pos: tuple[int, int], s: str) -> None:
        x, y = pos
        for dx, c in enumerate(s):
            tx = x + dx
            self.pos_to_char[tx, y] = c


# Print the given stuff.
def print_pos_to_info(print_info: PrintInfo) -> None:
    pos_to_char = print_info.pos_to_char
    pos_to_info = print_info.pos_to_info

    data = list[tuple[tuple[int, int], str, list]]()
    for pos, char in pos_to_char.items():
        info = list(pos_to_info.get(pos, list()))
        data.append((pos, char, info))

    # Sort primarily by y-coordinate and secondarily by x-coordinate.
    data.sort(key=lambda x: x[0][0])
    data.sort(key=lambda x: x[0][1])

    prev_y = 0
    prev_x = 0
    for (x, y), char, info in data:
        # print(x, y)
        # continue
        print(Style.RESET_ALL, end="")

        # Print the line-breaks.
        while prev_y < y:
            print("\n", end="")
            prev_y += 1
            prev_x = 0

        # Print the spaces.
        while prev_x < x:
            print(" ", end="")
            prev_x += 1

        # Add the formatting.
        for f in info:
            print(f, end="")

        # Print the character.
        print(char, end="")
        prev_x += 1

    # Add a newline at the end.
    print("")


def add_board_borders(board: Board, print_info: PrintInfo) -> None:
    w, h = board.width, board.height
    tw, th = w * 2 + 1, h * 2 + 1

    pos_to_char = print_info.pos_to_char
    pos_to_info = print_info.pos_to_info

    # Add the corners.
    pos_to_char[0, 0] = "┌"
    pos_to_char[tw - 1, 0] = "┐"
    pos_to_char[0, th - 1] = "└"
    pos_to_char[tw - 1, th - 1] = "┘"

    # Add the first row.
    for x in range(1, tw - 1):
        if x % 2 == 1:
            pos_to_char[x, 0] = "─"
        else:
            pos_to_char[x, 0] = "┬"

    # Add the last row.
    for x in range(1, tw - 1):
        if x % 2 == 1:
            pos_to_char[x, th - 1] = "─"
        else:
            pos_to_char[x, th - 1] = "┴"

    # Add the odd-numbered rows (zero-indexing).
    for x in range(0, tw):
        if x % 2 == 0:
            for y in range(1, th, 2):
                pos_to_char[x, y] = "│"

    # Add the first column.
    for y in range(1, th - 1):
        if y % 2 == 1:
            pos_to_char[0, y] = "│"
        else:
            pos_to_char[0, y] = "├"

    # Add the last column.
    for y in range(1, th - 1):
        if y % 2 == 1:
            pos_to_char[tw - 1, y] = "│"
        else:
            pos_to_char[tw - 1, y] = "┤"

    # Add the even-numbered rows.
    for x in range(1, tw - 1):
        for y in range(2, th - 1, 2):
            if x % 2 == 1:
                pos_to_char[x, y] = "─"
            else:
                pos_to_char[x, y] = "┼"


MULTIPLIER_TO_STYLE = {
    TileMultiplier(multiplier=2): Back.CYAN,
    TileMultiplier(multiplier=3): Back.BLUE,
    WordMultiplier(multiplier=2): Back.LIGHTRED_EX,
    WordMultiplier(multiplier=3): Back.RED,
}


# Add the coloring for the tiles with multipliers.
def add_multiplier_coloring(board: Board, print_info: PrintInfo) -> None:
    for board_pos, multiplier in board.position_to_multiplier.items():
        # TODO ignore covered tiles(?).
        f = MULTIPLIER_TO_STYLE.get(multiplier, Back.GREEN)
        x, y = board_pos
        pos = 2 * x + 1, 2 * y + 1
        # pos = x, y

        print_info.add_format(pos=pos, f=f)


# Add the name of the game.
def add_game_name(state: GameState, print_info: PrintInfo) -> None:
    x0 = state.board.width * 2 + 3
    print_info.print(pos=(x0, 1), s=f"Game: {state.config.config_name}")


# Add the current player
def add_current_player(state: GameState, print_info: PrintInfo) -> None:
    x0 = state.board.width * 2 + 3
    print_info.print(
        pos=(x0, 3), s=f"To move: {state.current_player.get_name_or_number()}"
    )


# Add the score information.
def add_score_info(state: GameState, print_info: PrintInfo) -> None:
    x0 = state.board.width * 2 + 3
    y0 = 6

    print_info.print(pos=(x0, y0 - 1), s="Scores:")
    for i, player in enumerate(state.player_order):
        score = state.player_to_state[player].score
        print_info.print(pos=(x0, y0 + i), s=f"{player.get_name_or_number()}: {score}")


# Add the rack information.
def add_rack_info(state: GameState, print_info: PrintInfo) -> None:
    x0 = state.board.width * 2 + 3
    y0 = 8 + len(state.player_order)

    print_info.print(pos=(x0, y0 - 1), s="Racks:")
    for i, player in enumerate(state.player_order):
        tiles = state.player_to_state[player].tiles
        ls = [t.letter if t.letter is not None else "*" for t in tiles]  # type: ignore
        l_str = "".join(ls)
        print_info.print(pos=(x0, y0 + i), s=f"{player.get_name_or_number()}: {l_str}")


# Add the letters played.
def add_letters_played_info(state: GameState, print_info: PrintInfo) -> None:
    for pos, tile in state.board.position_to_tile.items():
        x, y = pos
        tx, ty = 2 * x + 1, 2 * y + 1
        # c = tile.letter if isinstance(tile, LetterTile)
        c = " "
        if isinstance(tile, LetterTile):
            c = tile.letter
        elif isinstance(tile, BlankTile):
            c = tile.letter.lower()  # type: ignore
        print_info.pos_to_char[tx, ty] = c


# Pretty-print the given state.
def pretty_print_state(state: GameState) -> None:
    print_info = PrintInfo()

    # Add the borders around the board and the boxes.
    add_board_borders(board=state.board, print_info=print_info)

    # Add the coloring for multipliers.
    add_multiplier_coloring(board=state.board, print_info=print_info)

    # Add the name of the game.
    add_game_name(state=state, print_info=print_info)

    # Add the current player.
    add_current_player(state=state, print_info=print_info)

    # Add the scores.
    add_score_info(state=state, print_info=print_info)

    # Add the racks.
    add_rack_info(state=state, print_info=print_info)

    # Add the letters played.
    add_letters_played_info(state=state, print_info=print_info)

    # Print out the result.
    print_pos_to_info(print_info=print_info)

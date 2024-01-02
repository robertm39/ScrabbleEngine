from typing import (
    cast,
    Any,
    Generator,
    Self,
    Literal,
    MutableMapping,
    Mapping,
    Collection,
    Sequence,
    Iterable,
)
from enum import Enum
import copy
from dataclasses import dataclass
from frozendict import frozendict

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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


# Any tile.
class Tile:
    points: int

    # def __eq__(self, other):
    #     return self is other

    # def __hash__(self):
    #     return hash(id(self))


# A tile with a letter on it.
@dataclass
class LetterTile(Tile):
    letter: LETTER
    # points: int

    def __init__(self, letter: LETTER, points: int = 0) -> None:
        self.letter = letter
        self.points = points

    def __hash__(self) -> int:
        return hash(self.letter) & hash(self.points)

    def __eq__(self, other) -> bool:
        if type(other) is not type(self):
            return False

        return self.letter == other.letter and self.points == other.points


# A tile with nothing on it.
@dataclass
class BlankTile(Tile):
    letter: LETTER | None = None
    # points: int

    def __init__(self, letter: LETTER | None = None, points: int = 0) -> None:
        self.letter = letter
        self.points = points

    def __hash__(self) -> int:
        return hash(self.letter) ^ hash(self.points)

    def __eq__(self, other) -> bool:
        if type(other) is not type(self):
            return False

        return self.letter == other.letter and self.points == other.points


BoardPosition = tuple[int, int]


def get_board_position(x: int, y: int) -> BoardPosition:
    return x, y


# A multiplier on the board for a word.
@dataclass
class WordMultiplier:
    multiplier: int

    def __hash__(self) -> int:
        return hash(self.multiplier) ^ hash(type(self))


# A multiplier on the board for a tile.
@dataclass
class TileMultiplier:
    multiplier: int

    def __hash__(self) -> int:
        return hash(self.multiplier) ^ hash(type(self))


# Any multiplier on the board.
Multiplier = WordMultiplier | TileMultiplier


@dataclass
class GameConfig:
    playable_words: Collection[WORD]
    min_tiles_for_turn_in: int
    max_tiles_in_hand: int
    min_tiles_for_bingo: int
    bingo_points: int
    scoreless_turns_to_end_game: int
    config_name: str = ""

    def __init__(
        self,
        playable_words: Iterable[WORD],
        min_tiles_for_turn_in: int,
        max_tiles_in_hand: int,
        min_tiles_for_bonus: int,
        bonus_points: int,
        scoreless_turns_to_end_game: int,
        config_name: str = "",
    ):
        self.playable_words = frozenset(playable_words)
        self.min_tiles_for_turn_in = min_tiles_for_turn_in
        self.max_tiles_in_hand = max_tiles_in_hand
        self.min_tiles_for_bingo = min_tiles_for_bonus
        self.bingo_points = bonus_points
        self.scoreless_turns_to_end_game = scoreless_turns_to_end_game
        self.config_name = config_name


# A player in the game.
@dataclass
class Player:
    position: int
    name: str = ""

    def get_name_or_number(self) -> str:
        if self.name == "":
            return f"Player {self.position}"
        return self.name

    def __hash__(self) -> int:
        return hash(self.position)


# The state of a player in the game.
@dataclass
class PlayerState:
    player: Player
    score: int
    tiles: list[Tile]

    def __init__(self, player: Player, score: int, tiles: Iterable[Tile]) -> None:
        self.player = player
        self.score = score
        self.tiles = list(tiles)

    def get_visible_to(self, p: Player) -> "VISIBLE_PLAYER_STATE":
        if p == self.player:
            return self
        return VisiblePlayerState(
            player=self.player,
            score=self.score,
            tiles=[None] * len(self.tiles),
            # next_turn_skipped=self.next_turn_skipped,
        )


# The state of a player, as visible to other players.
@dataclass
class VisiblePlayerState:
    player: Player
    score: int
    tiles: list[None]
    # next_turn_skipped: bool


VISIBLE_PLAYER_STATE = PlayerState | VisiblePlayerState


# The state of the tile-bag.
@dataclass
class Bag:
    tiles: list[Tile]

    def __init__(self, tiles: Iterable[Tile]):
        self.tiles = list(tiles)

    def get_visible_to(self, p: Player) -> "VisibleTileBagState":
        return VisibleTileBagState(tiles=[None] * len(self.tiles))


# The state of the tile-bag, as visible to the players.
@dataclass
class VisibleTileBagState:
    tiles: list[None]


# A word on the board.
@dataclass
class WordOnBoard:
    position_to_tile: Mapping[BoardPosition, Tile]

    def __init__(self, position_to_tile: Mapping[BoardPosition, Tile]) -> None:
        self.position_to_tile = frozendict(position_to_tile)

        if len(self.position_to_tile) == 1:
            self.direction = Direction.HORIZONTAL
        else:
            p1, p2 = list(self.position_to_tile)[:2]
            if p1[0] != p2[0]:
                self.direction = Direction.HORIZONTAL
            else:
                self.direction = Direction.VERTICAL

        # self.word = self.get_word()
        pairs = list(self.position_to_tile.items())
        pairs.sort(key=lambda p: p[0][0] + p[0][1])
        letters = [p[1].letter for p in pairs]  # type: ignore
        self.word = cast(str, "".join(letters))

    # # Return the word spelled out in these tiles.
    # def get_word(self) -> WORD:
    #     pairs = list(self.position_to_tile.items())
    #     pairs.sort(key=lambda p: p[0][0] + p[0][1])
    #     letters = [p[1].letter for p in pairs]  # type: ignore
    #     return "".join(letters)

    # @property
    # def direction(self) -> Direction:


# Return all positions adjacent to one of the given positions, but not equal to one of the given positions.
def get_adjacent_positions(positions: Iterable[BoardPosition]) -> set[BoardPosition]:
    positions = set(positions)
    result = set[BoardPosition]()

    for x, y in positions:
        result.add((x + 1, y))
        result.add((x - 1, y))
        result.add((x, y + 1))
        result.add((x, y - 1))

    return {p for p in result if p not in positions}


# The state of the board.
@dataclass
class Board:
    width: int
    height: int
    starting_position: BoardPosition | None
    position_to_tile: MutableMapping[BoardPosition, Tile]
    position_to_multiplier: Mapping[BoardPosition, Multiplier]

    def __init__(
        self,
        width: int,
        height: int,
        position_to_tile: Mapping[BoardPosition, Tile],
        position_to_multiplier: Mapping[BoardPosition, Multiplier],
        starting_position: BoardPosition | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.starting_position = starting_position
        self.position_to_tile = dict(position_to_tile)
        self.position_to_multiplier = frozendict(position_to_multiplier)

    # Yield all positions on the board. TODO unit-test.
    def all_positions(self) -> Generator[BoardPosition, None, None]:
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

    # Return whether the given position is on the board.
    def contains_position(self, position: BoardPosition) -> bool:
        x, y = position
        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        return True

    # Return the tile at the given position, or None if there is none.
    def get_tile_at(self, position: BoardPosition) -> Tile | None:
        return self.position_to_tile.get(position, None)

    # Return the letter at the given position, or None if there is none.
    def get_letter_at(self, position: BoardPosition) -> LETTER | None:
        tile = self.get_tile_at(position)
        if tile is None:
            return None
        return getattr(tile, "letter", None)

    # Return the multiplier at the given position, or None if there is none.
    def get_multiplier_at(self, position: BoardPosition) -> Multiplier | None:
        return self.position_to_multiplier.get(position, None)

    # Return the state of the board, which is visible to all of the players.
    def get_visible_to(self, p: Player) -> Self:
        return self

    # Return all of the words on the board.
    def get_words(self) -> list[WordOnBoard]:
        result = list[WordOnBoard]()

        # Find all of the left-to-right words.
        # Find all of the tiles with no tile to their left.
        possible_l_to_r_word_starts = list[BoardPosition]()
        for position in self.position_to_tile:
            # to_left = BoardPosition(x=position.x - 1, y=position.y)
            to_left = position[0] - 1, position[1]
            if self.get_tile_at(to_left) is None:
                possible_l_to_r_word_starts.append(position)

        # For each of these tiles, find the sequence of tiles extending to the right from it.
        for word_start in possible_l_to_r_word_starts:
            # Find all of the tiles in the word.
            # word_position_to_tile = dict[BoardPosition, TilePlacing]()
            word_position_to_tile = dict[BoardPosition, Tile]()
            current_position = word_start
            while True:
                current_tile = self.get_tile_at(current_position)
                if current_tile is None:
                    break
                word_position_to_tile[current_position] = current_tile
                # current_position = BoardPosition(
                #     x=current_position.x + 1, y=current_position.y
                # )
                current_position = current_position[0] + 1, current_position[1]
            if len(word_position_to_tile) <= 1:
                continue
            result.append(WordOnBoard(position_to_tile=word_position_to_tile))

        # Find all of the top-to-bottom words.
        # Find all of the tiles with no tile above them.
        possible_t_to_b_word_starts = list[BoardPosition]()
        for position in self.position_to_tile:
            # to_up = BoardPosition(x=position.x, y=position.y - 1)
            to_up = position[0], position[1] - 1
            if self.get_tile_at(to_up) is None:
                possible_t_to_b_word_starts.append(position)

        # For each of these tiles, find the sequence of tiles extending down from it.
        for word_start in possible_t_to_b_word_starts:
            # Find all of the tiles in the word.
            # word_position_to_tile = dict[BoardPosition, TilePlacing]()
            word_position_to_tile = dict[BoardPosition, Tile]()
            current_position = word_start
            while True:
                current_tile = self.get_tile_at(current_position)
                if current_tile is None:
                    break
                word_position_to_tile[current_position] = current_tile
                # current_position = BoardPosition(
                #     x=current_position.x, y=current_position.y + 1
                # )
                current_position = current_position[0], current_position[1] + 1
            if len(word_position_to_tile) <= 1:
                continue
            result.append(WordOnBoard(position_to_tile=word_position_to_tile))

        return result


# The state of the entire game.
@dataclass
class GameState:
    config: GameConfig
    current_player: Player
    player_order: Sequence[Player]
    player_to_state: Mapping[Player, PlayerState]
    bag: Bag
    board: Board
    num_scoreless_turns: int = 0
    # turn_number: int = 0 #TODO add.
    game_finished: bool = False

    def __init__(
        self,
        config: GameConfig,
        current_player: Player,
        player_order: Iterable[Player],
        player_to_state: Mapping[Player, PlayerState],
        bag: Bag,
        board: Board,
        game_finished: bool = False,
    ):
        self.config = config
        self.current_player = current_player
        self.player_to_state = dict(player_to_state)
        self.player_order = tuple(player_order)
        self.bag = bag
        self.board = board
        self.game_finished = game_finished

    # Return a deep copy of this GameState.
    def copy(self) -> Any:
        # return copy.deepcopy(self)
        return GameState(
            config=self.config,
            current_player=self.current_player,
            player_to_state=copy.deepcopy(self.player_to_state),
            player_order=self.player_order,
            bag=copy.deepcopy(self.bag),
            board=copy.deepcopy(self.board),
            game_finished=self.game_finished,
        )

    # TODO get_visible_to(p: Player) -> VisibleGameState


@dataclass
class VisibleGameState:
    config: GameConfig
    current_player: Player
    player_order: Sequence[Player]
    player_to_state: Mapping[Player, PlayerState | VisiblePlayerState]
    bag_state: Bag | VisibleTileBagState
    board_state: Board
    game_finished: bool = False

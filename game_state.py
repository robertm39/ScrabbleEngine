from typing import Self, Literal, Mapping, Collection, Sequence, Iterable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from frozendict import frozendict

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


# Any tile.
class Tile:
    points: int

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(id(self))


# A tile with a letter on it.
@dataclass
class LetterTile(Tile):
    letter: LETTER
    points: int


# A tile with nothing on it.
@dataclass
class BlankTile(Tile):
    points: int


# # Any tile.
# TILE = BasicTile | BlankTile


# A position on the Scrabble board.
@dataclass
class BoardPosition:
    x: int  # Starting from 0, going from left to right.
    y: int  # Starting from 0, going from top to bottom.

    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y)

    def __lt__(self, other: Self) -> bool:
        if self.y < other.y:
            return True
        return self.x < other.x

    def __le__(self, other: Self) -> bool:
        return (self < other) or (self == other)

    def __gt__(self, other: Self) -> bool:
        if self.y > other.y:
            return True
        return self.x > other.x

    def __ge__(self, other: Self) -> bool:
        return (self > other) or (self == other)


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
    position_to_multiplier: Mapping[BoardPosition, MULTIPLIER]

    def contains_position(self, position: BoardPosition) -> bool:
        if position.x < 0 or position.y < 0:
            return False
        if self.width <= position.x or self.height <= position.y:
            return False
        return True


# The configuration of a Scrabble game.
@dataclass
class ScrabbleConfig:
    board_config: BoardConfig
    playable_words: Collection[WORD]
    tiles: Collection[Tile]
    max_tiles_in_hand: int
    min_tiles_for_bingo: int
    bingo_points: int

    def __init__(
        self,
        board_config: BoardConfig,
        playable_words: Collection[WORD],
        tiles: Collection[Tile],
        max_tiles_in_hand: int,
        min_tiles_for_bingo: int,
        bingo_points: int,
    ) -> None:
        self.board_config = board_config
        self.playable_words = set(playable_words)
        self.tiles = tuple(tiles)
        self.max_tiles_in_hand = max_tiles_in_hand
        self.min_tiles_for_bingo = min_tiles_for_bingo
        self.bingo_points = bingo_points


# A player in the game.
@dataclass
class Player:
    position: int

    def __hash__(self) -> int:
        return hash(self.position)


# The state of a player in the game.
@dataclass
class PlayerState:
    player: Player
    score: int
    tiles: list[Tile]
    # next_turn_skipped: bool

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
class TileBagState:
    tiles: list[Tile]

    def get_visible_to(self, p: Player) -> "VisibleTileBagState":
        return VisibleTileBagState(tiles=[None] * len(self.tiles))


# The state of the tile-bag, as visible to the players.
@dataclass
class VisibleTileBagState:
    tiles: list[None]


# Any placing of a tile.
class TilePlacing(ABC):
    @property
    @abstractmethod
    def position(self) -> BoardPosition:
        ...

    @property
    @abstractmethod
    def tile(self) -> Tile:
        ...

    @property
    @abstractmethod
    def letter(self) -> LETTER:
        ...


# A placing of a single non-blank tile.
# @dataclass
class LetterTilePlacing(TilePlacing):
    # tile: BasicTile
    # position: BoardPosition
    def __init__(self, tile: LetterTile, position: BoardPosition) -> None:
        self._tile = tile
        self._position = position

    @property
    def tile(self) -> Tile:
        return self._tile

    @property
    def position(self) -> BoardPosition:
        return self._position

    @property
    def letter(self) -> LETTER:
        return self.tile.letter  # type: ignore

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.tile == other.tile and self.position == other.position


# A placing of a blank tile.
# @dataclass
class BlankTilePlacing(TilePlacing):
    # tile: BlankTile
    # position: BoardPosition
    # letter: LETTER
    def __init__(
        self, tile: BlankTile, position: BoardPosition, letter: LETTER
    ) -> None:
        self._tile = tile
        self._position = position
        self._letter = letter

    @property
    def tile(self) -> Tile:
        return self._tile

    @property
    def position(self) -> BoardPosition:
        return self._position

    @property
    def letter(self) -> LETTER:
        return self._letter  # type: ignore

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (
            self.tile == other.tile
            and self.position == other.position
            and self.letter == other.letter
        )


# A word on the board.
@dataclass
class WordOnBoard:
    position_to_tile: Mapping[BoardPosition, TilePlacing]

    def __init__(self, position_to_tile: Mapping[BoardPosition, TilePlacing]) -> None:
        self.position_to_tile = frozendict(position_to_tile)

    # Return the word spelled out in these tiles.
    def get_word(self) -> WORD:
        placings = list(self.position_to_tile.values())
        placings.sort(key=lambda p: p.position)
        return "".join([p.letter for p in placings])


# The state of the board.
@dataclass
class BoardState:
    position_to_tile: Mapping[BoardPosition, TilePlacing]

    def __init__(self, position_to_tile: Mapping[BoardPosition, TilePlacing]) -> None:
        self.position_to_tile = frozendict(position_to_tile)

    # Return the tile at the given position.
    def get_tile_at(self, position: BoardPosition) -> TilePlacing | None:
        return self.position_to_tile.get(position, None)

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
            to_left = BoardPosition(x=position.x - 1, y=position.y)
            if self.get_tile_at(to_left) is None:
                possible_l_to_r_word_starts.append(position)

        # For each of these tiles, find the sequence of tiles extending to the right from it.
        for word_start in possible_l_to_r_word_starts:
            # Find all of the tiles in the word.
            word_position_to_tile = dict[BoardPosition, TilePlacing]()
            current_position = word_start
            while True:
                current_tile = self.get_tile_at(current_position)
                if current_tile is None:
                    break
                word_position_to_tile[current_position] = current_tile
                current_position = BoardPosition(
                    x=current_position.x + 1, y=current_position.y
                )
            if len(word_position_to_tile) <= 1:
                continue
            result.append(WordOnBoard(position_to_tile=word_position_to_tile))

        # Find all of the top-to-bottom words.
        # Find all of the tiles with no tile above them.
        possible_t_to_b_word_starts = list[BoardPosition]()
        for position in self.position_to_tile:
            to_up = BoardPosition(x=position.x, y=position.y - 1)
            if self.get_tile_at(to_up) is None:
                possible_t_to_b_word_starts.append(position)

        # For each of these tiles, find the sequence of tiles extending down from it.
        for word_start in possible_t_to_b_word_starts:
            # Find all of the tiles in the word.
            word_position_to_tile = dict[BoardPosition, TilePlacing]()
            current_position = word_start
            while True:
                current_tile = self.get_tile_at(current_position)
                if current_tile is None:
                    break
                word_position_to_tile[current_position] = current_tile
                current_position = BoardPosition(
                    x=current_position.x, y=current_position.y + 1
                )
            if len(word_position_to_tile) <= 1:
                continue
            result.append(WordOnBoard(position_to_tile=word_position_to_tile))

        return result


# The state of the entire game.
@dataclass
class GameState:
    config: ScrabbleConfig
    current_player: Player
    player_order: Sequence[Player]
    player_to_state: Mapping[Player, PlayerState | VisiblePlayerState]
    bag_state: TileBagState | VisibleTileBagState
    board_state: BoardState
    game_finished: bool = False

    def __init__(
        self,
        config: ScrabbleConfig,
        current_player: Player,
        player_order: Iterable[Player],
        player_to_state: Mapping[Player, PlayerState | VisiblePlayerState],
        bag_state: TileBagState | VisibleTileBagState,
        board_state: BoardState,
        game_finished: bool = False,
    ):
        self.config = config
        self.current_player = current_player
        self.player_to_state = frozendict(player_to_state)
        self.player_order = tuple(player_order)
        self.bag_state = bag_state
        self.board_state = board_state
        self.game_finished = game_finished

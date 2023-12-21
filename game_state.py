from typing import Self, Literal, Mapping, Collection, Sequence
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


# A player in the game.
@dataclass
class Player:
    position: int


# The state of a player in the game.
@dataclass
class PlayerState:
    player: Player
    score: int
    tiles: list[TILE]
    next_turn_skipped: bool

    def get_visible_to(self, p: Player) -> "VISIBLE_PLAYER_STATE":
        if p == self.player:
            return self
        return VisiblePlayerState(
            player=self.player,
            score=self.score,
            tiles=[None] * len(self.tiles),
            next_turn_skipped=self.next_turn_skipped,
        )


# The state of a player, as visible to other players.
@dataclass
class VisiblePlayerState:
    player: Player
    score: int
    tiles: list[None]
    next_turn_skipped: bool


VISIBLE_PLAYER_STATE = PlayerState | VisiblePlayerState


# The state of the tile-bag.
@dataclass
class TileBagState:
    tiles: list[TILE]

    def get_visible_to(self, p: Player) -> "VisibleTileBagState":
        return VisibleTileBagState(tiles=[None] * len(self.tiles))


# The state of the tile-bag, as visible to the players.
@dataclass
class VisibleTileBagState:
    tiles: list[None]


# The state of the board.
@dataclass
class BoardState:
    position_to_tile: dict[BoardPosition, TILE]

    # Return the tile at the given position.
    def get_tile_at(self, pos: BoardPosition) -> TILE | None:
        return self.position_to_tile.get(pos, None)

    # Return the state of the board, which is visible to all of the players.
    def get_visible_to(self, p: Player) -> Self:
        return self


# The state of the entire game.
@dataclass
class GameState:
    config: ScrabbleConfig
    current_player: Player
    player_to_state: dict[Player, PlayerState]
    bag_state: TileBagState
    board_state: BoardState
    game_finished: bool = False

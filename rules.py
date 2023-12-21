from dataclasses import dataclass

import game_state


# A placing of a single non-blank tile.
@dataclass
class BasicTilePlacing:
    tile: game_state.BasicTile
    position: game_state.BoardPosition


# A placing of a blank tile.
@dataclass
class BlankTilePlacing:
    tile: game_state.BlankTile
    position: game_state.BoardPosition
    letter: game_state.LETTER


# A placing of any tile.
TILE_PLACING = BasicTilePlacing | BlankTilePlacing

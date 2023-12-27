from dataclasses import dataclass
from abc import ABC, abstractmethod
from random import shuffle

# import game_state
from game_state import *
from game_state import BoardPosition, GameState

@dataclass
class LetterTilePlacing:
    tile: LetterTile

@dataclass
class BlankTilePlacing:
    tile: BlankTile
    letter: LETTER

# A placing of any tile.
TilePlacing = LetterTilePlacing | BlankTilePlacing


class Move(ABC):
    @abstractmethod
    def is_valid(self, state: GameState) -> bool:
        ...

    # @abstractmethod
    # def get_next_state(self, state: GameState) -> GameState:
    #     ...


# TODO change.
# A move where a single word is placed.
@dataclass
class PlaceTilesMove(Move):
    tile_placings: Mapping[BoardPosition, TilePlacing]

    def __init__(self, tile_placings: Mapping[BoardPosition, TilePlacing]) -> None:
        self.tile_placings = frozendict(tile_placings)

    # # Return all of the words made by this move.
    # def get_words_made(self, board_state: BoardState) -> list[WordOnBoard]:
    #     # First, see what words were already on the board.
    #     all_previous_words = board_state.get_words()

    #     new_position_to_tile = dict(board_state.position_to_tile)
    #     for placing in self.tile_placings:
    #         # new_position_to_tile[placing.position] = placing.tile
    #         new_position_to_tile[placing.position] = placing
    #     new_state = BoardState(position_to_tile=new_position_to_tile)
    #     all_words = new_state.get_words()
    #     return [w for w in all_words if w not in all_previous_words]

    # # Return whether this placement is linear, either top-to-bottom or left-to-right.
    # def _is_particular_linear_placement(
    #     self, board_state: BoardState, parallel_coord: str, perpendicular_coord: str
    # ) -> bool:
    #     def get_par(position: BoardPosition) -> int:
    #         return getattr(position, parallel_coord)

    #     def get_prp(position: BoardPosition) -> int:
    #         return getattr(position, perpendicular_coord)

    #     # At least one tile must be placed.
    #     if len(self.tile_placings) == 0:
    #         return False

    #     # If not all of the letters have the same perpendicular-coordinate, it isn't a linear word.
    #     if len([get_prp(placing.position) for placing in self.tile_placings]) > 1:
    #         return False

    #     prp = get_prp(self.tile_placings[0].position)

    #     # Determine the top and bottom ends of the word.
    #     min_par = min([get_par(placing.position) for placing in self.tile_placings])
    #     max_par = max([get_par(placing.position) for placing in self.tile_placings])

    #     # No two tiles may be in the same position.
    #     covered_positions = set[int]()
    #     for placing in self.tile_placings:
    #         if get_par(placing.position) in covered_positions:
    #             return False
    #         covered_positions.add(get_par(placing.position))

    #     # Each spot in-between the two tiles must be covered,
    #     # either by a tile already on the board or by a tile in the move.
    #     for par in range(min_par, max_par + 1):
    #         if (
    #             board_state.get_tile_at(
    #                 BoardPosition(**{parallel_coord: par, perpendicular_coord: prp})
    #             )
    #             is None
    #         ) and (par not in covered_positions):
    #             return False

    #     return True

    # # Return whether this move is any linear placement.
    # def _is_any_linear_placement(self, board_state: BoardState) -> bool:
    #     return self._is_particular_linear_placement(
    #         board_state=board_state, parallel_coord="x", perpendicular_coord="y"
    #     ) or self._is_particular_linear_placement(
    #         board_state=board_state, parallel_coord="y", perpendicular_coord="x"
    #     )

    # def is_valid(self, state: GameState) -> bool:
    #     # A move must place at least one tile.
    #     if len(self.tile_placings) == 0:
    #         return False

    #     # If the move uses the same tile multiple times, it isn't valid.
    #     used_tiles = set[Tile]()
    #     for placing in self.tile_placings:
    #         if placing.tile in used_tiles:
    #             return False
    #         used_tiles.add(placing.tile)

    #     # If the move uses tiles the active player doesn't have, it isn't valid.
    #     current_player_state = state.player_to_state[state.current_player]
    #     for placing in self.tile_placings:
    #         if not placing.tile in current_player_state.tiles:
    #             return False

    #     # If the move places a tile outside the board, it isn't valid.
    #     for placing in self.tile_placings:
    #         if not state.config.board_config.contains_position(placing.position):
    #             return False

    #     # If the move places a tile onto a tile already on the board, it isn't valid.
    #     for placing in self.tile_placings:
    #         if state.board_state.get_tile_at(placing.position) is not None:
    #             return False

    #     # The move must be in a line, either from left to right or from top to bottom.
    #     if not self._is_any_linear_placement(board_state=state.board_state):
    #         return False

    #     # All words made by this placement must be in the dictionary.
    #     new_words = self.get_words_made(board_state=state.board_state)
    #     new_word_vals = [w.get_word() for w in new_words]
    #     for word in new_word_vals:
    #         if not word in state.config.playable_words:
    #             return False

    #     return True

    # # Return the number of points scored in a particular word in this move.
    # def get_points_for_word(self, state: GameState, word: WordOnBoard) -> int:
    #     player_tiles = state.player_to_state[state.current_player].tiles

    #     # Determine the sum of the points of the tiles, taking tile multipliers into account.
    #     word_multiplier = 1
    #     word_points = 0
    #     for placing in word.position_to_tile.values():
    #         # Get the base score of the tile.
    #         tile_points = placing.tile.points

    #         # If this is our tile, apply the tile-multiplier, if any.
    #         if (
    #             placing.tile in player_tiles
    #             and placing.position in state.config.board_config.position_to_multiplier
    #         ):
    #             multiplier = state.config.board_config.position_to_multiplier[
    #                 placing.position
    #             ]
    #             if isinstance(multiplier, TileMultiplier):
    #                 tile_points *= multiplier.multiplier
    #             elif isinstance(multiplier, WordMultiplier):
    #                 word_multiplier *= multiplier.multiplier

    #         word_points += tile_points
    #     word_points *= word_multiplier
    #     return word_points

    # def get_next_state(self, state: GameState) -> GameState:
    #     # Get all of the new words.
    #     new_words = self.get_words_made(board_state=state.board_state)

    #     # Determine the number of points scored with words.
    #     word_points = 0
    #     for word in new_words:
    #         word_points += self.get_points_for_word(state=state, word=word)

    #     turn_points = word_points
    #     # Determine whether there was a bingo, and add the points if there was.
    #     if len(self.tile_placings) >= state.config.min_tiles_for_bingo:
    #         turn_points += state.config.bingo_points

    #     # Determine the new total score of the player.
    #     player_state = state.player_to_state[state.current_player]
    #     new_score = player_state.score + turn_points

    #     # Remove the played tiles from the player's rack.
    #     new_player_tiles = list[Tile]()
    #     played_tiles = [placing.tile for placing in self.tile_placings]
    #     for tile in player_state.tiles:
    #         if not tile in played_tiles:
    #             new_player_tiles.append(tile)  # type: ignore

    #     # Place the tiles on the board.
    #     new_position_to_tile = dict(state.board_state.position_to_tile)
    #     for placing in self.tile_placings:
    #         new_position_to_tile[placing.position] = placing
    #     new_board_state = BoardState(position_to_tile=new_position_to_tile)

    #     # Draw new tiles.
    #     num_tiles_to_draw = min(len(played_tiles), len(state.bag_state.tiles))
    #     bag_tiles = list(state.bag_state.tiles)
    #     shuffle(bag_tiles)
    #     drawn_tiles, remaining_tiles = (
    #         bag_tiles[:num_tiles_to_draw],
    #         bag_tiles[num_tiles_to_draw:],
    #     )
    #     new_player_tiles.extend(drawn_tiles)  # type: ignore
    #     new_player_state = PlayerState(
    #         player=state.current_player, score=new_score, tiles=new_player_tiles
    #     )
    #     new_player_to_state = dict(state.player_to_state)
    #     new_player_to_state[state.current_player] = new_player_state

    #     new_bag_state = TileBagState(tiles=remaining_tiles)  # type: ignore

    #     # If there were already no tiles to draw, and the player has no tiles left,
    #     # give the bonuses and penalties for unplayed tiles and end the game.

    #     # Advance to the next player.
    #     player_index = state.player_order.index(state.current_player)
    #     next_index = get_next_player_index(player_index, len(state.player_order))
    #     next_player = state.player_order[next_index]

    #     return GameState(
    #         config=state.config,
    #         current_player=next_player,
    #         player_order=state.player_order,
    #         player_to_state=new_player_to_state,
    #         bag_state=new_bag_state,
    #         board_state=new_board_state,
    #     )


# A move where some tiles are exchanged for new tiles.
@dataclass
class ExchangeTilesMove(Move):
    tiles: list[Tile]

    def is_valid(self, state: GameState) -> bool:
        player_tiles = state.player_to_state[state.current_player].tiles

        # You can only exchange tiles that you have.
        for tile in self.tiles:
            if not tile in player_tiles:
                return False

        # You can't have duplicates in the list of tiles to turn in.
        prev_tiles = list[Tile]()
        for tile in self.tiles:
            if tile in prev_tiles:
                return False
            prev_tiles.append(tile)

        # You can only turn in tiles if at least seven tiles are in the bag.
        if len(state.bag_state.tiles) < 7:
            return False

        return True

    # # Return the state after exchanging these tiles.
    # def get_next_state(self, state: GameState) -> GameState:
    #     # Get the tiles in the bag and shuffle them.
    #     bag_tiles = list(state.bag_state.tiles)
    #     shuffle(bag_tiles)

    #     # Draw tiles from the bag, and put the exchanged ones in.
    #     n_drawn = len(self.tiles)
    #     drawn_tiles, rest_tiles = bag_tiles[:n_drawn], bag_tiles[n_drawn:]
    #     new_bag_tiles = self.tiles + rest_tiles
    #     shuffle(new_bag_tiles)

    #     # Get the new bag-state.
    #     new_bag_state = TileBagState(tiles=new_bag_tiles)  # type: ignore

    #     # Get the new player-state.
    #     current_player_state = state.player_to_state[state.current_player]
    #     new_player_tiles = list[Tile]()
    #     for tile in current_player_state.tiles:
    #         if not tile in self.tiles:
    #             new_player_tiles.append(tile)  # type: ignore
    #     new_player_tiles.extend(drawn_tiles)  # type: ignore
    #     new_player_state = PlayerState(
    #         player=state.current_player,
    #         score=current_player_state.score,
    #         tiles=new_player_tiles,
    #     )
    #     new_player_to_state = dict(state.player_to_state)
    #     new_player_to_state[state.current_player] = new_player_state

    #     player_index = state.player_order.index(state.current_player)
    #     next_index = get_next_player_index(player_index, len(state.player_order))
    #     next_player = state.player_order[next_index]

    #     return GameState(
    #         config=state.config,
    #         current_player=next_player,
    #         player_order=state.player_order,
    #         player_to_state=new_player_to_state,
    #         bag_state=new_bag_state,
    #         board_state=state.board_state,
    #     )


# Return the index of the next player.
def get_next_player_index(index: int, num_players: int) -> int:
    result = index + 1
    if result == num_players:
        return 0
    return result


# A move where the player passes.
class PassMove(Move):
    def is_valid(self, state: GameState) -> bool:
        return True

    # # Return the next state after passing. The only thing that changes is whose turn it is.
    # def get_next_state(self, state: GameState) -> GameState:
    #     player_index = state.player_order.index(state.current_player)
    #     next_index = get_next_player_index(player_index, len(state.player_order))
    #     next_player = state.player_order[next_index]

    #     return GameState(
    #         config=state.config,
    #         current_player=next_player,
    #         player_order=state.player_order,
    #         player_to_state=state.player_to_state,
    #         bag_state=state.bag_state,
    #         board_state=state.board_state,
    #         game_finished=state.game_finished,
    #     )


# A move-getter. Either an AI or a human player.
class MoveGetter(ABC):
    @abstractmethod
    def get_move(self, state: GameState) -> PlaceTilesMove:
        ...

    def notify_new_state(self, state: GameState) -> None:
        pass

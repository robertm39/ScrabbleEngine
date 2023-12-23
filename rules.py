from dataclasses import dataclass
from abc import ABC, abstractmethod
from random import shuffle

# import game_state
from game_state import *
from game_state import BoardPosition, GameState


# # A placing of any tile.
# TilePlacing = LetterTilePlacing | BlankTilePlacing


class Move(ABC):
    @abstractmethod
    def is_valid(self, state: GameState) -> bool:
        ...


# A move where a single word is placed.
@dataclass
class PlaceTilesMove(Move):
    tile_placings: list[TilePlacing]

    # Return all of the words made by this move.
    def get_words_made(self, board_state: BoardState) -> list[WordOnBoard]:
        # First, see what words were already on the board.
        all_previous_words = board_state.get_words()

        new_position_to_tile = dict(board_state.position_to_tile)
        for placing in self.tile_placings:
            # new_position_to_tile[placing.position] = placing.tile
            new_position_to_tile[placing.position] = placing
        new_state = BoardState(position_to_tile=new_position_to_tile)
        all_words = new_state.get_words()
        return [w for w in all_words if w not in all_previous_words]

    # Return whether this placement is linear, either top-to-bottom or left-to-right.
    def _is_particular_linear_placement(
        self, board_state: BoardState, parallel_coord: str, perpendicular_coord: str
    ) -> bool:
        def get_par(position: BoardPosition) -> int:
            return getattr(position, parallel_coord)

        def get_prp(position: BoardPosition) -> int:
            return getattr(position, perpendicular_coord)

        # At least one tile must be placed.
        if len(self.tile_placings) == 0:
            return False

        # If not all of the letters have the same perpendicular-coordinate, it isn't a linear word.
        if len([get_prp(placing.position) for placing in self.tile_placings]) > 1:
            return False

        prp = get_prp(self.tile_placings[0].position)

        # Determine the top and bottom ends of the word.
        min_par = min([get_par(placing.position) for placing in self.tile_placings])
        max_par = max([get_par(placing.position) for placing in self.tile_placings])

        # No two tiles may be in the same position.
        covered_positions = set[int]()
        for placing in self.tile_placings:
            if get_par(placing.position) in covered_positions:
                return False
            covered_positions.add(get_par(placing.position))

        # Each spot in-between the two tiles must be covered,
        # either by a tile already on the board or by a tile in the move.
        for par in range(min_par, max_par + 1):
            if (
                board_state.get_tile_at(
                    BoardPosition(**{parallel_coord: par, perpendicular_coord: prp})
                )
                is None
            ) and (par not in covered_positions):
                return False

        return True

    # Return whether this move is any linear placement.
    def _is_any_linear_placement(self, board_state: BoardState) -> bool:
        return self._is_particular_linear_placement(
            board_state=board_state, parallel_coord="x", perpendicular_coord="y"
        ) or self._is_particular_linear_placement(
            board_state=board_state, parallel_coord="y", perpendicular_coord="x"
        )

    def is_valid(self, state: GameState) -> bool:
        # A move must place at least one tile.
        if len(self.tile_placings) == 0:
            return False

        # If the move uses the same tile multiple times, it isn't valid.
        used_tiles = set[Tile]()
        for placing in self.tile_placings:
            if placing.tile in used_tiles:
                return False
            used_tiles.add(placing.tile)

        # If the move uses tiles the active player doesn't have, it isn't valid.
        current_player_state = state.player_to_state[state.current_player]
        for placing in self.tile_placings:
            if not placing.tile in current_player_state.tiles:
                return False

        # If the move places a tile outside the board, it isn't valid.
        for placing in self.tile_placings:
            if not state.config.board_config.contains_position(placing.position):
                return False

        # If the move places a tile onto a tile already on the board, it isn't valid.
        for placing in self.tile_placings:
            if state.board_state.get_tile_at(placing.position) is not None:
                return False

        # The move must be in a line, either from left to right or from top to bottom.
        if not self._is_any_linear_placement(board_state=state.board_state):
            return False

        # All words made by this placement must be in the dictionary.
        new_words = self.get_words_made(board_state=state.board_state)
        new_word_vals = [w.get_word() for w in new_words]
        for word in new_word_vals:
            if not word in state.config.playable_words:
                return False

        return True


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

    # Return the state after exchanging these tiles.
    def get_next_state(self, state: GameState) -> GameState:
        # Get the tiles in the bag and shuffle them.
        bag_tiles = state.bag_state.tiles
        shuffle(bag_tiles)

        # Draw tiles from the bag, and put the exchanged ones in.
        n_drawn = len(self.tiles)
        drawn_tiles, rest_tiles = bag_tiles[:n_drawn], bag_tiles[n_drawn:]
        new_bag_tiles = self.tiles + rest_tiles
        shuffle(new_bag_tiles)

        # Get the new bag-state.
        new_bag_state = TileBagState(tiles=new_bag_tiles)  # type: ignore

        # Get the new player-state.
        current_player_state = state.player_to_state[state.current_player]
        new_player_tiles = list[Tile]()
        for tile in current_player_state.tiles:
            if not tile in self.tiles:
                new_player_tiles.append(tile)  # type: ignore
        new_player_tiles.extend(drawn_tiles)  # type: ignore
        new_player_state = PlayerState(
            player=state.current_player,
            score=current_player_state.score,
            tiles=new_player_tiles,
        )
        new_player_to_state = dict(state.player_to_state)
        new_player_to_state[state.current_player] = new_player_state

        player_index = state.player_order.index(state.current_player)
        next_index = get_next_player_index(player_index, len(state.player_order))
        next_player = state.player_order[next_index]

        return GameState(
            config=state.config,
            current_player=next_player,
            player_order=state.player_order,
            player_to_state=new_player_to_state,
            bag_state=new_bag_state,
            board_state=state.board_state,
        )


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

    # Return the next state after passing. The only thing that changes is whose turn it is.
    def get_next_state(self, state: GameState) -> GameState:
        player_index = state.player_order.index(state.current_player)
        next_index = get_next_player_index(player_index, len(state.player_order))
        next_player = state.player_order[next_index]

        return GameState(
            config=state.config,
            current_player=next_player,
            player_order=state.player_order,
            player_to_state=state.player_to_state,
            bag_state=state.bag_state,
            board_state=state.board_state,
            game_finished=state.game_finished,
        )


# MOVE = PlaceWordMove | ExchangeTilesMove | PassMove


# A move-getter. Either an AI or a human player.
class MoveGetter(ABC):
    @abstractmethod
    def get_move(self, state: GameState) -> PlaceTilesMove:
        ...

    def notify_new_state(self, state: GameState) -> None:
        pass


# # Return whether the given move places its tiles in a line from left to right.
# def is_left_to_right_placement(move: PlaceWordMove) -> bool:
#     # If not all of the letters have the same y-coordinate, it isn't a left-to-right word.
#     if len([placing.position.y for placing in move.tile_placings]) > 1:
#         return False

#     # Determine the left and right ends of the word.
#     min_x = min([placing.position.x for placing in move.tile_placings])
#     max_x = max([placing.position.x for placing in move.tile_placings])

#     # There must be exactly enough letters to go from the left end to the right end.
#     if len(move.tile_placings) != (max_x - min_x + 1):
#         return False

#     # Each spot in-between must be covered. This is equivalent to there not being any duplicates,
#     # because we have already checked that the number of tiles is correct.
#     covered_positions = set[int]()
#     for placing in move.tile_placings:
#         if placing.position.x in covered_positions:
#             return False
#     return True


# # This is redundant with the method for left-to-right, but I don't want to deal with that right now.
# # Return whether the given move places its tiles in a line from top to bottom.
# def is_top_to_bottom_placement(move: PlaceWordMove, board_state: BoardState) -> bool:
#     # At least one tile must be placed.
#     if len(move.tile_placings) == 0:
#         return False

#     # If not all of the letters have the same x-coordinate, it isn't a top-to-bottom word.
#     if len([placing.position.x for placing in move.tile_placings]) > 1:
#         return False

#     x = move.tile_placings[0].position.x

#     # Determine the top and bottom ends of the word.
#     min_y = min([placing.position.y for placing in move.tile_placings])
#     max_y = max([placing.position.y for placing in move.tile_placings])

#     # No two tiles may be in the same position.
#     covered_positions = set[int]()
#     for placing in move.tile_placings:
#         if placing.position.y in covered_positions:
#             return False
#         covered_positions.add(placing.position.y)

#     # Each spot in-between the two tiles must be covered,
#     # either by a tile already on the board or by a tile in the move.
#     for y in range(min_y, max_y + 1):
#         if (board_state.get_tile_at(BoardPosition(x=x, y=y)) is None) and (
#             y not in covered_positions
#         ):
#             return False

#     # # There must be exactly enough letters to go from the top end to the bottom end.
#     # if len(move.tile_placings) != (max_y - min_y + 1):
#     #     return False

#     # # Each spot in-between must be covered. This is equivalent to there not being any duplicates,
#     # # because we have already checked that the number of tiles is correct.
#     # return True
#     return True


# # Return whether the given move is valid in the given state.
# def is_move_valid(state: GameState, move: MOVE) -> bool:
#     # All passes are valid.
#     if isinstance(move, PassMove):
#         return True

#     # You may only exchange tiles if at least seven tiles are in the bag.
#     if isinstance(move, ExchangeTilesMove)

#     # # A move must place

#     # # If the move uses the same tile multiple times, it isn't valid.
#     # used_tiles = set[TILE]()
#     # for placing in move.tile_placings:
#     #     if placing.tile in used_tiles:
#     #         return False
#     #     used_tiles.add(placing.tile)

#     # # If the move uses tiles the active player doesn't have, it isn't valid.
#     # current_player_state = state.player_to_state[state.current_player]
#     # for placing in move.tile_placings:
#     #     if not placing.tile in current_player_state.tiles:
#     #         return False

#     # # If the move places a tile outside the board, it isn't valid.
#     # for placing in move.tile_placings:
#     #     if not state.config.board_config.contains_position(placing.position):
#     #         return False

#     # # If the move places a tile onto a tile already on the board, it isn't valid.
#     # for placing in move.tile_placings:
#     #     if state.board_state.get_tile_at(placing.position) is not None:
#     #         return False

#     # # If two tiles


# def get_next_state(state: GameState, move: Move) -> GameState:
#     pass

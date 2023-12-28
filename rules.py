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


# Any Scrabble move.
class Move(ABC):
    # Return whether this move is valid in the given state.
    @abstractmethod
    def is_valid(self, state: GameState) -> bool:
        ...

    # Perform this move by changing the given state.
    @abstractmethod
    def perform(self, state: GameState) -> None:
        ...


# TODO change.
# A move where a single word is placed.
@dataclass
class PlaceTilesMove(Move):
    position_to_placing: Mapping[BoardPosition, TilePlacing]

    def __init__(
        self, position_to_placing: Mapping[BoardPosition, TilePlacing]
    ) -> None:
        self.position_to_placing = frozendict(position_to_placing)

    # Return all of the words made by this move.
    def get_words_made(self, board: Board) -> list[WordOnBoard]:
        # First, see what words were already on the board.
        all_previous_words = board.get_words()

        new_position_to_tile = dict(board.position_to_tile)
        for position, placing in self.position_to_placing.items():
            # new_position_to_tile[placing.position] = placing.tile
            if isinstance(placing, BlankTilePlacing):
                tile = BlankTile(letter=placing.letter)
            else:
                tile = placing.tile

            new_position_to_tile[position] = tile
        new_state = Board(
            width=board.width,
            height=board.height,
            position_to_tile=new_position_to_tile,
            position_to_multiplier=board.position_to_multiplier,
        )
        all_words = new_state.get_words()
        return [w for w in all_words if w not in all_previous_words]

    # Return whether this placement is linear, either top-to-bottom or left-to-right.
    def _is_particular_linear_placement(
        self, board: Board, parallel_coord: str, perpendicular_coord: str
    ) -> bool:
        def get_index(coord: str):
            return 0 if coord == "x" else 1

        def get_par(position: BoardPosition) -> int:
            # return getattr(position, parallel_coord)
            return position[get_index(coord=parallel_coord)]

        def get_prp(position: BoardPosition) -> int:
            # return getattr(position, perpendicular_coord)
            return position[get_index(coord=perpendicular_coord)]

        # At least one tile must be placed.
        if len(self.position_to_placing) == 0:
            return False

        # If not all of the letters have the same perpendicular-coordinate, it isn't a linear word.
        if len({get_prp(position) for position in self.position_to_placing}) > 1:
            return False

        pairs = list(self.position_to_placing.items())

        prp = get_prp(pairs[0][0])

        # Determine the top and bottom ends of the word.
        min_par = min([get_par(position) for position in self.position_to_placing])
        max_par = max([get_par(position) for position in self.position_to_placing])

        # # No two tiles may be in the same position.
        covered_positions = set[int]()
        for position in self.position_to_placing:
            #     if get_par(position) in covered_positions:
            #         return False
            covered_positions.add(get_par(position))

        # Each spot in-between the two tiles must be covered,
        # either by a tile already on the board or by a tile in the move, but not both.
        for par in range(min_par, max_par + 1):
            board_has_tile = (
                board.get_tile_at(
                    get_board_position(
                        **{parallel_coord: par, perpendicular_coord: prp}
                    )
                )
                is not None
            )
            move_has_tile = par in covered_positions
            if board_has_tile and move_has_tile:
                return False
            if not (board_has_tile or move_has_tile):
                return False
            # if (
            #     # board_state.get_tile_at(
            #     #     BoardPosition(**{parallel_coord: par, perpendicular_coord: prp})
            #     # )
            #     board.get_tile_at(
            #         get_board_position(
            #             **{parallel_coord: par, perpendicular_coord: prp}
            #         )
            #     )
            #     is None
            # ) and (par not in covered_positions):
            #     return False

        return True

    # Return whether this move is any linear placement.
    def _is_any_linear_placement(self, board: Board) -> bool:
        return self._is_particular_linear_placement(
            board=board, parallel_coord="x", perpendicular_coord="y"
        ) or self._is_particular_linear_placement(
            board=board, parallel_coord="y", perpendicular_coord="x"
        )

    def is_valid(self, state: GameState) -> bool:
        # You can't do any moves if the game if over.
        if state.game_finished:
            return False

        # A move must place at least one tile.
        if len(self.position_to_placing) == 0:
            return False

        player_state = state.player_to_state[state.current_player]

        # Check if the player has all of the tiles to be played.
        move_tiles = [placing.tile for placing in self.position_to_placing.values()]
        if not all_tiles_available(
            available_tiles=player_state.tiles, requested_tiles=move_tiles
        ):
            return False

        # If the move places a tile outside the board, it isn't valid.
        for position in self.position_to_placing:
            if not state.board.contains_position(position):
                return False

        # If the move places a tile onto a tile already on the board, it isn't valid.
        for position in self.position_to_placing:
            if state.board.get_tile_at(position) is not None:
                return False

        # The move must be in a line, either from left to right or from top to bottom.
        if not self._is_any_linear_placement(board=state.board):
            return False

        # At least one tile in the move must be adjacent to a tile already on the board,
        # unless there are no tiles already on the board, in which case the move
        # must place at least one tile on the designated starting position.
        if len(state.board.position_to_tile) == 0:
            if state.board.starting_position is not None:
                on_starting_position = False
                for position in self.position_to_placing:
                    if position == state.board.starting_position:
                        on_starting_position = True
                        break
                if not on_starting_position:
                    return False
        else:
            adj_to_board = get_adjacent_positions(
                positions=state.board.position_to_tile
            )
            one_adj_to_board = False
            for position in self.position_to_placing:
                if position in adj_to_board:
                    one_adj_to_board = True
                    break
            if not one_adj_to_board:
                return False

        # All words made by this placement must be in the dictionary.
        new_words = self.get_words_made(board=state.board)
        new_word_vals = [w.get_word() for w in new_words]
        for word in new_word_vals:
            if not word in state.config.playable_words:
                return False

        # The move must make at least one new word.
        if len(new_words) == 0:
            return False

        return True

    def perform(self, state: GameState) -> None:
        ...  # TODO implement.

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


# Return the mapping from a tile to the number of times it occurs in the given list. TODO generify(?).
def get_tile_to_count(tiles: Iterable[Tile]) -> Mapping[Tile, int]:
    tile_to_count = dict[Tile, int]()

    for tile in tiles:
        prev_count = tile_to_count.get(tile, 0)
        tile_to_count[tile] = prev_count + 1
    return tile_to_count


# Return whether all of the requested tiles are available.
def all_tiles_available(
    available_tiles: Iterable[Tile], requested_tiles: Iterable[Tile]
) -> bool:
    available_tile_to_count = get_tile_to_count(tiles=available_tiles)
    req_tile_to_count = get_tile_to_count(requested_tiles)

    for tile, req_count in req_tile_to_count.items():
        available_count = available_tile_to_count.get(tile, 0)
        if available_count < req_count:
            return False

    return True


# A move where some tiles are exchanged for new tiles.
@dataclass
class ExchangeTilesMove(Move):
    tiles: list[Tile]

    def __init__(self, tiles: Iterable[Tile]) -> None:
        self.tiles = list(tiles)

    def is_valid(self, state: GameState) -> bool:
        # TODO make a downcall in the base-class so I don't have to code this repeatedly(?).
        # You can't do any moves if the game is over.
        if state.game_finished:
            return False

        # Check that the player is only turning in tiles he has.
        if not all_tiles_available(
            available_tiles=state.player_to_state[state.current_player].tiles,
            requested_tiles=self.tiles,
        ):
            return False
        # # TODO compute this once and store the result to save time.
        # move_tile_to_count = get_tile_to_count(self.tiles)

        # player_tiles = state.player_to_state[state.current_player].tiles
        # player_tile_to_count = get_tile_to_count(player_tiles)

        # for tile, move_count in move_tile_to_count.items():
        #     player_count = player_tile_to_count.get(tile, 0)
        #     if player_count < move_count:
        #         return False

        # You can only turn in tiles if at least seven tiles are in the bag.
        if len(state.bag.tiles) < state.config.min_tiles_for_turn_in:
            return False

        return True

    def perform(self, state: GameState) -> None:
        state.num_scoreless_turns += 1
        end_game_for_scoreless_turns(state)

        player_state = state.player_to_state[state.current_player]

        # Remove the tiles to be exchanged from the player's tiles.
        for tile in self.tiles:
            try:
                player_state.tiles.remove(tile)
            except ValueError:
                # We tried to remove a tile that wasn't there. The is_valid() method should have caught this.
                pass

        # Give the player the same number of tiles (or as many as possible) from the bag.
        tiles_to_draw = min(len(self.tiles), len(state.bag.tiles))
        shuffle(state.bag.tiles)
        drawn_tiles, remaining_tiles = (
            state.bag.tiles[:tiles_to_draw],
            state.bag.tiles[tiles_to_draw:],
        )
        player_state.tiles.extend(drawn_tiles)

        # Put the player's tiles into the bag and shuffle it.
        state.bag.tiles = remaining_tiles + self.tiles
        shuffle(state.bag.tiles)

        # Finally, advance to the next player.
        advance_player(state)


# Return the index of the next player.
def get_next_player_index(index: int, num_players: int) -> int:
    result = index + 1
    if result == num_players:
        return 0
    return result


# Advance play to the next player.
def advance_player(state: GameState) -> None:
    state.current_player = Player(
        get_next_player_index(
            state.current_player.position, num_players=len(state.player_order)
        )
    )


# End the game if enough scoreless turns have passed.
def end_game_for_scoreless_turns(state: GameState) -> None:
    if state.num_scoreless_turns >= state.config.scoreless_turns_to_end_game:
        state.game_finished = True


# A move where the player passes.
class PassMove(Move):
    def is_valid(self, state: GameState) -> bool:
        return not state.game_finished

    def perform(self, state: GameState) -> None:
        state.num_scoreless_turns += 1
        end_game_for_scoreless_turns(state)
        advance_player(state)


# A move-getter. Either an AI or a human player.
class MoveGetter(ABC):
    @abstractmethod
    def get_move(self, state: GameState) -> PlaceTilesMove:
        ...

    def notify_new_state(self, state: GameState) -> None:
        pass

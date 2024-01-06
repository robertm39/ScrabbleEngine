from dataclasses import dataclass
from abc import ABC, abstractmethod
from random import shuffle

# import game_state
from constants import *
from game_state import *
from game_state import BoardPosition, GameState


@dataclass
class LetterTilePlacing:
    tile: LetterTile

    def __init__(self, tile: LetterTile) -> None:
        self.tile = tile
        self._hash: int | None = None

    @property
    def letter(self) -> LETTER:
        return self.tile.letter

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.tile) ^ hash(type(self))
        return self._hash


@dataclass
class BlankTilePlacing:
    tile: BlankTile
    letter: LETTER

    def __init__(self, tile: BlankTile, letter: LETTER) -> None:
        self.tile = tile
        self.letter = letter
        self._hash: int | None = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.tile) ^ hash(self.letter) ^ hash(type(self))
        return self._hash


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


# For each player, deduct the points of the tiles he still has in his rack from his score.
# If requested, also add the points of all other player's tiles to the current player's score.
def deduct_final_tile_points(state: GameState, add_to_current_player: bool) -> None:
    # Get the tile points for each other player.
    total_other_player_tile_points = 0
    for other_player, other_player_state in state.player_to_state.items():
        if add_to_current_player and (other_player == state.current_player):
            continue
        other_player_tile_points = 0
        for tile in other_player_state.tiles:
            other_player_tile_points += tile.points

        # Subtract these points from the score of this player.
        other_player_state.score -= other_player_tile_points
        total_other_player_tile_points += other_player_tile_points

    # If requested, add the points of the tiles in all other player's racks to the current player's score.
    if add_to_current_player:
        state.player_to_state[
            state.current_player
        ].score += total_other_player_tile_points


# Have the given player draw the given number of tiles.
def draw_tiles_for_player(player: PlayerState, bag: Bag, num_tiles: int) -> None:
    shuffle(bag.tiles)
    num_tiles = min(num_tiles, len(bag.tiles))
    drawn_tiles, remaining_tiles = bag.tiles[:num_tiles], bag.tiles[num_tiles:]
    player.tiles.extend(drawn_tiles)
    bag.tiles = remaining_tiles
    shuffle(bag.tiles)


# Draw the given number of tiles from the bag and return them.
def draw_tiles(bag: Bag, num_tiles: int) -> list[Tile]:
    shuffle(bag.tiles)
    num_tiles = min(num_tiles, len(bag.tiles))
    drawn_tiles, remaining_tiles = bag.tiles[:num_tiles], bag.tiles[num_tiles:]
    bag.tiles = remaining_tiles
    shuffle(bag.tiles)  # TODO maybe remove this.
    return drawn_tiles


# Return the horizontal word at the given position, if any.
def get_horizontal_word_at(board: Board, pos: BoardPosition) -> WordOnBoard | None:
    center = board.get_letter_at(pos)
    if center is None:
        return None

    # Get the start of the word.
    x, y = pos
    start_x = x
    while True:
        start_x -= 1
        if board.get_letter_at((start_x, y)) is None:
            start_x += 1
            break

    # Get the end of the word.
    end_x = x
    while True:
        end_x += 1
        if board.get_letter_at((end_x, y)) is None:
            end_x -= 1
            break

    # Don't count one-letter words.
    if start_x == end_x:
        return None

    pos_to_tile = dict[BoardPosition, Tile]()
    for x in range(start_x, end_x + 1):
        letter_pos = x, y
        tile = board.get_tile_at(letter_pos)
        if tile is None:
            return None  # Shouldn't happen
        pos_to_tile[letter_pos] = tile
    return WordOnBoard(position_to_tile=pos_to_tile)


# Return the vertical word at the given position, if any.
def get_vertical_word_at(board: Board, pos: BoardPosition) -> WordOnBoard | None:
    center = board.get_letter_at(pos)
    if center is None:
        return None

    # Get the start of the word.
    x, y = pos
    start_y = y
    while True:
        start_y -= 1
        if board.get_letter_at((x, start_y)) is None:
            start_y += 1
            break

    # Get the end of the word.
    end_y = y
    while True:
        end_y += 1
        if board.get_letter_at((x, end_y)) is None:
            end_y -= 1
            break

    # Don't count one-letter words.
    if start_y == end_y:
        return None

    pos_to_tile = dict[BoardPosition, Tile]()
    for y in range(start_y, end_y + 1):
        letter_pos = x, y
        tile = board.get_tile_at(letter_pos)
        if tile is None:
            return None  # Shouldn't happen
        pos_to_tile[letter_pos] = tile
    return WordOnBoard(position_to_tile=pos_to_tile)


# A move where a single word is placed.
@dataclass
class PlaceTilesMove(Move):
    position_to_placing: Mapping[BoardPosition, TilePlacing]

    def __init__(
        self, position_to_placing: Mapping[BoardPosition, TilePlacing]
    ) -> None:
        self.position_to_placing = frozendict(position_to_placing)
        self._hash: int | None = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.position_to_placing)
        return self._hash

    # Return all of the words made by this move.
    def get_words_made(self, board: Board) -> list[WordOnBoard]:
        board = board.copy()

        for position, placing in self.position_to_placing.items():
            if isinstance(placing, BlankTilePlacing):
                tile = BlankTile(letter=placing.letter)
            else:
                tile = placing.tile
            board.position_to_tile[position] = tile
        
        result = list[WordOnBoard]()
        is_vertical = False
        is_horizontal = False
        prev_position: BoardPosition|None = None
        for position in self.position_to_placing:
            if prev_position is not None:
                # Check whether we're horizontal or vertical.
                p_x, p_y = prev_position
                x, y = position
                if x != p_x:
                    is_horizontal = True
                elif y != p_y:
                    is_vertical=True

            prev_position = position

            # If we aren't vertical (yet), check for the vertical word here.
            if not is_vertical:
                word = get_vertical_word_at(board=board, pos=position)
                if word is not None:
                    result.append(word)
                    
            # If we aren't horizontal (yet), check for the horizontal word here.
            if not is_horizontal:
                word = get_horizontal_word_at(board=board, pos=position)
                if word is not None:
                    result.append(word)
        
        return result

        # # First, see what words were already on the board.
        # all_previous_words = board.get_words()

        # new_position_to_tile = dict(board.position_to_tile)
        # for position, placing in self.position_to_placing.items():
        #     if isinstance(placing, BlankTilePlacing):
        #         tile = BlankTile(letter=placing.letter)
        #     else:
        #         tile = placing.tile
        #     new_position_to_tile[position] = tile
        # new_state = Board(
        #     width=board.width,
        #     height=board.height,
        #     position_to_tile=new_position_to_tile,
        #     position_to_multiplier=board.position_to_multiplier,
        # )
        # all_words = new_state.get_words()
        # return [w for w in all_words if w not in all_previous_words]

    # Return whether this placement is linear, either top-to-bottom or left-to-right.
    def _is_particular_linear_placement(
        self, board: Board, parallel_coord: str, perpendicular_coord: str
    ) -> bool:
        def get_index(coord: str):
            return 0 if coord == "x" else 1

        def get_par(position: BoardPosition) -> int:
            return position[get_index(coord=parallel_coord)]

        def get_prp(position: BoardPosition) -> int:
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

        # Reordering this to make move generation faster. (bad idea?)
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

        # Reordering this as well. (bad idea?)
        # All words made by this placement must be in the dictionary.
        new_words = self.get_words_made(board=state.board)
        # new_word_vals = [w.get_word() for w in new_words]
        new_word_vals = [w.word for w in new_words]
        for word in new_word_vals:
            if not word in state.config.playable_words:
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

        # # At least one tile in the move must be adjacent to a tile already on the board,
        # # unless there are no tiles already on the board, in which case the move
        # # must place at least one tile on the designated starting position.
        # if len(state.board.position_to_tile) == 0:
        #     if state.board.starting_position is not None:
        #         on_starting_position = False
        #         for position in self.position_to_placing:
        #             if position == state.board.starting_position:
        #                 on_starting_position = True
        #                 break
        #         if not on_starting_position:
        #             return False
        # else:
        #     adj_to_board = get_adjacent_positions(
        #         positions=state.board.position_to_tile
        #     )
        #     one_adj_to_board = False
        #     for position in self.position_to_placing:
        #         if position in adj_to_board:
        #             one_adj_to_board = True
        #             break
        #     if not one_adj_to_board:
        #         return False

        # # All words made by this placement must be in the dictionary.
        # new_words = self.get_words_made(board=state.board)
        # new_word_vals = [w.get_word() for w in new_words]
        # for word in new_word_vals:
        #     if not word in state.config.playable_words:
        #         return False

        # The move must make at least one new word.
        if len(new_words) == 0:
            return False

        return True

    # Return the number of points scored in a particular word in this move.
    def get_points_for_word(self, board: Board, word: WordOnBoard) -> int:
        # Determine the sum of the points of the tiles, taking tile multipliers into account.
        word_multiplier = 1
        word_points = 0
        for position, tile in word.position_to_tile.items():
            # Get the base score of the tile.
            tile_points = tile.points  # type: ignore

            # If this is our tile, apply the tile-multiplier, if any.
            if (
                position in self.position_to_placing
                and board.get_multiplier_at(position) is not None
            ):
                # multiplier = state.config.board_config.position_to_multiplier[
                #     tile.position
                # ]
                multiplier = board.get_multiplier_at(position)
                if isinstance(multiplier, TileMultiplier):
                    tile_points *= multiplier.multiplier
                elif isinstance(multiplier, WordMultiplier):
                    word_multiplier *= multiplier.multiplier

            word_points += tile_points
        word_points *= word_multiplier
        return word_points

    def perform(self, state: GameState) -> None:
        # Get all of the new words.
        new_words = self.get_words_made(board=state.board)

        # Determine the number of points scored with words.
        word_points = 0
        for word in new_words:
            word_points += self.get_points_for_word(board=state.board, word=word)
        turn_points = word_points

        # Determine whether there was a bingo, and add the points if there was.
        if len(self.position_to_placing) >= state.config.min_tiles_for_bingo:
            turn_points += state.config.bingo_points

        # Add the points to the player's score.
        player_state = state.player_to_state[state.current_player]
        player_state.score += turn_points

        # Update the number of consecutive scoreless turns.
        # TODO does this actually count as a scoreless turn?
        # (It is possible, if you place one blank tile, making a single word made with two blank tiles.)
        if turn_points > 0:
            state.num_scoreless_turns = 0
        else:
            state.num_scoreless_turns += 1

        # If enough scoreless turns have passed, end the game.
        end_game_for_scoreless_turns(state)

        # Remove the played tiles from the player's rack.
        for placing in self.position_to_placing.values():
            player_state.tiles.remove(placing.tile)

        # Place the tiles on the board.
        for position, placing in self.position_to_placing.items():
            tile = placing.tile
            if isinstance(placing, BlankTilePlacing):
                tile = BlankTile(letter=placing.letter, points=placing.tile.points)
            state.board.position_to_tile[position] = tile

        # If there are no tiles to draw, and the player has no tiles left,
        # give the bonuses and penalties for unplayed tiles and end the game.
        # Otherwise, draw new tiles.
        if len(state.bag.tiles) == 0 and len(player_state.tiles) == 0:
            state.game_finished = True
            deduct_final_tile_points(state=state, add_to_current_player=True)
        else:
            # Draw new tiles.
            draw_tiles_for_player(
                player=player_state,
                bag=state.bag,
                num_tiles=len(self.position_to_placing),
            )
            # num_tiles_to_draw = min(len(state.bag.tiles), len(self.position_to_placing))
            # shuffle(state.bag.tiles)
            # drawn_tiles, remaining_tiles = (
            #     state.bag.tiles[:num_tiles_to_draw],
            #     state.bag.tiles[num_tiles_to_draw:],
            # )
            # player_state.tiles.extend(drawn_tiles)
            # state.bag.tiles = remaining_tiles

        # If the game is finished, don't advance to the next player.
        if state.game_finished:
            return

        # Advance to the next player.
        advance_player(state)


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
        draw_tiles_for_player(
            player=player_state, bag=state.bag, num_tiles=len(self.tiles)
        )
        # tiles_to_draw = min(len(self.tiles), len(state.bag.tiles))
        # shuffle(state.bag.tiles)
        # drawn_tiles, remaining_tiles = (
        #     state.bag.tiles[:tiles_to_draw],
        #     state.bag.tiles[tiles_to_draw:],
        # )
        # player_state.tiles.extend(drawn_tiles)

        # state.bag.tiles = remaining_tiles + self.tiles
        # Put the player's tiles into the bag and shuffle it.
        state.bag.tiles.extend(self.tiles)
        shuffle(state.bag.tiles)

        # If the game is finished, don't advance to the next player.
        if state.game_finished:
            return

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
    # state.current_player = state.player_order[
    #     get_next_player_index(
    #         state.current_player.position, num_players=len(state.player_order)
    #     )
    # ]


# End the game if enough scoreless turns have passed.
def end_game_for_scoreless_turns(state: GameState) -> None:
    if state.num_scoreless_turns >= state.config.scoreless_turns_to_end_game:
        state.game_finished = True
        deduct_final_tile_points(state=state, add_to_current_player=False)


# A move where the player passes.
class PassMove(Move):
    def is_valid(self, state: GameState) -> bool:
        return not state.game_finished

    def perform(self, state: GameState) -> None:
        state.num_scoreless_turns += 1
        end_game_for_scoreless_turns(state)

        # If the game is finished, don't advance to the next player.
        if state.game_finished:
            return
        advance_player(state)


# TODO Take only the state visible to the player.
# A move-getter. Either an AI or a human player.
class MoveGetter(ABC):
    @abstractmethod
    def get_move(self, state: GameState) -> Move:
        ...

    def notify_new_state(self, state: GameState) -> None:
        pass

# from typing
import itertools

from game_state import *
from rules import *
import infix_data


# def get_horizontal_placements_for_word(
#     board: Board, tiles: list[Tile], word: str
# ) -> list[PlaceTilesMove]:
#     result = list[PlaceTilesMove]()

#     # Get the mapping from each letter to the tiles you can use for it.
#     letter_to_tiles = {l: list[Tile]() for l in word}
#     for tile in tiles:
#         if isinstance(tile, LetterTile):
#             letter_to_tiles[tile.letter].append(tile)
#         elif isinstance(tile, BlankTile):
#             for l_tiles in letter_to_tiles.values():
#                 l_tiles.append(tile)

#     tiles_usable = [letter_to_tiles[l] for l in word]
#     for tile_comb in itertools.product(*tiles_usable):
#         tiles_left = tiles.copy()

#         # See if this combination of tiles is possible.
#         usable = True
#         for tile in tile_comb:
#             if not tile in tiles_left:
#                 usable = False
#                 break
#             tiles_left.remove(tile)
#         if not usable:
#             continue

#         # Make a word-placement using this combination of tiles.

#     return result

# def get_allPla


def get_placements(state: GameState, x: int, y: int) -> list[PlaceTilesMove]:
    result = list[PlaceTilesMove]()

    # board = state.board
    tiles = state.player_to_state[state.current_player].tiles
    # print(f"Tiles: {''.join([('*' if t.letter is None else t.letter) for t in tiles])}") # type: ignore

    # This doesn't even generate all possible moves.
    for r in range(1, 8):
        for perm in itertools.permutations(tiles, r=r):
            # print(f"Perm: {''.join([('*' if t.letter is None else t.letter) for t in perm])}") # type: ignore
            position_to_placings = list[dict[BoardPosition, TilePlacing]]()
            position_to_placings.append(dict[BoardPosition, TilePlacing]())
            dx = 0
            # for dx, tile in enumerate(perm):
            for tile in perm:
                # If there's already a tile here, move forward.
                while state.board.get_tile_at((x + dx, y)) is not None:
                    dx += 1
                position = x + dx, y
                dx += 1

                placings = list[TilePlacing]()
                if isinstance(tile, LetterTile):
                    placings = [LetterTilePlacing(tile=tile)]
                elif isinstance(tile, BlankTile):
                    placings = [BlankTilePlacing(tile=tile, letter=l) for l in ALPHABET]  # type: ignore
                new_position_to_placings = list[dict[BoardPosition, TilePlacing]]()

                for placing in placings:
                    for old_position_to_placing in position_to_placings:
                        new_position_to_placing = old_position_to_placing.copy()
                        new_position_to_placing[position] = placing
                        new_position_to_placings.append(new_position_to_placing)
                position_to_placings = new_position_to_placings
            for position_to_placing in position_to_placings:
                move = PlaceTilesMove(position_to_placing=position_to_placing)
                # words_made = move.get_words_made(board=state.board)
                # print("")
                # print([w.get_word() for w in words_made])
                if move.is_valid(state=state):
                    result.append(move)

            # Do the whole thing again.
            position_to_placings = list[dict[BoardPosition, TilePlacing]]()
            position_to_placings.append(dict[BoardPosition, TilePlacing]())
            # for dy, tile in enumerate(perm):
            dy = 0
            # for tile in enumerate(perm):
            for tile in perm:
                # position = x, y + dy

                # If there's already a tile here, move forward.
                while state.board.get_tile_at((x, y + dy)) is not None:
                    dy += 1
                position = x, y + dy
                dy += 1

                placings = list[TilePlacing]()
                if isinstance(tile, LetterTile):
                    placings = [LetterTilePlacing(tile=tile)]
                elif isinstance(tile, BlankTile):
                    placings = [BlankTilePlacing(tile=tile, letter=l) for l in ALPHABET]  # type: ignore
                new_position_to_placings = list[dict[BoardPosition, TilePlacing]]()
                for placing in placings:
                    for old_position_to_placing in position_to_placings:
                        new_position_to_placing = old_position_to_placing.copy()
                        new_position_to_placing[position] = placing
                        new_position_to_placings.append(new_position_to_placing)
                position_to_placings = new_position_to_placings
            for position_to_placing in position_to_placings:
                move = PlaceTilesMove(position_to_placing=position_to_placing)
                if move.is_valid(state=state):
                    result.append(move)

    return result


# def get_vertical_placements_for_word(
#     board: Board, tiles: list[Tile], word: str
# ) -> list[PlaceTilesMove]:
#     result = list[PlaceTilesMove]()

#     return result


# This doesn't even find all of the legal moves. TODO fix.
# Specifically, it only tries permutations of tiles that are themselves legal words,
# which skips some moves where letters on the board are the beginning, middle or end of a word.
# This actually skips a very large number of moves.


# Return all legal tile-placements for the given player in the given state.
def get_all_place_tiles_moves_naive(
    state: GameState,  # , player: Player
) -> list[PlaceTilesMove]:
    board = state.board
    # tiles = state.player_to_state[state.current_player].tiles

    result = list[PlaceTilesMove]()

    # # Try placing combination of tiles, from every position, in every direction.
    # for x in range(board.width):
    #     for y in range(board.height):
    #         for move in get_placements(state=state, x=x, y=y):
    #             result.append(move)

    tiles = state.player_to_state[state.current_player].tiles
    for r in range(1, 8):
        for perm in itertools.permutations(tiles, r=r):
            # Compute all possible placings.
            all_placings = list[list[TilePlacing]]()
            all_placings.append(list[TilePlacing]())

            for tile in perm:
                # Determine all ways to place these tiles.
                one_tile_placings = list[TilePlacing]()
                if isinstance(tile, LetterTile):
                    one_tile_placings = [LetterTilePlacing(tile=tile)]
                elif isinstance(tile, BlankTile):
                    one_tile_placings = [BlankTilePlacing(tile=tile, letter=l) for l in ALPHABET]  # type: ignore

                new_all_placings = list[list[TilePlacing]]()
                for prev_placing in all_placings:
                    for one_tile_placing in one_tile_placings:
                        new_placing = prev_placing.copy()
                        new_placing.append(one_tile_placing)
                        new_all_placings.append(new_placing)
                all_placings = new_all_placings

                for placing in all_placings:
                    # If this word isn't playable, don't bother with it.
                    word = [p.letter for p in placing]
                    word = "".join(word)
                    if not word in state.config.playable_words:
                        continue

                    # Try placing this word in every possible place, horizontally.
                    for x0 in range(0, board.width - len(perm) + 1):
                        for y0 in range(board.height):
                            dx = 0
                            pos_to_placing = dict[BoardPosition, TilePlacing]()
                            for t_placing in placing:
                                # Get the current position.
                                while board.get_tile_at((x0 + dx, y0)) is not None:
                                    dx += 1
                                pos = x0 + dx, y0
                                dx += 1

                                pos_to_placing[pos] = t_placing
                            move = PlaceTilesMove(position_to_placing=pos_to_placing)
                            if move.is_valid(state=state):
                                result.append(move)

                    # Try placing this word in every possible place, vertically.
                    for x0 in range(board.width):
                        for y0 in range(0, board.height - len(perm) + 1):
                            dy = 0
                            pos_to_placing = dict[BoardPosition, TilePlacing]()
                            for t_placing in placing:
                                # Get the current position.
                                while board.get_tile_at((x0, y0 + dy)) is not None:
                                    dy += 1
                                pos = x0, y0 + dy
                                dy += 1

                                pos_to_placing[pos] = t_placing
                            move = PlaceTilesMove(position_to_placing=pos_to_placing)
                            if move.is_valid(state=state):
                                result.append(move)

    return result


# Information about what letters can be played where. (This could be computed only on parts of the board that changed.)
class PlayableLetterInfo:
    def __init__(
        self, board: Board, words: Collection[WORD], infix_info: infix_data.InfixData
    ) -> None:
        self.board = board
        self.words = frozenset(words)
        self.infix_info = infix_info

        pos_to_vertical_letters = dict[BoardPosition, tuple[LETTER, ...]]()

        # See what letters can be placed vertically in each spot.
        for pos in board.all_positions():
            # if pos in [(7, 6), (7, 8)]:
            #     pass
            # The letters that make horizontal words can be placed vertically.
            prefix = self._get_horizontal_prefix(pos=pos)
            suffix = self._get_horizontal_suffix(pos=pos)

            # We could just use the entire alphabet for possible_middle_letters. TODO check which approach is faster.
            after_prefix = self.infix_info.get_all_suffixes(prefix)
            before_suffix = self.infix_info.get_all_prefixes(suffix)

            # before_suffix = self.infix_info.infix_to_prefixes.get(suffix, frozenset())
            possible_middle_letters = [c for c in after_prefix if c in before_suffix]
            middle_letters = list[LETTER]()
            for c in possible_middle_letters:
                # See the horizontal word made.
                overall_word = prefix + c + suffix
                if len(overall_word) == 1 or (overall_word in self.words):
                    middle_letters.append(c)  # type: ignore
            pos_to_vertical_letters[pos] = tuple(middle_letters)
        self.pos_to_vertical_letters = frozendict(pos_to_vertical_letters)

        # See what letters can be placed horizontally in each spot.
        pos_to_horizontal_letters = dict[BoardPosition, tuple[LETTER, ...]]()
        for pos in board.all_positions():
            # The letters that make vertical words can be placed horizontally.
            prefix = self._get_vertical_prefix(pos=pos)
            suffix = self._get_vertical_suffix(pos=pos)

            # We could just use the entire alphabet for possible_middle_letters. TODO check which approach is faster.
            after_prefix = self.infix_info.get_all_suffixes(prefix)
            before_suffix = self.infix_info.get_all_prefixes(suffix)

            possible_middle_letters = [c for c in after_prefix if c in before_suffix]
            middle_letters = list[LETTER]()
            for c in possible_middle_letters:
                # See the vertical word made.
                overall_word = prefix + c + suffix
                if len(overall_word) == 1 or (overall_word in self.words):
                    middle_letters.append(c)  # type: ignore
                # if prefix + c + suffix in self.words:
                #     middle_letters.append(c)  # type: ignore
            pos_to_horizontal_letters[pos] = tuple(middle_letters)
        self.pos_to_horizontal_letters = frozendict(pos_to_horizontal_letters)

    def _get_horizontal_affix(self, pos: BoardPosition, inc: Literal[-1, 1]) -> str:
        x, y = pos
        backwards_prefix = list[str]()
        while True:
            x += inc
            letter = self.board.get_letter_at((x, y))
            if letter is None:
                break
            backwards_prefix.append(letter)
        return "".join(backwards_prefix[::inc])  # Reverse it if we went backwards.

    # Return the horizontal prefix before this spot.
    def _get_horizontal_prefix(self, pos: BoardPosition) -> str:
        return self._get_horizontal_affix(pos=pos, inc=-1)

    # Return the horizontal suffix after this spot.
    def _get_horizontal_suffix(self, pos: BoardPosition) -> str:
        return self._get_horizontal_affix(pos=pos, inc=1)

    def _get_vertical_affix(self, pos: BoardPosition, inc: Literal[-1, 1]) -> str:
        # TODO Eliminate this redundancy.
        x, y = pos
        backwards_prefix = list[str]()
        while True:
            y += inc
            letter = self.board.get_letter_at((x, y))
            if letter is None:
                break
            backwards_prefix.append(letter)
        return "".join(backwards_prefix[::inc])  # Reverse it if we went backwards.

    # Return the vertical prefix above this spot.
    def _get_vertical_prefix(self, pos: BoardPosition) -> str:
        return self._get_vertical_affix(pos=pos, inc=-1)

    # Return the vertical suffix below this spot.
    def _get_vertical_suffix(self, pos: BoardPosition) -> str:
        return self._get_vertical_affix(pos=pos, inc=1)


# The state of the algorithm for finding the tiles to place.
@dataclass
class PlaceTilesState:
    pos_to_tile_placed: Mapping[BoardPosition, TilePlacing]
    start_pos: BoardPosition
    word: str
    tiles_left: Sequence[Tile]
    before_begin_pos: BoardPosition
    after_end_pos: BoardPosition
    ignore_one_tile_moves: bool

    def __init__(
        self,
        pos_to_tile_placed: dict[BoardPosition, TilePlacing],
        start_pos: BoardPosition,
        word: str,
        tiles_left: list[Tile],
        before_begin_pos: BoardPosition,
        after_end_pos: BoardPosition,
        ignore_one_tile_moves=False,
    ) -> None:
        self.pos_to_tile_placed = frozendict(pos_to_tile_placed)
        self.start_pos = start_pos
        self.word = word
        self.tiles_left = tuple(tiles_left)
        self.before_begin_pos = before_begin_pos
        self.after_end_pos = after_end_pos
        self.ignore_one_tile_moves = ignore_one_tile_moves


# Return all the possible tile-placings at the given spot, given the acceptable letters.
def get_all_possible_placings(
    ok_side_letters: Collection[LETTER], ok_letters: Collection[LETTER], tile: Tile
) -> list[TilePlacing]:
    # Get all of the possible tile-placings.
    placings = list[TilePlacing]()
    if isinstance(tile, BlankTile):
        for letter in ok_side_letters:
            if letter in ok_letters:
                placings.append(BlankTilePlacing(tile=tile, letter=letter))
    elif isinstance(tile, LetterTile):
        # If the letter is okay, we can place this tile here.
        if tile.letter in ok_side_letters and tile.letter in ok_letters:
            placings.append(LetterTilePlacing(tile=tile))
    return placings
    # new_tiles_left = list(place_tiles_state.tiles_left)
    # new_tiles_left.remove(tile)


# Finds place-tiles moves.
class PlaceTilesMoveFinder:
    def __init__(self, words: Collection[WORD]) -> None:
        self.words = frozenset(words)
        self.infix_data = infix_data.InfixData(words=self.words)

    # Return all vertical moves, only going down.
    # Assumes that there is no tile directly above or below the column of already-placed tiles. TODO check for this.
    def _rec_get_all_vertical_moves_down(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        place_tiles_state: PlaceTilesState,
    ) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()

        # # See if the current state already makes a word.
        # # If it does, and if it at least one tile has been placed, count that.
        # min_tiles_for_move = 2 if place_tiles_state.ignore_one_tile_moves else 1
        # if (place_tiles_state.word in self.words or len(place_tiles_state.word)==1) and len(
        #     place_tiles_state.pos_to_tile_placed
        # ) >= min_tiles_for_move:
        if (
            place_tiles_state.word in self.words or len(place_tiles_state.word) == 1
        ) and len(place_tiles_state.pos_to_tile_placed) > 0:
            move = PlaceTilesMove(
                position_to_placing=place_tiles_state.pos_to_tile_placed
            )
            result.add(move)

        # Check if there's any room to place tiles. If there isn't, we can't make any more moves.
        place_pos = place_tiles_state.after_end_pos
        if not state.board.contains_position(place_pos):
            return result

        # For each tile we could place, try placing it, add all the tiles beneath it, and see if it's still okay.
        # If it is, recursively get all words you can make with it placed.
        # # Also, if it's already a word, add that.
        x = place_pos[0]
        ok_letters = playable_letter_info.pos_to_vertical_letters.get(
            place_pos, tuple[LETTER, ...]()
        )
        ok_suffixes = self.infix_data.get_all_suffixes(place_tiles_state.word)
        unique_tiles = set(place_tiles_state.tiles_left)
        for tile in unique_tiles:
            # Get all of the possible tile-placings.
            placings = get_all_possible_placings(
                ok_side_letters=ok_letters, ok_letters=ok_suffixes, tile=tile  # type: ignore
            )
            new_tiles_left = list(place_tiles_state.tiles_left)
            new_tiles_left.remove(tile)

            for placing in placings:
                current_word = place_tiles_state.word + placing.letter

                # Add all of the tiles already there, skipping if they can't make a word.
                check_y = place_pos[1]
                placing_works = True
                while True:
                    check_y += 1
                    letter_below = state.board.get_letter_at((x, check_y))
                    if letter_below is None:
                        # We're past all of the tiles at the top.
                        break
                    ok_suffixes = self.infix_data.get_all_suffixes(current_word)
                    if not letter_below in ok_suffixes:
                        placing_works = False
                        break
                    current_word = current_word + letter_below
                if not placing_works:
                    continue

                # As far as we're aware, this placing could work.
                # Recursively get all moves with this tile placed.
                new_after_end_pos = x, check_y
                new_pos_to_tile_placed = dict(place_tiles_state.pos_to_tile_placed)
                new_pos_to_tile_placed[place_pos] = placing

                new_place_tiles_state = PlaceTilesState(
                    pos_to_tile_placed=new_pos_to_tile_placed,
                    start_pos=place_tiles_state.start_pos,
                    word=current_word,
                    tiles_left=new_tiles_left,
                    before_begin_pos=place_tiles_state.before_begin_pos,
                    after_end_pos=new_after_end_pos,
                )
                result.update(
                    self._rec_get_all_vertical_moves_down(
                        state=state,
                        playable_letter_info=playable_letter_info,
                        place_tiles_state=new_place_tiles_state,
                    )
                )

        return result

    # The recursive part for getting all vertical moves.
    # Assumes that there is no tile directly above or below the column of already-placed tiles. TODO check for this.
    def _rec_get_all_vertical_moves(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        place_tiles_state: PlaceTilesState,
    ) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()

        # Get all moves going down from here.
        result.update(
            self._rec_get_all_vertical_moves_down(
                state=state,
                playable_letter_info=playable_letter_info,
                place_tiles_state=place_tiles_state,
            )
        )

        # Check if there's room on the board to place a tile above us.
        if state.board.contains_position(place_tiles_state.before_begin_pos):
            # For each tile we could place above us, recursively get all moves with it placed.
            unique_tiles = set(place_tiles_state.tiles_left)
            place_pos = place_tiles_state.before_begin_pos
            x = place_pos[0]
            ok_letters = playable_letter_info.pos_to_vertical_letters.get(
                place_pos, tuple[LETTER, ...]()
            )
            ok_prefixes = self.infix_data.get_all_prefixes(place_tiles_state.word)
            for tile in unique_tiles:
                # Get all of the possible tile-placings.
                placings = get_all_possible_placings(
                    ok_side_letters=ok_letters, ok_letters=ok_prefixes, tile=tile  # type: ignore
                )
                new_tiles_left = list(place_tiles_state.tiles_left)
                new_tiles_left.remove(tile)

                # For each placing, add all tiles right above it and see if it works.
                # If it does, recursively get all moves using it.
                for placing in placings:
                    current_word = placing.letter + place_tiles_state.word

                    # Add all of the tiles already there, skipping if they can't make a word.
                    check_y = place_pos[1]
                    placing_works = True
                    while True:
                        check_y -= 1
                        letter_above = state.board.get_letter_at((x, check_y))
                        if letter_above is None:
                            # We're past all of the tiles at the top.
                            break
                        ok_prefixes = self.infix_data.get_all_prefixes(current_word)
                        if not letter_above in ok_prefixes:
                            placing_works = False
                            break
                        current_word = letter_above + current_word
                    new_before_begin_pos = x, check_y

                    # If the placing doesn't work, don't use it.
                    # Whether the placing works depends only on the letter placed,
                    # so this method will do some redundant computation when there are blank tiles. TODO fix, if necessary.
                    if not placing_works:
                        continue

                    # As far as we're aware, this placing could work.
                    new_pos_to_tile_placed = dict(place_tiles_state.pos_to_tile_placed)
                    new_pos_to_tile_placed[place_pos] = placing

                    new_place_tiles_state = PlaceTilesState(
                        pos_to_tile_placed=new_pos_to_tile_placed,
                        start_pos=place_tiles_state.start_pos,
                        word=current_word,
                        tiles_left=new_tiles_left,
                        before_begin_pos=new_before_begin_pos,
                        after_end_pos=place_tiles_state.after_end_pos,
                    )

                    # Recursively get all vertical moves with this tile-placing.
                    result.update(
                        self._rec_get_all_vertical_moves(
                            state=state,
                            playable_letter_info=playable_letter_info,
                            place_tiles_state=new_place_tiles_state,
                        )
                    )

        return result

    # Return all moves that start at the given already-played position and go out along the vertical axis.
    def _get_all_vertical_straight_moves(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        pos: BoardPosition,
        placing_at_pos: TilePlacing | None = None,
    ) -> set[PlaceTilesMove]:
        board = state.board
        current_word = list[str]()

        # TODO deal with the case where we are given an empty tile.
        if placing_at_pos is None:
            current_word.append(board.get_letter_at(pos))  # type: ignore
            tiles_left = state.player_to_state[state.current_player].tiles
        else:
            current_word.append(placing_at_pos.letter)
            tiles_left = list(state.player_to_state[state.current_player].tiles)
            tiles_left.remove(placing_at_pos.tile)

        # Add the already-existing suffix, and determine the position after the end of the current word (or letter).
        x, y = pos
        while True:
            y += 1
            letter = board.get_letter_at((x, y))
            if letter is None:
                break
            current_word.append(letter)
        end_y = y

        # Add the already-existing prefix, and determine the position before the beginning of the current word (or letter).
        x, y = pos
        while True:
            y -= 1
            letter = board.get_letter_at((x, y))
            if letter is None:
                break
            current_word = [letter] + current_word  # TODO Make this faster.
        begin_y = y

        # The state for the recursive algorithm.
        pos_to_tile_placed = dict()
        if placing_at_pos is not None:
            pos_to_tile_placed[pos] = placing_at_pos

        place_tiles_state = PlaceTilesState(
            pos_to_tile_placed=pos_to_tile_placed,
            start_pos=pos,
            word="".join(current_word),
            # tiles_left=state.player_to_state[state.current_player].tiles,
            tiles_left=tiles_left,
            before_begin_pos=(x, begin_y),
            after_end_pos=(x, end_y),
        )

        # Return all of the vertical moves from here using the recursive algorithm.
        return self._rec_get_all_vertical_moves(
            state=state,
            playable_letter_info=playable_letter_info,
            place_tiles_state=place_tiles_state,
        )

    # Return all horizontal moves, only going right.
    # Assumes that there is no tile directly before or after the row of already-placed tiles. TODO check for this.
    def _rec_get_all_horizontal_moves_right(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        place_tiles_state: PlaceTilesState,
    ) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()

        # See if the current state already makes a word.
        # If it does, and if it at least one tile has been placed, count that.
        if (
            place_tiles_state.word in self.words or len(place_tiles_state.word) == 1
        ) and len(place_tiles_state.pos_to_tile_placed) > 0:
            move = PlaceTilesMove(
                position_to_placing=place_tiles_state.pos_to_tile_placed
            )
            result.add(move)

        # Check if there's any room to place tiles. If there isn't, we can't make any more moves.
        place_pos = place_tiles_state.after_end_pos
        if not state.board.contains_position(place_pos):
            return result

        # For each tile we could place, try placing it, add all the tiles beneath it, and see if it's still okay.
        # If it is, recursively get all words you can make with it placed.
        # # Also, if it's already a word, add that.
        # x = place_pos[0]
        y = place_pos[1]
        ok_letters = playable_letter_info.pos_to_horizontal_letters.get(
            place_pos, tuple[LETTER, ...]()
        )
        ok_suffixes = self.infix_data.get_all_suffixes(place_tiles_state.word)
        unique_tiles = set(place_tiles_state.tiles_left)
        for tile in unique_tiles:
            # Get all of the possible tile-placings.
            placings = get_all_possible_placings(
                ok_side_letters=ok_letters, ok_letters=ok_suffixes, tile=tile  # type: ignore
            )
            new_tiles_left = list(place_tiles_state.tiles_left)
            new_tiles_left.remove(tile)

            for placing in placings:
                current_word = place_tiles_state.word + placing.letter

                # Add all of the tiles already there, skipping if they can't make a word.
                check_x = place_pos[0]
                placing_works = True
                while True:
                    check_x += 1
                    letter_after = state.board.get_letter_at((check_x, y))
                    if letter_after is None:
                        # We're past all of the tiles at the top.
                        break
                    ok_suffixes = self.infix_data.get_all_suffixes(current_word)
                    if not letter_after in ok_suffixes:
                        placing_works = False
                        break
                    current_word = current_word + letter_after
                if not placing_works:
                    continue

                # As far as we're aware, this placing could work.
                # Recursively get all moves with this tile placed.
                new_after_end_pos = check_x, y
                new_pos_to_tile_placed = dict(place_tiles_state.pos_to_tile_placed)
                new_pos_to_tile_placed[place_pos] = placing

                new_place_tiles_state = PlaceTilesState(
                    pos_to_tile_placed=new_pos_to_tile_placed,
                    start_pos=place_tiles_state.start_pos,
                    word=current_word,
                    tiles_left=new_tiles_left,
                    before_begin_pos=place_tiles_state.before_begin_pos,
                    after_end_pos=new_after_end_pos,
                )
                result.update(
                    self._rec_get_all_horizontal_moves_right(
                        state=state,
                        playable_letter_info=playable_letter_info,
                        place_tiles_state=new_place_tiles_state,
                    )
                )

        return result

    # The recursive part for getting all horizontal moves.
    # Assumes that there is no tile directly to before or after the row of already-placed tiles. TODO check for this.
    def _rec_get_all_horizontal_moves(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        place_tiles_state: PlaceTilesState,
    ) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()

        # Get all moves going right from here.
        result.update(
            self._rec_get_all_horizontal_moves_right(
                state=state,
                playable_letter_info=playable_letter_info,
                place_tiles_state=place_tiles_state,
            )
        )

        # Check if there's room on the board to place a tile above us.
        if state.board.contains_position(place_tiles_state.before_begin_pos):
            # For each tile we could place above us, recursively get all moves with it placed.
            unique_tiles = set(place_tiles_state.tiles_left)
            place_pos = place_tiles_state.before_begin_pos
            y = place_pos[1]
            ok_letters = playable_letter_info.pos_to_horizontal_letters.get(
                place_pos, tuple[LETTER, ...]()
            )
            ok_prefixes = self.infix_data.get_all_prefixes(place_tiles_state.word)
            for tile in unique_tiles:
                # Get all of the possible tile-placings.
                placings = get_all_possible_placings(
                    ok_side_letters=ok_letters, ok_letters=ok_prefixes, tile=tile  # type: ignore
                )
                new_tiles_left = list(place_tiles_state.tiles_left)
                new_tiles_left.remove(tile)

                # For each placing, add all tiles right above it and see if it works.
                # If it does, recursively get all moves using it.
                for placing in placings:
                    current_word = placing.letter + place_tiles_state.word

                    # Add all of the tiles already there, skipping if they can't make a word.
                    check_x = place_pos[0]
                    placing_works = True
                    while True:
                        check_x -= 1
                        letter_before = state.board.get_letter_at((check_x, y))
                        if letter_before is None:
                            # We're past all of the tiles at the top.
                            break
                        ok_prefixes = self.infix_data.get_all_prefixes(current_word)
                        if not letter_before in ok_prefixes:
                            placing_works = False
                            break
                        current_word = letter_before + current_word
                    new_before_begin_pos = check_x, y

                    # If the placing doesn't work, don't use it.
                    # Whether the placing works depends only on the letter placed,
                    # so this method will do some redundant computation when there are blank tiles. TODO fix, if necessary.
                    if not placing_works:
                        continue

                    # As far as we're aware, this placing could work.
                    new_pos_to_tile_placed = dict(place_tiles_state.pos_to_tile_placed)
                    new_pos_to_tile_placed[place_pos] = placing

                    new_place_tiles_state = PlaceTilesState(
                        pos_to_tile_placed=new_pos_to_tile_placed,
                        start_pos=place_tiles_state.start_pos,
                        word=current_word,
                        tiles_left=new_tiles_left,
                        before_begin_pos=new_before_begin_pos,
                        after_end_pos=place_tiles_state.after_end_pos,
                    )

                    # Recursively get all horizontal moves with this tile-placing.
                    result.update(
                        self._rec_get_all_horizontal_moves(
                            state=state,
                            playable_letter_info=playable_letter_info,
                            place_tiles_state=new_place_tiles_state,
                        )
                    )

        return result

    # Return all moves that start at the given already-played position and go out along the horizontal axis.
    def _get_all_horizontal_straight_moves(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        pos: BoardPosition,
    ) -> set[PlaceTilesMove]:
        board = state.board
        current_word = list[str]()
        # TODO deal with the case where we are given an empty tile.
        current_word.append(board.get_letter_at(pos))  # type: ignore

        # Add the already-existing suffix, and determine the position after the end of the current word (or letter).
        x, y = pos
        while True:
            x += 1
            letter = board.get_letter_at((x, y))
            if letter is None:
                break
            current_word.append(letter)
        end_x = x

        # Add the already-existing prefix, and determine the position before the beginning of the current word (or letter).
        x, y = pos
        while True:
            x -= 1
            letter = board.get_letter_at((x, y))
            if letter is None:
                break
            current_word = [letter] + current_word  # TODO Make this faster.
        begin_x = x

        # The state for the recursive algorithm.
        place_tiles_state = PlaceTilesState(
            pos_to_tile_placed=dict(),
            start_pos=pos,
            word="".join(current_word),
            tiles_left=state.player_to_state[state.current_player].tiles,
            before_begin_pos=(begin_x, y),
            after_end_pos=(end_x, y),
        )

        # Return all of the horizontal moves from here using the recursive algorithm.
        return self._rec_get_all_horizontal_moves(
            state=state,
            playable_letter_info=playable_letter_info,
            place_tiles_state=place_tiles_state,
        )

    # Return all moves that start at the given already-played position and go out along one axis.
    def _get_all_straight_moves(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        pos: BoardPosition,
    ) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()

        result.update(
            self._get_all_vertical_straight_moves(
                state=state, playable_letter_info=playable_letter_info, pos=pos
            )
        )
        result.update(
            self._get_all_horizontal_straight_moves(
                state=state, playable_letter_info=playable_letter_info, pos=pos
            )
        )

        return result

    # Return all vertical offset moves from the given position.
    def _get_all_vertical_offset_moves(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        pos: BoardPosition,
    ) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()
        x, y = pos

        # # Determine the current horizontal word at this position.
        # horizontal_word = cast(str, board.get_letter_at(pos))
        # c_x = x
        # while True:
        #     c_x += 1
        #     l = board.get_letter_at((c_x, y))
        #     if l is None:
        #         break
        #     horizontal_word = horizontal_word + l
        # c_x = x
        # while True:
        #     c_x -= 1
        #     l = board.get_letter_at((c_x, y))
        #     if l is None:
        #         break
        #     horizontal_word = l + horizontal_word

        for x_diff in (-1, 1):
            # If the spot to the side is open, try to make vertical moves there.
            spot_to_side = x + x_diff, y
            if state.board.get_tile_at(spot_to_side) is not None:
                continue
            # TODO Maybe see what the vertical prefix and suffix for the word would be
            # in order to narrow down what letters we'll try to place.

            # See what tiles we can place there.
            # ok_letters = self.infix_data.get_all_suffixes(horizontal_word)
            unique_tiles = set(state.player_to_state[state.current_player].tiles)
            ok_side_letters = playable_letter_info.pos_to_vertical_letters[spot_to_side]
            for tile in unique_tiles:
                placings = get_all_possible_placings(ok_side_letters=ok_side_letters, ok_letters=ALPHABET, tile=tile)  # type: ignore
                # For each placing, see all vertical words you can make with it.
                for placing in placings:
                    result.update(
                        self._get_all_vertical_straight_moves(
                            state=state,
                            playable_letter_info=playable_letter_info,
                            pos=spot_to_side,
                            placing_at_pos=placing,
                        )
                    )

        return result

    # Return all horizontal offset moves from the given position.
    def _get_all_horizontal_offset_moves(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        pos: BoardPosition,
    ) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()

        return result

    # Return all moves that start at the given already-played position, go out one square in one axis,
    # and then go out along the other axis.
    def _get_all_offset_moves(
        self,
        state: GameState,
        playable_letter_info: PlayableLetterInfo,
        pos: BoardPosition,
    ) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()

        result.update(
            self._get_all_vertical_offset_moves(
                state=state, playable_letter_info=playable_letter_info, pos=pos
            )
        )
        result.update(
            self._get_all_horizontal_offset_moves(
                state=state, playable_letter_info=playable_letter_info, pos=pos
            )
        )

        return result

    def get_all_place_tiles_moves(self, state: GameState) -> set[PlaceTilesMove]:
        result = set[PlaceTilesMove]()

        playable_letter_info = PlayableLetterInfo(
            board=state.board, words=self.words, infix_info=self.infix_data
        )

        board = state.board
        for pos in board.position_to_tile:
            result.update(
                self._get_all_straight_moves(
                    state=state, playable_letter_info=playable_letter_info, pos=pos
                )
            )
            result.update(
                self._get_all_offset_moves(
                    state=state, playable_letter_info=playable_letter_info, pos=pos
                )
            )

        return result

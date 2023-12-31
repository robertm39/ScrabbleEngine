# from typing
import itertools

from game_state import *
from rules import *


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


TREE = dict[str | None, "TREE"]


class Trie:
    def __init__(self) -> None:
        self.tree = TREE()

    # Add the given string to the given subtree in this trie.
    def _add(self, tree: TREE, s: str) -> None:
        # If the string is empty, mark this as a terminal node.
        if len(s) == 0:
            tree[None] = TREE()
            return
        c, rest = s[:1], s[1:]
        if not c in tree:
            tree[c] = TREE()
        self._add(tree=tree[c], s=rest)

    # Add the given string to this trie.
    def add(self, s: str) -> None:
        self._add(tree=self.tree, s=s)

    # Return whether the given string is in the given subtree in this trie.
    def _contains(self, tree: TREE, s: str) -> bool:
        if len(s) == 0:
            return None in tree
        c, rest = s[:1], s[1:]
        subtree = tree.get(c, None)
        if subtree is None:
            return False
        return self._contains(tree=subtree, s=rest)

    # Return whether the given string is in this trie.
    def __contains__(self, s: Any) -> bool:
        if not isinstance(s, str):
            return False
        return self._contains(tree=self.tree, s=s)


PREFIX_TRIE_DELIMITER = "."


class PrefixTrie:
    def __init__(self, delimiter=PREFIX_TRIE_DELIMITER) -> None:
        self.trie = Trie()
        self.delimiter = delimiter

    def add(self, s: str) -> None:
        # Add all orderings except for the one where the entire word is the prefix.
        for middle_index in range(len(s)):
            prefix_and_suffix = (
                s[:middle_index][::-1] + self.delimiter + s[middle_index:]
            )
            self.trie.add(prefix_and_suffix)

        # Add the ordering where the entire word is the prefix,
        # which doesn't make use of the delimiter at all.
        self.trie.add(s[::-1])

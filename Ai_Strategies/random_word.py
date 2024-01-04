from random import choice
import time

from game_state import GameState
from rules import *

import move_generation


# A strategy that plays a random word if possible, and passes otherwise.
class RandomWordStrategy(MoveGetter):
    def __init__(self) -> None:
        self.moves_finder: move_generation.PlaceTilesMoveFinder | None = None

    # Initialize the moves-finder, if it isn't already initialized.
    def _init_moves_finder(self, state: GameState) -> None:
        if self.moves_finder is None:
            self.moves_finder = move_generation.PlaceTilesMoveFinder(
                words=state.config.playable_words
            )

    def get_move(self, state: GameState) -> Move:
        self._init_moves_finder(state=state)
        # before = time.time()
        # placement_moves = move_generation.get_all_place_tiles_moves_naive(state=state)
        # after = time.time()
        # print(f"Took {after-before:.2f} seconds.")
        placement_moves = list(self.moves_finder.get_all_place_tiles_moves(state=state))  # type: ignore

        # print(f"Found {len(placement_moves)} placement moves.")
        if placement_moves:
            return choice(placement_moves)
        return PassMove()

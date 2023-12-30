from random import choice
import time

from game_state import GameState
from rules import *

import move_generation


# A strategy that plays a random word if possible, and passes otherwise.
class RandomWordStrategy(MoveGetter):
    def get_move(self, state: GameState) -> Move:
        before = time.time()
        placement_moves = move_generation.get_all_place_tiles_moves_naive(state=state)
        after = time.time()
        print(f"Took {after-before:.2f} seconds.")
        # print(f"Found {len(placement_moves)} placement moves.")
        if placement_moves:
            return choice(placement_moves)
        return PassMove()

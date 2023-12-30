from random import choice
import time

from game_state import GameState
from rules import *

import move_generation


# A strategy that plays the highest scoring word, or passes if it doesn't find any.
class HighestScoringWordStrategy(MoveGetter):
    def get_move(self, state: GameState) -> Move:
        before = time.time()
        placement_moves = move_generation.get_all_place_tiles_moves_naive(state=state)
        after = time.time()
        print(f"Took {after-before:.2f} seconds.")
        print(f"Found {len(placement_moves)} placement moves.")
        if placement_moves:
            before_score = state.player_to_state[state.current_player].score
            highest_scoring_move = None
            highest_score = -1
            for move in placement_moves:
                after_state = state.copy()
                move.perform(after_state)
                after_score = (
                    after_state.player_to_state[state.current_player].score
                    - before_score
                )
                if after_score > highest_score:
                    highest_score = after_score
                    highest_scoring_move = move
            if highest_scoring_move is not None:
                return highest_scoring_move

        return PassMove()

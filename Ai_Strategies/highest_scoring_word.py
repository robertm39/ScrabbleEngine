from random import choice

from game_state import GameState
from rules import *

import move_generation


# A strategy that plays the highest scoring word, or passes if it doesn't find any.
class HighestScoringWordStrategy(MoveGetter):
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

        placement_moves = self.moves_finder.get_all_place_tiles_moves(state=state)  # type: ignore

        num_invalid_moves = 0
        for move in placement_moves:
            if not move.is_valid(state=state):
                num_invalid_moves += 1
        if num_invalid_moves > 0:
            s = f"!!!{num_invalid_moves} INVALID MOVES!!!"
            print("!" * len(s))
            print(s)
            print("!" * len(s))

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

from random import choice

from game_state import GameState
from rules import *

import move_generation

VALUE_PER_TILE = 100


# A strategy that likes both points and playing tiles.
class ScoreAndTilesStrategy(MoveGetter):
    def __init__(self, value_per_tile: float=VALUE_PER_TILE) -> None:
        self.moves_finder: move_generation.PlaceTilesMoveFinder | None = None
        self.value_per_tile = value_per_tile

    def get_name(self) -> str:
        return f"{type(self).__name__}(value_per_tile={self.value_per_tile})"

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
            highest_value_move = None
            highest_value = -1
            for move in placement_moves:
                after_state = state.copy()
                move.perform(after_state)
                after_score = (
                    after_state.player_to_state[state.current_player].score
                    - before_score
                )
                value = (
                    after_score + len(move.position_to_placing) * self.value_per_tile
                )

                if value > highest_value:
                    highest_value = value
                    highest_value_move = move
            if highest_value_move is not None:
                return highest_value_move

        return PassMove()

from random import choice

from game_state import GameState
from rules import *

import move_generation


# A strategy that plays the move that uses the most tiles, or passes if it doesn't find any.
class MostTilesPlayedStrategy(MoveGetter):
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

        # If there aren't any moves, pass.
        if not placement_moves:
            return PassMove()

        most_tiles_moves = list[PlaceTilesMove]()
        most_tiles = 0
        # Get the moves with the most tiles played.
        for move in placement_moves:
            num_tiles = len(move.position_to_placing)
            if num_tiles > most_tiles:
                most_tiles_moves.clear()
                most_tiles_moves.append(move)
                most_tiles = num_tiles
            elif num_tiles == most_tiles:
                most_tiles_moves.append(move)

        # If there aren't any moves here (which shouldn't ever happen), pass.
        if not most_tiles_moves:
            return PassMove()

        # Among the moves with the most tiles played, choose the one that gets the most points.
        before_score = state.player_to_state[state.current_player].score
        highest_scoring_move = None
        highest_score = -1
        for move in most_tiles_moves:
            after_state = state.copy()
            move.perform(after_state)
            after_score = (
                after_state.player_to_state[state.current_player].score - before_score
            )
            if after_score > highest_score:
                highest_score = after_score
                highest_scoring_move = move
        if highest_scoring_move is not None:
            return highest_scoring_move

        return PassMove()

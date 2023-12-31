from typing import Generator
import random

from game_state import *
from rules import *
import ai_strategies


# Run a game of Scrabble.
# TODO only give each player the state visible to it.
def run_game(
    state: GameState, player_to_strategy: Mapping[Player, MoveGetter]
) -> Generator[tuple[Move | None, GameState], None, None]:
    # Randomly determine the starting player.
    starting_player = random.choice(state.player_order)
    state.current_player = starting_player

    # Randomly draw tiles for each player.
    for player_state in state.player_to_state.values():
        draw_tiles(
            player=player_state, bag=state.bag, num_tiles=state.config.max_tiles_in_hand
        )

    # Yield the initial state.
    yield None, state.copy()

    while not state.game_finished:
        # Get the current player's move.
        strategy = player_to_strategy[state.current_player]
        move = strategy.get_move(state=state.copy())

        # If it isn't valid, replace it with a pass move.
        if not move.is_valid(state=state):
            move = PassMove()

        # Double-check that the move is now valid.
        if not move.is_valid(state=state):
            break  # TODO log this(?).

        # Perform the move.
        move.perform(state=state)

        # Yield the move and the new state.
        yield move, state.copy()

from game_state import GameState
from rules import *


# A strategy that always passes.
class AlwaysPassStrategy(MoveGetter):
    def get_move(self, state: GameState) -> Move:
        return PassMove()

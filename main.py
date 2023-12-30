from game_state import *
from rules import *
from utils import *
import ai_strategies
import game_runner


# Run a game between two AI players.
def test_1():
    p0 = Player(0)
    pass_0 = ai_strategies.AlwaysPassStrategy()
    p0_state = PlayerState(player=p0, score=0, tiles=list())

    p1 = Player(1)
    pass_1 = ai_strategies.AlwaysPassStrategy()
    p1_state = PlayerState(player=p1, score=0, tiles=list())

    player_to_strategy = {p0: pass_0, p1: pass_1}
    player_to_state = {p0: p0_state, p1: p1_state}

    board = get_board_from_strings(multiplier_string=SCRABBLE_MULTIPLIER_STRING)
    bag = Bag(tiles=get_scrabble_tiles())
    initial_state = GameState(
        config=get_scrabble_config(),
        current_player=p0,
        player_order=(p0, p1),
        player_to_state=player_to_state,
        bag=bag,
        board=board,
    )

    print(initial_state)

    for move, state in game_runner.run_game(
        state=initial_state, player_to_strategy=player_to_strategy
    ):
        print("")
        print(move)
        print(state)

    print("")
    print("")
    print("Finished.")


def main():
    test_1()


if __name__ == "__main__":
    main()

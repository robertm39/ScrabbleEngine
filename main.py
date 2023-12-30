from game_state import *
from rules import *
from utils import *
import ai_strategies
import game_runner


# Run a game between two AI players.
def test_1():
    p0 = Player(0)
    # pass_0 = ai_strategies.AlwaysPassStrategy()
    # p0_strat = ai_strategies.RandomWordStrategy()
    p0_strat = ai_strategies.HighestScoringWordStrategy()
    p0_state = PlayerState(player=p0, score=0, tiles=list())

    p1 = Player(1)
    # pass_1 = ai_strategies.AlwaysPassStrategy()
    # p1_strat = ai_strategies.RandomWordStrategy()
    p1_strat = ai_strategies.HighestScoringWordStrategy()
    p1_state = PlayerState(player=p1, score=0, tiles=list())

    player_to_strategy = {p0: p0_strat, p1: p1_strat}
    player_to_state = {p0: p0_state, p1: p1_state}

    # board = get_board_from_strings(multiplier_string=SCRABBLE_MULTIPLIER_STRING)
    board = get_scrabble_board()
    bag = Bag(tiles=get_scrabble_tiles())
    initial_state = GameState(
        config=get_scrabble_config(),
        current_player=p0,
        player_order=(p0, p1),
        player_to_state=player_to_state,
        bag=bag,
        board=board,
    )

    # print(initial_state)
    # pretty_print_state(state=initial_state)
    # return
    state = initial_state

    # input("Next turn:")
    for move, state in game_runner.run_game(
        state=initial_state, player_to_strategy=player_to_strategy
    ):
        print("")
        # print(move)
        # print(state)
        pretty_print_state(state=state)
        # input("Next turn:")
        # break

    print("")
    print("")
    print("Finished.")
    winner = get_highest_score_player(state=state)
    print(f"{winner.get_name_or_number()} wins!")


def main():
    test_1()


if __name__ == "__main__":
    main()

import time

from game_state import *
from rules import *
from utils import *
import ai_strategies
import game_runner
import tournament


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


# Run a basic tournament.
def tournament_1():
    player_1 = tournament.TournamentPlayer(
        get_strategy=lambda: ai_strategies.ScoreAndTilesStrategy(), name="Player 1"
    )
    player_2 = tournament.TournamentPlayer(
        get_strategy=lambda: ai_strategies.HighestScoringWordStrategy(), name="Player 2"
    )

    before = time.time()
    results = tournament.do_tournament_matches(
        player_1=player_1, player_2=player_2, num_matches=5
    )
    after = time.time()
    print(f"Took {after-before:.2f} seconds.")
    print(f"Player 1 won {results.num_player_1_wins} times.")
    print(f"Player 2 won {results.num_player_2_wins} times.")
    print(f"There were {results.num_ties} ties.")


def tournament_2():
    players = [
        tournament.TournamentPlayer(
            get_strategy=lambda: ai_strategies.HighestScoringWordStrategy(),
            name="Highest_Score",
        ),
        tournament.TournamentPlayer(
            get_strategy=lambda: ai_strategies.ScoreAndTilesStrategy(value_per_tile=0.5),
            name="Tiles_0.5",
        ),
        tournament.TournamentPlayer(
            get_strategy=lambda: ai_strategies.ScoreAndTilesStrategy(value_per_tile=1),
            name="Tiles_1.0",
        ),
        tournament.TournamentPlayer(
            get_strategy=lambda: ai_strategies.ScoreAndTilesStrategy(value_per_tile=1.5),
            name="Tiles_1.5",
        ),
        tournament.TournamentPlayer(
            get_strategy=lambda: ai_strategies.ScoreAndTilesStrategy(value_per_tile=2),
            name="Tiles_2",
        ),
        tournament.TournamentPlayer(
            get_strategy=lambda: ai_strategies.ScoreAndTilesStrategy(value_per_tile=2.5),
            name="Tiles_2.5",
        ),
        tournament.TournamentPlayer(
            get_strategy=lambda: ai_strategies.ScoreAndTilesStrategy(value_per_tile=3.0),
            name="Tiles_3.0",
        ),
    ]

    # num_matches_per_pairing = 20

    # win_prob_table[p1_index, p2_index] is the estimated chance that p1 will beat p2 in a game.
    # win_prob_table = dict[tuple[int, int], float]()
    win_table = dict[tuple[int, int], int]()
    # loss_table = dict[tuple[int, int], int]()

    # Initialize the tables to zero.
    for i in range(len(players)):
        for j in range(len(players)):
            win_table[i, j] = 0
            # loss_table[i, j] = 0

    # # Every player is assumed to have a 50% chance of beating itself.
    # for i in range(len(players)):
    #     win_prob_table[i, i] = 0.5

    # Run each matchup of the tournament.
    # for _ in range(num_matches_per_pairing):
    round_num = 1
    while True:
        print(f"Round {round_num}.")
        round_num += 1

        # Print the names.
        print("")
        print("Names:")
        for player_i, player in enumerate(players):
            print(f"{player_i}: {player.name}")
        print("")

        for p1_index in range(len(players) - 1):
            for p2_index in range(p1_index + 1, len(players)):
                p1 = players[p1_index]
                p2 = players[p2_index]
                print(f"{p1.name} vs {p2.name}.")

                results = tournament.do_tournament_matches(
                    player_1=p1, player_2=p2, num_matches=1
                )

                win_table[p1_index, p2_index] += results.num_player_1_wins
                # loss_table[p2_index, p1_index] += results.num_player_1_wins

                win_table[p2_index, p1_index] += results.num_player_2_wins
                # loss_table

                # p1_win_prob = results.num_player_1_wins / (
                #     results.num_player_1_wins + results.num_player_2_wins
                # )
                # p2_win_prob = 1 - p1_win_prob
                # win_prob_table[p1_index, p2_index] = p1_win_prob
                # win_prob_table[p2_index, p1_index] = p2_win_prob

        print("")

        # Print the win-table.
        print("Win table:")
        for p1_i in range(len(players)):
            for p2_i in range(len(players)):
                print(f"{p1_i}, {p2_i}: {win_table[p1_i, p2_i]}")

        # Print the probability table.
        print("")
        print("Win-prob table:")
        for p1_i in range(len(players)):
            for p2_i in range(len(players)):
                num_wins = win_table[p1_i, p2_i]
                num_losses = win_table[p2_i, p1_i]
                if num_wins + num_losses == 0:
                    win_prob = 0.5
                else:
                    win_prob = num_wins / (num_wins + num_losses)
                print(f"{p1_i}, {p2_i}: {win_prob:0.2f}")
        print("")
        print("")

    # # Print the names.
    # for i, player in enumerate(players):
    #     print(f"{i}: {player.name}")
    # print("")

    # # Print the results.
    # for p1_index in range(len(players)):
    #     for p2_index in range(len(players)):
    #         print(f"{p1_index}, {p2_index}: {win_prob_table[p1_index, p2_index]:.02f}")


def main():
    # test_1()
    # tournament_1()
    tournament_2()


if __name__ == "__main__":
    main()

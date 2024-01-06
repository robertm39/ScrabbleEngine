from typing import Callable
from dataclasses import dataclass
from random import shuffle
from enum import Enum

from utils import *
from rules import *
import game_runner


# A player in a tournament.
@dataclass
class TournamentPlayer:
    get_strategy: Callable[[], MoveGetter]
    name: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class GameResult(Enum):
    PLAYER_1_WINS = "PLAYER_1_WINS"
    PLAYER_2_WINS = "PLAYER_2_WINS"
    TIE = "TIE"


# The results of a match or game in a tournament.
@dataclass
class MatchResults:
    player_1: TournamentPlayer
    player_2: TournamentPlayer
    num_player_1_wins: int
    num_player_2_wins: int
    num_ties: int


# Run a single game in a tournament match.
def do_tournament_game(
    state: GameState,
    player_1: TournamentPlayer,
    player_1_rack: list[Tile],
    player_2: TournamentPlayer,
    player_2_rack: list[Tile],
) -> GameResult:
    state = state.copy()

    player_1_rack = list(player_1_rack)
    player_2_rack = list(player_2_rack)

    # Give the players their racks.
    p1 = state.player_order[0]
    p2 = state.player_order[1]
    state.player_to_state[p1].tiles = player_1_rack
    state.player_to_state[p2].tiles = player_2_rack

    # Shuffle the tiles in the bag.
    shuffle(state.bag.tiles)

    # Set the starting player.
    state.current_player = p1

    # Get the strategies.
    player_to_strategy = {
        p1: player_1.get_strategy(),
        p2: player_2.get_strategy(),
    }

    # Play the game until the end.
    for _, new_state in game_runner.run_game(
        state=state, player_to_strategy=player_to_strategy, random_init=False
    ):
        pass

    # Determine the winner.
    p1_score = state.player_to_state[p1].score
    p2_score = state.player_to_state[p2].score
    # print(f"Player 1: {p1_score}, Player 2: {p2_score}")
    if p1_score > p2_score:
        return GameResult.PLAYER_1_WINS
    if p2_score > p1_score:
        return GameResult.PLAYER_2_WINS

    # No tiebreaker. This is the official tournament rule.
    return GameResult.TIE


# Run a tournament match between the two players.
# TODO make the config of the game configurable.
def do_tournament_match(
    player_1: TournamentPlayer, player_2: TournamentPlayer
) -> MatchResults:
    # Set up the initial state.
    p1 = Player(0)
    p2 = Player(1)
    state = GameState(
        config=get_scrabble_config(),
        current_player=p1,
        player_order=(p1, p2),
        player_to_state={
            p1: PlayerState(p1, 0, list()),
            p2: PlayerState(p2, 0, list()),
        },
        bag=Bag(get_scrabble_tiles()),
        board=get_scrabble_board(),
    )

    # Shuffle the tiles in the bag and determine the two starting racks.
    shuffle(state.bag.tiles)
    # print(f"There are {len(state.bag.tiles)} in the bag before drawing racks.")
    rack_1 = draw_tiles(bag=state.bag, num_tiles=7)
    rack_2 = draw_tiles(bag=state.bag, num_tiles=7)
    # print(f"There are {len(state.bag.tiles)} in the bag after drawing racks.")

    # # Run four games, with each player going first and second with both racks.
    # results = list[GameResult]()
    # results.append(
    #     do_tournament_game(
    #         state=state.copy(),
    #         player_1=player_1,
    #         player_1_rack=rack_1,
    #         player_2=player_2,
    #         player_2_rack=rack_2,
    #     )
    # )
    # results.append(
    #     do_tournament_game(
    #         state=state.copy(),
    #         player_1=player_2,
    #         player_1_rack=rack_1,
    #         player_2=player_1,
    #         player_2_rack=rack_2,
    #     )
    # )
    # results.append(
    #     do_tournament_game(
    #         state=state.copy(),
    #         player_1=player_1,
    #         player_1_rack=rack_2,
    #         player_2=player_2,
    #         player_2_rack=rack_1,
    #     )
    # )
    # results.append(
    #     do_tournament_game(
    #         state=state.copy(),
    #         player_1=player_2,
    #         player_1_rack=rack_2,
    #         player_2=player_1,
    #         player_2_rack=rack_1,
    #     )
    # )

    # Run all four games, keeping track of the number of wins.
    num_player_1_wins = 0
    num_player_2_wins = 0
    num_ties = 0

    # Run the game where player 1 goes first with the first rack.
    result = do_tournament_game(
        state=state.copy(),
        player_1=player_1,
        player_1_rack=rack_1,
        player_2=player_2,
        player_2_rack=rack_2,
    )
    if result == GameResult.PLAYER_1_WINS:
        num_player_1_wins += 1
    elif result == GameResult.PLAYER_2_WINS:
        num_player_2_wins += 1
    elif result == GameResult.TIE:
        num_ties += 1

    # Run the game where player 1 goes first with the second rack.
    result = do_tournament_game(
        state=state.copy(),
        player_1=player_1,
        player_1_rack=rack_2,
        player_2=player_2,
        player_2_rack=rack_1,
    )
    if result == GameResult.PLAYER_1_WINS:
        num_player_1_wins += 1
    elif result == GameResult.PLAYER_2_WINS:
        num_player_2_wins += 1
    elif result == GameResult.TIE:
        num_ties += 1

    # Run the game where player 2 goes first with the first rack.
    result = do_tournament_game(
        state=state.copy(),
        player_1=player_2,
        player_1_rack=rack_1,
        player_2=player_1,
        player_2_rack=rack_2,
    )
    if result == GameResult.PLAYER_1_WINS:
        # We have to reverse this, because player 2 was going first.
        num_player_2_wins += 1
    elif result == GameResult.PLAYER_2_WINS:
        num_player_1_wins += 1
    elif result == GameResult.TIE:
        num_ties += 1

    # Run the game where player 2 goes first with the second rack.
    result = do_tournament_game(
        state=state.copy(),
        player_1=player_2,
        player_1_rack=rack_2,
        player_2=player_1,
        player_2_rack=rack_1,
    )
    if result == GameResult.PLAYER_1_WINS:
        num_player_2_wins += 1
    elif result == GameResult.PLAYER_2_WINS:
        num_player_1_wins += 1
    elif result == GameResult.TIE:
        num_ties += 1

    # # Add up the number of wins for each player, and the number of ties.
    # for result in results:
    #     if result == GameResult.PLAYER_1_WINS:
    #         num_player_1_wins += 1
    #     elif result == GameResult.PLAYER_2_WINS:
    #         num_player_2_wins += 1
    #     elif result == GameResult.TIE:
    #         num_ties += 1

    return MatchResults(
        player_1=player_1,
        player_2=player_2,
        num_player_1_wins=num_player_1_wins,
        num_player_2_wins=num_player_2_wins,
        num_ties=num_ties,
    )


# Run the requested number of tournament matches and return the aggregate results.
def do_tournament_matches(
    player_1: TournamentPlayer, player_2: TournamentPlayer, num_matches: int
) -> MatchResults:
    num_player_1_wins = 0
    num_player_2_wins = 0
    num_ties = 0
    for i in range(num_matches):
        # print(f"Match {i+1} out of {num_matches}:")
        match_results = do_tournament_match(player_1=player_1, player_2=player_2)
        # print("")
        num_player_1_wins += match_results.num_player_1_wins
        num_player_2_wins += match_results.num_player_2_wins
        num_ties += match_results.num_ties

    return MatchResults(
        player_1=player_1,
        player_2=player_2,
        num_player_1_wins=num_player_1_wins,
        num_player_2_wins=num_player_2_wins,
        num_ties=num_ties,
    )

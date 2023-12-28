import unittest

from game_state import *
from rules import *
from utils import *


class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_board_from_strings_1(self):
        board = get_board_from_strings(tile_string="")
        exp_board = Board(
            width=0, height=0, position_to_tile=dict(), position_to_multiplier=dict()
        )
        self.assertEqual(board, exp_board)

        board = get_board_from_strings()
        exp_board = Board(
            width=0, height=0, position_to_tile=dict(), position_to_multiplier=dict()
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_2(self):
        board = get_board_from_strings(tile_string="A")
        exp_board = Board(
            width=1,
            height=1,
            position_to_tile={(0, 0): LetterTile("A")},
            position_to_multiplier=dict(),
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_3(self):
        board = get_board_from_strings(tile_string="a")
        exp_board = Board(
            width=1,
            height=1,
            position_to_tile={(0, 0): BlankTile("A")},
            position_to_multiplier=dict(),
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_4(self):
        board = get_board_from_strings(tile_string="QI")
        exp_board = Board(
            width=2,
            height=1,
            position_to_tile={
                (0, 0): LetterTile("Q"),
                (1, 0): LetterTile("I"),
            },
            position_to_multiplier=dict(),
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_5(self):
        board = get_board_from_strings(tile_string="QI\n N")
        exp_board = Board(
            width=2,
            height=2,
            position_to_tile={
                (0, 0): LetterTile("Q"),
                (1, 0): LetterTile("I"),
                (1, 1): LetterTile("N"),
            },
            position_to_multiplier=dict(),
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_6(self):
        board = get_board_from_strings(multiplier_string="")
        exp_board = Board(
            width=0,
            height=0,
            position_to_tile=dict(),
            position_to_multiplier=dict(),
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_7(self):
        board = get_board_from_strings(multiplier_string="2")
        exp_board = Board(
            width=1,
            height=1,
            position_to_tile=dict(),
            position_to_multiplier={(0, 0): WordMultiplier(2)},
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_8(self):
        board = get_board_from_strings(multiplier_string="2A")
        exp_board = Board(
            width=2,
            height=1,
            position_to_tile=dict(),
            position_to_multiplier={
                (0, 0): WordMultiplier(2),
                (1, 0): TileMultiplier(2),
            },
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_9(self):
        board = get_board_from_strings(multiplier_string="2 A\n B ")
        exp_board = Board(
            width=3,
            height=2,
            position_to_tile=dict(),
            position_to_multiplier={
                (0, 0): WordMultiplier(2),
                (2, 0): TileMultiplier(2),
                (1, 1): TileMultiplier(3),
            },
        )
        self.assertEqual(board, exp_board)

    def test_get_board_from_strings_10(self):
        board = get_board_from_strings(
            multiplier_string=(
                "3  A   3   A  3\n"
                " 2   B   B   2 \n"
                "  2   A A   2  \n"
                "A  2   A   2  A\n"
                "    2     2    \n"
                " B   B   B   B \n"
                "  A   A A   A  \n"
                "3  A   2   A  3\n"
                "  A   A A   A  \n"
                " B   B   B   B \n"
                "    2     2    \n"
                "A  2   A   2  A\n"
                "  2   A A   2  \n"
                " 2   B   B   2 \n"
                "3  A   3   A  3"
            )
        )
        exp_board = Board(
            width=15,
            height=15,
            position_to_tile=dict(),
            position_to_multiplier={
                # Triple word score.
                (0, 0): WordMultiplier(3),
                (7, 0): WordMultiplier(3),
                (14, 0): WordMultiplier(3),
                (0, 7): WordMultiplier(3),
                (14, 7): WordMultiplier(3),
                (0, 14): WordMultiplier(3),
                (7, 14): WordMultiplier(3),
                (14, 14): WordMultiplier(3),
                # The X going through the center of the board.
                (1, 1): WordMultiplier(2),
                (2, 2): WordMultiplier(2),
                (3, 3): WordMultiplier(2),
                (4, 4): WordMultiplier(2),
                (5, 5): TileMultiplier(3),
                (6, 6): TileMultiplier(2),
                (7, 7): WordMultiplier(2),
                (8, 8): TileMultiplier(2),
                (9, 9): TileMultiplier(3),
                (10, 10): WordMultiplier(2),
                (11, 11): WordMultiplier(2),
                (12, 12): WordMultiplier(2),
                (13, 13): WordMultiplier(2),
                (13, 1): WordMultiplier(2),
                (12, 2): WordMultiplier(2),
                (11, 3): WordMultiplier(2),
                (10, 4): WordMultiplier(2),
                (9, 5): TileMultiplier(3),
                (8, 6): TileMultiplier(2),
                (6, 8): TileMultiplier(2),
                (5, 9): TileMultiplier(3),
                (4, 10): WordMultiplier(2),
                (3, 11): WordMultiplier(2),
                (2, 12): WordMultiplier(2),
                (1, 13): WordMultiplier(2),
                # The arrows pointing toward the center of the board.
                # The arrow on the left.
                (1, 5): TileMultiplier(3),
                (2, 6): TileMultiplier(2),
                (3, 7): TileMultiplier(2),
                (2, 8): TileMultiplier(2),
                (1, 9): TileMultiplier(3),
                # The arrow on the top.
                (5, 1): TileMultiplier(3),
                (6, 2): TileMultiplier(2),
                (7, 3): TileMultiplier(2),
                (8, 2): TileMultiplier(2),
                (9, 1): TileMultiplier(3),
                # The arrow on the right.
                (13, 5): TileMultiplier(3),
                (12, 6): TileMultiplier(2),
                (11, 7): TileMultiplier(2),
                (12, 8): TileMultiplier(2),
                (13, 9): TileMultiplier(3),
                # The arrow on the bottom.
                (5, 13): TileMultiplier(3),
                (6, 12): TileMultiplier(2),
                (7, 11): TileMultiplier(2),
                (8, 12): TileMultiplier(2),
                (9, 13): TileMultiplier(3),
                # The additional double-letter scores on the edge of the board.
                (3, 0): TileMultiplier(2),
                (11, 0): TileMultiplier(2),
                (0, 3): TileMultiplier(2),
                (0, 11): TileMultiplier(2),
                (3, 14): TileMultiplier(2),
                (11, 14): TileMultiplier(2),
                (14, 3): TileMultiplier(2),
                (14, 11): TileMultiplier(2),
            },
        )
        self.assertEqual(board, exp_board)

    def test_get_place_tiles_move_from_string_1(self):
        move = get_place_tiles_move_from_string("CAT")
        exp_move = PlaceTilesMove(
            position_to_placing={
                (0, 0): LetterTilePlacing(tile=LetterTile("C")),
                (1, 0): LetterTilePlacing(tile=LetterTile("A")),
                (2, 0): LetterTilePlacing(tile=LetterTile("T")),
            }
        )
        self.assertEqual(move, exp_move)

    def test_get_place_tiles_move_from_string_2(self):
        move = get_place_tiles_move_from_string("B\no\ng")
        exp_move = PlaceTilesMove(
            position_to_placing={
                (0, 0): LetterTilePlacing(tile=LetterTile("B")),
                (0, 1): BlankTilePlacing(tile=BlankTile(), letter="O"),
                (0, 2): BlankTilePlacing(tile=BlankTile(), letter="G"),
            }
        )
        self.assertEqual(move, exp_move)

    def test_get_place_tiles_move_from_string_3(self):
        # Test that we can make invalid moves with this. This is necessary for testing the is_valid() method.
        move = get_place_tiles_move_from_string("CAT\nCAT")
        exp_move = PlaceTilesMove(
            position_to_placing={
                (0, 0): LetterTilePlacing(tile=LetterTile("C")),
                (1, 0): LetterTilePlacing(tile=LetterTile("A")),
                (2, 0): LetterTilePlacing(tile=LetterTile("T")),
                (0, 1): LetterTilePlacing(tile=LetterTile("C")),
                (1, 1): LetterTilePlacing(tile=LetterTile("A")),
                (2, 1): LetterTilePlacing(tile=LetterTile("T")),
            }
        )
        self.assertEqual(move, exp_move)


class StateTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_word_1(self):
        word = WordOnBoard(
            position_to_tile={
                (1, 0): LetterTile("A"),
                (0, 0): BlankTile("Z"),
                (2, 0): LetterTile("G"),
            }
        )
        self.assertEqual(word.get_word(), "ZAG")

    def test_get_word_2(self):
        word = WordOnBoard(
            position_to_tile={
                (0, 1): LetterTile("A"),
                (0, 0): LetterTile("Z"),
                (0, 2): BlankTile("G"),
            }
        )
        self.assertEqual(word.get_word(), "ZAG")

    def test_get_tile_at_get_letter_at(self):
        board = get_board_from_strings(tile_string="CaT \n AAr")
        self.assertEqual(board.get_tile_at((0, 0)), LetterTile("C"))
        self.assertEqual(board.get_tile_at((1, 0)), BlankTile("A"))
        self.assertEqual(board.get_tile_at((2, 0)), LetterTile("T"))
        self.assertEqual(board.get_tile_at((3, 0)), None)
        self.assertEqual(board.get_tile_at((0, 1)), None)
        self.assertEqual(board.get_tile_at((1, 1)), LetterTile("A"))
        self.assertEqual(board.get_tile_at((2, 1)), LetterTile("A"))
        self.assertEqual(board.get_tile_at((3, 1)), BlankTile("R"))

        self.assertEqual(board.get_letter_at((0, 0)), "C")
        self.assertEqual(board.get_letter_at((1, 0)), "A")
        self.assertEqual(board.get_letter_at((2, 0)), "T")
        self.assertEqual(board.get_letter_at((3, 0)), None)
        self.assertEqual(board.get_letter_at((0, 1)), None)
        self.assertEqual(board.get_letter_at((1, 1)), "A")
        self.assertEqual(board.get_letter_at((2, 1)), "A")
        self.assertEqual(board.get_letter_at((3, 1)), "R")

    def test_get_multiplier_at(self):
        board = get_board_from_strings(multiplier_string=" 2\nB ")
        self.assertEqual(board.get_multiplier_at((0, 0)), None)
        self.assertEqual(board.get_multiplier_at((1, 0)), WordMultiplier(2))
        self.assertEqual(board.get_multiplier_at((0, 1)), TileMultiplier(3))
        self.assertEqual(board.get_multiplier_at((1, 1)), None)

    def test_get_visible_to(self):
        board = get_board_from_strings(tile_string="CAT \n AAR")
        self.assertEqual(board.get_visible_to(Player(1)), board)

    def test_get_words_1(self):
        board = get_board_from_strings()
        self.assertListEqual(list(), board.get_words())

    def test_get_words_2(self):
        board = get_board_from_strings(tile_string="DOG")
        words = [get_word_on_board_from_string(tile_string="DOG")]
        self.assertCountEqual(board.get_words(), words)

    def test_get_words_3(self):
        board = get_board_from_strings(tile_string="DOG\nI  \nN  ")
        words = [
            get_word_on_board_from_string(tile_string="DOG"),
            get_word_on_board_from_string("D\nI\nN"),
        ]
        self.assertCountEqual(board.get_words(), words)

    def test_get_words_4(self):
        board = get_board_from_strings(
            tile_string=(
                "GROUND OVER\n"
                "OE PE  B   \n"
                " D     JO  \n"
                " SINK  E   \n"
                "    ABACA  \n"
                "       T   "
            )
        )
        words = [
            get_word_on_board_from_string(
                tile_string=(
                    "GROUND     \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "       OVER\n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n"
                    "OE         \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n"
                    "   PE      \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n"
                    "           \n"
                    "       JO  \n"
                    "           \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n"
                    "           \n"
                    "           \n"
                    " SINK      \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "    ABACA  \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "G          \n"
                    "O          \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    " R         \n"
                    " E         \n"
                    " D         \n"
                    " S         \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "   U       \n"
                    "   P       \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "    N      \n"
                    "    E      \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n"
                    "           \n"
                    "           \n"
                    "    K      \n"
                    "    A      \n"
                    "           "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "       O   \n"
                    "       B   \n"
                    "       J   \n"
                    "       E   \n"
                    "       C   \n"
                    "       T   "
                )
            ),
        ]
        self.assertCountEqual(board.get_words(), words)


class RulesTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.p0 = Player(0)
        self.p1 = Player(1)

        self.empty_config = ScrabbleConfig(
            playable_words=tuple(),
            min_tiles_for_turn_in=7,
            max_tiles_in_hand=7,
            min_tiles_for_bingo=7,
            bingo_points=50,
            scoreless_turns_to_end_game=6,
        )
        self.empty_state = GameState(
            config=self.empty_config,
            current_player=self.p0,
            player_order=(self.p0, self.p1),
            player_to_state={
                self.p0: PlayerState(player=self.p0, score=0, tiles=list()),
                self.p1: PlayerState(player=self.p1, score=0, tiles=list()),
            },
            bag_state=Bag(tiles=list()),
            board_state=get_board_from_strings(),
        )

    def test_end_game_for_scoreless_turns(self):
        state = self.empty_state.copy()
        end_game_for_scoreless_turns(state)
        self.assertFalse(state.game_finished)

        state.num_scoreless_turns = 6
        end_game_for_scoreless_turns(state)
        self.assertTrue(state.game_finished)

        state.num_scoreless_turns = 0
        end_game_for_scoreless_turns(state)
        self.assertTrue(state.game_finished)

    def test_get_tile_to_count(self):
        pairs = (
            (list(), dict()),
            ([LetterTile("A")], {LetterTile("A"): 1}),
            ([LetterTile("A")] * 2, {LetterTile("A"): 2}),
            (
                [LetterTile("Q"), BlankTile(), LetterTile("F"), LetterTile("F")],
                {LetterTile("Q"): 1, BlankTile(): 1, LetterTile("F"): 2},
            ),
            ([BlankTile()] * 3, {BlankTile(): 3}),
        )
        for tiles, exp_tile_to_count in pairs:
            tile_to_count = get_tile_to_count(tiles)
            self.assertDictEqual(tile_to_count, exp_tile_to_count)

    def test_get_next_player_index(self):
        pairs = (
            ((0, 2), 1),
            ((1, 2), 0),
            ((0, 3), 1),
            ((1, 3), 2),
            ((2, 3), 0),
            ((0, 4), 1),
            ((1, 4), 2),
            ((2, 4), 3),
            ((3, 4), 0),
        )
        for (index, num_players), exp_next_player in pairs:
            next_player = get_next_player_index(index=index, num_players=num_players)
            self.assertEqual(next_player, exp_next_player)

    def test_advance_player(self):
        state = self.empty_state.copy()
        self.assertEqual(state.current_player, self.p0)
        advance_player(state)
        self.assertEqual(state.current_player, self.p1)
        advance_player(state)
        self.assertEqual(state.current_player, self.p0)

    def test_all_tiles_available(self):
        pairs = (
            ((list(), list()), True),
            ((list(), [LetterTile("A")]), False),
            (([LetterTile("A")], list()), True),
            (([LetterTile("A")], [LetterTile("A")]), True),
            (([LetterTile("B")], [LetterTile("A")]), False),
            (([LetterTile("B"), LetterTile("A")], [LetterTile("A")]), True),
            (([LetterTile("B"), BlankTile()], [BlankTile()]), True),
            ((list(), [BlankTile()]), False),
        )
        for (available, requested), exp_all_available in pairs:
            all_available = all_tiles_available(
                available_tiles=available, requested_tiles=requested
            )
            self.assertEqual(all_available, exp_all_available)

    def test_get_adjacent_positions(self):
        pairs = (
            ([(0, 0)], [(-1, 0), (1, 0), (0, -1), (0, 1)]),
            ([(0, 0), (1, 0)], [(-1, 0), (0, -1), (0, 1), (1, -1), (1, 1), (2, 0)]),
        )
        for positions, exp_adjacent in pairs:
            adjacent = get_adjacent_positions(positions=positions)
            self.assertCountEqual(adjacent, exp_adjacent)

    def test_pass_move_is_valid(self):
        move = PassMove()
        state = self.empty_state.copy()
        self.assertTrue(move.is_valid(state))
        state.game_finished = True
        self.assertFalse(move.is_valid(state))

    def test_pass_move_perform_1(self):
        move = PassMove()
        next_state = self.empty_state.copy()
        move.perform(next_state)

        exp_next_state = self.empty_state.copy()
        exp_next_state.current_player = self.p1
        exp_next_state.num_scoreless_turns = 1
        self.assertEqual(next_state, exp_next_state)

    def test_pass_move_perform_2(self):
        move = PassMove()
        state = self.empty_state.copy()

        state.current_player = self.p1

        next_state = state.copy()
        move.perform(next_state)

        exp_next_state = state.copy()
        exp_next_state.current_player = self.p0
        exp_next_state.num_scoreless_turns = 1
        self.assertEqual(next_state, exp_next_state)

    def test_pass_move_perform_3(self):
        move = PassMove()
        state = self.empty_state.copy()
        for _ in range(5):
            move.perform(state)
        self.assertFalse(state.game_finished)
        move.perform(state)
        self.assertTrue(state.game_finished)

    def test_exchange_tiles_move_is_valid_1(self):
        state = self.empty_state.copy()

        # Test checking if there are enough tiles in the bag for an exchange to be legal.
        move = ExchangeTilesMove(tiles=list())
        self.assertFalse(move.is_valid(state))

        state.bag.tiles = [LetterTile("A")] * 7
        self.assertTrue(move.is_valid(state))

        # You can't do any move if the game is over.
        state.game_finished = True
        self.assertFalse(move.is_valid(state))

        state = self.empty_state.copy()

    def test_exchange_tiles_move_is_valid_2(self):
        state = self.empty_state.copy()
        state.bag.tiles = [LetterTile("A")] * 7
        move_1 = ExchangeTilesMove(tiles=[LetterTile("A")])

        # Test checking if the player has all of the tiles to be exchanged.
        self.assertFalse(move_1.is_valid(state))
        state.player_to_state[self.p0].tiles.append(LetterTile("A"))
        self.assertTrue(move_1.is_valid(state))

        state = self.empty_state.copy()
        state.bag.tiles = [LetterTile("A")] * 7
        move_2 = ExchangeTilesMove(tiles=[LetterTile("E"), BlankTile()])
        self.assertFalse(move_2.is_valid(state))
        state.player_to_state[self.p0].tiles.append(LetterTile("A"))
        self.assertFalse(move_2.is_valid(state))
        state.player_to_state[self.p0].tiles.append(LetterTile("E"))
        self.assertFalse(move_2.is_valid(state))
        state.player_to_state[self.p0].tiles.append(BlankTile())
        self.assertTrue(move_2.is_valid(state))
        state.player_to_state[self.p0].tiles.append(LetterTile("E"))
        self.assertTrue(move_2.is_valid(state))

    def test_exchange_tiles_move_perform_1(self):
        state = self.empty_state.copy()

        state.config.min_tiles_for_turn_in = 1
        state.bag.tiles.append(LetterTile("A"))
        state.player_to_state[self.p0].tiles.append(LetterTile("B"))
        move = ExchangeTilesMove(tiles=[LetterTile("B")])
        move.perform(state)

        exp_state = self.empty_state.copy()
        exp_state.config.min_tiles_for_turn_in = 1
        exp_state.bag.tiles.append(LetterTile("B"))
        exp_state.player_to_state[self.p0].tiles.append(LetterTile("A"))
        exp_state.num_scoreless_turns = 1
        exp_state.current_player = self.p1

        self.assertEqual(exp_state, state)

    def test_exchange_tiles_move_perform_2(self):
        state = self.empty_state.copy()
        letters = "ABCDEFG"
        state.bag.tiles = [LetterTile(l) for l in letters]  # type: ignore

        p0_state = state.player_to_state[self.p0]
        p0_state.tiles.append(LetterTile("O"))
        move = ExchangeTilesMove(tiles=[LetterTile("O")])
        move.perform(state)

        self.assertIn(LetterTile("O"), state.bag.tiles)
        self.assertNotIn(LetterTile("O"), p0_state.tiles)
        self.assertEqual(len(p0_state.tiles), 1)
        self.assertIn(p0_state.tiles[0].letter, letters)  # type: ignore

    def test_exchange_tiles_move_perform_3(self):
        state = self.empty_state.copy()
        state.config.min_tiles_for_turn_in = 0
        move = ExchangeTilesMove(tiles=list())

        for _ in range(5):
            move.perform(state)
        self.assertFalse(state.game_finished)
        move.perform(state)
        self.assertTrue(state.game_finished)

    # Assert that the given tile-placement moves have the given orientations.
    def _assert_orientation(
        self,
        board: Board,
        tile_strings: Iterable[str],
        horizontal: bool,
        vertical: bool,
    ) -> None:
        for tile_string in tile_strings:
            move = get_place_tiles_move_from_string(tile_string=tile_string)
            self.assertEqual(
                move._is_particular_linear_placement(
                    board, parallel_coord="x", perpendicular_coord="y"
                ),
                horizontal,
            )
            self.assertEqual(
                move._is_particular_linear_placement(
                    board, parallel_coord="y", perpendicular_coord="x"
                ),
                vertical,
            )
            self.assertEqual(
                move._is_any_linear_placement(board), horizontal or vertical
            )

    # Assert that the given tile-placement moves are horizontal.
    def _assert_horizontal(self, board: Board, tile_strings: Iterable[str]) -> None:
        self._assert_orientation(
            board=board, tile_strings=tile_strings, horizontal=True, vertical=False
        )

    # Assert that the given tile-placement moves are vertical.
    def _assert_vertical(self, board: Board, tile_strings: Iterable[str]) -> None:
        self._assert_orientation(
            board=board, tile_strings=tile_strings, horizontal=False, vertical=True
        )

    # Assert that the given tile-placement moves are neither horizontal nor vertical.
    def _assert_neither_orientation(
        self, board: Board, tile_strings: Iterable[str]
    ) -> None:
        self._assert_orientation(
            board=board, tile_strings=tile_strings, horizontal=False, vertical=False
        )

    def test_place_tiles_move_is_particular_linear_placement_1(self):
        state = self.empty_state.copy()

        horizontal = (
            "CAT",
            "\nABACA",
        )
        self._assert_horizontal(board=state.board, tile_strings=horizontal)

        vertical = (
            "D\nO\ng",
            "\n\n  O\n  A\n  T\n  M\n  E\n  A\n  L",
        )
        self._assert_vertical(board=state.board, tile_strings=vertical)

        neither = (
            "D G",
            "C\n A\n  T",
            "RA DIO",
        )
        self._assert_neither_orientation(board=state.board, tile_strings=neither)

    def test_place_tiles_move_is_particular_linear_placement_2(self):
        state = self.empty_state.copy()
        move_1 = get_place_tiles_move_from_string("")
        self.assertFalse(
            move_1._is_particular_linear_placement(
                board=state.board, parallel_coord="x", perpendicular_coord="y"
            )
        )
        self.assertFalse(
            move_1._is_particular_linear_placement(
                board=state.board, parallel_coord="y", perpendicular_coord="x"
            )
        )

    def test_place_tiles_move_is_particular_linear_placement_3(self):
        state = self.empty_state.copy()
        state.board = get_board_from_strings(
            tile_string=(
                "        \n"
                "CATAPULT\n"
                "       O\n"
                "       P\n"
                "       P\n"
                "       L\n"
                "       E\n"
            )
        )

        horizontal = ("\n\n      N T", "\n\n\n      A E")
        self._assert_horizontal(board=state.board, tile_strings=horizontal)

        vertical = (
            " B\n\n G",
            "\n\nA\nR",
        )
        self._assert_vertical(board=state.board, tile_strings=vertical)

        neither = (
            "D G",
            "C\n A\n  T",
            "\nWITH",
            "RA DIO",
            "D\n\n\nG",
        )
        self._assert_neither_orientation(board=state.board, tile_strings=neither)

    def test_place_tiles_move_get_words_made_1(self):
        board = get_board_from_strings(tile_string="DA")
        move = get_place_tiles_move_from_string(tile_string="\nAA")

        new_words = (
            get_word_on_board_from_string(tile_string="\nAA"),
            get_word_on_board_from_string(tile_string="D\nA"),
            get_word_on_board_from_string(tile_string=" A\n A"),
        )
        self.assertCountEqual(new_words, move.get_words_made(board=board))

    def test_place_tiles_move_get_words_made_2(self):
        board = get_board_from_strings(tile_string="DA")
        move = get_place_tiles_move_from_string(tile_string="  B")

        new_words = [get_word_on_board_from_string(tile_string="DAB")]
        self.assertCountEqual(new_words, move.get_words_made(board=board))

    def test_place_tiles_move_get_words_made_3(self):
        board = get_board_from_strings(tile_string="INDEX")
        move = get_place_tiles_move_from_string(tile_string="\n AEDILE")

        new_words = (
            get_word_on_board_from_string(tile_string="\n AEDILE"),
            get_word_on_board_from_string(tile_string=" N\n A"),
            get_word_on_board_from_string(tile_string="  D\n  E"),
            get_word_on_board_from_string(tile_string="   E\n   D"),
            get_word_on_board_from_string(tile_string="    X\n    I"),
        )
        self.assertCountEqual(new_words, move.get_words_made(board=board))

    def test_place_tiles_move_is_valid_1(self):
        move_1 = get_place_tiles_move_from_string(tile_string="DOGE")

        # Test checking if the game is over.
        state = self.empty_state.copy()
        state.board = get_board_from_strings(tile_string="    \n    \n    ")
        state.player_to_state[self.p0].tiles = [
            LetterTile("D"),
            LetterTile("O"),
            LetterTile("G"),
            LetterTile("E"),
        ]
        state.game_finished = True
        self.assertFalse(move_1.is_valid(state=state))

        # Test checking if the move has at least one tile.
        move_2 = get_place_tiles_move_from_string(tile_string="")
        self.assertFalse(move_2.is_valid(state=state))

        # Test checking if the player has the tiles.
        state = self.empty_state.copy()
        state.board = get_board_from_strings(tile_string="    \n    \n    ")
        state.player_to_state[self.p0].tiles = list()
        self.assertFalse(move_1.is_valid(state=state))

        # Test checking if the word fits on the board.
        state = self.empty_state.copy()
        state.board = get_board_from_strings(tile_string="   \n   \n   ")
        state.player_to_state[self.p0].tiles = [
            LetterTile("D"),
            LetterTile("O"),
            LetterTile("G"),
            LetterTile("E"),
        ]
        self.assertFalse(move_1.is_valid(state=state))

        # Test checking if the move places a tile onto a tile already on the board.
        state = self.empty_state.copy()
        state.board = get_board_from_strings(tile_string="APPLE")
        state.player_to_state[self.p0].tiles = [
            LetterTile("W"),
            LetterTile("I"),
            LetterTile("T"),
            LetterTile("H"),
        ]
        move_3 = get_place_tiles_move_from_string(tile_string="WITH")
        self.assertFalse(move_3.is_valid(state=state))

        # Test checking if the move is in a line.
        for tile_string in ("u nder", "b\n i\ng", "with in"):
            state = self.empty_state.copy()
            state.board = get_board_from_strings(
                tile_string="       \n       \n       \n       "
            )
            state.player_to_state[self.p0].tiles = [BlankTile()] * 7
            move_4 = get_place_tiles_move_from_string(tile_string=tile_string)
            self.assertFalse(move_4.is_valid(state=state))

        # Test checking that, if there are no tiles on the board, the move covers the starting position.
        state = self.empty_state.copy()
        state.board = get_board_from_strings(tile_string="       ")
        state.board.starting_position = (3, 0)
        state.player_to_state[self.p0].tiles = [
            LetterTile("D"),
            LetterTile("O"),
            LetterTile("G"),
        ]
        move_5 = get_place_tiles_move_from_string(tile_string="DOG")
        self.assertFalse(move_5.is_valid(state=state))

        # Test checking that, if any tiles are placed, at least one tile in the move is adjacent to a tile on the board.
        state = self.empty_state.copy()
        state.board = get_board_from_strings(tile_string="CAT\n   \n   ")
        state.player_to_state[self.p0].tiles = [
            LetterTile("D"),
            LetterTile("O"),
            LetterTile("G"),
        ]
        move_6 = get_place_tiles_move_from_string(tile_string="\n\nDOG")
        self.assertFalse(move_6.is_valid(state=state))

        # Test checking if the move makes at least one word.
        state = self.empty_state.copy()
        move_7 = get_place_tiles_move_from_string(tile_string="A")
        state.player_to_state[self.p0].tiles = [LetterTile("A")]
        self.assertFalse(move_7.is_valid(state=state))


if __name__ == "__main__":  #
    unittest.main()

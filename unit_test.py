import unittest

from game_state import *
from rules import *
from utils import *
from move_generation import *
import infix_data


class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_tile_from_char_1(self):
        pairs = (
            ("A", LetterTile("A")),
            ("R", LetterTile("R")),
            ("f", BlankTile("F")),
            ("x", BlankTile("X")),
            ("*", BlankTile()),
        )
        for c, exp_tile in pairs:
            tile = get_tile_from_char(c=c, letter_to_points=dict())
            self.assertEqual(tile, exp_tile)

    def test_get_tile_from_char_2(self):
        letter_to_points = {"A": 1, "R": 2, "X": 10}
        pairs = (
            ("A", LetterTile("A", points=1)),
            ("R", LetterTile("R", points=2)),
            ("f", BlankTile("F", points=0)),
            ("x", BlankTile("X", points=0)),
            ("*", BlankTile()),
        )
        for c, exp_tile in pairs:
            tile = get_tile_from_char(c=c, letter_to_points=letter_to_points)
            self.assertEqual(tile, exp_tile)

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
        move = get_place_tiles_move_from_string("B\no\nb")
        exp_move = PlaceTilesMove(
            position_to_placing={
                (0, 0): LetterTilePlacing(tile=LetterTile("B")),
                (0, 1): BlankTilePlacing(tile=BlankTile(), letter="O"),
                (0, 2): BlankTilePlacing(tile=BlankTile(), letter="B"),
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

    def test_get_place_tiles_move_from_string_4(self):
        move = get_place_tiles_move_from_string(
            "CAT", letter_to_points={"C": 3, "A": 1, "T": 2}
        )
        exp_move = PlaceTilesMove(
            position_to_placing={
                (0, 0): LetterTilePlacing(tile=LetterTile("C", points=3)),
                (1, 0): LetterTilePlacing(tile=LetterTile("A", points=1)),
                (2, 0): LetterTilePlacing(tile=LetterTile("T", points=2)),
            }
        )
        self.assertEqual(move, exp_move)

    def test_get_tiles_from_string_1(self):
        pairs = (
            ("", list()),
            ("A", [LetterTile("A")]),
            ("AGO", [LetterTile("A"), LetterTile("G"), LetterTile("O")]),
            ("A*O", [LetterTile("A"), BlankTile(), LetterTile("O")]),
        )
        for tile_string, exp_tiles in pairs:
            tiles = get_tiles_from_string(tile_string=tile_string)
            self.assertCountEqual(tiles, exp_tiles)

    def test_get_tiles_from_string_2(self):
        letter_to_points = {"A": 1, "G": 2, "O": 3}
        pairs = (
            ("", list()),
            ("A", [LetterTile("A", 1)]),
            ("AGO", [LetterTile("A", 1), LetterTile("G", 2), LetterTile("O", 3)]),
            ("A*O", [LetterTile("A", 1), BlankTile(), LetterTile("O", 3)]),
        )
        for tile_string, exp_tiles in pairs:
            tiles = get_tiles_from_string(
                tile_string=tile_string, letter_to_points=letter_to_points
            )
            self.assertCountEqual(tiles, exp_tiles)


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
        # self.assertEqual(word.get_word(), "ZAG")
        self.assertEqual(word.word, "ZAG")

    def test_get_word_2(self):
        word = WordOnBoard(
            position_to_tile={
                (0, 1): LetterTile("A"),
                (0, 0): LetterTile("Z"),
                (0, 2): BlankTile("G"),
            }
        )
        # self.assertEqual(word.get_word(), "ZAG")
        self.assertEqual(word.word, "ZAG")

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

        self.empty_config = GameConfig(
            playable_words=tuple(),
            min_tiles_for_turn_in=7,
            max_tiles_in_hand=7,
            min_tiles_for_bonus=7,
            bonus_points=50,
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
            bag=Bag(tiles=list()),
            board=get_board_from_strings(),
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

    def test_deduct_final_tile_points_1(self):
        state = self.empty_state.copy()

        state.player_to_state[self.p0].tiles = [LetterTile("A", points=1)]
        state.player_to_state[self.p1].tiles = [LetterTile("Q", points=10)]
        deduct_final_tile_points(state=state, add_to_current_player=False)

        self.assertEqual(state.player_to_state[self.p0].score, -1)
        self.assertEqual(state.player_to_state[self.p1].score, -10)

    def test_deduct_final_tile_points_2(self):
        state = self.empty_state.copy()

        state.player_to_state[self.p0].tiles = [LetterTile("A", points=1)]
        state.player_to_state[self.p1].tiles = [
            LetterTile("Q", points=10),
            LetterTile("C", points=3),
        ]
        deduct_final_tile_points(state=state, add_to_current_player=False)

        self.assertEqual(state.player_to_state[self.p0].score, -1)
        self.assertEqual(state.player_to_state[self.p1].score, -13)

    def test_deduct_final_tile_points_3(self):
        state = self.empty_state.copy()

        state.player_to_state[self.p1].tiles = [
            LetterTile("Q", points=10),
            LetterTile("C", points=3),
        ]
        deduct_final_tile_points(state=state, add_to_current_player=True)

        self.assertEqual(state.player_to_state[self.p0].score, 13)
        self.assertEqual(state.player_to_state[self.p1].score, -13)

    def test_draw_tiles_1(self):
        state = self.empty_state.copy()
        state.bag.tiles = get_tiles_from_string("A")
        draw_tiles(state.player_to_state[self.p0], state.bag, 1)

        exp_state = self.empty_state.copy()
        exp_state.player_to_state[self.p0].tiles = get_tiles_from_string("A")
        self.assertEqual(state, exp_state)

    def test_draw_tiles_2(self):
        state = self.empty_state.copy()
        state.bag.tiles = get_tiles_from_string("A")
        draw_tiles(state.player_to_state[self.p0], state.bag, 2)

        exp_state = self.empty_state.copy()
        exp_state.player_to_state[self.p0].tiles = get_tiles_from_string("A")
        self.assertEqual(state, exp_state)

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

    def test_pass_move_perform_4(self):
        state = self.empty_state.copy()

        state.player_to_state[self.p0].tiles = [LetterTile("A", points=1)]
        state.player_to_state[self.p1].tiles = [LetterTile("Q", points=10)]

        move = PassMove()
        for i in range(5):
            move.perform(state)
            self.assertEqual(state.num_scoreless_turns, i + 1)
        self.assertFalse(state.game_finished)
        move.perform(state)
        self.assertEqual(state.num_scoreless_turns, 6)
        self.assertTrue(state.game_finished)

        self.assertEqual(state.player_to_state[self.p0].score, -1)
        self.assertEqual(state.player_to_state[self.p1].score, -10)

    def test_exchange_tiles_move_is_valid_1(self):
        state = self.empty_state.copy()

        # Test checking if there are enough tiles in the bag for an exchange to be legal.
        move = ExchangeTilesMove(tiles=list())
        self.assertFalse(move.is_valid(state))

        state.bag.tiles = get_tiles_from_string("A" * 7)
        self.assertTrue(move.is_valid(state))

        # You can't do any move if the game is over.
        state.game_finished = True
        self.assertFalse(move.is_valid(state))

        state = self.empty_state.copy()

    def test_exchange_tiles_move_is_valid_2(self):
        state = self.empty_state.copy()
        state.bag.tiles = get_tiles_from_string("A" * 7)
        move_1 = ExchangeTilesMove(tiles=[LetterTile("A")])

        # Test checking if the player has all of the tiles to be exchanged.
        self.assertFalse(move_1.is_valid(state))
        state.player_to_state[self.p0].tiles.append(LetterTile("A"))
        self.assertTrue(move_1.is_valid(state))

        state = self.empty_state.copy()
        state.bag.tiles = get_tiles_from_string("A" * 7)
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
        state.player_to_state[self.p0].tiles = get_tiles_from_string("DOGE")
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
        state.player_to_state[self.p0].tiles = get_tiles_from_string("DOGE")
        self.assertFalse(move_1.is_valid(state=state))

        # Test checking if the move places a tile onto a tile already on the board.
        state = self.empty_state.copy()
        state.board = get_board_from_strings(tile_string="APPLE")
        state.player_to_state[self.p0].tiles = get_tiles_from_string("WITH")
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
        state.player_to_state[self.p0].tiles = get_tiles_from_string("DOG")
        move_5 = get_place_tiles_move_from_string(tile_string="DOG")
        self.assertFalse(move_5.is_valid(state=state))

        # Test checking that, if any tiles are placed, at least one tile in the move is adjacent to a tile on the board.
        state = self.empty_state.copy()
        state.board = get_board_from_strings(tile_string="CAT\n   \n   ")
        state.player_to_state[self.p0].tiles = get_tiles_from_string("DOG")
        move_6 = get_place_tiles_move_from_string(tile_string="\n\nDOG")
        self.assertFalse(move_6.is_valid(state=state))

        # Test checking if the move makes at least one word.
        state = self.empty_state.copy()
        move_7 = get_place_tiles_move_from_string(tile_string="A")
        state.player_to_state[self.p0].tiles = [LetterTile(letter="A")]
        self.assertFalse(move_7.is_valid(state=state))

    def test_place_tiles_move_get_points_for_word(self):
        pairs = (
            ("   ", 6),
            ("2  ", 12),
            (" 2 ", 12),
            ("  2", 12),
            ("A  ", 7),
            ("  B", 12),
            ("2 B", 24),
            (" 2B", 24),
            (" 2A", 18),
            ("33B", 108),
        )
        for multiplier_string, exp_points in pairs:
            board = get_board_from_strings(
                multiplier_string=multiplier_string, tile_string="   "
            )
            move = get_place_tiles_move_from_string(
                tile_string="DOG", letter_to_points={"D": 1, "O": 2, "G": 3}
            )
            word = move.get_words_made(board=board)[0]
            self.assertEqual(
                move.get_points_for_word(board=board, word=word), exp_points
            )

    def test_place_tiles_move_perform_1(self):
        # Test a normal case.
        state = self.empty_state.copy()
        letter_to_points = {"B": 1, "A": 1, "G": 1}
        state.bag.tiles = [BlankTile()]
        state.player_to_state[self.p0].tiles = get_tiles_from_string(
            "BAG", letter_to_points=letter_to_points
        )
        state.board = get_board_from_strings(tile_string="   ")

        move = get_place_tiles_move_from_string(
            "BAG", letter_to_points=letter_to_points
        )

        move.perform(state=state)

        exp_state = self.empty_state.copy()
        exp_state.board = get_board_from_strings(
            tile_string="BAG", letter_to_points=letter_to_points
        )
        exp_state.player_to_state[self.p0].score = 3
        exp_state.player_to_state[self.p0].tiles = [BlankTile()]
        exp_state.current_player = self.p1

        self.assertEqual(state, exp_state)

    def test_place_tiles_move_perform_2(self):
        # Test a case with a 50-point bonus.
        state = self.empty_state.copy()
        letter_to_points = {c: 1 for c in "OSTRICH"}
        state.bag.tiles = [BlankTile()]
        state.player_to_state[self.p0].tiles = get_tiles_from_string(
            "OSTRICH", letter_to_points=letter_to_points
        )
        state.board = get_board_from_strings(tile_string="       ")

        move = get_place_tiles_move_from_string(
            "OSTRICH", letter_to_points=letter_to_points
        )

        move.perform(state=state)

        exp_state = self.empty_state.copy()
        exp_state.board = get_board_from_strings(
            tile_string="OSTRICH", letter_to_points=letter_to_points
        )
        exp_state.player_to_state[self.p0].score = 57
        exp_state.player_to_state[self.p0].tiles = [BlankTile()]
        exp_state.current_player = self.p1

        self.assertEqual(state, exp_state)

    def test_place_tiles_move_perform_3(self):
        # Test that the number of scoreless turns is reset to zero.
        state = self.empty_state.copy()
        state.num_scoreless_turns = 5
        letter_to_points = {"B": 1, "A": 1, "G": 1}
        state.bag.tiles = [BlankTile()]
        state.player_to_state[self.p0].tiles = get_tiles_from_string(
            "BAG", letter_to_points=letter_to_points
        )
        state.board = get_board_from_strings(tile_string="   ")

        move = get_place_tiles_move_from_string(
            "BAG", letter_to_points=letter_to_points
        )

        move.perform(state=state)

        exp_state = self.empty_state.copy()
        exp_state.board = get_board_from_strings(
            tile_string="BAG", letter_to_points=letter_to_points
        )
        exp_state.player_to_state[self.p0].score = 3
        exp_state.player_to_state[self.p0].tiles = [BlankTile()]
        exp_state.current_player = self.p1

        self.assertEqual(state, exp_state)

    def test_place_tiles_move_perform_4(self):
        # Test that the number of scoreless turns is incremented if no points are scored.
        state = self.empty_state.copy()
        state.num_scoreless_turns = 0
        letter_to_points = dict()
        state.bag.tiles = [BlankTile()]
        state.player_to_state[self.p0].tiles = [BlankTile()]
        state.board = get_board_from_strings(tile_string="a ")

        move = get_place_tiles_move_from_string(" t", letter_to_points=letter_to_points)

        move.perform(state=state)

        exp_state = self.empty_state.copy()
        exp_state.num_scoreless_turns = 1
        exp_state.board = get_board_from_strings(
            tile_string="at", letter_to_points=letter_to_points
        )
        exp_state.player_to_state[self.p0].tiles = [BlankTile()]
        exp_state.current_player = self.p1

        self.assertEqual(state, exp_state)

    def test_place_tiles_move_perform_5(self):
        # Test that the number of scoreless turns is not incremented when the word placed
        # scores no points, but the player does get a 50-point bonus.
        state = self.empty_state.copy()
        state.num_scoreless_turns = 5
        letter_to_points = dict()
        state.bag.tiles = [BlankTile()]
        state.player_to_state[self.p0].tiles = [BlankTile()] * 7
        state.board = get_board_from_strings(tile_string="       ")

        move = get_place_tiles_move_from_string(
            "ostrich", letter_to_points=letter_to_points
        )

        move.perform(state=state)

        exp_state = self.empty_state.copy()
        exp_state.board = get_board_from_strings(
            tile_string="ostrich", letter_to_points=letter_to_points
        )
        exp_state.num_scoreless_turns = 0
        exp_state.player_to_state[self.p0].score = 50
        exp_state.player_to_state[self.p0].tiles = [BlankTile()]
        exp_state.current_player = self.p1

        self.assertEqual(state, exp_state)

    def test_place_tiles_move_perform_6(self):
        # Test that the game ends and play doesn't advance to the next player
        # if this is the sixth scoreless turn in a row.
        state = self.empty_state.copy()
        state.num_scoreless_turns = 5
        letter_to_points = dict()
        state.bag.tiles = [BlankTile()]
        state.player_to_state[self.p0].tiles = [BlankTile()]
        state.board = get_board_from_strings(tile_string="a ")

        move = get_place_tiles_move_from_string(" t", letter_to_points=letter_to_points)

        move.perform(state=state)

        exp_state = self.empty_state.copy()
        exp_state.board = get_board_from_strings(
            tile_string="at", letter_to_points=letter_to_points
        )
        exp_state.num_scoreless_turns = 6
        exp_state.player_to_state[self.p0].tiles = [BlankTile()]
        exp_state.game_finished = True

        self.assertEqual(state, exp_state)

    def test_place_tiles_move_perform_7(self):
        # Test a normal case.
        state = self.empty_state.copy()
        letter_to_points = {"A": 1, "E": 1, "D": 1, "I": 1, "L": 1, "N": 1, "X": 10}
        state.bag.tiles = [BlankTile()]
        state.player_to_state[self.p0].tiles = get_tiles_from_string(
            "AEDILE", letter_to_points=letter_to_points
        )
        state.board = get_board_from_strings(
            tile_string="INDEX  \n       ", letter_to_points=letter_to_points
        )

        move = get_place_tiles_move_from_string(
            "\n AEDILE", letter_to_points=letter_to_points
        )

        move.perform(state=state)

        exp_state = self.empty_state.copy()
        exp_state.board = get_board_from_strings(
            tile_string="INDEX  \n AEDILE", letter_to_points=letter_to_points
        )
        exp_state.player_to_state[self.p0].score = 23
        exp_state.player_to_state[self.p0].tiles = [BlankTile()]
        exp_state.current_player = self.p1

        self.assertEqual(state, exp_state)


class MoveGenerationTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.small_dictionary = frozenset(
            {
                "AA",
                "AB",
                "AT",
                "BA",
                "TA",
                "ABA",
                "ATT",
                "BAA",
                "BAT",
                "TAB",
                "TAT",
                "ABBA",
                "BABA",
                "BATT",
                "BATATA",
            }
        )
        self.p0 = Player(0)
        board = get_scrabble_board()
        config = get_scrabble_config()
        config.playable_words = self.small_dictionary
        self.empty_state = GameState(
            config=config,
            current_player=self.p0,
            player_order=[self.p0],
            player_to_state={self.p0: PlayerState(self.p0, 0, list())},
            bag=Bag(list()),
            board=board,
        )

        self.moves_finder = PlaceTilesMoveFinder(words=self.small_dictionary)

    def test_infix_data_1(self):
        infix_info = infix_data.InfixData(words=self.small_dictionary)

        exp_can_add_at_start = {l: frozenset() for l in ALPHABET}

        exp_can_add_at_start.update(
            {
                "A": frozenset(
                    {"A", "B", "T", "BA", "TT", "BB", "BBA", "TA", "TAT", "TATA"}
                ),
                "B": frozenset(
                    {
                        "A",
                        "AA",
                        "AT",
                        "B",
                        "BA",
                        "AB",
                        "ABA",
                        "ATT",
                        "ATA",
                        "ATAT",
                        "ATATA",
                    }
                ),
                "T": frozenset({"A", "T", "AB", "AT", "ATA"}),
            }
        )
        self.assertDictEqual(dict(infix_info.can_add_at_start), exp_can_add_at_start)

        exp_can_add_at_end = {l: frozenset() for l in ALPHABET}
        exp_can_add_at_end.update(
            {
                "A": frozenset(
                    {
                        "A",
                        "B",
                        "T",
                        "AB",
                        "AT",
                        "BA",
                        "ABB",
                        "BB",
                        "BAB",
                        "BAT",
                        "BATAT",
                        "ATAT",
                        "TAT",
                    }
                ),
                "B": frozenset({"A", "TA", "AB", "B", "BA"}),
                "T": frozenset({"A", "AT", "T", "BA", "TA", "BAT", "BATA", "ATA"}),
            }
        )

        self.assertDictEqual(dict(infix_info.can_add_at_end), exp_can_add_at_end)

        exp_infix_to_prefixes = {
            "A": frozenset({"A", "T", "B"}),
            "B": frozenset({"A", "B"}),
            "T": frozenset({"A", "T"}),
            "AA": frozenset({"B"}),
            "AB": frozenset({"T", "B"}),
            "AT": frozenset({"B", "T"}),
            "BA": frozenset({"A", "B"}),
            "BB": frozenset({"A"}),
            "TA": frozenset({"A"}),
            "TT": frozenset({"A"}),
            "ABA": frozenset({"B"}),
            "ATA": frozenset({"B", "T"}),
            "ATT": frozenset({"B"}),
            "BBA": frozenset({"A"}),
            "TAT": frozenset({"A"}),
            "ATAT": frozenset({"B"}),
            "TATA": frozenset({"A"}),
            "ATATA": frozenset({"B"}),
        }
        self.assertDictEqual(dict(infix_info.infix_to_prefixes), exp_infix_to_prefixes)

        exp_infix_to_suffixes = {
            "A": frozenset({"A", "B", "T"}),
            "B": frozenset({"A", "B"}),
            "T": frozenset({"A", "T"}),
            "AB": frozenset({"A", "B"}),
            "AT": frozenset({"A", "T"}),
            "BA": frozenset({"A", "B", "T"}),
            "BB": frozenset({"A"}),
            "TA": frozenset({"B", "T"}),
            "ABB": frozenset({"A"}),
            "BAB": frozenset({"A"}),
            "BAT": frozenset({"A", "T"}),
            "ATA": frozenset({"T"}),
            "TAT": frozenset({"A"}),
            "BATA": frozenset({"T"}),
            "ATAT": frozenset({"A"}),
            "BATAT": frozenset({"A"}),
        }
        self.assertDictEqual(dict(infix_info.infix_to_suffixes), exp_infix_to_suffixes)

    def test_get_all_vertical_straight_moves_1(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)

        # Give the player a single B.
        b = LetterTile("B", points=1)
        state.player_to_state[self.p0].tiles = [b]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            PlaceTilesMove(position_to_placing={(7, 6): LetterTilePlacing(tile=b)}),
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=b)}),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_2(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)

        # Give the player a B and an A.
        a = LetterTile("A", points=1)
        b = LetterTile("B", points=1)
        state.player_to_state[self.p0].tiles = [a, b]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            #
            # BA
            PlaceTilesMove(position_to_placing={(7, 6): LetterTilePlacing(tile=b)}),
            #
            # AB
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=b)}),
            #
            # AA
            PlaceTilesMove(position_to_placing={(7, 6): LetterTilePlacing(tile=a)}),
            #
            # AA
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=a)}),
            #
            # BAA
            PlaceTilesMove(
                position_to_placing={
                    (7, 5): LetterTilePlacing(tile=b),
                    (7, 6): LetterTilePlacing(tile=a),
                }
            ),
            #
            # BAA
            PlaceTilesMove(
                position_to_placing={
                    (7, 6): LetterTilePlacing(tile=b),
                    (7, 8): LetterTilePlacing(tile=a),
                }
            ),
            #
            # ABA
            PlaceTilesMove(
                position_to_placing={
                    (7, 5): LetterTilePlacing(tile=a),
                    (7, 6): LetterTilePlacing(tile=b),
                }
            ),
            #
            # ABA
            PlaceTilesMove(
                position_to_placing={
                    (7, 8): LetterTilePlacing(tile=b),
                    (7, 9): LetterTilePlacing(tile=a),
                }
            ),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_3(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[6, 6] = LetterTile("B", points=1)
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)

        # Give the player a single B.
        b = LetterTile("B", points=1)
        state.player_to_state[self.p0].tiles = [b]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=b)}),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_4(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[6, 6] = LetterTile("B", points=1)
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)

        # Give the player a single A.
        a = LetterTile("A", points=1)
        state.player_to_state[self.p0].tiles = [a]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            PlaceTilesMove(position_to_placing={(7, 6): LetterTilePlacing(tile=a)}),
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=a)}),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_5(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[6, 6] = LetterTile("B", points=1)
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)

        # Give the player an A and a B.
        a = LetterTile("A", points=1)
        b = LetterTile("B", points=1)
        state.player_to_state[self.p0].tiles = [a, b]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            #
            # BA, AA
            PlaceTilesMove(position_to_placing={(7, 6): LetterTilePlacing(tile=a)}),
            #
            # AA
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=a)}),
            #
            # AB
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=b)}),
            # BAA, BA
            PlaceTilesMove(
                position_to_placing={
                    (7, 5): LetterTilePlacing(tile=b),
                    (7, 6): LetterTilePlacing(tile=a),
                }
            ),
            #
            # ABA
            PlaceTilesMove(
                position_to_placing={
                    (7, 8): LetterTilePlacing(tile=b),
                    (7, 9): LetterTilePlacing(tile=a),
                }
            ),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_6(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)
        state.board.position_to_tile[6, 8] = LetterTile("B", points=1)

        # Give the player a single B.
        b = LetterTile("B", points=1)
        state.player_to_state[self.p0].tiles = [b]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            PlaceTilesMove(position_to_placing={(7, 6): LetterTilePlacing(tile=b)}),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_7(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)
        state.board.position_to_tile[6, 8] = LetterTile("B", points=1)

        # Give the player an A and a B.
        a = LetterTile("A", points=1)
        b = LetterTile("B", points=1)
        state.player_to_state[self.p0].tiles = [a, b]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            # BA
            PlaceTilesMove(position_to_placing={(7, 6): LetterTilePlacing(tile=b)}),
            #
            # AA
            PlaceTilesMove(position_to_placing={(7, 6): LetterTilePlacing(tile=a)}),
            #
            # AA, BA
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=a)}),
            #
            # BAA, BA
            PlaceTilesMove(
                position_to_placing={
                    (7, 6): LetterTilePlacing(tile=b),
                    (7, 8): LetterTilePlacing(tile=a),
                }
            ),
            #
            # ABA
            PlaceTilesMove(
                position_to_placing={
                    (7, 5): LetterTilePlacing(tile=a),
                    (7, 6): LetterTilePlacing(tile=b),
                }
            ),
            #
            # BAA
            PlaceTilesMove(
                position_to_placing={
                    (7, 5): LetterTilePlacing(tile=b),
                    (7, 6): LetterTilePlacing(tile=a),
                }
            ),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_8(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[7, 6] = LetterTile("B", points=1)
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)

        # Give the player a single A.
        a = LetterTile("A", points=1)
        state.player_to_state[self.p0].tiles = [a]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            PlaceTilesMove(position_to_placing={(7, 5): LetterTilePlacing(tile=a)}),
            PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=a)}),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_9(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[7, 7] = LetterTile("A", points=1)
        state.board.position_to_tile[7, 8] = LetterTile("B", points=1)

        # Give the player a single A.
        a = LetterTile("A", points=1)
        state.player_to_state[self.p0].tiles = [a]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 7)
        )

        exp_moves = [
            PlaceTilesMove(position_to_placing={(7, 9): LetterTilePlacing(tile=a)}),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_10(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[7, 0] = LetterTile("A", points=1)

        # Give the player a single B.
        b = LetterTile("B", points=1)
        state.player_to_state[self.p0].tiles = [b]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 0)
        )

        exp_moves = [
            PlaceTilesMove(position_to_placing={(7, 1): LetterTilePlacing(tile=b)}),
            # PlaceTilesMove(position_to_placing={(7, 8): LetterTilePlacing(tile=b)}),
        ]
        self.assertCountEqual(moves, exp_moves)

    def test_get_all_vertical_straight_moves_11(self):
        state = self.empty_state.copy()
        state.board.position_to_tile[7, 14] = LetterTile("A", points=1)

        # Give the player a single B.
        b = LetterTile("B", points=1)
        state.player_to_state[self.p0].tiles = [b]

        # Get the playable letter info.
        playable_letter_info = PlayableLetterInfo(
            board=state.board,
            words=state.config.playable_words,
            infix_info=self.moves_finder.infix_data,
        )
        moves = self.moves_finder._get_all_vertical_straight_moves(
            state=state, playable_letter_info=playable_letter_info, pos=(7, 14)
        )

        exp_moves = [
            PlaceTilesMove(position_to_placing={(7, 13): LetterTilePlacing(tile=b)}),
        ]
        self.assertCountEqual(moves, exp_moves)


if __name__ == "__main__":  #
    unittest.main()

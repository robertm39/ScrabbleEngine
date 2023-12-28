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
                "       T   \n"
            )
        )
        words = [
            get_word_on_board_from_string(tile_string=("GROUND     ")),
            get_word_on_board_from_string(tile_string=("       OVER")),
            get_word_on_board_from_string(tile_string=("           \n" "OE         ")),
            get_word_on_board_from_string(tile_string=("           \n" "   PE      ")),
            get_word_on_board_from_string(
                tile_string=("           \n" "           \n" "       JO  ")
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n" "           \n" "           \n" " SINK      "
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n"
                    "           \n"
                    "           \n"
                    "           \n"
                    "    ABACA  "
                )
            ),
            get_word_on_board_from_string(
                tile_string=("G          \n" "O          \n")
            ),
            get_word_on_board_from_string(
                tile_string=(
                    " R         \n" " E         \n" " D         \n" " S         \n"
                )
            ),
            get_word_on_board_from_string(
                tile_string=("   U       \n" "   P       \n")
            ),
            get_word_on_board_from_string(
                tile_string=("    N      \n" "    E      \n")
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "           \n"
                    "           \n"
                    "           \n"
                    "    K      \n"
                    "    A      \n"
                )
            ),
            get_word_on_board_from_string(
                tile_string=(
                    "       O   \n"
                    "       B   \n"
                    "       J   \n"
                    "       E   \n"
                    "       C   \n"
                    "       T   \n"
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
        self.assertEqual(next_state, exp_next_state)

    def test_pass_move_perform_2(self):
        move = PassMove()
        state = self.empty_state.copy()

        state.current_player = self.p1

        next_state = state.copy()
        move.perform(next_state)

        exp_next_state = state.copy()
        exp_next_state.current_player = self.p0
        self.assertEqual(next_state, exp_next_state)

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
        exp_state.current_player = self.p1

        self.assertEqual(exp_state, state)

    def test_exchange_tiles_move_perform_2(self):
        state = self.empty_state.copy()
        letters = "ABCDEFG"
        state.bag.tiles = [LetterTile(l) for l in letters] # type: ignore

        p0_state = state.player_to_state[self.p0]
        p0_state.tiles.append(LetterTile("O"))
        move = ExchangeTilesMove(tiles=[LetterTile("O")])
        move.perform(state)

        self.assertIn(LetterTile("O"), state.bag.tiles)
        self.assertNotIn(LetterTile("O"), p0_state.tiles)
        self.assertEqual(len(p0_state.tiles), 1)
        self.assertIn(p0_state.tiles[0].letter, letters) # type: ignore


#     def test_get_words_made_1(self):
#         board_state = BoardState(position_to_tile=dict())
#         q_tile = LetterTile(letter="Q", points=10)
#         i_tile = LetterTile(letter="I", points=1)
#         x7_y7 = BoardPosition(x=7, y=7)
#         x8_y7 = BoardPosition(x=8, y=7)
#         move = PlaceTilesMove(
#             tile_placings=[
#                 LetterTilePlacing(tile=q_tile, position=x7_y7),
#                 LetterTilePlacing(tile=i_tile, position=x8_y7),
#             ]
#         )
#         word = WordOnBoard(
#             position_to_tile={
#                 x7_y7: LetterTilePlacing(tile=q_tile, position=x7_y7),
#                 x8_y7: LetterTilePlacing(tile=i_tile, position=x8_y7),
#             }
#         )
#         self.assertEqual(word.get_word(), "QI")
#         self.assertCountEqual([word], move.get_words_made(board_state=board_state))

#     def test_get_words_made_2(self):
#         a1 = LetterTile(letter="A", points=1)
#         a2 = LetterTile(letter="A", points=1)
#         b = LetterTile(letter="B", points=2)
#         x3_y3 = BoardPosition(x=3, y=3)
#         x4_y3 = BoardPosition(x=4, y=3)
#         x4_y2 = BoardPosition(x=4, y=2)
#         position_to_tile = {
#             x3_y3: LetterTilePlacing(tile=a1, position=x3_y3),
#             x4_y3: LetterTilePlacing(tile=a2, position=x4_y3),
#         }
#         new_word = WordOnBoard(
#             position_to_tile={
#                 x4_y2: LetterTilePlacing(tile=b, position=x4_y2),
#                 x4_y3: LetterTilePlacing(tile=a2, position=x4_y3),
#             }
#         )
#         self.assertEqual(new_word.get_word(), "BA")
#         move = PlaceTilesMove(tile_placings=[LetterTilePlacing(tile=b, position=x4_y2)])
#         board_state = BoardState(position_to_tile=position_to_tile)
#         self.assertCountEqual([new_word], move.get_words_made(board_state=board_state))

#     def test_get_points_scored_1(self):
#         x0_y0 = BoardPosition(x=0, y=0)
#         x1_y0 = BoardPosition(x=1, y=0)
#         k = LetterTile(letter="K", points=5)
#         k_place = LetterTilePlacing(tile=k, position=x0_y0)
#         a = LetterTile(letter="A", points=1)
#         a_place = LetterTilePlacing(tile=a, position=x1_y0)
#         t = LetterTile(letter="T", points=1)
#         placings = [k_place, a_place]
#         position_to_tile = {x0_y0: k_place, x1_y0: a_place}
#         word = WordOnBoard(position_to_tile=position_to_tile)
#         board_state = BoardState(position_to_tile=dict())

#         pairs = (
#             (dict(), 6),
#             ({x0_y0: TileMultiplier(2)}, 11),
#             ({x0_y0: TileMultiplier(3)}, 16),
#             ({x1_y0: TileMultiplier(2)}, 7),
#             ({x1_y0: TileMultiplier(3)}, 8),
#             ({x0_y0: WordMultiplier(2)}, 12),
#             ({x0_y0: WordMultiplier(3)}, 18),
#             ({x1_y0: WordMultiplier(2)}, 12),
#             ({x1_y0: WordMultiplier(3)}, 18),
#             ({x0_y0: TileMultiplier(3), x1_y0: WordMultiplier(3)}, 48),
#             ({x0_y0: TileMultiplier(3), x1_y0: WordMultiplier(2)}, 32),
#         )
#         for position_to_multiplier, exp_points in pairs:
#             config = ScrabbleConfig(
#                 board_config=BoardConfig(
#                     width=2, height=2, position_to_multiplier=position_to_multiplier
#                 ),
#                 playable_words=["KA"],
#                 tiles=[k, a],
#                 max_tiles_in_hand=2,
#                 min_tiles_for_bingo=7,
#                 bingo_points=50,
#             )
#             player = Player(position=0)
#             state = GameState(
#                 config=config,
#                 current_player=player,
#                 player_to_state={
#                     player: PlayerState(player=player, score=0, tiles=[k, a])
#                 },
#                 player_order=(player,),
#                 bag_state=TileBagState(tiles=[t]),
#                 board_state=board_state,
#                 game_finished=False,
#             )

#             move = PlaceTilesMove(tile_placings=placings)
#             points_scored = move.get_points_for_word(state=state, word=word)
#             self.assertEqual(points_scored, exp_points)


if __name__ == "__main__":  #
    unittest.main()

import unittest

from game_state import *
from rules import *


class StateTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_words_1(self):
        board_state = BoardState(position_to_tile=dict())
        self.assertListEqual(list(), board_state.get_words())

    def test_get_words_2(self):
        x0_y0 = BoardPosition(x=0, y=0)
        x1_y0 = BoardPosition(x=1, y=0)
        position_to_tile = {
            x0_y0: LetterTilePlacing(
                tile=LetterTile(letter="A", points=1), position=x0_y0
            ),
            x1_y0: LetterTilePlacing(
                tile=LetterTile(letter="A", points=1), position=x1_y0
            ),
        }
        word = WordOnBoard(position_to_tile=position_to_tile)
        self.assertEqual(word.get_word(), "AA")
        board_state = BoardState(position_to_tile=position_to_tile)
        self.assertCountEqual([word], board_state.get_words())

    def test_get_words_3(self):
        x0_y1 = BoardPosition(x=0, y=1)
        x1_y1 = BoardPosition(x=1, y=1)
        x1_y0 = BoardPosition(x=1, y=0)

        a_1 = LetterTile(letter="A", points=1)
        a_2 = LetterTile(letter="A", points=1)
        b = LetterTile(letter="B", points=1)

        position_to_tile = {
            x0_y1: LetterTilePlacing(tile=a_1, position=x0_y1),
            x1_y1: LetterTilePlacing(tile=a_2, position=x1_y1),
            x1_y0: LetterTilePlacing(tile=b, position=x1_y0),
        }
        w1_position_to_tile = {
            x0_y1: LetterTilePlacing(tile=a_1, position=x0_y1),
            x1_y1: LetterTilePlacing(tile=a_2, position=x1_y1),
        }
        w2_position_to_tile = {
            x1_y0: LetterTilePlacing(tile=b, position=x1_y0),
            x1_y1: LetterTilePlacing(tile=a_2, position=x1_y1),
        }
        word_1 = WordOnBoard(position_to_tile=w1_position_to_tile)
        word_2 = WordOnBoard(position_to_tile=w2_position_to_tile)
        self.assertEqual(word_1.get_word(), "AA")
        self.assertEqual(word_2.get_word(), "BA")
        board_state = BoardState(position_to_tile=position_to_tile)
        self.assertCountEqual([word_1, word_2], board_state.get_words())

    def test_get_words_4(self):
        x0_y0 = BoardPosition(x=0, y=0)
        x1_y0 = BoardPosition(x=1, y=0)
        x0_y1 = BoardPosition(x=0, y=1)
        x1_y1 = BoardPosition(x=1, y=1)
        a1 = LetterTile(letter="A", points=1)
        a2 = LetterTile(letter="A", points=1)
        a3 = LetterTile(letter="A", points=1)
        a4 = LetterTile(letter="A", points=1)
        position_to_tile = {
            x0_y0: LetterTilePlacing(tile=a1, position=x0_y0),
            x1_y0: LetterTilePlacing(tile=a2, position=x1_y0),
            x0_y1: LetterTilePlacing(tile=a3, position=x0_y1),
            x1_y1: LetterTilePlacing(tile=a4, position=x1_y1),
        }
        w1_position_to_tile = {
            x0_y0: LetterTilePlacing(tile=a1, position=x0_y0),
            x1_y0: LetterTilePlacing(tile=a2, position=x1_y0),
        }
        w2_position_to_tile = {
            x0_y1: LetterTilePlacing(tile=a3, position=x0_y1),
            x1_y1: LetterTilePlacing(tile=a4, position=x1_y1),
        }
        w3_position_to_tile = {
            x0_y0: LetterTilePlacing(tile=a1, position=x0_y0),
            x0_y1: LetterTilePlacing(tile=a3, position=x0_y1),
        }
        w4_position_to_tile = {
            x1_y0: LetterTilePlacing(tile=a2, position=x1_y0),
            x1_y1: LetterTilePlacing(tile=a4, position=x1_y1),
        }
        word_1 = WordOnBoard(w1_position_to_tile)
        word_2 = WordOnBoard(w2_position_to_tile)
        word_3 = WordOnBoard(w3_position_to_tile)
        word_4 = WordOnBoard(w4_position_to_tile)
        words = [word_1, word_2, word_3, word_4]
        for w in words:
            self.assertEqual(w.get_word(), "AA")
        board_state = BoardState(position_to_tile)
        self.assertCountEqual(words, board_state.get_words())


class RulesTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_words_made_1(self):
        board_state = BoardState(position_to_tile=dict())
        q_tile = LetterTile(letter="Q", points=10)
        i_tile = LetterTile(letter="I", points=1)
        x7_y7 = BoardPosition(x=7, y=7)
        x8_y7 = BoardPosition(x=8, y=7)
        move = PlaceTilesMove(
            tile_placings=[
                LetterTilePlacing(tile=q_tile, position=x7_y7),
                LetterTilePlacing(tile=i_tile, position=x8_y7),
            ]
        )
        word = WordOnBoard(
            position_to_tile={
                x7_y7: LetterTilePlacing(tile=q_tile, position=x7_y7),
                x8_y7: LetterTilePlacing(tile=i_tile, position=x8_y7),
            }
        )
        self.assertEqual(word.get_word(), "QI")
        self.assertCountEqual([word], move.get_words_made(board_state=board_state))

    def test_get_words_made_2(self):
        a1 = LetterTile(letter="A", points=1)
        a2 = LetterTile(letter="A", points=1)
        b = LetterTile(letter="B", points=2)
        x3_y3 = BoardPosition(x=3, y=3)
        x4_y3 = BoardPosition(x=4, y=3)
        x4_y2 = BoardPosition(x=4, y=2)
        position_to_tile = {
            x3_y3: LetterTilePlacing(tile=a1, position=x3_y3),
            x4_y3: LetterTilePlacing(tile=a2, position=x4_y3),
        }
        new_word = WordOnBoard(
            position_to_tile={
                x4_y2: LetterTilePlacing(tile=b, position=x4_y2),
                x4_y3: LetterTilePlacing(tile=a2, position=x4_y3),
            }
        )
        self.assertEqual(new_word.get_word(), "BA")
        move = PlaceTilesMove(tile_placings=[LetterTilePlacing(tile=b, position=x4_y2)])
        board_state = BoardState(position_to_tile=position_to_tile)
        self.assertCountEqual([new_word], move.get_words_made(board_state=board_state))


if __name__ == "__main__":
    unittest.main()

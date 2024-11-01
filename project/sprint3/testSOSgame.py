import unittest
from SOSgame import SOSgame

class TestSOSgame(unittest.TestCase):
    def setUp(self):
        # setup for each test
        self.simple_game = SOSgame(board_size = 3, game_mode = "Simple")
        self.general_game = SOSgame(board_size = 3, game_mode = "General")

    def test_initialization(self):
        # test initial game setup
        self.assertEqual(len(self.simple_game.board), 3)
        self.assertEqual(self.simple_game.game_mode, "Simple")
        self.assertEqual(self.simple_game.player1score, 0)
        self.assertEqual(self.simple_game.player2score, 0)
        self.assertFalse(self.simple_game.is_game_over())

    def test_simple_mode_win(self):
        # set moves to create an "SOS" in simple mode and check if the game is over
        self.simple_game.set_move(0, 0, 'S')
        self.simple_game.set_move(0, 1, 'O')
        self.simple_game.set_move(0, 2, 'S')  # this should trigger a win

        self.assertTrue(self.simple_game.is_game_over())
        self.assertEqual(self.simple_game.get_winner(), "Player 1")
        self.assertEqual(self.simple_game.player1score, 1)

    def test_simple_mode_no_win(self):
        # test that no winner is declared if no "SOS" exists
        self.simple_game.set_move(0, 0, 'S')
        self.simple_game.set_move(0, 1, 'S')
        self.simple_game.set_move(0, 2, 'O')

        self.assertFalse(self.simple_game.is_game_over())
        self.assertIsNone(self.simple_game.get_winner())

    def test_general_mode_scoring(self):
        # create multiple "SOS" sequences in general mode and check scores
        self.general_game.set_move(0, 0, 'S')
        self.general_game.set_move(0, 1, 'O')
        self.general_game.set_move(0, 2, 'S')  # SOS formed for Player 1
        self.general_game.switch_player()

        self.general_game.set_move(1, 0, 'S')
        self.general_game.set_move(1, 1, 'O')
        self.general_game.set_move(1, 2, 'S')  # SOS formed for Player 2
        self.general_game.switch_player()

        self.assertEqual(self.general_game.player1score, 1)
        self.assertEqual(self.general_game.player2score, 1)

    def test_general_mode_end(self):
        # test if the game ends when the board is full in general mode
        moves = [
            (0, 0, 'S'), (0, 1, 'O'), (0, 2, 'S'),
            (1, 0, 'O'), (1, 1, 'S'), (1, 2, 'O'),
            (2, 0, 'S'), (2, 1, 'O'), (2, 2, 'S')
        ]
        for row, col, value in moves:
            self.general_game.set_move(row, col, value)

        self.assertTrue(self.general_game.is_game_over())
        # test for a draw if scores are equal or check for the correct winner
        if self.general_game.player1score == self.general_game.player2score:
            self.assertEqual(self.general_game.get_winner(), "Draw")
        else:
            expected_winner = "Player 1" if self.general_game.player1score > self.general_game.player2score else "Player 2"
            self.assertEqual(self.general_game.get_winner(), expected_winner)

    def test_player_switching(self):
        # test that players switch correctly after each move
        initial_player = self.simple_game.current_player
        self.simple_game.set_move(0, 0, 'S')
        self.simple_game.switch_player()
        self.assertNotEqual(self.simple_game.current_player, initial_player)

if __name__ == "__main__":
    unittest.main()

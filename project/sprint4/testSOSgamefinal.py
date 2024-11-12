import unittest
from SOSgamefinal import SimpleSOSGame, GeneralSOSGame, ComputerPlayer

class TestComputerOpponent(unittest.TestCase):

    def setUp(self):
        # setting up the game instances for testing
        self.simple_game = SimpleSOSGame(board_size=3)
        self.general_game = GeneralSOSGame(board_size=3)
        self.simple_game.player1 = ComputerPlayer()
        self.simple_game.player2 = ComputerPlayer()
        self.general_game.player1 = ComputerPlayer()
        self.general_game.player2 = ComputerPlayer()

    def test_computer_move_simple(self):
        # test that the computer makes a move in the simple game
        self.simple_game.current_player = "Player 1"
        self.simple_game.player1.make_move(self.simple_game)

        # verify that a move was made by checking if any cell is filled
        move_made = any(cell != '' for row in self.simple_game.board for cell in row)
        self.assertTrue(move_made)

        # additional check to ensure the move is valid
        for row in range(self.simple_game.board_size):
            for col in range(self.simple_game.board_size):
                if self.simple_game.board[row][col] != '':
                    self.assertIn(self.simple_game.board[row][col], ['S', 'O'])

    def test_computer_moves_alternate_symbols(self):
        # test that the computer alternates between 'S' and 'O' symbols
        comp_player = ComputerPlayer()
        symbols = []
        for _ in range(4):
            comp_player.make_move(self.general_game)
            for row in self.general_game.board:
                for cell in row:
                    if cell != '':
                        symbols.append(cell)
                        break
                if symbols:
                    break

        self.assertGreaterEqual(len(symbols), 1)  # ensure at least one move was made
        # ensure both 'S' and 'O' are in the moves (since moves alternate)
        self.assertIn('S', symbols)
        self.assertIn('O', symbols)

    def test_computer_move_general(self):
        # test computer moves in general game mode
        self.general_game.current_player = "Player 1"
        self.general_game.player1.make_move(self.general_game)

        # verify that a move was made
        move_made = any(cell != '' for row in self.general_game.board for cell in row)
        self.assertTrue(move_made)

        # verify that the move is valid (within board bounds)
        for row in range(self.general_game.board_size):
            for col in range(self.general_game.board_size):
                if self.general_game.board[row][col] != '':
                    self.assertIn(self.general_game.board[row][col], ['S', 'O'])

    def test_computer_scoring(self):
        # test that the computer can score in general mode
        self.general_game.set_move(0, 0, 'S')
        self.general_game.set_move(0, 1, 'O')
        self.general_game.set_move(0, 2, 'S')
        self.assertEqual(self.general_game.player1score, 1)  # ensure the scoring logic works

if __name__ == '__main__':
    unittest.main()

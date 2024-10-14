import unittest
from SOSgame import SOSgame

class testSOSGame(unittest.TestCase):

    def setUp(self):
        # set up a default version of the game
        self.game = SOSgame()
    
    def test_set_move(self):
        # test that placing an 'S' in an empty cell is successful
        move_success = self.game.set_move(0, 0, 'S')
        self.assertTrue(move_success)
        self.assertEqual(self.game.board[0][0], 'S')

        # test that placing another 'O' in the same cell fails
        move_fail = self.game.set_move(0, 0, 'O')
        self.assertFalse(move_fail)
        self.assertEqual(self.game.board[0][0], 'S')  # the board shouldn't change

    def test_switch_player(self):
        # test that player switches after a valid move
        self.assertEqual(self.game.current_player, "Player 1")  # initial player

        self.game.switch_player()
        self.assertEqual(self.game.current_player, "Player 2")  # after first switch

        self.game.switch_player()
        self.assertEqual(self.game.current_player, "Player 1")  # after second switch, back to Player 1

    def test_reset_game(self):
        # test that game will reset itself to default values when prompted to
        game = SOSgame(3)
        game.set_move(0, 0, 'S')
        game.reset_game()
        self.assertEqual(game.board[0][0], '')
        self.assertEqual(game.current_player, "Player 1")

if __name__ == '__main__':
    unittest.main()

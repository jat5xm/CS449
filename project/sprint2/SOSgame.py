class SOSgame:
    def __init__(self, board_size = 3, game_mode = "Simple"):
        self.board_size = board_size
        self.game_mode = game_mode
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "Player 1"
    
    def set_move(self, row, col, value):
        # place a 'S' or 'O' on any available cell
        if self.board[row][col] == '':
            self.board[row][col] = value
            return True
        return False

    def switch_player(self):
        # switch the current player after a move
        if self.current_player == "Player 1":
            self.current_player = "Player 2"
        else:
            self.current_player = "Player 1"
    
    def get_board(self):
        # return the current game board
        return self.board

    def reset_game(self):
        # reset the game board and player turn
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "Player 1"

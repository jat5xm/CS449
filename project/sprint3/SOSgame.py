class SOSgame:
    def __init__(self, board_size = 3, game_mode = "Simple"):
        self.board_size = board_size
        self.game_mode = game_mode
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "Player 1"
        self.player1score = 0
        self.player2score = 0
        self.game_over = False

    def set_move(self, row, col, value):
        # place a 'S' or 'O' on an available cell if allowed
        if self.board[row][col] == '':
            self.board[row][col] = value
            self.checkSOS(row, col)
            return True
        return False

    def switch_player(self):
        # switch current player after a move
        if self.current_player == "Player 1":
            self.current_player = "Player 2"
        else:
            self.current_player = "Player 1"

    def reset_game(self):
        # reset the game board and player scores starting with Player 1
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "Player 1"
        self.player1score = 0
        self.player2score = 0
        self.game_over = False

    def get_board(self):
        # return the current game board
        return self.board

    def checkSOS(self, row, col):
        # check for SOS sequence in row, column, and diagonal directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            try:
                if (
                    0 <= row + dr < self.board_size and 0 <= row + 2*dr < self.board_size
                    and 0 <= col + dc < self.board_size and 0 <= col + 2*dc < self.board_size
                ):
                    if (
                        self.board[row][col] == 'S'
                        and self.board[row + dr][col + dc] == 'O'
                        and self.board[row + 2*dr][col + 2*dc] == 'S'
                    ):
                        self.update_score()
                        if self.game_mode == "Simple":
                            self.game_over = True
                            return
            except IndexError:
                continue

        # check if the board is full to determine if the game is over in general mode
        if all(cell != '' for row in self.board for cell in row):
            self.game_over = True

    def update_score(self):
        # update score based on the current player
        if self.current_player == "Player 1":
            self.player1score += 1
        else:
            self.player2score += 1

    def is_game_over(self):
        # return if the game is over
        return self.game_over

    def get_winner(self):
        # determine the winner based on the game mode and scores
        if self.game_mode == "Simple":
            return self.current_player if self.game_over else None
        elif self.game_mode == "General":
            if self.player1score > self.player2score:
                return "Player 1"
            elif self.player2score > self.player1score:
                return "Player 2"
            else:
                return "Draw"
            

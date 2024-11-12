from abc import ABC, abstractmethod
import random

class Player(ABC):
    @abstractmethod
    def make_move(self, game):
        pass

class HumanPlayer(Player):
    def make_move(self, game):
        pass  # move logic will be handled by user input in the UI

class ComputerPlayer(Player):
    def __init__(self):
        self.previous_symbol = None

    def make_move(self, game):
        valid_moves = [(r, c) for r in range(game.board_size) for c in range(game.board_size) if game.board[r][c] == '']
        if valid_moves:
            # randomly choose a valid move
            move = random.choice(valid_moves)

            # ensure the computer alternates between 'S' and 'O' when possible
            symbol = random.choice(['S', 'O'])
            if self.previous_symbol:
                # Alternate if possible
                symbol = 'S' if self.previous_symbol == 'O' else 'O'

            # make the move
            game.set_move(move[0], move[1], symbol)
            self.previous_symbol = symbol

# original BaseSOSGame and its derived classes
class BaseSOSGame(ABC):
    def __init__(self, board_size = 3):
        self.board_size = board_size
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "Player 1"
        self.player1 = None
        self.player2 = None
        self.player1score = 0
        self.player2score = 0
        self.game_over = False

    def set_move(self, row, col, value):
        if self.board[row][col] == '':
            self.board[row][col] = value
            self.check_sos(row, col)
            return True
        return False

    def switch_player(self):
        self.current_player = "Player 1" if self.current_player == "Player 2" else "Player 2"

    def reset_game(self):
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "Player 1"
        self.player1score = 0
        self.player2score = 0
        self.game_over = False

    def get_board(self):
        return self.board

    def is_game_over(self):
        return self.game_over

    def update_score(self):
        if self.current_player == "Player 1":
            self.player1score += 1
        else:
            self.player2score += 1

class SimpleSOSGame(BaseSOSGame):
    def check_sos(self, row, col):
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
                        self.game_over = True
                        return
            except IndexError:
                continue

    def get_winner(self):
        return self.current_player if self.game_over else None

class GeneralSOSGame(BaseSOSGame):
    def check_sos(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        sos_found = False
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
                        sos_found = True
            except IndexError:
                continue
        
        if all(cell != '' for row in self.board for cell in row):
            self.game_over = True

    def get_winner(self):
        if not self.game_over:
            return None
        if self.player1score > self.player2score:
            return "Player 1"
        elif self.player2score > self.player1score:
            return "Player 2"
        else:
            return "Draw"
          

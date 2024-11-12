import tkinter as tk
import time
from tkinter import messagebox
from SOSgamefinal import BaseSOSGame, SimpleSOSGame, GeneralSOSGame, HumanPlayer, ComputerPlayer  # type: ignore

class SOSGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        
        # initialize the start menu
        self.create_start_menu()
    
    def create_start_menu(self):
        # start menu frame
        self.start_menu = tk.Frame(self.root)
        self.start_menu.pack()

        # left side layout for options
        options_frame = tk.Frame(self.start_menu)
        options_frame.pack(side = "left", padx = 10, pady = 10)

        # game mode selection
        self.mode_var = tk.StringVar(value = "Simple")
        tk.Label(options_frame, text = "Select game mode:").pack()
        tk.Radiobutton(options_frame, text = "Simple", variable = self.mode_var, value = "Simple").pack()
        tk.Radiobutton(options_frame, text = "General", variable = self.mode_var, value = "General").pack()

        # board size selection
        tk.Label(options_frame, text = "Select board size: ").pack()
        self.size_var = tk.IntVar(value = 3)
        size_menu = tk.OptionMenu(options_frame, self.size_var, 3, 4, 5, 6, 7, 8, command=self.update_preview)
        size_menu.pack()

        # player type selection
        tk.Label(options_frame, text = "Player 1 Type: ").pack()
        self.player1_type = tk.StringVar(value = "Human")
        tk.Radiobutton(options_frame, text = "Human", variable = self.player1_type, value = "Human").pack()
        tk.Radiobutton(options_frame, text = "Computer", variable = self.player1_type, value = "Computer").pack()

        tk.Label(options_frame, text="Player 2 Type: ").pack()
        self.player2_type = tk.StringVar(value = "Human")
        tk.Radiobutton(options_frame, text = "Human", variable = self.player2_type, value = "Human").pack()
        tk.Radiobutton(options_frame, text = "Computer", variable = self.player2_type, value = "Computer").pack()

        # start game button
        tk.Button(options_frame, text="START", command=self.start_game).pack()

        # right side preview frame
        self.preview_frame = tk.Frame(self.start_menu)
        self.preview_frame.pack(side="right", padx = 10, pady = 10)
        
        # initialize preview grid based on the initial size selection
        self.create_preview_grid()

    def create_preview_grid(self):
        # clear the current preview grid
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        # create a preview grid based on the selected board size
        board_size = self.size_var.get()
        for row in range(board_size):
            for col in range(board_size):
                label = tk.Label(self.preview_frame, text = "", width = 5, height = 2, relief = "solid")
                label.grid(row = row, column = col)

    def update_preview(self, *args):
        # update the preview grid when the board size changes
        self.create_preview_grid()

    def start_game(self):
        # initialize the actual game based on selected mode, size, and player types
        board_size = self.size_var.get()
        game_mode = self.mode_var.get()

        # initialize the game mode classes
        if game_mode == "Simple":
            self.game = SimpleSOSGame(board_size)
        else:
            self.game = GeneralSOSGame(board_size)

        # assign players
        self.game.player1 = HumanPlayer() if self.player1_type.get() == "Human" else ComputerPlayer()
        self.game.player2 = HumanPlayer() if self.player2_type.get() == "Human" else ComputerPlayer()

        # hide the start menu and display the game board
        self.start_menu.pack_forget()
        self.create_board()

    def create_board(self):
        # create the main game instance
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(padx = 20, pady = 20)

        # create the game board for placing moves
        self.buttons_frame = tk.Frame(self.game_frame)
        self.buttons_frame.pack(side = "left", padx = 10)

        self.buttons = [[None for _ in range(self.game.board_size)] for _ in range(self.game.board_size)]
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                button = tk.Button(self.buttons_frame, text = '', width = 5, height = 2,
                                   command = lambda r = row, c = col: self.make_move(r, c))
                button.grid(row=row, column = col)
                self.buttons[row][col] = button

        # player controls on the right side
        self.controls_frame = tk.Frame(self.game_frame)
        self.controls_frame.pack(side="right", padx = 10)

        self.choice_var = tk.StringVar(value="S")
        tk.Radiobutton(self.controls_frame, text = "S", variable = self.choice_var, value = "S").pack()
        tk.Radiobutton(self.controls_frame, text = "O", variable = self.choice_var, value = "O").pack()

        self.status_label = tk.Label(self.controls_frame, text = "Player 1's turn", fg="blue")
        self.status_label.pack()

        self.score_label = tk.Label(self.controls_frame, text = "Score - Player 1: 0 | Player 2: 0", fg="black")
        self.score_label.pack()

        # if the first player is a computer, make its move
        if isinstance(self.game.player1, ComputerPlayer):
            self.root.after(1000, self.make_computer_move)

    def make_move(self, row, col):
        # handle player move, apply color, and update the board and game state
        if not self.game.is_game_over():
            if isinstance(self.game.player1 if self.game.current_player == "Player 1" else self.game.player2, HumanPlayer):
                if self.game.set_move(row, col, self.choice_var.get()):
                    self.update_board(row, col)
                    self.check_game_status()
                    if not self.game.is_game_over():
                        self.game.switch_player()
                        self.update_status()
                        if isinstance(self.game.player1 if self.game.current_player == "Player 1" else self.game.player2, ComputerPlayer):
                            self.root.after(1000, self.make_computer_move)  # buffer for computer move
                else:
                    messagebox.showwarning("Invalid Move", "This cell is already occupied!")

    def make_computer_move(self):
        # let the computer make a move
        player = self.game.player1 if self.game.current_player == "Player 1" else self.game.player2
        player.make_move(self.game)
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if self.game.board[row][col] != self.buttons[row][col].cget('text'):
                    self.update_board(row, col)
        self.check_game_status()
        if not self.game.is_game_over():
            self.game.switch_player()
            self.update_status()

    def update_board(self, row, col):
        # update the board button display
        color = "blue" if self.game.current_player == "Player 1" else "red"
        self.buttons[row][col].config(text = self.game.board[row][col], fg = color)

    def update_status(self):
        # update status label and score label
        self.status_label.config(text = f"{self.game.current_player}'s turn",
                                 fg = "blue" if self.game.current_player == "Player 1" else "red")
        if isinstance(self.game, GeneralSOSGame):
            self.score_label.config(text = f"Score - Player 1: {self.game.player1score} | Player 2: {self.game.player2score}")

    def check_game_status(self):
        # check if the game is over and show the result
        if self.game.is_game_over():
            winner = self.game.get_winner()
            self.show_game_over(winner)

    def show_game_over(self, winner):
        # fisplay game over message with winner and restart option
        if winner == "Player 1":
            messagebox.showinfo("Game over!", f"{winner} wins!")
        elif winner == "Player 2":
            messagebox.showinfo("Game over!", f"{winner} wins!")
        else:
            messagebox.showinfo("Game over!", "It's a draw!")

        # ask if players want to start a new game
        if messagebox.askyesno("Game over!", "Would you like to start a new game?"):
            self.restart_game()
        else:
            self.root.destroy()

    def restart_game(self):
        # clear the current game board
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # reinitialize the start menu
        self.create_start_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = SOSGameUI(root)
    root.mainloop()
    

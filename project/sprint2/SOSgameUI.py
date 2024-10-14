import tkinter as tk
from tkinter import messagebox, simpledialog
from SOSgame import SOSgame

class SOSGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        
        # create an instance of the game logic
        self.game = SOSgame()

        # create the UI components (game options and board)
        self.create_game_options()
        self.create_board()

    def create_game_options(self):
        options_frame = tk.Frame(self.root)
        options_frame.pack(pady = 10)

        # board size selection
        tk.Label(options_frame, text = "Board size:").pack(side = tk.LEFT)
        self.board_size_var = tk.IntVar(value=3)  # default board size is 3, can only go up to 8
        tk.OptionMenu(options_frame, self.board_size_var, 3, 4, 5, 6, 7, 8).pack(side = tk.LEFT)

        # game mode selection (simple/general)
        tk.Label(options_frame, text = "Game mode:").pack(side = tk.LEFT)
        self.game_mode_var = tk.StringVar(value = "Simple")  # default game mode is Simple
        tk.OptionMenu(options_frame, self.game_mode_var, "Simple", "General").pack(side = tk.LEFT)

        # start game button
        tk.Button(options_frame, text = "Start game", command = self.start_game).pack(side = tk.LEFT)

    def create_board(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        # create buttons for the board cells
        self.buttons = []
        for i in range(self.game.board_size):
            row_buttons = []
            for j in range(self.game.board_size):
                button = tk.Button(self.board_frame, text = "", width = 5, height = 2,
                                   command = lambda i = i, j = j: self.on_click(i, j))
                button.grid(row = i, column = j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def start_game(self):
        board_size = self.board_size_var.get()  # get selected board size
        game_mode = self.game_mode_var.get()    # get selected game mode

        # update the game logic with new board size and mode
        self.game = SOSgame(board_size, game_mode)

        # clear the previous board and recreate buttons for the new board size
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.create_board()

    def on_click(self, row, col):
        current_player = self.game.current_player  # get the current player
        value = self.prompt_move_value(current_player)  # prompt player to choose 'S' or 'O'

        if value and self.game.set_move(row, col, value):
            # update the button text to display 'S' or 'O'
            self.buttons[row][col].config(text = value)
            self.game.switch_player()  # switch player after a valid move
        else:
            messagebox.showerror("Invalid move", "This cell is already occupied, try a different one!")  # show error if cell is taken

    def prompt_move_value(self, player):
        while True:
            value = simpledialog.askstring("Choose move", f"{player}: Choose 'S' or 'O'", parent = self.root)
            if value in ['S', 'O', 's', 'o']:  # only allow 'S' or 'O', case insensitive
                return value
            elif value is None:  # user canceled input
                return None
            else:
                messagebox.showerror("Invalid input", "Please choose either 'S' or 'O' to make a move")

# running the game
if __name__ == "__main__":
    root = tk.Tk()
    app = SOSGameUI(root)
    root.mainloop()

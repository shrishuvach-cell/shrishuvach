import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.resizable(False, False)
        
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = []
        
        self.create_board()
        
    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    self.window,
                    text="",
                    font=("Arial", 24),
                    width=5,
                    height=2,
                    command=lambda r=i, c=j: self.on_click(r, c)
                )
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
            
        self.reset_button = tk.Button(
            self.window,
            text="Reset Game",
            font=("Arial", 14),
            command=self.reset_game
        )
        self.reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")
        
    def on_click(self, row, col):
        if self.board[row][col] == "" and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a tie!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                
    def check_winner(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
                
        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
            
        return False
        
    def is_board_full(self):
        for row in self.board:
            if "" in row:
                return False
        return True
        
    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
                
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
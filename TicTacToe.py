import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player = "X"
        self.buttons = [[None]*3 for _ in range(3)]
        self.create_buttons()

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=('Arial', 40), width=5, height=2,
                                command=lambda row=i, col=j: self.on_button_click(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_button_click(self, row, col):
        btn = self.buttons[row][col]
        if btn["text"] == "":
            btn["text"] = self.player
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.player} wins!")
                self.reset_board()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
            else:
                self.player = "O" if self.player == "X" else "X"

    def check_winner(self):
        b = self.buttons
        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] != "":
                return True
            if b[0][i]["text"] == b[1][i]["text"] == b[2][i]["text"] != "":
                return True
        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] != "":
            return True
        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] != "":
            return True
        return False

    def is_board_full(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def reset_board(self):
        for row in self.buttons:
            for btn in row:
                btn["text"] = ""
        self.player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

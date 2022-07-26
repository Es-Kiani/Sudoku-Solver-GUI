# * Esfandiar-Kiani *
from typing import Any
from Module.Singleton import Singleton
# from Singleton import Singleton
from tkinter import *
from tkinter import Canvas, messagebox, ttk


class SudokuSolver(Singleton):
    def __init__(self, _puzzle: list = None) -> None:
        self._puzzle = _puzzle
        self.solvable = True
        self._row_Count = 9
        self._column_Count = 9
        self._valid_Numbers = list(range(1, 10))
        return

    def _next_Empty(self):
        for i in range(self._row_Count):
            for j in range(self._column_Count):
                if self._puzzle[i][j] == 0:
                    return i, j
        return None, None

    def _check_Valid(self, I: int, J: int, guessNum: int = None):
        row = self._puzzle[I]
        column = [self._puzzle[i][J] for i in range(self._row_Count)]
        square = []

        square_x = (I // 3) * 3
        square_y = (J // 3) * 3

        for i in range(square_x, square_x + 3):
            for j in range(square_y, square_y + 3):
                square.append(self._puzzle[i][j])

        neighbors = row + column + square

        if guessNum is None:
            guessNum = self._puzzle[I][J]

        if guessNum in neighbors:
            return False
        return True

    def _check_Solvable(self):
        for i in range(self._row_Count):
            for j in range(self._column_Count):
                if self._puzzle[i][j] != 0:
                    temp = self._puzzle[i][j]
                    self._puzzle[i][j] = 0
                    
                    if not self._check_Valid(i, j, temp):
                        self.solvable = False
                        return False
                    
                    self._puzzle[i][j] = temp
        return True

    def _start_Engine(self):
        row, col = self._next_Empty()

        # ? Last return
        if row is None:
            return True

        for guess in self._valid_Numbers:
            if self._check_Valid(row, col, guess):
                self._puzzle[row][col] = guess

                # ? Recursive (Backtracking) algorithm
                if SudokuSolver(self._puzzle)._start_Engine():
                    return True

            self._puzzle[row][col] = 0

        # ? Return False if guess is wrong
        return False

    def _writeTo_File(self, puzzle, fileName: str, filePath: str):
        if puzzle:
            self.__init__(puzzle)

        with open(f'{filePath}{fileName}.txt', 'a+') as file:
            file.write("\n")

            for i in range(self._row_Count):
                if i % 3 == 0:
                    file.write("\n")

                for j in range(self._column_Count):
                    if j % 3 == 0 and j != 0:
                        file.write("\t")
                    file.write(str(self._puzzle[i][j]))
                file.write("\n")

            file.write("\n")
            file.close()
        return

    def _solve(self, puzzle: list, writeToFile: bool = True, fileName: str = "Solved Sudoku", filePath: str = "./"):
        self.__init__(puzzle)

        if self._check_Solvable():
            self._start_Engine()
            if writeToFile:
                self._writeTo_File(self._puzzle, fileName, filePath)
            print(
                f"\nPuzzle Solved And Writhed To The «{filePath}{fileName}.txt».")
            return True, self._puzzle
        else:
            return False, self._puzzle


class GUISudokuSolver(Frame, SudokuSolver):
    def __init__(self) -> None:
        self._puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self._original_Puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self._is_Solved = False
        self.row, self.col = -1, -1
        self.margin, self.side = 15, 40
        self.width = self.height = self.margin * 2 + self.side * 9

    def _GUI_Builder(self) -> None:
        self._window = Tk()
        self._window.title("Sudoku Solver")
        self._window.resizable(False, False)

        Frame.__init__(self, self._window)

        self.canvas = Canvas(self._window, width=387, height=378)
        self.solveBtn = ttk.Button(
            self._window, text="Solve", cursor="hand2", command=self._solve)
        self.clearBtn = ttk.Button(
            self._window, text="Clear", cursor="hand2", command=self._clear)
        self._copyright = Label(
            self._window, text="©2021 Esfandiar Kiani, All rights reserved.")

        self.pack(fill=BOTH, expand="yes")
        self.canvas.pack(side=TOP, fill=BOTH)
        self.solveBtn.pack(side=LEFT, padx=("10", "0"),
                           pady=("0", "20"), expand="yes")
        self.clearBtn.pack(side=RIGHT, padx=("0", "10"),
                           pady=("0", "20"), expand="yes")
        self._copyright.pack(side=BOTTOM, pady=("60", "0"), expand="yes")

        self.canvas.bind("<Button-1>", self._cell_Clicked)
        self.canvas.bind("<Key>", self._key_Pressed)

        self._grid_Builder()

        self._window.mainloop()
        return

    def _grid_Builder(self) -> None:
        self.canvas.delete("numbers")
        self.canvas.delete("victory")
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0, y0 = self.margin + i * self.side, self.margin
            x1, y1 = self.margin + i * self.side, self.height - self.margin
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0, y0 = self.margin, self.margin + i * self.side
            x1, y1 = self.width - self.margin, self.margin + i * self.side
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

        tag = "numbers"
        for i in range(9):
            for j in range(9):
                text = str(self._puzzle[i][j])
                if text != '0':
                    color = "black" if text == str(
                        self._original_Puzzle[i][j]) else "seagreen"
                    x = self.margin + j * self.side + self.side / 2
                    y = self.margin + i * self.side + self.side / 2

                    self.canvas.create_text(
                        x, y, text=text, tags=tag, fill=color)

    def _cursor_Builder(self) -> None:
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = self.margin + self.col * self.side + 1
            y0 = self.margin + self.row * self.side + 1
            x1 = self.margin + (self.col + 1) * self.side - 1
            y1 = self.margin + (self.row + 1) * self.side - 1

            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="red", tags="cursor")
        return

    def _cell_Clicked(self, event) -> None:
        if self._is_Solved:
            return
        x, y = event.x, event.y
        if self.margin < x < self.width - self.margin and self.margin < y < self.height - self.margin:
            self.canvas.focus_set()

            row, col = (y-self.margin)/self.side, (x-self.margin)/self.side
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            else:
                self.row, self.col = int(row), int(col)
        else:
            self.row, self.col = -1, -1

        self._cursor_Builder()

    def _key_Pressed(self, event) -> None:
        if self._is_Solved:
            return
        if self.row >= 0 and self.col >= 0 and event.char in '0123456789':
            self._puzzle[self.row][self.col] = int(event.char)
            self._original_Puzzle[self.row][self.col] = int(event.char)
            self.row, self.col = -1, -1
            self._grid_Builder()
            self._cursor_Builder()
        return

    def _clear(self):
        yesORno = messagebox.askyesno(
            "Confirm", "Are You Sure You Want To Clear All The Table!?")
        if yesORno:
            self.__init__()
            self._grid_Builder()
        return

    def _solve(self) -> None:
        messagebox.showinfo(
            "Solving", "We Are Trying To Solve Your Puzzle If It's Possible...")

        is_Solved, solved_Puzzle = SudokuSolver()._solve(self._puzzle)

        if is_Solved:
            self._is_Solved, self._puzzle = is_Solved, solved_Puzzle
            self._grid_Builder()
            messagebox.showinfo(
                "Done", "Puzzle Solved And Result Saved To 'Solved Sudoku.txt' File \nNear Application File.\n\nClick OK To See It")
        else:
            messagebox.showerror("Unsolvable Puzzle",
                                 "Sorry...\nYour Puzzle Is Unsolvable!")
        return

    def run(self) -> None:
        self._GUI_Builder()
        return

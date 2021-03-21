import logging

import numpy as np


def highlight_string(text: str, style: str = "OKGREEN") -> str:
    styles = {
        "HEADER": "\033[95m",
        "OKBLUE": "\033[94m",
        "OKCYAN": "\033[96m",
        "OKGREEN": "\033[92m",
        "WARNING": "\033[93m",
        "FAIL": "\033[91m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
    }
    ENDC = "\033[0m"
    return f"{styles[style]}{text}{ENDC}"


class Sudoku:
    _set_directions = ["row", "col", "quadrant"]

    def __init__(self, board: list):
        """Iniitialize board

        Parameters
        ----------
        board : list
            2 dimensional array containing the values for the Sudoku

        Raises
        ------
        ValueError
            Raised if the the array is not square
        """

        self.size = len(board)
        self.field_size = int(np.sqrt(self.size))
        if self.field_size ** 2 != self.size:
            raise ValueError("Something is wrong with the input dimension")
        for row in board:
            if len(row) != self.size:
                raise ValueError("Not all rows have the same length.")
        #
        self.initial_board = np.hstack(board)
        self.current_board = np.hstack(board)

    def get_indices(self, pos):
        idx_row = pos // self.size
        idx_col = pos % self.size
        return idx_row, idx_col

    def get_position(self, idx_row, idx_col):
        return idx_row * self.size + idx_col

    def pretty_print(self, highlight=[[]]):
        vline = "-" * (2 * self.size + 2 * self.field_size + 1)
        string = vline + "\n"
        for idx_row in range(self.size):
            string += "|"
            for idx_col in range(self.size):
                position = self.get_position(idx_row, idx_col)
                val = self.current_board[position]
                val = str(val) if val != 0 else "_"
                if [idx_row, idx_col] in highlight:
                    val = highlight_string(val, style="FAIL")
                string += " " + val
                if idx_col % self.field_size == 2:
                    string += " |"
            if idx_row % self.field_size == 2:
                string += "\n" + vline
            string += "\n"
        return string

    def do_solve_step(self) -> bool:
        # 1. Look for unique possiblities
        # 2. Go over rows
        # 3. Go over columns
        # 4. Go over quadrants
        # 5. Do tryout
        logging.debug("")

    def check_matching(self, field_cnt: int, direction: str = "row"):
        if direction not in self._set_directions:
            raise ValueError(
                "direction has to be in [" + ", ".join(self._set_directions)
            )
        if field_cnt >= self.size:
            raise ValueError(
                "The field count has to be in [0," + str(self.size - 1) + "]"
            )

    def get_members(self, field_cnt: int, direction: str = "row") -> list:
        if direction == "row":
            return [field_cnt * self.size + i for i in range(self.size)]
        elif direction == "col":
            return [field_cnt + i * self.size for i in range(self.size)]
        elif direction == "quadrant":
            row_cnt = field_cnt // self.field_size
            col_cnt = field_cnt % self.field_size
            start_pos = (
                row_cnt * self.field_size * self.size + col_cnt * self.field_size
            )
            return [
                i
                for offset in range(0, self.field_size * self.size, self.size)
                for i in range(start_pos + offset, start_pos + offset + self.field_size)
            ]


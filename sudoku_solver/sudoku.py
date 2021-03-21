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
        self.initial_board = board
        self.current_board = board
        self.size = len(self.initial_board)
        self.field_size = int(np.sqrt(self.size))
        if self.field_size ** 2 != self.size:
            raise ValueError("Something is wrong with the input dimension")
        for row in self.initial_board:
            if len(row) != self.size:
                raise ValueError("Not all rows have the same length.")

    def pretty_print(self, highlight=[[]]):
        vline = "-" * (2 * self.size + 2 * self.field_size + 1)
        string = vline + "\n"
        for row_cnt, row in enumerate(self.current_board):
            string += "|"
            for col_cnt, col in enumerate(row):
                val = str(col)
                if [row_cnt, col_cnt] in highlight:
                    print("INSIDE")
                    val = highlight_string(val, style="FAIL")
                string += " " + val
                if col_cnt % self.field_size == 2:
                    string += " |"
            if row_cnt % self.field_size == 2:
                string += "\n" + vline
            string += "\n"
        return string

    def do_solve_step(self) -> bool:
        logging.debug("")


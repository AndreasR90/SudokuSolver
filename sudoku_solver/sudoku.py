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
        self.full_size = self.size ** 2
        self.field_size = int(np.sqrt(self.size))
        if self.field_size ** 2 != self.size:
            raise ValueError("Something is wrong with the input dimension")
        for row in board:
            if len(row) != self.size:
                raise ValueError("Not all rows have the same length.")
        # Make it 1d numpy
        self.initial_board = np.hstack(board)
        self.current_board = np.hstack(board)

        self.possible_vals = {}

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

    def solve(self) -> bool:
        cnt = 1
        while True:
            positions, changed = self.do_solve_step(change=True, single_step=False)
            if cnt % 100 == 0:
                print(cnt, positions)
                break
            cnt += 1
            if not changed:
                print("REGULAR BREAK")
                break

    def do_solve_step(self, change: bool = True, single_step: bool = False) -> dict:
        # 1. Look for unique possiblities
        logging.debug("Look for unqiue possibilites")
        changed = False
        positions = {}
        positions["cell"] = self.check_unique(change=change, single_step=single_step)
        if len(positions["cell"]) != 0:
            changed = True
        # 2. Go over rows
        # 3. Go over columns
        # 4. Go over quadrants
        for direction in self._set_directions:

            positions[direction] = self.check_field(
                direction=direction, change=change, single_step=single_step
            )
            if len(positions[direction]) != 0:
                changed = True
        # 2. Go over rows
        # 5. Do tryout

        return positions, changed

    def check_valid_board(self) -> bool:
        for direction in self._set_directions:
            for cnt in range(self.size):
                members = self.get_members(cnt, direction=direction)
                numbers = [
                    self.current_board[mb]
                    for mb in members
                    if self.current_board[mb] != 0
                ]
                if len(numbers) != len(set(numbers)):
                    return False
        return True

    def check_field(
        self, direction="row", change: bool = True, single_step: bool = False
    ) -> list:
        pos = []
        self.fill_possible_vals()
        for cnt in range(self.size):
            members = self.get_members(field_cnt=cnt, direction=direction)
            unkown_members = [
                member for member in members if self.current_board[member] == 0
            ]
            needed_vals = [
                i
                for i in range(1, 1 + self.size)
                if i not in self.current_board[members]
            ]
            for i in needed_vals:
                positions = [
                    mb for mb in unkown_members if i in self.possible_vals.get(mb, [0])
                ]
                if len(positions) == 1:
                    pos += positions
                    if change:
                        self.current_board[positions] = i
                        self.fill_possible_vals()
                        if single_step:
                            return [pos]
        return pos

    def check_unique(self, change: bool = True, single_step: bool = False,) -> list:
        unique = []
        self.fill_possible_vals()
        for pos in range(self.full_size):
            possible_states = self.possible_vals.get(pos, None)
            if not possible_states:
                continue
            if len(possible_states) == 1:
                unique += [pos]
                if change:
                    self.current_board[pos] = possible_states[0]
                    print("chgd", self.current_board[pos], pos)
                    self.fill_possible_vals()
                    print(self.check_possible_states(pos))
                    if single_step:
                        return [pos]
        return unique

    def fill_possible_vals(self):
        self.possible_vals = {}
        for pos in range(self.full_size):
            possible_states = self.check_possible_states(pos)
            if not possible_states:
                continue
            self.possible_vals[pos] = possible_states
        return self.possible_vals

    def check_matching(self, field_cnt: int, direction: str = "row"):
        if direction not in self._set_directions:
            raise ValueError(
                "direction has to be in [" + ", ".join(self._set_directions)
            )
        if field_cnt >= self.size:
            raise ValueError(
                "The field count has to be in [0," + str(self.size - 1) + "]"
            )
        raise NotImplementedError

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

    def get_other_members(self, pos: int, direction="row"):
        idx_row, idx_col = self.get_indices(pos)
        if direction == "row":
            field_index = idx_row
        if direction == "col":
            field_index = idx_col
        elif direction == "quadrant":
            field_index = (
                idx_row // self.field_size
            ) * self.field_size + idx_col // self.field_size
        all_members = self.get_members(field_cnt=field_index, direction=direction)
        return [member for member in all_members if member != pos]

    def check_possible_states(self, pos: int) -> list:
        if self.current_board[pos] != 0:
            return False
        possible_states = [i for i in range(1, 1 + self.size)]
        for direction in self._set_directions:
            other_members = self.get_other_members(pos, direction=direction)
            for o_member in other_members:
                val = self.current_board[o_member]
                if val in possible_states:
                    pos_idx = possible_states.index(self.current_board[o_member])
                    del possible_states[pos_idx]

        return possible_states


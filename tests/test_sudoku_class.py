import numpy as np
import pytest
from sudoku_solver.sudoku import Sudoku


class TestClassSudoku:
    start_board = [
        [2, 0, 6, 0, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 6, 7, 0],
        [7, 8, 9, 1, 0, 6, 2, 0, 0],
        [3, 1, 0, 0, 6, 5, 0, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 2, 0],
        [0, 9, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 1, 6, 0, 0, 0, 8, 3],
        [8, 6, 4, 0, 1, 0, 0, 5, 0],
        [0, 0, 3, 5, 8, 2, 4, 6, 1],
    ]
    start_board8x8 = [
        [2, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 7],
        [7, 8, 9, 1, 0, 6, 2, 0],
        [3, 1, 0, 0, 6, 5, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 2],
        [0, 9, 0, 0, 2, 0, 0, 4],
        [0, 0, 1, 6, 0, 0, 0, 8],
        [8, 6, 4, 0, 1, 0, 0, 5],
    ]
    size = 9
    field_size = 3

    def test_init(self):
        x = Sudoku(self.start_board)
        np.testing.assert_array_equal(x.initial_board, np.hstack(self.start_board))
        np.testing.assert_array_equal(x.current_board, np.hstack(self.start_board))
        assert x.size == self.size
        assert x.field_size == self.field_size

    def test_init_Exception(self):
        with pytest.raises(ValueError):
            Sudoku(self.start_board8x8)

        self.start_board8x8[1] = [1, 2, 3]
        with pytest.raises(ValueError):
            Sudoku(self.start_board8x8)

    def test_pretty_print(self):
        x = Sudoku(self.start_board)
        expected_string = (
            "-------------------------\n"
            + "| 2 _ 6 | _ _ _ | _ _ 8 |\n"
            + "| _ _ \x1b[91m_\x1b[0m | _ _ _ | 6 7 _ |\n"
            + "| 7 8 9 | 1 _ 6 | 2 _ _ |\n"
            + "-------------------------\n"
            + "| 3 1 _ | _ 6 5 | _ _ _ |\n"
            + "| _ _ _ | _ 9 1 | _ 2 _ |\n"
            + "| _ 9 _ | _ 2 _ | _ 4 _ |\n"
            + "-------------------------\n"
            + "| _ _ 1 | 6 _ _ | _ 8 3 |\n"
            + "| 8 6 4 | _ 1 _ | _ 5 _ |\n"
            + "| _ _ 3 | 5 8 2 | 4 6 1 |\n"
            + "-------------------------\n"
        )
        assert x.pretty_print(highlight=[[1, 2]]) == expected_string

    def test_index_and_position(self):
        x = Sudoku(self.start_board)
        assert x.get_position(0, 4) == 4
        assert x.get_position(2, 4) == 22
        assert x.get_indices(4) == (0, 4)
        assert x.get_indices(22) == (2, 4)

    def test_get_members(self):
        x = Sudoku(self.start_board)

        row = x.get_members(3, direction="row")
        row_expect = [27, 28, 29, 30, 31, 32, 33, 34, 35]
        assert row == row_expect

        col = x.get_members(5, direction="col")
        col_expect = [5, 14, 23, 32, 41, 50, 59, 68, 77]
        assert col == col_expect

        quadrant = x.get_members(5, direction="quadrant")
        quadrant_expect = [33, 34, 35, 42, 43, 44, 51, 52, 53]
        assert quadrant == quadrant_expect

        row = x.get_other_members(30, direction="row")
        row_expect = [27, 28, 29, 31, 32, 33, 34, 35]
        assert row == row_expect

        col = x.get_other_members(23, direction="col")
        col_expect = [5, 14, 32, 41, 50, 59, 68, 77]
        assert col == col_expect

        quadrant = x.get_other_members(44, direction="quadrant")
        quadrant_expect = [33, 34, 35, 42, 43, 51, 52, 53]
        assert quadrant == quadrant_expect

    def test_possible_states(self):
        x = Sudoku(self.start_board)

        pos_states = x.check_possible_states(1)
        pos_states_expected = [3, 4, 5]
        assert pos_states == pos_states_expected

        pos_states = x.check_possible_states(58)
        pos_states_expected = [4, 7]
        assert pos_states == pos_states_expected

        pos_states = x.check_possible_states(0)
        # this is fixed -> False
        pos_states_expected = False
        assert pos_states == pos_states_expected

    def test_check_unique(self):
        x = Sudoku(self.start_board)

        unique = x.check_unique(change=True, single_step=True)
        unique_expected = [11]
        possible_expected = {
            1: [3, 4],
            3: [3, 4, 7, 9],
            4: [3, 4, 5, 7],
            5: [3, 4, 7, 9],
            6: [1, 3, 5, 9],
            7: [1, 3, 9],
            9: [1, 4],
            10: [3, 4],
            12: [2, 3, 4, 8, 9],
            13: [3, 4],
            14: [3, 4, 8, 9],
            17: [4, 9],
            22: [3, 4, 5],
            25: [3],
            26: [4, 5],
            29: [2, 7, 8],
            30: [4, 7, 8],
            33: [7, 8, 9],
            34: [9],
            35: [7, 9],
            36: [4, 5, 6],
            37: [4, 5, 7],
            38: [7, 8],
            39: [3, 4, 7, 8],
            42: [3, 5, 7, 8],
            44: [5, 6, 7],
            45: [5, 6],
            47: [7, 8],
            48: [3, 7, 8],
            50: [3, 7, 8],
            51: [1, 3, 5, 7, 8],
            53: [5, 6, 7],
            54: [5, 9],
            55: [2, 5, 7],
            58: [4, 7],
            59: [4, 7, 9],
            60: [7, 9],
            66: [3, 7, 9],
            68: [3, 7, 9],
            69: [7, 9],
            71: [2, 7, 9],
            72: [9],
            73: [7],
        }
        assert unique == unique_expected
        assert x.possible_vals == possible_expected

        x = Sudoku(self.start_board)

        unique = x.check_unique(change=True, single_step=False)
        unique_expected = [11, 25, 34, 35, 72, 73]
        assert unique == unique_expected
        assert x.possible_vals != {}

        x = Sudoku(self.start_board)

        unique = x.check_unique(change=False, single_step=False)
        unique_expected = [11, 25, 34, 72, 73]
        assert unique == unique_expected
        np.testing.assert_array_equal(x.initial_board, x.current_board)

    def test_check_field(self):
        x = Sudoku(self.start_board)

        values = x.check_field(direction="row", change=True, single_step=False)
        expct = [9, 12, 14, 17, 29, 30, 33, 34, 51, 55, 54, 71, 73, 72]
        assert values == expct

        x = Sudoku(self.start_board)

        values = x.check_field(direction="col", change=True, single_step=False)
        expct = [9, 36, 45, 55, 29, 12, 7, 25, 34, 71, 44, 17]
        assert values == expct

        x = Sudoku(self.start_board)

        values = x.check_field(direction="quadrant", change=True, single_step=False)
        expct = [9, 12, 14, 29, 51, 42, 33, 55, 54, 73, 72, 71]
        assert values == expct

    def test_check_matching(self):
        # TODO
        x = Sudoku(self.start_board)
        with pytest.raises(ValueError):
            x.check_matching(0, direction="head")
        with pytest.raises(ValueError):
            x.check_matching(110, direction="row")


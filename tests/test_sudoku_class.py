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

    def test_check_matching(self):
        # TODO
        x = Sudoku(self.start_board)
        with pytest.raises(ValueError):
            x.check_matching(0, direction="head")
        with pytest.raises(ValueError):
            x.check_matching(110, direction="row")

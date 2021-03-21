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

        self.start_board8x8[0] = [1, 2, 3]
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

    def test_check_matching(self):
        x = Sudoku(self.start_board)
        with pytest.raises(ValueError):
            x.check_matching(0, direction="head")
        with pytest.raises(ValueError):
            x.check_matching(110, direction="row")

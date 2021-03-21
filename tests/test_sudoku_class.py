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
        assert x.initial_board == self.start_board
        assert x.current_board == self.start_board
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
            + "| 2 0 6 | 0 0 0 | 0 0 8 |\n"
            + "| 0 0 \x1b[91m0\x1b[0m | 0 0 0 | 6 7 0 |\n"
            + "| 7 8 9 | 1 0 6 | 2 0 0 |\n"
            + "-------------------------\n"
            + "| 3 1 0 | 0 6 5 | 0 0 0 |\n"
            + "| 0 0 0 | 0 9 1 | 0 2 0 |\n"
            + "| 0 9 0 | 0 2 0 | 0 4 0 |\n"
            + "-------------------------\n"
            + "| 0 0 1 | 6 0 0 | 0 8 3 |\n"
            + "| 8 6 4 | 0 1 0 | 0 5 0 |\n"
            + "| 0 0 3 | 5 8 2 | 4 6 1 |\n"
            + "-------------------------\n"
        )
        assert x.pretty_print(highlight=[[1, 2]]) == expected_string

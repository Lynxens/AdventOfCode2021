import unittest
import numpy as np
from typing import Union
from copy import deepcopy

FOUND = -1


def read(file_path: str) -> (np.ndarray, np.ndarray):
    numbers = np.loadtxt(file_path, delimiter=',', max_rows=1, dtype=int)
    boards_2d = np.loadtxt(file_path, skiprows=2, dtype=int)
    boards_3d = boards_2d.reshape((int(len(boards_2d) / 5), 5, 5))

    return numbers, boards_3d


def get_bingo_board(boards: np.ndarray):
    for (i, board) in enumerate(boards):
        if np.any(np.all(board == -1, axis=0)) or np.any(np.all(board == -1, axis=1)):
            return board.flatten(), i

    return None, None


def puzzle_1(numbers: np.ndarray, boards: np.ndarray) -> int:
    for number in numbers:
        boards[np.where(boards == number)] = FOUND

        bingo_board, _ = get_bingo_board(boards)

        if bingo_board is not None:
            return np.sum(bingo_board[np.where(bingo_board != FOUND)]) * number


def puzzle_2(numbers: np.ndarray, _boards: np.ndarray) -> int:
    boards = _boards[:, :, :]
    last_bingo_board = None
    last_bingo_number = None

    for number in numbers:
        boards[np.where(boards == number)] = FOUND

        while True:
            bingo_board, bingo_board_index = get_bingo_board(boards)

            if bingo_board is not None:
                last_bingo_board = deepcopy(bingo_board)
                last_bingo_number = number

                # Crappy delete
                boards = list(boards)
                del boards[bingo_board_index]
                boards = np.array(boards)
            else:
                break

    return np.sum(last_bingo_board[np.where(last_bingo_board != FOUND)]) * last_bingo_number


def run():
    numbers, boards = read('data/day4/input.txt')
    print(f"Puzzle 1: {puzzle_1(numbers, boards)}")
    print(f"Puzzle 2: {puzzle_2(numbers, boards)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        (self.numbers_example, self.boards_example) = read('data/day4/input_example.txt')
        (self.numbers, self.boards) = read('data/day4/input.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.numbers_example, self.boards_example), 4512)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.numbers, self.boards), 35711)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.numbers_example, self.boards_example), 1924)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.numbers, self.boards), 5586)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


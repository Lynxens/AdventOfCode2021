import unittest
import numpy as np
from math import ceil, floor


def read(file_path: str) -> np.ndarray:
    return np.loadtxt(file_path, delimiter=',', dtype=int)


def puzzle_1(data: np.ndarray) -> int:
    return int(np.sum(np.abs(data - np.median(data))))


def calculate_costs(data: np.ndarray, point: int) -> int:
    diff = np.abs(data - point)
    return int(np.sum((diff * 0.5) * (diff + 1)))


def puzzle_2(data: np.ndarray) -> int:
    return min(
        calculate_costs(data, floor(np.mean(data))),
        calculate_costs(data, ceil(np.mean(data)))
    )


def run():
    data = read('data/day7/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read('data/day7/input.txt')
        self.data_example = read('data/day7/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 37)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 354129)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 168)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 98905973)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


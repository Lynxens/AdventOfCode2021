import unittest
import numpy as np


def puzzle_1(depths: np.ndarray) -> int:
    return np.sum(np.diff(depths) > 0)


def puzzle_2(depths: np.ndarray) -> int:
    return np.sum(np.diff(np.convolve(depths, np.ones(3), mode='valid')) > 0)


def run():
    depths = np.loadtxt('data/day1/input1.txt', dtype=int)
    print(f"Puzzle 1: {puzzle_1(depths)}")
    print(f"Puzzle 2: {puzzle_2(depths)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.depths = np.loadtxt('data/day1/input1_test.txt', dtype=int)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.depths), 7)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.depths), 5)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


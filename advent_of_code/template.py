import unittest
import numpy as np

DAY = None


def read(file_path: str) -> np.ndarray:
    pass


def puzzle_1(data: np.ndarray) -> int:
    pass


def puzzle_2(data: np.ndarray) -> int:
    pass


def run():
    data = read(f'data/day{DAY}/input.txt')

    # print(f"Puzzle 1: {puzzle_1(data)}")
    # print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), None)

    # def test_puzzle_1(self):
    #     self.assertEqual(puzzle_1(self.data), None)
    #
    # def test_puzzle_2_example(self):
    #     self.assertEqual(puzzle_2(self.data_example), None)
    #
    # def test_puzzle_2(self):
    #     self.assertEqual(puzzle_2(self.data), None)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()

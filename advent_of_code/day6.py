import unittest
import numpy as np


def read(file_path: str) -> np.ndarray:
    return np.loadtxt(file_path, delimiter=',', dtype=int)


def spawn_fish(data: np.ndarray, days: int):
    # Frequency table fish
    frequency_table = [0] * 9
    for fish in data:
        frequency_table[fish] += 1

    for _ in range(days):
        # Count pregnant fish
        pregnant_fish = frequency_table[0]

        # Shift counts and add new and post pregnant fish
        del frequency_table[0]
        frequency_table.append(pregnant_fish)
        frequency_table[6] += pregnant_fish

    return frequency_table


def puzzle_1(data: np.ndarray) -> int:
    return sum(spawn_fish(data, 80))


def puzzle_2(data: np.ndarray) -> int:
    return sum(spawn_fish(data, 256))


def run():
    data = read('data/day6/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read('data/day6/input.txt')
        self.data_example = read('data/day6/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 5934)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 393019)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 26984457539)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 1757714216975)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


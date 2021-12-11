import unittest
import numpy as np
from scipy.signal import convolve2d

DAY = 11

KERNEL = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])


def read(file_path: str) -> np.ndarray:
    return np.genfromtxt(file_path, delimiter=1, dtype=int)


def flash_cycle(grid: np.ndarray) -> int:
    grid += 1

    burned_out_y = np.array([], dtype=int)
    burned_out_x = np.array([], dtype=int)
    spread_grid = np.zeros(grid.shape, dtype=int)

    while True:
        kindlings_y, kindlings_x = np.where(grid > 9)

        if len(kindlings_y) == 0:
            break

        spread_grid.fill(0)
        spread_grid[kindlings_y, kindlings_x] = 1
        spread_grid = convolve2d(spread_grid, KERNEL, mode='same')
        grid += spread_grid

        burned_out_y = np.concatenate((burned_out_y, kindlings_y))
        burned_out_x = np.concatenate((burned_out_x, kindlings_x))
        grid[burned_out_y, burned_out_x] = 0

    return len(burned_out_y)


def puzzle_1(data: np.ndarray) -> int:
    grid = np.copy(data)

    return sum([flash_cycle(grid) for _ in range(100)])


def puzzle_2(data: np.ndarray) -> int:
    number_of_octopuses = np.prod(data.shape)
    grid = np.copy(data)

    step = 1
    while flash_cycle(grid) != number_of_octopuses:
        step += 1

    return step


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 1656)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 1747)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 195)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 505)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


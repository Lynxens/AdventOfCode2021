import unittest
import numpy as np
from functools import reduce
import operator
from scipy.signal import argrelmin


DAY = 9

NOT_FOUND = 10


def read(file_path: str) -> np.ndarray:
    return np.genfromtxt(file_path, delimiter=1, dtype=int)


def is_min(data, row, col) -> bool:
    top = data[row - 1][col] if row > 0 else NOT_FOUND
    left = data[row][col - 1] if col > 0 else NOT_FOUND
    right = data[row][col + 1] if col < len(data[0]) - 1 else NOT_FOUND
    bottom = data[row + 1][col] if row < len(data) - 1 else NOT_FOUND

    return data[row, col] < min(top, left, bottom, right)


def puzzle_1_naive(data: np.ndarray) -> int:
    total = 0

    for row in range(len(data)):
        for col in range(len(data[0])):
            if is_min(data, row, col):
                total += 1 + data[row, col]

    return total


def coords_to_set(coords: (np.ndarray, np.ndarray)) -> set:
    return set(map(tuple, np.array(coords).T))


def puzzle_1(data: np.ndarray) -> int:
    padded_data = np.pad(data, 1, 'constant', constant_values=NOT_FOUND)

    # Find relative min coordinates
    # `argrelmin` finds local minima in a 1d array. Running this function over both axes gives
    # the coordinates of all local minima. The intersection of the sets of these of coordinates are the
    # minima we are looking for. (4x faster than the naive approach)
    local_minima_2d = np.array(list(
        coords_to_set(argrelmin(padded_data, axis=0)).intersection(coords_to_set(argrelmin(padded_data, axis=1)))
    )).T

    return len(local_minima_2d[0]) + np.sum(padded_data[local_minima_2d[0], local_minima_2d[1]])


def find_basin(data: np.ndarray, row: int, col: int, basin: set):
    # Out of range
    if row < 0 or row > len(data) - 1 or col < 0 or col > len(data[0]) - 1:
        return

    # Already in the basin
    if (row, col) in basin:
        return

    # Border found
    if data[row, col] == 9:
        return

    basin.add((row, col))
    find_basin(data, row - 1, col, basin)
    find_basin(data, row, col - 1, basin)
    find_basin(data, row, col + 1, basin)
    find_basin(data, row + 1, col, basin)

    return


def puzzle_2(data: np.ndarray) -> int:
    coords = coords_to_set(np.where(data != 9))
    basin_sizes = []

    while len(coords) > 0:
        (row, col) = next(iter(coords))

        basin = set()
        find_basin(data, row, col, basin)

        coords -= basin
        basin_sizes.append(len(basin))

    return reduce(operator.mul, sorted(basin_sizes, reverse=True)[:3])


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 15)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 550)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 1134)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 1100682)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


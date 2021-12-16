import unittest
import numpy as np
from heapq import heappop, heappush
from dataclasses import dataclass, field
from typing import Any

DAY = 15


def read(file_path: str) -> np.ndarray:
    return np.genfromtxt(file_path, delimiter=1, dtype=int)


@dataclass(order=True)
class Cell:
    risk: int
    position: Any = field(compare=False)


def find_safest_path(risk_grid: np.ndarray) -> int:
    start_pos = (len(risk_grid) - 1, len(risk_grid[0]) - 1)
    queue = [Cell(risk_grid[start_pos], start_pos)]

    visited = np.full(risk_grid.shape, False, dtype=bool)
    acc_risk = np.full(risk_grid.shape, float("inf"))
    acc_risk[start_pos] = risk_grid[start_pos]

    while len(queue) > 0:
        cell = heappop(queue)

        if visited[cell.position]:
            continue

        visited[cell.position] = True

        (y, x) = cell.position
        for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            next_y = y + dy
            next_x = x + dx

            if 0 <= next_y < len(risk_grid) and 0 <= next_x < len(risk_grid[0]) and not visited[next_y, next_x]:
                acc_risk[next_y, next_x] = min(acc_risk[next_y, next_x], cell.risk + risk_grid[next_y, next_x])
                heappush(queue, Cell(acc_risk[next_y, next_x], (next_y, next_x)))

    return int(acc_risk[0, 0] - risk_grid[0, 0])


def puzzle_1(data: np.ndarray) -> int:
    return find_safest_path(data)


def puzzle_2(data: np.ndarray) -> int:
    height = len(data)
    width = len(data[0])
    grid = np.zeros((height * 5, width * 5), dtype=int)

    for y in range(5):
        for x in range(5):
            grid[y * height:(y + 1) * height, x * width:(x + 1) * width] = data + (x + y)

    grid[grid > 9] -= 9

    return find_safest_path(grid)


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 40)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 447)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 315)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 2825)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()

import unittest
import numpy as np


def read(file_path: str) -> [(int, int, int, int)]:
    points = []

    with open(file_path) as f:
        for line in f.readlines():
            points.append(tuple(map(int, line.replace(' -> ', ',').split(','))))

    return points


def get_line_coordinates(x1: int, y1: int, x2: int, y2: int) -> np.ndarray:
    max_diff = max(abs(x1 - x2), abs(y1 - y2))
    return np.linspace(x1, x2, max_diff + 1, dtype=np.int32) * 1000 + np.linspace(y1, y2, max_diff + 1, dtype=np.int32)


def count_duplicate_coordinates(points: [(int, int, int, int)]) -> int:
    coordinates = np.array([], dtype=np.int32)

    for (x1, y1, x2, y2) in points:
        coordinates = np.concatenate((coordinates, get_line_coordinates(x1, y1, x2, y2)), axis=0)

    # Count non-unique coordinates
    return np.sum(np.unique(coordinates, return_counts=1)[1] > 1)


def puzzle_1(points: [(int, int, int, int)]) -> int:
    # Filter diagonal lines
    return count_duplicate_coordinates(list(filter(lambda point: point[0] == point[2] or point[1] == point[3], points)))


def puzzle_2(points: [(int, int, int, int)]) -> int:
    return count_duplicate_coordinates(points)


def run():
    points = read('data/day5/input.txt')

    print(f"Puzzle 1: {puzzle_1(points)}")
    print(f"Puzzle 2: {puzzle_2(points)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.points = read('data/day5/input.txt')
        self.points_example = read('data/day5/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.points_example), 5)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.points), 4655)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.points_example), 12)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.points), 20500)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


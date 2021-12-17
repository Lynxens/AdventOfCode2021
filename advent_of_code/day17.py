import unittest
import numpy as np
from math import floor, sqrt

DAY = 17


def x_series(initial_velocity: int, max_steps: int) -> np.ndarray:
    return np.cumsum(np.pad(np.arange(initial_velocity, 0, -1), (0, max(0, max_steps - abs(initial_velocity)))))


def y_series(max_value: int, vy: int = 0) -> np.ndarray:
    return np.cumsum(np.arange(0, -(floor(0.5 * (sqrt(1 + 8 * max_value) - 1)) + 1), -1) + vy)


def triangular_number(n: int) -> int:
    return (n * (n + 1)) // 2


def x_steps_in_target(vx: int, x_target_min: int, x_target_max: int, max_steps: int) -> np.ndarray:
    steps = x_series(vx, max_steps)
    return np.argwhere((x_target_min <= steps) & (steps <= x_target_max)).flatten()


def y_steps_in_target(vy: int, y_target_bottom: int, y_target_top: int) -> np.ndarray:
    if vy <= 0:
        offset = 0
        steps = y_series(-y_target_bottom, vy)
    else:
        offset = vy
        y_top = triangular_number(vy)
        steps = y_series(y_top - y_target_bottom) + y_top

    return np.argwhere((steps <= y_target_top) & (steps >= y_target_bottom)).flatten() + offset


def get_shots(x_min: int, x_max: int, y_bottom: int, y_top: int) -> (int, int):
    x_steps = {}

    for vx in range(x_max + 1):
        steps = x_steps_in_target(vx, x_min, x_max, abs(y_bottom) * 2)

        for step in steps:
            try:
                x_steps[step].append(vx)
            except KeyError:
                x_steps[step] = [vx]

    hits = set()
    for vy in range(y_bottom, abs(y_bottom)):
        steps = y_steps_in_target(vy, y_bottom, y_top)

        for step in steps:
            try:
                for vx in x_steps[step]:
                    hits.add((vx, vy))
            except KeyError:
                pass

    for hit in hits:
        yield hit


def puzzle_1(target_range: (int, int, int, int)) -> int:
    return max([triangular_number(vy) for (vx, vy) in get_shots(*target_range)])


def puzzle_2(target_range: (int, int, int, int)) -> int:
    return len(list(get_shots(*target_range)))


def run():
    data = (150, 171, -129, -70)

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = (150, 171, -129, -70)
        self.data_example = (20, 30, -10, -5)

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 45)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 8256)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 112)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 2326)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()

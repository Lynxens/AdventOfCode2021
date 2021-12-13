import unittest
import numpy as np

DAY = 13


def read(file_path: str) -> ({tuple}, [tuple]):
    coordinates = set()
    instructions = []

    with open(file_path) as f:
        instructions_found = False
        for line in f.readlines():
            line = line.strip()

            if line == '':
                instructions_found = True
                continue

            if instructions_found:
                instruction, value = line.split('=')
                instructions.append((instruction[-1], int(value)))
            else:
                [x, y] = line.split(',')
                coordinates.add((int(y), int(x)))

    return coordinates, instructions


def fold(coordinates: {tuple}, axis: str, value: int) -> {tuple}:
    def map_coordinate(a: int):
        return value - abs(a - value)

    new_coordinates = []
    if axis == 'y':
        for (y, x) in coordinates:
            if y < value:
                new_coordinates.append((y, x))
            elif y > value:
                new_coordinates.append((map_coordinate(y), x))
    else:
        for (y, x) in coordinates:
            if x < value:
                new_coordinates.append((y, x))
            elif x > value:
                new_coordinates.append((y, map_coordinate(x)))

    return set(new_coordinates)


def puzzle_1(coordinates: {tuple}, instructions: [tuple]) -> int:
    a = fold(coordinates, *instructions[0])

    return len(a)


def puzzle_2(coordinates: set, instructions: [tuple]) -> int:
    paper = coordinates.copy()
    for instruction in instructions:
        paper = fold(paper, *instruction)

    # Debug and look for yourself in SciView
    code = np.zeros((7, 40), dtype=int)
    for (y, x) in paper:
        code[y, x] = 1

    return len(paper)


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(*data)}")
    print(f"Puzzle 2: {puzzle_2(*data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(*self.data_example), 17)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(*self.data), 712)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(*self.data_example), 16)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(*self.data), 90)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()

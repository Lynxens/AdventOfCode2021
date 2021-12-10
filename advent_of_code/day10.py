import unittest
from collections import deque
from functools import reduce
import timeit

DAY = 10


CONVERSION_TABLE = {
    '(': '(',
    '[': '[',
    '{': '{',
    '<': '<',
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}


def read(file_path: str) -> list:
    with open(file_path) as f:
        return [line.strip() for line in f]


def is_balanced(line: str) -> (str, str, bool):
    stack = deque([])
    for char in line:
        if char in '([{<':
            stack.appendleft(char)
        else:
            if len(stack) == 0 or CONVERSION_TABLE[char] != stack[0]:
                return char, stack, False

            stack.popleft()

    return '', stack, True


def puzzle_1(data: list) -> int:
    points_table = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    points = 0
    for line in data:
        char, _, success = is_balanced(line)

        if not success:
            points += points_table[char]

    return points


def puzzle_2(data: list) -> int:
    points_table = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }

    scores = []

    for line in data:
        _, stack, success = is_balanced(line)

        if success:
            scores.append(reduce(lambda a, b: a * 5 + b, map(points_table.get, stack)))

    # Return middle score
    return sorted(scores)[len(scores) // 2]


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 26397)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 215229)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 288957)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 1105996483)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


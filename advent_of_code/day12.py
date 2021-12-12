import unittest
from collections import defaultdict

DAY = 12


def read(file_path: str) -> (dict, set):
    cave_system = defaultdict(set)
    small_caves = set([])
    large_caves = set([])

    with open(file_path) as f:
        for line in f:
            [a, b] = line.strip().split('-')

            if a != 'end' and b != 'start':
                cave_system[a].add(b)

            if b != 'end' and a != 'start':
                cave_system[b].add(a)

            for x in [a, b]:
                if x.isupper() or x == 'start' or x == 'end':
                    large_caves.add(x)
                else:
                    small_caves.add(x)

    return cave_system, small_caves, large_caves


def get_path(cave_system: dict, small_caves: set, visited: set, position: str) -> int:
    if position == 'end':
        return 1

    options = cave_system[position].difference(visited.intersection(small_caves))

    if len(options) == 0:
        return 0

    return sum([get_path(cave_system, small_caves, visited.union({option}), option) for option in options])


def puzzle_1(cave_system: dict, small_caves: set, _) -> int:
    return get_path(cave_system, small_caves, {'start'}, 'start')


def get_path_2(cave_system: dict, small_caves_left: list, large_caves: set, path: list, position: str) -> list:
    if position == 'end':
        return ['-'.join(path)]

    options = cave_system[position].intersection(set(small_caves_left).union(large_caves))

    if len(options) == 0:
        return []

    paths = []
    for option in options:
        new_small_caves_left = small_caves_left.copy()

        try:
            new_small_caves_left.remove(position)
        except ValueError:
            pass

        paths += get_path_2(cave_system, new_small_caves_left, large_caves, path + [option], option)

    return paths


def puzzle_2(cave_system: dict, small_caves: set, large_caves: set) -> int:
    paths = set()

    for cave in small_caves:
        paths.update(get_path_2(cave_system, list(small_caves) + [cave], large_caves, ['start'], 'start'))

    return len(paths)


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(*data)}")
    print(f"Puzzle 2: {puzzle_2(*data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example_small = read(f'data/day{DAY}/input_example_small.txt')
        self.data_example_medium = read(f'data/day{DAY}/input_example_medium.txt')
        self.data_example_large = read(f'data/day{DAY}/input_example_large.txt')

    def test_puzzle_1_example_small(self):
        self.assertEqual(puzzle_1(*self.data_example_small), 10)

    def test_puzzle_1_example_medium(self):
        self.assertEqual(puzzle_1(*self.data_example_medium), 19)

    def test_puzzle_1_example_large(self):
        self.assertEqual(puzzle_1(*self.data_example_large), 226)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(*self.data), 3679)

    def test_puzzle_2_example_small(self):
        self.assertEqual(puzzle_2(*self.data_example_small), 36)

    def test_puzzle_2_example_medium(self):
        self.assertEqual(puzzle_2(*self.data_example_medium), 103)

    def test_puzzle_2_example_large(self):
        self.assertEqual(puzzle_2(*self.data_example_large), 3509)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(*self.data), 107395)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


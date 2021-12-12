import unittest
from collections import defaultdict

DAY = 12


def read(file_path: str) -> (dict, set):
    cave_system = defaultdict(set)
    small_caves = set([])

    with open(file_path) as f:
        for line in f:
            [a, b] = line.strip().split('-')

            if a != 'end' and b != 'start':
                cave_system[a].add(b)

            if b != 'end' and a != 'start':
                cave_system[b].add(a)

            for x in [a, b]:
                if not x.isupper() and x != 'start' and x != 'end':
                    small_caves.add(x)

    return cave_system, small_caves


def get_path(cave_system: dict, small_caves: set, visited: set, position: str) -> int:
    if position == 'end':
        return 1

    options = cave_system[position].difference(visited.intersection(small_caves))

    if len(options) == 0:
        return 0

    return sum([get_path(cave_system, small_caves, visited.union({option}), option) for option in options])


def puzzle_1(cave_system: dict, small_caves: set) -> int:
    return get_path(cave_system, small_caves, {'start'}, 'start')


def get_path_double_visit(cave_system: dict, small_caves: set, double_visit_cave: str, visits: int, visited: list, position: str) -> list:
    if position == 'end':
        return ['-'.join(visited)]

    cannot_visit = set(visited).intersection(small_caves)

    if visits < 2 and double_visit_cave in cannot_visit:
        cannot_visit.remove(double_visit_cave)

    options = cave_system[position].difference(cannot_visit)

    if len(options) == 0:
        return []

    paths = []
    for option in options:
        paths += get_path_double_visit(
            cave_system, small_caves, double_visit_cave,
            visits + (1 if option == double_visit_cave else 0),
            visited + [option], option
        )

    return paths


def puzzle_2(cave_system: dict, small_caves: set) -> int:
    paths = set()

    for cave in small_caves:
        paths.update(get_path_double_visit(cave_system, small_caves, cave, 0, ['start'], 'start'))

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


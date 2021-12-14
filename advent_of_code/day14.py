import unittest
from collections import Counter, defaultdict, deque

DAY = 14


def read(file_path: str) -> (list, dict):
    with open(file_path) as f:
        polymer_template = f.readline().strip()
        f.readline()

        rules = {}
        for line in f.readlines():
            from_, to = line.strip().split(' -> ')
            rules[from_] = to

    return polymer_template, rules


# def puzzle_1(polymer_template: str, rules: dict) -> int:
#     # counts = dict(Counter(polymer_template))
#     #
#     # for i in range(len(polymer_template) - 1):
#     #     find_counts(polymer_template[i] + polymer_template[i + 1], rules, 10, counts)
#     #
#     # sorted_counts = sorted(counts.values())
#     # return sorted_counts[-1] - sorted_counts[0]
#
#     template = polymer_template
#
#     for _ in range(10):
#         template = parse_template(template, rules)
#
#     counts = Counter(template).most_common()
#     return counts[0][1] - counts[-1][1]

def get_initial_pairs_and_counts(template: list) -> (dict, dict):
    pairs = defaultdict(int)
    counter = defaultdict(int)

    for i in range(len(template) - 1):
        first_char = template[i]

        counter[first_char] += 1
        pairs[first_char + template[i + 1]] += 1

    counter[template[-1]] += 1

    return pairs, counter


def polymerize(counter: dict, pairs: dict, rules: dict) -> dict:
    new_pairs = defaultdict(int)
    for pair, amount in pairs.items():
        new_char = rules[pair]

        counter[new_char] += amount
        new_pairs[pair[0] + new_char] += amount
        new_pairs[new_char + pair[1]] += amount

    return new_pairs


def get_score(counter: dict) -> int:
    counts = sorted(counter.values())
    return counts[-1] - counts[0]


def puzzle_1(polymer_template: list, rules: dict) -> int:
    pairs, counter = get_initial_pairs_and_counts(polymer_template)

    for i in range(10):
        pairs = polymerize(counter, pairs, rules)

    return get_score(counter)


def puzzle_2(polymer_template: list, rules: dict) -> int:
    pairs, counter = get_initial_pairs_and_counts(polymer_template)

    for i in range(40):
        pairs = polymerize(counter, pairs, rules)

    return get_score(counter)


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(*data)}")
    print(f"Puzzle 2: {puzzle_2(*data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(*self.data_example), 1588)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(*self.data), 3213)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(*self.data_example), 2188189693529)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(*self.data), 3711743744429)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


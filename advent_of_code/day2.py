import unittest


def puzzle_1(file_path: str) -> int:
    horizontal = 0
    depth = 0

    with open(file_path) as f:
        for line in f.readlines():
            [action, value] = line.split(" ")
            value = int(value)

            if action == "forward":
                horizontal += value
            elif action == "up":
                depth -= value
            else:
                depth += value

    return horizontal * depth


def puzzle_2(file_path: str) -> int:
    aim = 0
    horizontal = 0
    depth = 0

    with open(file_path) as f:
        for line in f.readlines():
            [action, value] = line.split(" ")
            value = int(value)

            if action == "forward":
                horizontal += value
                depth += aim * value
            elif action == "up":
                aim -= value
            else:
                aim += value

    return horizontal * depth


def run():
    print(f"Puzzle 1: {puzzle_1('data/day2/input.txt')}")
    print(f"Puzzle 2: {puzzle_2('data/day2/input.txt')}")


class TestPuzzles(unittest.TestCase):
    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1('data/day2/input_example.txt'), 150)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1('data/day2/input.txt'), 1728414)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2('data/day2/input_example.txt'), 900)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2('data/day2/input.txt'), 1765720035)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


import unittest


def read(file_path: str) -> list:
    data = []

    with open(file_path) as f:
        for line in f.readlines():
            [signal_patterns, output_value] = line.strip().split(" | ")
            data.append((
                list(map(lambda x: set(list(x)), signal_patterns.split(" "))),
                list(map(lambda x: ''.join(sorted(list(x))), output_value.split(" "))))
            )

    return data


def puzzle_1(data: list) -> int:
    return sum(map(lambda line: len(list(filter(lambda x: len(x) in [2, 3, 4, 7], line[1]))), data))


def get_code_1(signal_pattern: list) -> set:
    return list(filter(lambda x: len(x) == 2, signal_pattern))[0]


def get_code_4(signal_pattern: list) -> set:
    return list(filter(lambda x: len(x) == 4, signal_pattern))[0]


def get_code_7(signal_pattern: list) -> set:
    return list(filter(lambda x: len(x) == 3, signal_pattern))[0]


def get_code_8(signal_pattern: list) -> set:
    return list(filter(lambda x: len(x) == 7, signal_pattern))[0]


def get_code_9(signal_pattern: list, code_4: set, code_7: set) -> set:
    return list(filter(lambda x: len(x) == 6 and code_4.issubset(x) and code_7.issubset(x), signal_pattern))[0]


def get_code_6(signal_pattern: list, code_8: set, code_1: set) -> (set, set):
    code_6 = list(filter(lambda x: len(x) == 6 and (code_8 - code_1).issubset(x), signal_pattern))[0]
    v_bottom_right = code_6 - (code_8 - code_1)

    return code_6, v_bottom_right


def get_code_0(signal_pattern: list, code_6: set, code_9: set) -> set:
    return list(filter(lambda x: len(x) == 6 and x != code_6 and x != code_9, signal_pattern))[0]


def get_code_3(signal_pattern: list, code_1: set) -> set:
    return list(filter(lambda x: len(x) == 5 and code_1.issubset(x), signal_pattern))[0]


def get_code_2(signal_pattern: list, v_bottom_right: set) -> set:
    return list(filter(lambda x: len(x) == 5 and not v_bottom_right.issubset(x), signal_pattern))[0]


def get_code_5(signal_pattern: list, code_2: set, code_3: set) -> set:
    return list(filter(lambda x: len(x) == 5 and x != code_2 and x != code_3, signal_pattern))[0]


def puzzle_2(data: list) -> int:
    total = 0

    for signal_pattern, output_value in data:
        code_1 = get_code_1(signal_pattern)
        code_4 = get_code_4(signal_pattern)
        code_7 = get_code_7(signal_pattern)
        code_8 = get_code_8(signal_pattern)
        code_9 = get_code_9(signal_pattern, code_4, code_7)
        code_6, v_bottom_right = get_code_6(signal_pattern, code_8, code_1)
        code_0 = get_code_0(signal_pattern, code_6, code_9)
        code_3 = get_code_3(signal_pattern, code_1)
        code_2 = get_code_2(signal_pattern, v_bottom_right)
        code_5 = get_code_5(signal_pattern, code_2, code_3)

        conversion_table = {
            ''.join(sorted(list(code))): str(i) for i, code in enumerate([
                code_0, code_1, code_2, code_3, code_4, code_5, code_6, code_7, code_8, code_9
            ])
        }

        total += int(''.join([conversion_table[code] for code in output_value]))

    return total


def run():
    data = read('data/day8/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read('data/day8/input.txt')
        self.data_example = read('data/day8/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 26)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 452)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 61229)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 1096964)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


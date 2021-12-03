import unittest
import numpy as np


def read(file_path: str) -> np.ndarray:
    return np.genfromtxt(file_path, delimiter=1, dtype=int)


def bit_array_to_dec(bit_array: np.ndarray) -> int:
    return int(b''.join(bit_array.astype('|S1')), 2)


def puzzle_1(bits: np.ndarray) -> int:
    counts = np.apply_along_axis(np.bincount, 1, bits.transpose())
    gamma_rate = bit_array_to_dec(np.argmax(counts, axis=1))
    epsilon_rate = bit_array_to_dec(np.argmin(counts, axis=1))

    return gamma_rate * epsilon_rate


def puzzle_2(bits: np.ndarray) -> int:
    remaining_bits_oxygen = bits[:, :]
    remaining_bits_co2 = bits[:, :]

    for i in range(len(bits[0])):
        if len(remaining_bits_oxygen) == 1:
            break

        bit = remaining_bits_oxygen[:, i]
        if len(bit[bit == 1]) >= len(bit) / 2:
            most_common = 1
        else:
            most_common = 0

        remaining_bits_oxygen = remaining_bits_oxygen[np.where(bit == most_common)]

    for i in range(len(bits[0])):
        if len(remaining_bits_co2) == 1:
            break

        bit = remaining_bits_co2[:, i]
        if len(bit[bit == 0]) <= len(bit) / 2:
            most_common = 0
        else:
            most_common = 1

        remaining_bits_co2 = remaining_bits_co2[np.where(bit == most_common)]

    return bit_array_to_dec(remaining_bits_oxygen[0]) * bit_array_to_dec(remaining_bits_co2[0])


def run():
    bits = read('data/day3/input.txt')
    print(f"Puzzle 1: {puzzle_1(bits)}")
    print(f"Puzzle 2: {puzzle_2(bits)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.bits_example = read('data/day3/input_example.txt')
        self.bits = read('data/day3/input.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.bits_example), 198)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.bits), 852500)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.bits_example), 230)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.bits), 1007985)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()


import unittest
import numpy as np

DAY = 16

VERSION_LENGTH = 3
TYPE_LENGTH = 3
LENGTH_TYPE_LENGTH = 1
LENGTH_TYPE_0_VALUE_LENGTH = 15
LENGTH_TYPE_1_VALUE_LENGTH = 11

# HEADER LENGTHS
HEADER_LITERAL = VERSION_LENGTH + TYPE_LENGTH
HEADER_BASE = VERSION_LENGTH + TYPE_LENGTH + LENGTH_TYPE_LENGTH
HEADER_TYPE_0 = HEADER_BASE + LENGTH_TYPE_0_VALUE_LENGTH
HEADER_TYPE_1 = HEADER_BASE + LENGTH_TYPE_1_VALUE_LENGTH


def read(file_path: str) -> str:
    with open(file_path) as f:
        return f.readline().strip()


def hex_to_bin(hex_number: str) -> str:
    return bin(int('1' + hex_number, 16))[3:]


def bin_to_decimal(bin_number: str) -> int:
    return int(bin_number, 2)


class BITS:
    def __init__(self, bin_code: str):
        self.code = bin_code
        self.version = bin_to_decimal(self.code[:3])
        self.packet_type_id = bin_to_decimal(self.code[3:6])
        self.version_sum = self.version
        self.payload_length = 0

        if self.is_literal:
            self.value = self.literal()
        else:
            self.length_type_id = int(self.code[6])
            self.value = self.operators[self.packet_type_id](self.get_sub_packets())

    operators = {
        0: np.sum,
        1: np.prod,
        2: np.min,
        3: np.max,
        5: lambda x: int(x[0] > x[1]),
        6: lambda x: int(x[0] < x[1]),
        7: lambda x: int(x[0] == x[1])
    }

    @property
    def header_length(self) -> int:
        if self.is_literal:
            return HEADER_LITERAL

        if self.length_type_id == 0:
            return HEADER_TYPE_0
        else:
            return HEADER_TYPE_1

    @property
    def is_literal(self) -> bool:
        return self.packet_type_id == 4

    @property
    def length(self):
        return self.header_length + self.payload_length

    def get_sub_packets_type_0(self):
        sub_packets_length = bin_to_decimal(self.code[HEADER_BASE:HEADER_TYPE_0])

        while self.payload_length < sub_packets_length:
            yield

    def get_sub_packets_type_1(self):
        number_of_packets = bin_to_decimal(self.code[HEADER_BASE:HEADER_TYPE_1])

        for _ in range(number_of_packets):
            yield

    def get_sub_packets(self) -> np.ndarray:
        iterator = self.get_sub_packets_type_0 if self.length_type_id == 0 else self.get_sub_packets_type_1
        values = []

        for _ in iterator():
            sub_packet = BITS(self.code[self.header_length + self.payload_length:])
            values.append(sub_packet.value)
            self.payload_length += sub_packet.length
            self.version_sum += sub_packet.version_sum

        return np.array(values)

    def next_bits(self, offset, n):
        return self.code[offset:offset + n]

    def literal(self) -> int:
        bits = ''

        while True:
            five_bits = self.next_bits(self.header_length + self.payload_length, 5)
            bits += five_bits[1:]
            self.payload_length += 5

            if five_bits[0] == '0':
                break

        return bin_to_decimal(bits)


def puzzle_1(data: str) -> int:
    return BITS(hex_to_bin(data)).version_sum


def puzzle_2(data: str) -> int:
    return BITS(hex_to_bin(data)).value


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example_3 = '8A004A801A8002F478'
        self.data_example_4 = '620080001611562C8802118E34'
        self.data_example_5 = 'C0015000016115A2E0802F182340'
        self.data_example_6 = 'A0016C880162017C3686B18A3D4780'
        self.data_example_7 = 'C200B40A82'
        self.data_example_8 = '04005AC33890'
        self.data_example_9 = '880086C3E88112'
        self.data_example_10 = 'CE00C43D881120'
        self.data_example_11 = 'D8005AC2A8F0'
        self.data_example_12 = 'F600BC2D8F'
        self.data_example_13 = '9C005AC2F8F0'
        self.data_example_14 = '9C0141080250320F1802104A08'

    def test_puzzle_1_example_3(self):
        self.assertEqual(puzzle_1(self.data_example_3), 16)

    def test_puzzle_1_example_4(self):
        self.assertEqual(puzzle_1(self.data_example_4), 12)

    def test_puzzle_1_example_5(self):
        self.assertEqual(puzzle_1(self.data_example_5), 23)

    def test_puzzle_1_example_6(self):
        self.assertEqual(puzzle_1(self.data_example_6), 31)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 981)

    def test_puzzle_2_example_7(self):
        self.assertEqual(puzzle_2(self.data_example_7), 3)

    def test_puzzle_2_example_8(self):
        self.assertEqual(puzzle_2(self.data_example_8), 54)

    def test_puzzle_2_example_9(self):
        self.assertEqual(puzzle_2(self.data_example_9), 7)

    def test_puzzle_2_example_10(self):
        self.assertEqual(puzzle_2(self.data_example_10), 9)

    def test_puzzle_2_example_11(self):
        self.assertEqual(puzzle_2(self.data_example_11), 1)

    def test_puzzle_2_example_12(self):
        self.assertEqual(puzzle_2(self.data_example_12), 0)

    def test_puzzle_2_example_13(self):
        self.assertEqual(puzzle_2(self.data_example_13), 0)

    def test_puzzle_2_example_14(self):
        self.assertEqual(puzzle_2(self.data_example_14), 1)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 299227024091)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()

import unittest
from typing import Union, Any
from math import ceil, floor
from ast import literal_eval
from itertools import permutations

DAY = 18


class Leaf:
    def __init__(self, value: int):
        self.value = value

    def magnitude(self):
        return self.value

    def increment_depth(self):
        return

    @property
    def should_split(self) -> bool:
        return self.value > 9

    @property
    def should_explode(self) -> bool:
        return False

    @staticmethod
    def explode() -> bool:
        return False

    @staticmethod
    def split() -> bool:
        return False

    @property
    def is_last_tree(self) -> bool:
        return False

    @staticmethod
    def is_leaf() -> bool:
        return True

    def __str__(self):
        return self.value


class Tree:
    def __init__(self, left, right, parent=None, depth=0):
        self.parent = parent
        self.depth = depth

        if isinstance(left, Tree):
            self.left = left
            self.left.parent = self
            self.left.increment_depth()
        elif isinstance(left, int):
            self.left = Leaf(left)
        else:
            self.left = Tree(left[0], left[1], self, depth + 1)

        if isinstance(right, Tree):
            self.right = right
            self.right.parent = self
            self.right.increment_depth()
        elif isinstance(right, int):
            self.right = Leaf(right)
        else:
            self.right = Tree(right[0], right[1], self, depth + 1)

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def increment_depth(self):
        self.depth += 1
        self.left.increment_depth()
        self.right.increment_depth()

    def get_leaf_on_right(self) -> Union[Leaf, None]:
        previous = self
        node = self.parent
        while node is not None:
            if node.right is not previous:
                node = node.right
                break

            previous = node
            node = node.parent

        if node is None:
            return None

        while not isinstance(node, Leaf):
            node = node.left

        return node

    def get_leaf_on_left(self) -> Union[Leaf, None]:
        previous = self
        node = self.parent
        while node is not None:
            if node.left is not previous:
                node = node.left
                break

            previous = node
            node = node.parent

        if node is None:
            return None

        while not isinstance(node, Leaf):
            node = node.right

        return node

    def explode_node(self):
        assert isinstance(self.left, Leaf)
        assert isinstance(self.right, Leaf)

        leaf_on_left = self.get_leaf_on_left()
        if leaf_on_left is not None:
            leaf_on_left.value += self.left.value

        leaf_on_right = self.get_leaf_on_right()
        if leaf_on_right is not None:
            leaf_on_right.value += self.right.value

    def split_node(self, leaf):
        return Tree(
            int(floor(leaf.value / 2)),
            int(ceil(leaf.value / 2)),
            self,
            self.depth + 1
        )

    def reduce(self):
        while self.explode() or self.split():
            continue
        return

    def explode(self) -> bool:
        if self.left.should_explode:
            self.left.explode_node()
            self.left = Leaf(0)
            return True

        if self.left.explode():
            return True

        if self.right.should_explode:
            self.right.explode_node()
            self.right = Leaf(0)
            return True

        return self.right.explode()

    def split(self) -> bool:
        if self.left.should_split:
            assert isinstance(self.left, Leaf)
            self.left = self.split_node(self.left)
            return True

        if self.left.split():
            return True

        if self.right.should_split:
            assert isinstance(self.right, Leaf)
            self.right = self.split_node(self.right)
            return True

        return self.right.split()

    @property
    def is_last_tree(self) -> bool:
        return isinstance(self.left, Leaf) and isinstance(self.right, Leaf)

    @property
    def should_explode(self) -> bool:
        return self.is_last_tree and self.depth >= 4

    @property
    def should_split(self) -> bool:
        return False

    def __str__(self):
        return f'[{self.left.__str__()},{self.right.__str__()}]'


def combine_trees(*trees) -> Tree:
    main_tree = Tree(trees[0][0], trees[0][1])
    main_tree.reduce()

    for tree in trees[1:]:
        main_tree = Tree(main_tree, Tree(tree[0], tree[1]))
        main_tree.reduce()

    return main_tree


def read(file_path: str) -> Any:
    with open(file_path) as f:
        return tuple([literal_eval(line.strip()) for line in f.readlines()])


def puzzle_1(data: tuple) -> int:
    return combine_trees(*data).magnitude()


def puzzle_2(data: tuple) -> int:
    return max([max(combine_trees(data[i], data[j]).magnitude(), combine_trees(data[i], data[j]).magnitude()) for (i, j) in permutations(range(len(data)), 2)])


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example_0 = read(f'data/day{DAY}/input_example_0.txt')
        self.data_example_1 = read(f'data/day{DAY}/input_example_1.txt')

    def test_magnitude_1(self):
        self.assertEqual(Tree([1, 2], [[3, 4], 5]).magnitude(), 143)

    def test_magnitude_2(self):
        self.assertEqual(Tree([[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]).magnitude(), 1384)

    def test_magnitude_3(self):
        self.assertEqual(Tree([[[1, 1], [2, 2]], [3, 3]], [4, 4]).magnitude(), 445)

    def test_magnitude_4(self):
        self.assertEqual(Tree([[[3, 0], [5, 3]], [4, 4]], [5, 5]).magnitude(), 791)

    def test_magnitude_5(self):
        self.assertEqual(Tree([[[5, 0], [7, 4]], [5, 5]], [6, 6]).magnitude(), 1137)

    def test_magnitude_6(self):
        self.assertEqual(Tree([[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]).magnitude(), 3488)

    def test_combine_trees_1(self):
        self.assertEqual(
            combine_trees([1, 1], [2, 2], [3, 3], [4, 4]).magnitude(),
            Tree([[[1, 1], [2, 2]], [3, 3]], [4, 4]).magnitude()
        )

    def test_explode_1(self):
        self.assertEqual(
            combine_trees([[[[[9, 8], 1], 2], 3], 4]).magnitude(),
            Tree([[[0, 9], 2], 3], 4).magnitude()
        )

    def test_explode_2(self):
        self.assertEqual(
            combine_trees([7, [6, [5, [4, [3, 2]]]]]).magnitude(),
            Tree(7, [6, [5, [7, 0]]]).magnitude()
        )

    def test_explode_3(self):
        self.assertEqual(
            combine_trees([[6, [5, [4, [3, 2]]]], 1]).magnitude(),
            Tree([6, [5, [7, 0]]], 3).magnitude()
        )

    def test_explode_4(self):
        self.assertEqual(
            combine_trees([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]).magnitude(),
            Tree([3, [2, [8, 0]]], [9, [5, [7, 0]]]).magnitude()
        )

    def test_explode_5(self):
        self.assertEqual(
            combine_trees([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]).magnitude(),
            Tree([3, [2, [8, 0]]], [9, [5, [7, 0]]]).magnitude()
        )

    def test_explode_and_split(self):
        self.assertEqual(
            combine_trees([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]).magnitude(),
            Tree([[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]).magnitude()
        )

    def test_puzzle_1_example_3(self):
        self.assertEqual(
            puzzle_1(([1, 1], [2, 2], [3, 3], [4, 4])),
            Tree([[[1, 1], [2, 2]], [3, 3]], [4, 4]).magnitude()
        )

    def test_puzzle_1_example_4(self):
        self.assertEqual(
            puzzle_1(([1, 1], [2, 2], [3, 3], [4, 4], [5, 5])),
            Tree([[[3, 0], [5, 3]], [4, 4]], [5, 5]).magnitude()
        )

    def test_puzzle_1_example_5(self):
        self.assertEqual(
            puzzle_1(([1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6])),
            Tree([[[5, 0], [7, 4]], [5, 5]], [6, 6]).magnitude()
        )

    def test_puzzle_1_example_0(self):
        self.assertEqual(
            puzzle_1(self.data_example_0),
            Tree([[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]).magnitude()
        )

    def test_puzzle_1_example_1(self):
        self.assertEqual(puzzle_1(self.data_example_1), 4140)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 3987)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example_1), 3993)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 4500)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()

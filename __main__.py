from os.path import dirname, basename, isfile, join
import glob
import sys
from io import StringIO
from math import floor


class Capturing(list):
    """
    Capture print output from function
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class Day:
    def __init__(self, title: str):
        self.title = title
        self.text: [str] = []

    @property
    def is_completed(self) -> bool:
        return len(self.text) > 0

    @property
    def width(self) -> int:
        if self.is_completed:
            return max(len(self.title), max(map(lambda x: len(x), self.text)))
        else:
            return len(self.title)

    @property
    def height(self) -> int:
        return len(self.text)


class Calendar:
    def __init__(self):
        self.grid: [[Day]] = [[Day(f'Day {day}') for day in range(i, i + 5)] for i in range(1, 25, 5)]

    def add(self, module: str, text: [str]):
        day = int(module[3:]) - 1

        row = floor(day / 5)
        col = day % 5

        self.grid[row][col].text = text

    def col_width(self, col: int) -> int:
        return max(max([self.grid[row][col].width for row in range(5)]), 15)

    def row_height(self, row: int) -> int:
        return max([self.grid[row][col].height for col in range(5)])

    @property
    def grid_width(self) -> int:
        return sum([self.col_width(col) for col in range(5)]) + 6

    def print(self):
        # Title top bar
        print('-' * self.grid_width)

        # Title
        calendar_title = 'AdventOfCode 2021'
        half = floor((self.grid_width - len(calendar_title)) / 2) - 1
        print(f'|{" " * half}{calendar_title}{" " * (self.grid_width - half - len(calendar_title) - 2)}|')

        for row in range(5):
            # Header top bar
            print('-' * self.grid_width)

            # Header
            for col in range(5):
                col_width = self.col_width(col)
                title = self.grid[row][col].title

                print(f'|{title}{" " * (col_width - len(title))}', end='')
            print('|')

            # Header bottom bar
            print('-' * self.grid_width)

            # Text
            for line in range(max(4, self.row_height(row))):
                for col in range(5):
                    col_width = self.col_width(col)
                    text = self.grid[row][col].text

                    try:
                        print(f'|{text[line]}{" " * (col_width - len(text[line]))}', end='')
                    except IndexError:
                        print(f'|{" " * col_width}', end='')
                print('|')

        # Bottom bar
        print('-' * self.grid_width)


def main():
    # Load all available day modules
    days = [basename(f)[:-3] for f in glob.glob(join(dirname(__file__), "src/day*.py")) if isfile(f)]

    calendar = Calendar()
    for day in days:
        puzzles = __import__(day)

        with Capturing() as output:
            puzzles.run()

        calendar.add(day, list(output))

    calendar.print()


if __name__ == '__main__':
    main()

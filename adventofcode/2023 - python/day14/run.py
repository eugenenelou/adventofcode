import sys
from enum import Enum, auto
from functools import cached_property
from pathlib import Path


class Tile(Enum):
    EMPTY = 0
    CUBE = 1
    ROUNDED = 2

    @classmethod
    def from_str(cls, value: str) -> "Tile":
        match value:
            case ".":
                return cls.EMPTY
            case "#":
                return cls.CUBE
            case "O":
                return cls.ROUNDED
        raise ValueError(f"{value=}")


labels = {
    Tile.EMPTY: ".",
    Tile.CUBE: "#",
    Tile.ROUNDED: "O",
}


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


deltas = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
}


class Grid:
    def __init__(self, values: list[list[Tile]]):
        self.values = values

    @property
    def identifier(self):
        return tuple(tile.value for row in self.values for tile in row)

    @classmethod
    def from_id(cls, identifier: tuple[int, ...], width: int) -> "Grid":
        values = []
        for i in range(0, len(identifier), width):
            values.append([Tile(value) for value in identifier[i : i + width]])
        return cls(values)

    @cached_property
    def height(self):
        return len(self.values)

    @cached_property
    def width(self):
        return len(self.values[0])

    def column(self, y):
        return [row[y] for row in self.values]

    def load(self, direction: Direction):
        if direction != Direction.NORTH:
            raise ValueError
        load = 0
        for x, row in enumerate(self.values):
            for tile in row:
                if tile == Tile.ROUNDED:
                    load += self.height - x
        return load

    def display(self):
        for row in self.values:
            print("".join(labels[tile] for tile in row))

    def tilt(self, direction: Direction):
        if direction == Direction.NORTH:
            for y in range(self.width):
                for x in range(self.height):
                    if self.values[x][y] == Tile.ROUNDED:
                        for i in range(x - 1, -1, -1):
                            tile = self.values[i][y]
                            if tile == Tile.CUBE or tile == Tile.ROUNDED:
                                x_stop = i
                                break
                        else:
                            x_stop = -1
                        if x_stop < x - 1:
                            self.values[x_stop + 1][y] = Tile.ROUNDED
                            self.values[x][y] = Tile.EMPTY
        if direction == Direction.SOUTH:
            for y in range(self.width):
                for x in range(self.height - 1, -1, -1):
                    if self.values[x][y] == Tile.ROUNDED:
                        for i in range(x + 1, self.height):
                            tile = self.values[i][y]
                            if tile == Tile.CUBE or tile == Tile.ROUNDED:
                                x_stop = i
                                break
                        else:
                            x_stop = self.height
                        if x_stop > x + 1:
                            self.values[x_stop - 1][y] = Tile.ROUNDED
                            self.values[x][y] = Tile.EMPTY
        if direction == Direction.EAST:
            for x in range(self.height):
                for y in range(self.width - 1, -1, -1):
                    if self.values[x][y] == Tile.ROUNDED:
                        for i in range(y + 1, self.width):
                            tile = self.values[x][i]
                            if tile == Tile.CUBE or tile == Tile.ROUNDED:
                                y_stop = i
                                break
                        else:
                            y_stop = self.width
                        if y_stop > y + 1:
                            self.values[x][y_stop - 1] = Tile.ROUNDED
                            self.values[x][y] = Tile.EMPTY
        if direction == Direction.WEST:
            for x in range(self.height):
                for y in range(self.width):
                    if self.values[x][y] == Tile.ROUNDED:
                        for i in range(y - 1, -1, -1):
                            tile = self.values[x][i]
                            if tile == Tile.CUBE or tile == Tile.ROUNDED:
                                y_stop = i
                                break
                        else:
                            y_stop = -1
                        if y_stop < y - 1:
                            self.values[x][y_stop + 1] = Tile.ROUNDED
                            self.values[x][y] = Tile.EMPTY


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return Grid([[Tile.from_str(char) for char in row] for row in content.split("\n")])


def main1(grid: Grid):
    grid.display()
    grid.tilt(Direction.NORTH)
    print("\n")
    grid.display()
    return grid.load(Direction.NORTH)


def main2(grid: Grid):
    known_grids = {}
    grid_by_id = []
    for i in range(1_000_000_000):
        grid.tilt(Direction.NORTH)
        grid.tilt(Direction.WEST)
        grid.tilt(Direction.SOUTH)
        grid.tilt(Direction.EAST)

        # grid.display()
        # print("\n")

        id_ = grid.identifier
        # print("id_", id_)
        if id_ in known_grids:
            last_idx = known_grids[id_]
            cycle = i - last_idx

            offset = (1_000_000_000 - i - 1) % cycle
            result_idx = i - (cycle - offset)

            grid = Grid.from_id(grid_by_id[result_idx], grid.width)
            return grid.load(Direction.NORTH)

        known_grids[id_] = i
        grid_by_id.append(id_)

    return grid.load(Direction.NORTH)
    pass


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)

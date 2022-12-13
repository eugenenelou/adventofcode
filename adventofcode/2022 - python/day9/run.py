import re
import sys
from functools import lru_cache
from pathlib import Path
from pprint import pprint
from tkinter import scrolledtext


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    for line in content.split('\n'):
        a, b = line.split(' ')
        yield a, int(b)

def main1(instructions):
    # grid = [[True]]
    head = (0, 0)
    tail = (0, 0)
    results = set()
    
    # def extend(direction, steps):
    #     nonlocal grid
    #     nonlocal head
    #     nonlocal tail
    #     match direction:
    #         case 'U':
    #             n = steps - head[0]
    #             if n > 0:
    #                 cols = len(grid[0])
    #                 grid = [[False] * cols] + grid
    #                 head = (head[0] + n, head[1])
    #                 tail = (tail[0] + n, tail[1])
    #         case 'D':
    #             n = steps - len(grid) + 1 + head[0]
    #             if n > 0:
    #                 cols = len(grid[0])
    #                 grid = grid - [[False] * cols]
    #         case 'R':
    #             n = steps - len(grid[0]) + 1 + head[1]
    #             if n > 0:
    #                 grid = [row + [False] * n for row in grid]
    #         case 'L':
    #             n = steps - head[1]
    #             if n > 0:
    #                 grid = [[False] * n+ row for row in grid]
    #                 head = (head[0], head[1] + n)
    #                 tail = (tail[0], tail[1]+ n)

    def move(direction):
        nonlocal head
        nonlocal tail
        x, y = head
        a, b = tail
        match direction:
            case 'U':
                head = (x-1, y)
            case 'D':
                head = (x+1, y)
            case 'L':
                head = (x, y-1)
            case 'R':
                head = (x, y+1)
        
        x, y = head
        delta_row, delta_col = x - a, y - b
        
        move_row = 0
        move_col = 0
        
        if abs(delta_row) > 1:
            move_row = 1 if delta_row > 0 else -1
        elif abs(delta_row) > 0 and abs(delta_col) > 1:
            move_row = 1 if delta_row > 0 else -1
        if abs(delta_col) > 1:
            move_col = 1 if delta_col > 0 else -1
        elif abs(delta_col) > 0 and abs(delta_row) > 1:
            move_col = 1 if delta_col > 0 else -1
            
        tail = (a + move_row, b + move_col)



    for direction, steps in instructions:
        # extend(direction, steps)
        for i in range(steps):
            move(direction)
            # print('head', head, 'tail', tail)
            results.add(tail)
            
    return len(results)

def main2(instructions):
    # grid = [[True]]
    knots = [(0,0) ]*10
    results = set()


    def move(direction, head, tail):
        # print('move', head, tail)
        x, y = head
        a, b = tail
        match direction:
            case 'U':
                head = (x-1, y)
            case 'D':
                head = (x+1, y)
            case 'L':
                head = (x, y-1)
            case 'R':
                head = (x, y+1)
            case _:
                pass

        x, y = head
        delta_row, delta_col = x - a, y - b

        move_row = 0
        move_col = 0
        
        # print('delta_row', delta_row)
        # print('delta_col', delta_col)

        if abs(delta_row) > 1:
            move_row = 1 if delta_row > 0 else -1
        elif abs(delta_row) > 0 and abs(delta_col) > 1:
            move_row = 1 if delta_row > 0 else -1
        if abs(delta_col) > 1:
            move_col = 1 if delta_col > 0 else -1
        elif abs(delta_col) > 0 and abs(delta_row) > 1:
            move_col = 1 if delta_col > 0 else -1

        tail = (a + move_row, b + move_col)
        
        # print('result', head, tail)
        # print('')
        return head, tail



    for direction, steps in instructions:
        for _ in range(steps):
            print(knots)
            for i in range(len(knots) - 1):
                head, tail = knots[i:i+2]
                knots[i], knots[i+1] = move(direction if i == 0 else None, head, tail)
            results.add(knots[-1])
        print('\n\n')
    return len(results)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)

use std::env;
use std::fs;

#[derive(PartialEq, Debug, Copy, Clone)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

#[derive(PartialEq, Debug, Copy, Clone)]
enum Cell {
    Horizontal,
    Vertical,
    ChangeDirection(Direction, Direction), // (left-right, up-down)
    Letter(char),
    Empty,
}

fn parse_input(file_path: &String) -> ((usize, usize), Vec<Vec<Cell>>) {
    let mut grid: Vec<Vec<Cell>> = fs::read_to_string(file_path)
        .expect("Cannot read file")
        .split("\r\n")
        .map(|row| {
            row.chars()
                .map(|c| match c {
                    '|' => Cell::Vertical,
                    '-' => Cell::Horizontal,
                    '+' => Cell::ChangeDirection(Direction::Left, Direction::Up),
                    ' ' => Cell::Empty,
                    letter => Cell::Letter(letter),
                })
                .collect()
        })
        .collect();
    let height = grid.len();
    let width = grid[0].len();
    for i in 0..(height - 1) {
        let (until_row, from_next_row) = grid.split_at_mut(i + 1);
        let row = until_row.last_mut().unwrap();
        let next_row = &from_next_row[0];
        for j in 0..width {
            if let Cell::ChangeDirection(_, _) = row[j] {
                let mut horizontal = Direction::Left;
                let mut vertical = Direction::Up;
                let mut changed = false;
                if row[j + 1] != Cell::Empty {
                    horizontal = Direction::Right;
                    changed = true;
                }
                if next_row[j] != Cell::Empty {
                    vertical = Direction::Down;
                    changed = true
                }
                if changed {
                    row[j] = Cell::ChangeDirection(horizontal, vertical);
                }
            }
        }
    }
    let mut y: usize = 0;
    for (idx, cell) in grid[0].iter().enumerate() {
        match cell {
            Cell::Vertical => {
                y = idx;
                break;
            }
            _ => (),
        }
    }
    ((0, y), grid)
}

fn run(start: (usize, usize), grid: Vec<Vec<Cell>>) -> (String, i32) {
    let mut direction = Direction::Down;
    let (mut x, mut y) = start;
    let mut current = grid[x][y];
    let mut encountered_letters: Vec<char> = vec![];
    let mut steps = 0;
    while current != Cell::Empty {
        steps += 1;
        match direction {
            Direction::Down => {
                x += 1;
            }
            Direction::Left => {
                y -= 1;
            }
            Direction::Up => {
                x -= 1;
            }
            Direction::Right => {
                y += 1;
            }
        };
        current = grid[x][y];
        match current {
            Cell::Empty => break,
            Cell::Letter(letter) => {
                encountered_letters.push(letter);
            }
            Cell::ChangeDirection(hor, ver) => {
                direction = match direction {
                    Direction::Down | Direction::Up => hor,
                    Direction::Left | Direction::Right => ver,
                }
            }
            _ => (),
        }
    }
    (encountered_letters.iter().collect(), steps)
}

fn run1(start: (usize, usize), grid: Vec<Vec<Cell>>) -> String {
    run(start, grid).0
}

fn run2(start: (usize, usize), grid: Vec<Vec<Cell>>) -> i32 {
    run(start, grid).1
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");
    let (start, grid) = parse_input(file_path);

    if is_part_two {
        println!("Result 2 is {}", run2(start, grid))
    } else {
        println!("Result 1 is {}", run1(start, grid))
    }
}

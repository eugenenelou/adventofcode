use std::collections::HashSet;
use std::env;
use std::fs;
fn parse_input(file_path: &String) -> (HashSet<String>, isize) {
    let mut infected_nodes: HashSet<String> = HashSet::new();
    let content = fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned();
    content.lines().enumerate().for_each(|(i, line)| {
        line.chars().enumerate().for_each(|(j, char_)| {
            if char_ == '#' {
                let key = format!("{},{}", i, j);
                infected_nodes.insert(key);
            }
        })
    });
    (
        infected_nodes,
        content.lines().into_iter().next().unwrap().len() as isize,
    )
}

enum Direction {
    Up,
    Right,
    Down,
    Left,
}

impl Direction {
    fn turn_left(&self) -> Self {
        match *self {
            Direction::Up => Direction::Left,
            Direction::Right => Direction::Up,
            Direction::Down => Direction::Right,
            Direction::Left => Direction::Down,
        }
    }
    fn turn_right(&self) -> Self {
        match *self {
            Direction::Up => Direction::Right,
            Direction::Right => Direction::Down,
            Direction::Down => Direction::Left,
            Direction::Left => Direction::Up,
        }
    }

    fn move_forward(&self, position: (isize, isize)) -> (isize, isize) {
        match *self {
            Direction::Up => (position.0 - 1, position.1),
            Direction::Right => (position.0, position.1 + 1),
            Direction::Down => (position.0 + 1, position.1),
            Direction::Left => (position.0, position.1 - 1),
        }
    }
}

fn run1(mut infected_nodes: HashSet<String>, size: isize) -> u32 {
    let mut position = (size / 2, size / 2);
    let mut direction = Direction::Up;
    let mut count = 0;
    let mut key = format!("{},{}", position.0, position.1);

    for _ in 0..10000 {
        direction = if infected_nodes.remove(&key) {
            direction.turn_right()
        } else {
            infected_nodes.insert(key);
            count += 1;
            direction.turn_left()
        };
        position = direction.move_forward(position);
        key = format!("{},{}", position.0, position.1);
    }

    count
}

fn run2(mut infected_nodes: HashSet<String>, size: isize) -> u32 {
    let mut weakened_nodes: HashSet<String> = HashSet::new();
    let mut flagged_nodes: HashSet<String> = HashSet::new();

    let mut position = (size / 2, size / 2);
    let mut direction = Direction::Up;
    let mut count = 0;
    let mut key = format!("{},{}", position.0, position.1);

    for _ in 0..10000000 {
        direction = if infected_nodes.remove(&key) {
            flagged_nodes.insert(key);
            direction.turn_right()
        } else if weakened_nodes.remove(&key) {
            infected_nodes.insert(key);
            count += 1;
            direction
        } else if flagged_nodes.remove(&key) {
            direction.turn_left().turn_left()
        } else {
            weakened_nodes.insert(key);
            direction.turn_left()
        };

        position = direction.move_forward(position);
        key = format!("{},{}", position.0, position.1);
    }

    count
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");
    let (nodes, size) = parse_input(file_path);

    if is_part_two {
        println!("Result 2 is {}", run2(nodes, size))
    } else {
        println!("Result 1 is {}", run1(nodes, size))
    }
}

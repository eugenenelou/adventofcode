use std::env;
use std::fs;
fn parse_input(file_path: &String) -> String {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
}

fn run1(_input: String) -> u32 {
    let mut score = 0;
    let mut depth = 0;
    let mut in_garbage = false;
    let mut is_cancelled = false;
    for char_ in _input.chars() {
        if is_cancelled {
            is_cancelled = false;
            continue;
        }
        match (char_, in_garbage) {
            ('!', _) => {
                is_cancelled = true;
            }
            ('>', true) => {
                in_garbage = false;
            }
            (_, true) => {}
            ('<', _) => {
                in_garbage = true;
            }
            ('{', _) => {
                depth += 1;
            }
            ('}', _) => {
                score += depth;
                depth -= 1;
            }
            (_, _) => {}
        }
    }
    score
}

fn run2(_input: String) -> u32 {
    let mut score = 0;
    let mut in_garbage = false;
    let mut is_cancelled = false;
    for char_ in _input.chars() {
        if is_cancelled {
            is_cancelled = false;
            continue;
        }
        match (char_, in_garbage) {
            ('!', _) => {
                is_cancelled = true;
            }
            ('>', true) => {
                in_garbage = false;
            }
            (_, true) => score += 1,
            ('<', _) => {
                in_garbage = true;
            }
            (_, _) => {}
        }
    }
    score
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");
    let input = parse_input(file_path);

    if is_part_two {
        println!("Result 2 is {}", run2(input))
    } else {
        println!("Result 1 is {}", run1(input))
    }
}

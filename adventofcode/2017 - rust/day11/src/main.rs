use std::env;
use std::fs;
fn parse_input(file_path: &String) -> Vec<String> {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .split(",")
        .map(|word| word.to_owned())
        .collect()
}

fn run1(_input: Vec<String>) -> i32 {
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    for direction in _input {
        match direction.as_str() {
            "n" => {
                y -= 2;
            }
            "ne" => {
                y -= 1;
                x += 1;
            }
            "se" => {
                y += 1;
                x += 1;
            }
            "s" => {
                y += 2;
            }
            "sw" => {
                y += 1;
                x -= 1;
            }
            "nw" => {
                y -= 1;
                x -= 1;
            }
            _ => panic!("Unrecognized direction {}", direction),
        }
    }
    x = x.abs();
    y = y.abs();
    if x > y {
        return x;
    }
    return x + (y - x) / 2;
}

fn run2(_input: Vec<String>) -> i32 {
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut maxi = 0;
    for direction in _input {
        match direction.as_str() {
            "n" => {
                y -= 2;
            }
            "ne" => {
                y -= 1;
                x += 1;
            }
            "se" => {
                y += 1;
                x += 1;
            }
            "s" => {
                y += 2;
            }
            "sw" => {
                y += 1;
                x -= 1;
            }
            "nw" => {
                y -= 1;
                x -= 1;
            }
            _ => panic!("Unrecognized direction {}", direction),
        }

        let ax = x.abs();
        let ay = y.abs();
        let current_distance;
        if ax > ay {
            current_distance = ax;
        } else {
            current_distance = ax + (ay - ax) / 2;
        }
        if current_distance > maxi {
            maxi = current_distance
        }
    }
    maxi
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

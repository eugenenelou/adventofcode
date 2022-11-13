use std::env;
use std::fs;
fn parse_input(file_path: &String) -> Vec<u32> {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .chars()
        .map(|c| c.to_digit(10).unwrap())
        .collect()
}

fn run1(digits: Vec<u32>) -> u32 {
    let mut result = 0;
    for i in 0..digits.len() - 1 {
        if digits[i] == digits[i + 1] {
            result += digits[i];
        }
    }
    if digits.first() == digits.last() {
        result += digits[0]
    }
    result
}

fn run2(digits: Vec<u32>) -> u32 {
    let half = digits.len() / 2;
    let mut results = 0;
    for i in 0..half {
        if digits[i] == digits[i + half] {
            results += 2 * digits[i];
        }
    }
    results
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

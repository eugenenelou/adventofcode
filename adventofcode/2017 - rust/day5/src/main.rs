use std::env;
use std::fs;

fn parse_input(file_path: &String) -> Vec<i32> {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .lines()
        .map(|line| line.parse::<i32>().unwrap())
        .collect()
}

fn run1(mut input: Vec<i32>) -> u32 {
    let mut idx: i32 = 0;
    let n = input.len() as i32;
    let mut steps = 0;
    while idx >= 0 && idx < n {
        let new_idx = idx + input[idx as usize];
        input[idx as usize] += 1;
        idx = new_idx.try_into().unwrap();
        steps += 1;
    }
    steps
}

fn run2(mut input: Vec<i32>) -> u32 {
    let mut idx: i32 = 0;
    let n = input.len() as i32;
    let mut steps = 0;
    while idx >= 0 && idx < n {
        let offset = input[idx as usize];
        let new_idx = idx + offset;
        if offset > 2 {
            input[idx as usize] -= 1;
        } else {
            input[idx as usize] += 1;
        }
        idx = new_idx.try_into().unwrap();
        steps += 1;
    }
    steps
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

use std::env;
use std::fs;
fn parse_input(file_path: &String) -> String {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
}

fn run1(_input: String) -> u32 {
    0
}

fn run2(_input: String) -> u32 {
    0
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

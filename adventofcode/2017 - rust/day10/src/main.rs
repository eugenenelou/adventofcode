use std::env;
use std::fs;
fn parse_input(file_path: &String) -> Vec<usize> {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .split(',')
        .map(|raw| raw.parse::<usize>().unwrap())
        .collect()
}

fn parse_input_2(file_path: &String) -> Vec<usize> {
    let mut input_: Vec<usize> = fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .chars()
        .map(|raw| (raw as u8) as usize)
        .collect();
    input_.extend_from_slice(&[17, 31, 73, 47, 23]);
    input_
}
const SIZE: usize = 256;

fn run1(_input: Vec<usize>) -> usize {
    let mut values: Vec<usize> = (0..SIZE).collect();
    let mut skip = 0;
    let mut position = 0;
    for range in _input {
        // swap first with last, second with second to last ...
        let swap_count = range / 2;
        for i in 0..swap_count {
            values.swap(
                (position + i) % SIZE,
                (position + range - 1 - i + SIZE) % SIZE,
            );
        }
        position = (position + range + skip) % SIZE;
        skip += 1;
    }
    values[0] * values[1]
}

fn run2(_input: Vec<usize>) -> String {
    let mut values: Vec<usize> = (0..SIZE).collect();
    let mut skip = 0;
    let mut position = 0;
    for _ in 0..64 {
        for range in _input.iter() {
            // swap first with last, second with second to last ...
            let swap_count = range / 2;
            for i in 0..swap_count {
                values.swap(
                    (position + i) % SIZE,
                    (position + range - 1 - i + SIZE) % SIZE,
                );
            }
            position = (position + range + skip) % SIZE;
            skip += 1;
        }
    }
    let mut dense_numbers = Vec::<usize>::with_capacity(16);
    for i in 0..16 {
        let mut dense = 0;
        for j in 0..16 {
            dense = dense ^ values[i * 16 + j];
        }
        dense_numbers.push(dense);
    }
    dense_numbers
        .iter()
        .map(|number| format!("{:02x}", number))
        .collect::<Vec<_>>()
        .join("")
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");

    if is_part_two {
        println!("Result 2 is {}", run2(parse_input_2(file_path)))
    } else {
        println!("Result 1 is {}", run1(parse_input(file_path)))
    }
}

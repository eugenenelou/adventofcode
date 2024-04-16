use core::panic;
use std::collections::HashMap;
use std::env;
use std::fs;

const NAMES: &str = "abcdefghijklmnop";
// const SIZE: usize = 5;
const SIZE: usize = 16;

enum Operation {
    Spin(usize),
    Exchange(usize, usize),
    Partner(char, char),
}

fn parse_input(file_path: &String) -> (Vec<char>, Vec<Operation>) {
    let operations = fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
        .split(",")
        .map(
            |raw_operation| match raw_operation.chars().nth(0).unwrap() {
                's' => Operation::Spin(raw_operation[1..].parse().unwrap()),
                'x' => {
                    let mut iter = raw_operation[1..].split("/");
                    let a: usize = iter.next().unwrap().parse().unwrap();
                    let b: usize = iter.next().unwrap().parse().unwrap();
                    Operation::Exchange(a, b)
                }
                'p' => {
                    let mut iter = raw_operation[1..].split("/");
                    let a = iter.next().unwrap().chars().nth(0).unwrap();
                    let b = iter.next().unwrap().chars().nth(0).unwrap();
                    Operation::Partner(a, b)
                }
                _ => panic!("Unexpected operation: {}", raw_operation),
            },
        )
        .collect();

    let programs = NAMES.chars().take(SIZE).collect();
    (programs, operations)
}

fn swap(mut values: Vec<char>, i: usize, j: usize) -> Vec<char> {
    let a = values[i];
    values[i] = values[j];
    values[j] = a;
    values
}

fn run1(mut programs: Vec<char>, operations: &Vec<Operation>) -> Vec<char> {
    for operation in operations {
        match operation {
            Operation::Spin(n) => {
                programs = (0..SIZE).map(|i| programs[(i + SIZE - n) % SIZE]).collect()
            }
            Operation::Exchange(i, j) => {
                programs = swap(programs, *i, *j);
            }
            Operation::Partner(a, b) => {
                let mut first: Option<usize> = None;
                for j in 0..SIZE {
                    let value = programs[j];
                    if value == *a || value == *b {
                        match first {
                            Some(i) => programs = swap(programs, i, j),
                            None => first = Some(j),
                        }
                    }
                }
            }
        }
    }
    programs
}

fn run2(mut programs: Vec<char>, operations: Vec<Operation>) -> String {
    let mut known_words: HashMap<String, usize> = HashMap::new();
    let mut i: usize = 0;
    loop {
        i += 1;
        programs = run1(programs, &operations);
        let word = programs.iter().collect::<String>();
        if let Some(start_idx) = known_words.get(&word) {
            let cycle_len = i - start_idx;
            let last_cycle_len = (1000000000 - i) % cycle_len;
            let result_idx = i - cycle_len + last_cycle_len;
            for (word, idx) in known_words.into_iter() {
                if idx == result_idx {
                    return word;
                }
            }
            panic!("idx {} not found in hash map", result_idx);
        } else {
            known_words.insert(word, i);
        }
    }
}
fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");
    let (programs, operations) = parse_input(file_path);

    if is_part_two {
        println!("Result 2 is {}", run2(programs, operations))
    } else {
        println!(
            "Result 1 is {}",
            run1(programs, &operations).iter().collect::<String>()
        )
    }
}

use std::env;
use std::fs;
fn parse_input(file_path: &String) -> Vec<Vec<u32>> {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .lines()
        .map(|line| {
            line.trim()
                .split(" ")
                .map(|c| c.parse::<u32>().unwrap())
                .collect()
        })
        .collect()
}

fn run1(input: Vec<Vec<u32>>) -> u32 {
    input.into_iter().fold(0, |sum: u32, row| {
        sum + {
            let (min, max) =
                row.into_iter()
                    .fold((u32::MAX, 0), |(mut min, mut max): (u32, u32), n| {
                        if n < min {
                            min = n;
                        }
                        if n > max {
                            max = n;
                        }
                        (min, max)
                    });
            max - min
        }
    })
}

fn run2(input: Vec<Vec<u32>>) -> u32 {
    input.into_iter().fold(0, |sum: u32, row| {
        sum + {
            let mut result: u32 = 0;
            'outer: for i in 0..row.len() {
                for j in i + 1..row.len() {
                    let a = row[i];
                    let b = row[j];
                    if a % b == 0 {
                        result = a / b;
                        break 'outer;
                    }
                    if b % a == 0 {
                        result = b / a;
                        break 'outer;
                    }
                }
            }
            result
        }
    })
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

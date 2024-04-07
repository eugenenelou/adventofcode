use std::env;
use std::fs;
fn parse_input(file_path: &String) -> Vec<(u32, u32)> {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .split("\r\n")
        .map(|raw| {
            let mut iter = raw.split(": ");
            let idx: u32 = iter.next().unwrap().parse().unwrap();
            let range: u32 = iter.next().unwrap().parse().unwrap();
            (idx, range)
        })
        .collect()
}

fn run1(_input: Vec<(u32, u32)>) -> u32 {
    _input
        .into_iter()
        .map(|(idx, range)| {
            if (idx % ((range - 1) * 2)) == 0 {
                idx * range
            } else {
                0
            }
        })
        .sum()
}

fn run2(mut _input: Vec<(u32, u32)>) -> u32 {
    let mut i = 0;
    loop {
        if _input.iter().all(|(idx, _)| *idx != 0) {
            return i;
        }
        for i in 0.._input.len() {
            let (idx, range) = _input[i];
            _input[i] = ((idx + 1) % ((range - 1) * 2), range);
        }
        i += 1;
    }
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

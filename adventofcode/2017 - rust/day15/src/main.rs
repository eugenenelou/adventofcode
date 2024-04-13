use std::env;
use std::fs;

fn parse_input(file_path: &String) -> (u64, u64) {
    let binding = fs::read_to_string(file_path).expect("Cannot read file");
    let mut iter = binding.trim().split("\r\n").map(|v| v.parse::<u64>());
    let a = iter.next().unwrap().unwrap();
    let b = iter.next().unwrap().unwrap();
    (a, b)
}

fn generate_a(n: u64) -> u64 {
    (n * 16807) % 2147483647
}

fn generate_b(n: u64) -> u64 {
    (n * 48271) % 2147483647
}

fn last_16_bits_match(a: u64, b: u64) -> bool {
    (a % 2u64.pow(16)) == (b % 2u64.pow(16))
}

fn run1(_input: (u64, u64)) -> u64 {
    let (mut a, mut b) = _input;
    let mut res: u64 = 0;
    for _ in 0..40000000 {
        a = generate_a(a);
        b = generate_b(b);
        if last_16_bits_match(a, b) {
            res += 1;
        }
    }
    res
}

fn generate_a_2(n: u64) -> u64 {
    let mut res = n;
    loop {
        res = (res * 16807) % 2147483647;
        if res % 4 == 0 {
            return res;
        }
    }
}

fn generate_b_2(n: u64) -> u64 {
    let mut res = n;
    loop {
        res = (res * 48271) % 2147483647;
        if res % 8 == 0 {
            return res;
        }
    }
}

fn run2(_input: (u64, u64)) -> u64 {
    let (mut a, mut b) = _input;
    let mut res: u64 = 0;
    for _ in 0..5000000 {
        a = generate_a_2(a);
        b = generate_b_2(b);
        if last_16_bits_match(a, b) {
            res += 1;
        }
    }
    res
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

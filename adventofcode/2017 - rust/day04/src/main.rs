use std::collections::HashSet;
use std::env;
use std::fs;

fn is_valid_passphrase_1(passphrase: &str) -> bool {
    let words: Vec<&str> = passphrase.split(" ").collect();
    let unique_words: HashSet<&str> = passphrase.split(" ").collect();
    words.len() == unique_words.len()
}

fn is_valid_passphrase_2(passphrase: &str) -> bool {
    let words: Vec<&str> = passphrase.split(" ").collect();
    let unique_words: HashSet<String> = passphrase
        .split(" ")
        .map(|word| {
            let mut letters = word.chars().collect::<Vec<_>>();
            letters.sort_unstable();
            letters.iter().collect::<String>()
        })
        .collect();
    words.len() == unique_words.len()
}

fn run1(file_path: &String) -> u32 {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .lines()
        .fold(0, |sum, line| sum + is_valid_passphrase_1(line) as u32)
}

fn run2(file_path: &String) -> u32 {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .lines()
        .fold(0, |sum, line| sum + is_valid_passphrase_2(line) as u32)
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");
    if is_part_two {
        println!("Result 2 is {}", run2(file_path))
    } else {
        println!("Result 1 is {}", run1(file_path))
    }
}

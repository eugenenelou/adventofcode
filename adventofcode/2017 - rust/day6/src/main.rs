use std::collections::HashMap;
use std::env;

fn hash_vec(configuration: &Vec<u8>) -> String {
    configuration.iter().map(|n| *n as char).collect::<String>()
}

fn redistribute(mut configuration: Vec<u8>) -> Vec<u8> {
    let n = configuration.len();
    // rev the vec because max_by_key return the last in case of equality but we want the first
    let (idx, &max) = configuration
        .iter()
        .rev()
        .enumerate()
        .map(|(idx, val)| (n - 1 - idx, val))
        .max_by_key(|(_idx, &val)| val)
        .unwrap();
    configuration[idx] = 0;
    for i in idx + 1..idx + 1 + (max as usize) {
        configuration[i % n] += 1;
    }
    configuration
}

fn run(second_part: bool) -> u32 {
    // let mut configuration: Vec<u8> = vec![0, 2, 7, 0];
    let mut configuration: Vec<u8> = vec![0, 5, 10, 0, 11, 14, 13, 4, 11, 8, 8, 7, 1, 4, 12, 11];
    let mut known_configurations = HashMap::new();
    let mut i = 0;
    loop {
        println!("configuration: {:?}", configuration);
        configuration = redistribute(configuration);
        i += 1;
        let hash = hash_vec(&configuration);
        if known_configurations.contains_key(&hash) {
            if second_part {
                return i - *known_configurations.get(&hash).unwrap();
            }
            break;
        }
        known_configurations.insert(hash, i);
    }
    i
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let is_part_two = args.len() > 2 && args[2].eq("--two");

    println!("Result is {}", run(is_part_two))
}

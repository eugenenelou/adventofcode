use regex::Regex;
use std::env;
use std::fs;

#[derive(Debug)]
struct Vector {
    x: i32,
    y: i32,
    z: i32,
}

fn parse_input(file_path: &String) -> Vec<Vector> {
    let input_regex: Regex = Regex::new(r"a=<(-?\d+),(-?\d+),(-?\d+)>").unwrap();
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
        .split("\r\n")
        .map(|line| {
            let accelerations = input_regex.captures(line).unwrap();
            let ax: i32 = accelerations.get(1).unwrap().as_str().parse().unwrap();
            let ay: i32 = accelerations.get(2).unwrap().as_str().parse().unwrap();
            let az: i32 = accelerations.get(3).unwrap().as_str().parse().unwrap();
            Vector {
                x: ax,
                y: ay,
                z: az,
            }
        })
        .collect()
}

fn run1(_input: Vec<Vector>) -> usize {
    // max of Ax^2 + Ay^2 + Az^2
    let distances: Vec<(usize, i32)> = _input
        .iter()
        .enumerate()
        .map(|(idx, vector)| (idx, vector.x.abs() + vector.y.abs() + vector.z.abs()))
        .collect();
    println!("{:?}", distances);
    let mini = _input
        .iter()
        .enumerate()
        .map(|(idx, vector)| (idx, vector.x.abs() + vector.y.abs() + vector.z.abs()))
        .min_by_key(|(_, d)| *d)
        .unwrap();
    for (idx, distance) in distances {
        if distance == mini.1 {
            println!("idx: {} is mini", idx);
        }
    }
    // we can try the few solutions one by one.
    // if we wanted to be exact we could just compute the distance for a high value of time
    // and take the smaller one.
    mini.0
}

fn run2(_input: Vec<Vector>) -> u32 {
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

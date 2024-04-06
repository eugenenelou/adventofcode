use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Debug)]
enum Condition {
    GT,
    GE,
    LT,
    LE,
    EQ,
    NE,
}

fn condition_from_string(raw: &str) -> Condition {
    match raw {
        "<=" => Condition::LE,
        "<" => Condition::LT,
        ">=" => Condition::GE,
        ">" => Condition::GT,
        "==" => Condition::EQ,
        "!=" => Condition::NE,
        _ => panic!("Unrecognized condition: {}", raw),
    }
}

impl Condition {
    fn check(&self, registry_value: i32, value: i32) -> bool {
        match self {
            Condition::GT => registry_value > value,
            Condition::GE => registry_value >= value,
            Condition::LT => registry_value < value,
            Condition::LE => registry_value <= value,
            Condition::EQ => registry_value == value,
            Condition::NE => registry_value != value,
        }
    }
}

#[derive(Debug)]
struct Operation {
    registry: String,
    diff: i32,
    condition_registry: String,
    condition: Condition,
    condition_value: i32,
}

fn parse_input(file_path: &String) -> Vec<Operation> {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .split("\r\n")
        .map(|line| {
            let elements: Vec<&str> = line.split(" ").collect();
            Operation {
                registry: elements[0].to_string(),
                diff: elements[2].parse::<i32>().unwrap()
                    * (if elements[1] == "inc" { 1 } else { -1 }),
                condition_registry: elements[4].to_string(),
                condition: condition_from_string(elements[5]),
                condition_value: elements[6].parse().unwrap(),
            }
        })
        .collect()
}

fn run1(_input: Vec<Operation>) -> i32 {
    let mut registries: HashMap<&String, i32> = HashMap::new();
    _input.iter().for_each(|operation| {
        let current_value = *registries.entry(&operation.condition_registry).or_default();
        if operation
            .condition
            .check(current_value, operation.condition_value)
        {
            let new_value = *registries.entry(&operation.registry).or_default() + operation.diff;
            registries.insert(&operation.registry, new_value);
        }
    });
    *registries.values().max().unwrap()
}

fn run2(_input: Vec<Operation>) -> i32 {
    let mut registries: HashMap<&String, i32> = HashMap::new();
    let mut highest: i32 = 0;
    _input.iter().for_each(|operation| {
        let current_value = *registries.entry(&operation.condition_registry).or_default();
        if operation
            .condition
            .check(current_value, operation.condition_value)
        {
            let new_value = *registries.entry(&operation.registry).or_default() + operation.diff;
            if new_value > highest {
                highest = new_value
            }
            registries.insert(&operation.registry, new_value);
        }
    });
    highest
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

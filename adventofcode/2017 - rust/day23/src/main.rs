use std::collections::HashMap;
use std::env;
use std::fs;
enum Value {
    Register(String),
    Number(i64),
}

enum Instruction {
    Set(String, Value),
    Sub(String, Value),
    Mul(String, Value),
    Jnz(Value, Value),
}

fn to_value(raw: &str) -> Value {
    match raw.parse::<i64>() {
        Ok(n) => Value::Number(n),
        Err(_) => Value::Register(raw.to_string()),
    }
}

fn parse_input(file_path: &String) -> Vec<Instruction> {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .lines()
        .map(|row| {
            let mut iter = row.split(" ");
            match iter.next().unwrap() {
                "set" => Instruction::Set(
                    iter.next().unwrap().to_string(),
                    to_value(iter.next().unwrap()),
                ),
                "sub" => Instruction::Sub(
                    iter.next().unwrap().to_string(),
                    to_value(iter.next().unwrap()),
                ),
                "mul" => Instruction::Mul(
                    iter.next().unwrap().to_string(),
                    to_value(iter.next().unwrap()),
                ),
                "jnz" => Instruction::Jnz(
                    to_value(iter.next().unwrap()),
                    to_value(iter.next().unwrap()),
                ),
                value => panic!("unexpected instruction: {}", value),
            }
        })
        .collect()
}

fn get_value(register: &HashMap<String, i64>, value: &Value) -> i64 {
    match value {
        Value::Register(letter) => *register.get(letter).unwrap(),
        Value::Number(n) => *n,
    }
}

fn run1(instructions: Vec<Instruction>, a0: i64) -> i64 {
    let mut idx = 0;
    let mut register: HashMap<String, i64> = HashMap::new();
    for letter in "abcdefghijklmnopqrstuvwxyz".split("") {
        register.insert(letter.to_string(), 0);
    }
    register.insert(String::from("a"), a0);
    let mut count = 0;
    loop {
        if idx == instructions.len() {
            break;
        }
        println!("register: {:?}", register.values());
        match &instructions[idx] {
            Instruction::Set(x, y) => {
                register.insert(x.to_string(), get_value(&register, y));
            }
            Instruction::Sub(x, y) => {
                let y_value = get_value(&register, y);
                register.entry(x.to_string()).and_modify(|n| *n -= y_value);
            }
            Instruction::Mul(x, y) => {
                count += 1;
                let y_value = get_value(&register, y);
                register.entry(x.to_string()).and_modify(|n| *n *= y_value);
            }
            Instruction::Jnz(x, y) => {
                let y_value = get_value(&register, y);
                if get_value(&register, x) != 0 {
                    idx = (idx as isize + y_value as isize) as usize;
                    continue;
                }
            }
        }
        idx += 1;
    }
    count
}

fn is_prime(num: u64) -> bool {
    for i in 2..=(num as f64).sqrt() as u64 {
        if num % i == 0 {
            return false;
        }
    }
    true
}

fn run2(_input: Vec<Instruction>) -> u32 {
    // The algorithm counts the non-prime numbers between two numbers b and c
    let b = 105700;
    // c = b + 17000
    let mut result = 0;
    for i in 0..=1000 {
        let n = b + i * 17;
        if !is_prime(n) {
            result += 1;
        }
    }
    result
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");
    let input = parse_input(file_path);

    if is_part_two {
        println!("Result 2 is {}", run2(input))
    } else {
        println!("Result 1 is {}", run1(input, 0))
    }
}

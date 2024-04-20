use std::collections::HashMap;
use std::collections::VecDeque;
use std::env;
use std::fs;

enum Value {
    Register(String),
    Number(i64),
}

enum Instruction {
    Snd(Value),
    Set(String, Value),
    Add(String, Value),
    Mul(String, Value),
    Mod(String, Value),
    Rcv(String),
    Jgz(Value, Value),
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
        .split("\r\n")
        .map(|row| {
            let mut iter = row.split(" ");
            match iter.next().unwrap() {
                "snd" => Instruction::Snd(to_value(iter.next().unwrap())),
                "rcv" => Instruction::Rcv(iter.next().unwrap().to_string()),
                "set" => Instruction::Set(
                    iter.next().unwrap().to_string(),
                    to_value(iter.next().unwrap()),
                ),
                "add" => Instruction::Add(
                    iter.next().unwrap().to_string(),
                    to_value(iter.next().unwrap()),
                ),
                "mul" => Instruction::Mul(
                    iter.next().unwrap().to_string(),
                    to_value(iter.next().unwrap()),
                ),
                "mod" => Instruction::Mod(
                    iter.next().unwrap().to_string(),
                    to_value(iter.next().unwrap()),
                ),
                "jgz" => Instruction::Jgz(
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

fn run1(instructions: Vec<Instruction>) -> i64 {
    let mut idx = 0;
    let mut register: HashMap<String, i64> = HashMap::new();
    for letter in "abcdefghijklmnopqrstuvwxyz".split("") {
        register.insert(letter.to_string(), 0);
    }
    let mut last_sound = 0;
    loop {
        match &instructions[idx] {
            Instruction::Snd(value) => {
                last_sound = get_value(&register, value);
            }
            Instruction::Set(x, y) => {
                register.insert(x.to_string(), get_value(&register, y));
            }
            Instruction::Add(x, y) => {
                let y_value = get_value(&register, y);
                register.entry(x.to_string()).and_modify(|n| *n += y_value);
            }
            Instruction::Mul(x, y) => {
                let y_value = get_value(&register, y);
                register.entry(x.to_string()).and_modify(|n| *n *= y_value);
            }
            Instruction::Mod(x, y) => {
                let y_value = get_value(&register, y);
                register.entry(x.to_string()).and_modify(|n| *n %= y_value);
            }
            Instruction::Jgz(x, y) => {
                let y_value = get_value(&register, y);
                if get_value(&register, x) > 0 {
                    idx = (idx as isize + y_value as isize) as usize;
                    continue;
                }
            }
            Instruction::Rcv(x) => {
                if *register.get(x).unwrap() != 0 {
                    return last_sound;
                }
            }
        }
        idx += 1;
    }
}

struct Program {
    send_count: u32,
    queue: VecDeque<i64>,
    idx: usize,
    registers: HashMap<String, i64>,
    finished: bool,
    blocked: bool,
}

impl Program {
    fn run(&mut self, instructions: &Vec<Instruction>, other: &mut Program) {
        loop {
            match &instructions[self.idx] {
                Instruction::Snd(value) => {
                    other.queue.push_back(get_value(&self.registers, &value));
                    self.send_count += 1;
                    other.blocked = false;
                }
                Instruction::Set(x, y) => {
                    self.registers
                        .insert(x.to_string(), get_value(&self.registers, &y));
                }
                Instruction::Add(x, y) => {
                    let y_value = get_value(&self.registers, &y);
                    self.registers
                        .entry(x.to_string())
                        .and_modify(|n| *n += y_value);
                }
                Instruction::Mul(x, y) => {
                    let y_value = get_value(&self.registers, &y);
                    self.registers
                        .entry(x.to_string())
                        .and_modify(|n| *n *= y_value);
                }
                Instruction::Mod(x, y) => {
                    let y_value = get_value(&self.registers, &y);
                    self.registers
                        .entry(x.to_string())
                        .and_modify(|n| *n %= y_value);
                }
                Instruction::Jgz(x, y) => {
                    let y_value = get_value(&self.registers, &y);
                    if get_value(&self.registers, &x) > 0 {
                        self.idx = (self.idx as isize + y_value as isize) as usize;
                        continue;
                    }
                }
                Instruction::Rcv(x) => match self.queue.pop_front() {
                    Some(n) => {
                        self.registers.insert(x.to_string(), n);
                    }
                    None => {
                        self.blocked = true;
                        return;
                    }
                },
            }
            self.idx += 1;
            if self.idx == instructions.len() {
                self.finished = true;
                return;
            }
        }
    }
}

fn init_registers(n: i64) -> HashMap<String, i64> {
    let mut registers = HashMap::new();
    for letter in "abcdefghijklmnopqrstuvwxyz".split("") {
        registers.insert(letter.to_string(), 0);
    }
    registers.insert(String::from("p"), n);
    registers
}

fn run2(instructions: Vec<Instruction>) -> u32 {
    let mut p0 = Program {
        send_count: 0,
        queue: VecDeque::new(),
        idx: 0,
        registers: init_registers(0),
        finished: false,
        blocked: false,
    };
    let mut p1 = Program {
        send_count: 0,
        queue: VecDeque::new(),
        idx: 0,
        registers: init_registers(1),
        finished: false,
        blocked: false,
    };
    let mut is_zero_turn = true;
    while (!p0.blocked || !p1.blocked) && (!p0.finished || !p1.finished) {
        if is_zero_turn {
            p0.run(&instructions, &mut p1);
        } else {
            p1.run(&instructions, &mut p0);
        }
        is_zero_turn = !is_zero_turn;
    }
    p1.send_count
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

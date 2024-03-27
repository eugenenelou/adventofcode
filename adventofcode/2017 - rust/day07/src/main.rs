use regex::Regex;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
// use std::iter::zip;

struct Program {
    name: String,
    weight: u32,
    sub_towers: Vec<String>,
}

impl Program {
    fn from_raw(line: &str) -> Program {
        let input_regex: Regex = Regex::new(r"^(\S+) \((\d+)\)(?: -> ((\S+, )*\S+))?").unwrap();
        let cap = input_regex.captures(line).unwrap();
        let sub_towers: Vec<String> = match cap.get(3) {
            None => vec![],
            Some(s) => s.as_str().split(", ").map(|n| n.to_string()).collect(),
        };
        let name = cap[1].to_string();
        return Program {
            name: name,
            weight: cap[2].parse::<u32>().unwrap(),
            sub_towers,
        };
    }
}

fn parse_input(file_path: &String) -> Vec<Program> {
    fs::read_to_string(file_path)
        .expect(format!("Cannot read file: {}", file_path).as_str())
        .trim()
        .to_owned()
        .split("\n")
        .map(Program::from_raw)
        .collect()
}

fn run1(programs: &Vec<Program>) -> String {
    let mut all_programs = HashMap::new();
    let mut all_non_bottom_programs = HashSet::new();
    for program in programs {
        for sub_name in program.sub_towers.iter() {
            all_non_bottom_programs.insert(sub_name.clone());
        }
        all_programs.insert(program.name.clone(), program);
    }
    let mut root_programs = HashSet::from_iter(all_programs.keys().into_iter().map(|s| s.clone()))
        .difference(&all_non_bottom_programs)
        .map(|s| s.clone())
        .collect::<Vec<String>>();
    if root_programs.len() > 1 {
        panic!("Found more than 1 bottom programs: {:?}", root_programs);
    }
    let root_program_name = root_programs.pop().unwrap();
    all_programs
        .remove(&root_program_name)
        .unwrap()
        .name
        .clone()
}

#[derive(Debug)]
enum BalanceResult {
    OK(u32),
    Unbalanced(u32),
}

impl BalanceResult {
    fn unwrap(&self) -> u32 {
        match self {
            BalanceResult::OK(n) => *n,
            BalanceResult::Unbalanced(_) => panic!("Failed to unwrap"),
        }
    }
}

fn check_balance(tower: &HashMap<String, Program>, program_name: &str) -> BalanceResult {
    let program = tower.get(program_name).unwrap();
    match program.sub_towers.len() {
        0 => BalanceResult::OK(program.weight),
        1 => {
            let sub_balance = check_balance(&tower, &program.sub_towers[0]);
            match sub_balance {
                BalanceResult::Unbalanced(_) => return sub_balance,
                BalanceResult::OK(weight) => return BalanceResult::OK(program.weight + weight),
            }
        }
        _ => {
            let sub_weights: Vec<BalanceResult> = program
                .sub_towers
                .iter()
                .map(|name| check_balance(tower, name))
                .collect();
            for sub_weight in sub_weights.iter() {
                match sub_weight {
                    BalanceResult::Unbalanced(weight) => return BalanceResult::Unbalanced(*weight),
                    BalanceResult::OK(_) => (),
                }
            }
            let first_weight = sub_weights[0].unwrap();
            if sub_weights
                .iter()
                .all(|result| result.unwrap() == first_weight)
            {
                return BalanceResult::OK(
                    program.weight + first_weight * program.sub_towers.len() as u32,
                );
            }
            if program.sub_towers.len() == 2 {
                panic!("Cannot handle unbalanced subtree of 2, need to go to the parent program for this")
            }
            let mut found_first_weight = 0;
            let mut other_value = 0;
            let mut other_value_idx: usize = 0;
            for (idx, sub_weight_result) in sub_weights.iter().enumerate() {
                let sub_weight = sub_weight_result.unwrap();
                if sub_weight == first_weight {
                    found_first_weight += 1;
                } else {
                    other_value = sub_weight;
                    other_value_idx = idx
                }
            }
            if found_first_weight > 1 {
                // the expected weight is first_weight
                let sub_program_weight = tower
                    .get(&program.sub_towers[other_value_idx])
                    .unwrap()
                    .weight;
                return BalanceResult::Unbalanced(sub_program_weight + first_weight - other_value);
            } else {
                let sub_program_weight = tower.get(&program.sub_towers[0]).unwrap().weight;

                return BalanceResult::Unbalanced(sub_program_weight + other_value - first_weight);
            }
        }
    }
}

fn run2(programs: Vec<Program>) -> u32 {
    let root_program_name = run1(&programs);

    let mut all_programs = HashMap::new();
    for program in programs {
        all_programs.insert(program.name.clone(), program);
    }

    match check_balance(&all_programs, &root_program_name) {
        BalanceResult::OK(_) => panic!("Root program is balanced"),
        BalanceResult::Unbalanced(weight) => weight,
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
        println!("Result 1 is {:?}", run1(&input))
    }
}

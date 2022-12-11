use regex::Regex;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
// use std::iter::zip;

struct Program<'a> {
    name: &'a String,
    weight: u32,
    sub_towers: Vec<String>,
}

impl Program<'_> {
    fn from_raw(line: &str) -> Program {
        let input_regex: Regex = Regex::new(r"^(\S+) \((\d+)\)(?: -> ((\S+, )*\S+))?").unwrap();
        let cap = input_regex.captures(line).unwrap();
        let sub_towers: Vec<String> = match cap.get(3) {
            None => vec![],
            Some(s) => s.as_str().split(", ").map(|n| n.to_string()).collect(),
        };
        return Program {
            name: &cap[1].to_string(),
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

fn run1<'a>(programs: Vec<Program>) -> &'a Program {
    let mut all_programs = HashMap::new();
    let mut all_non_bottom_programs = HashSet::new();
    for program in programs {
        all_programs.insert(program.name, &program);
        for sub_name in program.sub_towers.iter() {
            all_non_bottom_programs.insert(sub_name);
        }
    }
    let mut root_programs = HashSet::from_iter(all_programs.keys().map(|s| *s).into_iter())
        .difference(&all_non_bottom_programs) // how to move the values from "all_programs" instead of copying?
        .map(|s| *s)
        .collect::<Vec<&String>>();
    if root_programs.len() > 1 {
        panic!("Found more than 1 bottom programs: {:?}", root_programs);
    }
    let root_program_name = root_programs.pop().unwrap();
    all_programs.get(&root_program_name).unwrap()
}

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

// fn balance(tower: HashMap<&String, Vec<Program>>, program: &Program) -> BalanceResult {
//     // returnst the total weight of the node and its sub nodes
//     match tower.get(program.name) {
//         None => return BalanceResult::OK(program.weight),
//         Some(programs) => {
//             let sub_balance_results: Vec<BalanceResult> = programs
//                 .iter()
//                 .map(|program| balance(tower, program))
//                 .collect();
//             for sub_balance in sub_balance_results.into_iter() {
//                 match sub_balance {
//                     BalanceResult::Unbalanced(_) => return sub_balance,
//                     BalanceResult::OK(_) => (),
//                 }
//             }
//             match sub_balance_results[..] {
//                 [r] => return BalanceResult::OK(r.unwrap() + program.weight),
//                 _ => {
//                     let weight_counts = HashMap::new();
//                     for sub_balance_result in sub_balance_results {
//                         let sub_weight = sub_balance_result.unwrap();
//                         let weight = weight_counts.get(&sub_weight);
//                         if weight == None {
//                             weight_counts.insert(sub_weight, 1);
//                         } else {
//                             weight_counts.insert(sub_weight, weight.unwrap() + 1);
//                         }
//                     }
//                     let mut imba_weight = None; // imbalanced weight of the total sub tree
//                     let mut bal_weight = None; // balanced weight of the total sub tree
//                                                // we need then to find which node to updated, and add the delta (balanced - imbalanced) to its weight
//                     for (weight, count) in weight_counts.iter() {
//                         // we assume that in case of imbalance, only one node will have a unique value
//                         if *count == 1 {
//                             imba_weight = Some(weight);
//                         } else {
//                             bal_weight = Some(weight);
//                         }
//                     }
//                     if bal_weight == None {
//                         panic!("No able to found the expected balanced weight")
//                     }
//                     if imba_weight != None {
//                         for (program, program_total_weight) in zip(programs, sub_balance_results) {
//                             if program_total_weight.unwrap() == *imba_weight.unwrap() {
//                                 return BalanceResult::Unbalanced(
//                                     program.weight + bal_weight.unwrap() - imba_weight.unwrap(),
//                                 );
//                             }
//                         }
//                     }
//                     return BalanceResult::OK(
//                         program.weight
//                             + sub_balance_results.iter().map(|r| r.unwrap()).sum::<u32>(),
//                     );
//                 }
//             }
//         }
//     }
// }

// fn run2(programs: Vec<Program>) -> BalanceResult {
//     let root_program = run1(programs);
//     let program_tower: HashMap<&String, Vec<Program>> =
//         programs.into_iter().fold(HashMap::new(), |acc, program| {
//             match acc.get(program.name) {
//                 None => {
//                     acc.insert(program.name, vec![program]);
//                 }
//                 Some(programs) => {
//                     programs.push(program);
//                 }
//             }
//             acc
//         });
//     balance(program_tower, &root_program)
// }

fn run2(_programs: Vec<Program>) -> BalanceResult {
    BalanceResult::OK(0)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");
    let input = parse_input(file_path);

    if is_part_two {
        println!("Result 2 is {}", run2(input).unwrap())
    } else {
        println!("Result 1 is {:?}", run1(input).name)
    }
}

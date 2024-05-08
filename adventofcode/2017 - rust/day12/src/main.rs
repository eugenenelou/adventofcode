use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
fn parse_input(file_path: &String) -> HashMap<u32, Vec<u32>> {
    let mut mapping: HashMap<u32, Vec<u32>> = HashMap::new();
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
        .lines()
        .for_each(|row| {
            let mut iter = row.splitn(2, " <-> ");
            let ifrom = iter.next().unwrap().parse::<u32>().unwrap();
            let tos: Vec<u32> = iter
                .next()
                .unwrap()
                .split(", ")
                .map(|raw| raw.parse::<u32>().unwrap())
                .collect();
            mapping.insert(ifrom, tos);
        });
    mapping
}

fn run1(mapping: HashMap<u32, Vec<u32>>) -> usize {
    let mut seen: HashSet<u32> = HashSet::new();
    seen.insert(0);
    let mut to_visit: Vec<u32> = vec![0];
    println!("{:?}", mapping);
    while to_visit.len() > 0 {
        let mut new_to_visit = vec![];
        for i in 0..to_visit.len() {
            for to in mapping.get(&to_visit[i]).unwrap() {
                if !seen.contains(to) {
                    seen.insert(*to);
                    new_to_visit.push(*to);
                }
            }
        }
        to_visit = new_to_visit;
    }
    seen.len()
}

fn run2(mapping: HashMap<u32, Vec<u32>>) -> u32 {
    let mut groups = 0;
    let mut seen: HashSet<u32> = HashSet::new();
    let mut to_visit: Vec<u32> = vec![];
    for start in mapping.keys() {
        if !seen.contains(start) {
            groups += 1;
            to_visit.push(*start);
        }
        while to_visit.len() > 0 {
            let mut new_to_visit = vec![];
            for i in 0..to_visit.len() {
                for to in mapping.get(&to_visit[i]).unwrap() {
                    if !seen.contains(to) {
                        seen.insert(*to);
                        new_to_visit.push(*to);
                    }
                }
            }
            to_visit = new_to_visit;
        }
    }
    groups
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

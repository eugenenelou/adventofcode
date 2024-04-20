use core::panic;
use std::collections::LinkedList;
use std::env;
use std::fs;
fn parse_input(file_path: &String) -> usize {
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .parse::<usize>()
        .unwrap()
}

fn run1(steps: usize) -> usize {
    let mut list: LinkedList<usize> = LinkedList::new();
    list.push_back(0);
    list.push_back(1);
    let mut idx: usize = 1;
    for i in 2..2018 {
        idx = (idx + steps + 1) % i;
        let mut queue = list.split_off(idx as usize);
        if i == 2017 {
            return queue.pop_front().unwrap();
        }
        list.push_back(i as usize);
        list.extend(queue);
    }
    panic!("should have finished already");
}

fn run2(steps: usize) -> usize {
    let mut zero_idx = 0;
    let mut current_idx = 1;
    let mut value_after_zero = 1;
    for i in 2..50000000 {
        current_idx = (current_idx + steps + 1) % i;
        if current_idx <= zero_idx {
            zero_idx += 1;
        } else if current_idx == zero_idx + 1 {
            value_after_zero = i;
        }
    }
    value_after_zero
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

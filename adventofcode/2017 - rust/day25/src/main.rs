use std::collections::VecDeque;
use std::env;
use std::fs;

use regex::Regex;

#[derive(Debug)]
struct Action {
    write_value: bool,
    to_left: bool,
    new_state: usize,
}

#[derive(Debug)]
struct State {
    action_if_zero: Action,
    action_if_one: Action,
}

fn parse_input(file_path: &String) -> (u32, Vec<State>) {
    let file = fs::read_to_string(file_path).expect("Cannot read file");
    let mut iter = file.trim().lines().into_iter();
    iter.next();
    let steps = Regex::new(r"\d+")
        .unwrap()
        .captures(iter.next().unwrap())
        .unwrap()
        .get(0)
        .unwrap()
        .as_str()
        .parse()
        .unwrap();

    let mut states: Vec<State> = Vec::with_capacity(26);
    let offset = 'A' as usize;
    let in_state_regex = Regex::new(r"state ([A-Z])").unwrap();
    loop {
        if let None = iter.next() {
            break;
        }
        let state_idx = (in_state_regex
            .captures(iter.next().unwrap())
            .unwrap()
            .get(1)
            .unwrap()
            .as_str()
            .chars()
            .next()
            .unwrap() as usize)
            - offset;
        let mut state = State {
            action_if_zero: Action {
                write_value: false,
                to_left: false,
                new_state: 25,
            },
            action_if_one: Action {
                write_value: false,
                to_left: false,
                new_state: 25,
            },
        };
        for _ in 0..2 {
            let action = if iter.next().unwrap().contains('0') {
                &mut state.action_if_zero
            } else {
                &mut state.action_if_one
            };
            if iter.next().unwrap().contains('1') {
                action.write_value = true;
            }
            if iter.next().unwrap().contains("left") {
                action.to_left = true;
            }
            action.new_state = (in_state_regex
                .captures(iter.next().unwrap())
                .unwrap()
                .get(1)
                .unwrap()
                .as_str()
                .chars()
                .next()
                .unwrap() as usize)
                - offset;
        }
        if states.len() != state_idx {
            panic!("The state descriptions are not sorted");
        }
        states.push(state);
    }

    (steps, states)
}

fn run1(steps: u32, states: Vec<State>) -> u32 {
    let mut current_state = 0;
    let mut tape = VecDeque::from([false]);
    let mut idx = 0;
    let mut tape_len = 1;
    for _ in 0..steps {
        let state = &states[current_state];
        let action = if tape[idx] {
            &state.action_if_one
        } else {
            &state.action_if_zero
        };
        tape[idx] = action.write_value;
        current_state = action.new_state;
        if action.to_left {
            if idx > 0 {
                idx -= 1;
            } else {
                tape.insert(0, false);
                tape_len += 1;
            }
        } else {
            idx += 1;
            if idx == tape_len {
                tape_len += 1;
                tape.push_back(false);
            }
        }
    }
    tape.into_iter()
        .fold(0, |sum, value| if value { sum + 1 } else { sum })
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let (steps, states) = parse_input(file_path);
    println!("Result 1 is {}", run1(steps, states))
}

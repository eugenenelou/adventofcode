use std::cell::RefCell;
use std::collections::HashMap;
use std::env;
use std::fs;
use std::rc::Rc;

struct Domino {
    taken: bool,
    v1: u64,
    v2: u64,
}

enum Socket {
    Left(Rc<RefCell<Domino>>),
    Right(Rc<RefCell<Domino>>),
}

impl Socket {
    fn unwrap(&self) -> &RefCell<Domino> {
        match self {
            Socket::Left(v) => v,
            Socket::Right(v) => v,
        }
    }
}
fn parse_input(file_path: &String) -> HashMap<u64, Vec<Socket>> {
    let mut dominos: HashMap<u64, Vec<Socket>> = HashMap::new();
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
        .lines()
        .for_each(|line| {
            let mut iter = line.split("/");
            let v1 = iter.next().unwrap().parse().unwrap();
            let v2 = iter.next().unwrap().parse().unwrap();
            let domino = Rc::new(RefCell::new(Domino {
                taken: false,
                v1: v1,
                v2: v2,
            }));
            dominos
                .entry(v1)
                .or_default()
                .push(Socket::Right(domino.clone()));
            dominos.entry(v2).or_default().push(Socket::Left(domino));
        });
    dominos
}

fn run_inner_1(dominos: &HashMap<u64, Vec<Socket>>, last_value: u64, strength: u64) -> u64 {
    let empty = Vec::new();
    let next_sockets: Vec<&Socket> = dominos
        .get(&last_value)
        .unwrap_or(&empty)
        .iter()
        .filter(|socket| !socket.unwrap().borrow().taken)
        .collect();
    if next_sockets.len() == 0 {
        return strength;
    }
    next_sockets
        .iter()
        .map(|socket| {
            let new_last_value = match socket {
                Socket::Left(domino) => domino.borrow().v1,
                Socket::Right(domino) => domino.borrow().v2,
            };
            socket.unwrap().borrow_mut().taken = true;
            let result = run_inner_1(
                dominos,
                new_last_value,
                strength + last_value + new_last_value,
            );
            socket.unwrap().borrow_mut().taken = false;
            result
        })
        .max()
        .unwrap()
}
fn run1(dominos: HashMap<u64, Vec<Socket>>) -> u64 {
    run_inner_1(&dominos, 0, 0)
}

fn run_inner_2(
    dominos: &HashMap<u64, Vec<Socket>>,
    last_value: u64,
    length: u64,
    strength: u64,
) -> (u64, u64) {
    let empty = Vec::new();
    let next_sockets: Vec<&Socket> = dominos
        .get(&last_value)
        .unwrap_or(&empty)
        .iter()
        .filter(|socket| !socket.unwrap().borrow().taken)
        .collect();
    if next_sockets.len() == 0 {
        return (length, strength);
    }
    next_sockets
        .iter()
        .map(|socket| {
            let new_last_value = match socket {
                Socket::Left(domino) => domino.borrow().v1,
                Socket::Right(domino) => domino.borrow().v2,
            };
            socket.unwrap().borrow_mut().taken = true;
            let result = run_inner_2(
                dominos,
                new_last_value,
                length + 1,
                strength + last_value + new_last_value,
            );
            socket.unwrap().borrow_mut().taken = false;
            result
        })
        .max_by(|a, b| {
            if a.0 == b.0 {
                return a.1.cmp(&b.1);
            }
            a.0.cmp(&b.0)
        })
        .unwrap()
}
fn run2(dominos: HashMap<u64, Vec<Socket>>) -> u64 {
    run_inner_2(&dominos, 0, 0, 0).1
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

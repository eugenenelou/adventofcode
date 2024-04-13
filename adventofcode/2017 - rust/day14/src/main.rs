use std::collections::HashMap;
use std::env;
use std::fs;
fn parse_input(file_path: &String) -> String {
    println!("{}", file_path);
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
}

const SIZE: usize = 256;

fn knot_hash(key: String) -> u128 {
    let mut bytes: Vec<usize> = key.chars().map(|raw| (raw as u8) as usize).collect();
    bytes.extend_from_slice(&[17, 31, 73, 47, 23]);

    let mut values: Vec<usize> = (0..SIZE).collect();
    let mut skip = 0;
    let mut position = 0;
    for _ in 0..64 {
        for range in bytes.iter() {
            // swap first with last, second with second to last ...
            let swap_count = range / 2;
            for i in 0..swap_count {
                values.swap(
                    (position + i) % SIZE,
                    (position + range - 1 - i + SIZE) % SIZE,
                );
            }
            position = (position + range + skip) % SIZE;
            skip += 1;
        }
    }
    let mut dense_numbers = Vec::<usize>::with_capacity(16);
    for i in 0..16 {
        let mut dense = 0;
        for j in 0..16 {
            dense = dense ^ values[i * 16 + j];
        }
        dense_numbers.push(dense);
    }
    u128::from_str_radix(
        &dense_numbers
            .iter()
            .map(|number| format!("{:02x}", number))
            .collect::<Vec<_>>()
            .join(""),
        16,
    )
    .unwrap()
}

fn run1(_input: String) -> u32 {
    (0..128).fold(0, |acc, idx| {
        acc + knot_hash(format!("{}-{}", _input, idx)).count_ones()
    })
}

fn identifier(x: usize, y: usize) -> usize {
    return x * 1000 + y;
}

fn merge_groups(groups: &mut HashMap<usize, u32>, from: u32, into: u32) {
    for (_, val) in groups.iter_mut() {
        if *val == from {
            *val = into
        }
    }
}

fn run2(_input: String) -> u32 {
    let grid: Vec<Vec<bool>> = (0..128)
        .map(|idx| {
            let hash = knot_hash(format!("{}-{}", _input, idx));
            (0..128).map(|bit| hash & (1 << bit) != 0).collect()
        })
        .collect::<Vec<Vec<bool>>>();
    let mut groups: HashMap<usize, u32> = HashMap::new();
    let mut group_idx: u32 = 0;
    let mut merged: u32 = 0;
    let positions_to_check: Vec<(isize, isize)> = vec![(-1, 0), (0, -1)];
    for i in 0..128 {
        let row = &grid[i];
        for j in 0..128 {
            if row[j] {
                let mut group: Option<u32> = None;
                for (d_x, d_y) in positions_to_check.iter() {
                    if (*d_x == -1 && i == 0) || (*d_y == -1 && j == 0) {
                        continue;
                    }
                    let neighbor_x = (i as isize + *d_x) as usize;
                    let neighbor_y = (j as isize + *d_y) as usize;
                    if grid[neighbor_x][neighbor_y] {
                        let id = identifier(neighbor_x, neighbor_y);
                        let neighbor_group = *groups.get(&id).unwrap();
                        group = match group {
                            None => {
                                groups.insert(identifier(i, j), neighbor_group);
                                Some(neighbor_group)
                            }
                            Some(group_value) => {
                                if group_value != neighbor_group {
                                    merge_groups(&mut groups, neighbor_group, group_value);
                                    merged += 1;
                                    groups.insert(identifier(i, j), group_value);
                                }
                                group
                            }
                        }
                    }
                }
                match group {
                    None => {
                        group_idx += 1;
                        groups.insert(identifier(i, j), group_idx);
                    }
                    Some(_) => (),
                }
            }
        }
    }
    group_idx - merged
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

use std::collections::HashMap;
use std::env;
use std::fs;

fn get_variants_2(chars: Vec<char>) -> Vec<Vec<char>> {
    return vec![
        vec![0, 1, 2, 3],
        vec![1, 0, 3, 2],
        vec![2, 0, 3, 1],
        vec![3, 2, 1, 0],
        vec![1, 3, 0, 2],
        vec![3, 1, 2, 0],
        vec![2, 3, 0, 1],
        vec![0, 2, 1, 3],
    ]
    .into_iter()
    .map(|indexes| indexes.into_iter().map(|idx| chars[idx]).collect())
    .collect();
}

fn get_variants_3(chars: Vec<char>) -> Vec<Vec<char>> {
    return vec![
        vec![0, 1, 2, 3, 4, 5, 6, 7, 8],
        vec![6, 3, 0, 7, 4, 1, 8, 5, 2],
        vec![8, 7, 6, 5, 4, 3, 2, 1, 0],
        vec![2, 5, 8, 1, 4, 7, 0, 3, 6],
        vec![2, 1, 0, 5, 4, 3, 8, 7, 6],
        vec![8, 5, 2, 7, 4, 1, 6, 3, 0],
        vec![6, 7, 8, 3, 4, 5, 0, 1, 2],
        vec![0, 3, 6, 1, 4, 7, 2, 5, 8],
    ]
    .into_iter()
    .map(|indexes| indexes.into_iter().map(|idx| chars[idx]).collect())
    .collect();
}
fn get_variants(chars: Vec<char>) -> Vec<Vec<char>> {
    match chars.len() {
        4 => get_variants_2(chars),
        9 => get_variants_3(chars),
        _ => panic!("Unrecognized pattern size: {:?}", chars),
    }
}

fn parse_input(file_path: &String) -> HashMap<String, String> {
    let mut patterns: HashMap<String, String> = HashMap::new();
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
        .lines()
        .for_each(|line| {
            let mut iter = line.split(" => ");
            let from = iter.next().unwrap().replace("/", "");
            let to = iter.next().unwrap().replace("/", "");
            for pattern in get_variants(from.chars().collect()) {
                // assume the patterns are mutually exclusive
                patterns.insert(pattern.iter().collect(), to.clone());
            }
        });
    patterns
}

fn run(patterns: HashMap<String, String>, n: usize) -> u32 {
    let mut grid: Vec<char> = ".#...####".chars().collect();
    let mut size = 3;

    for _ in 0..n {
        let block_size = if size % 2 == 0 { 2 } else { 3 };
        let block_count = size / block_size;

        let new_size = if size % 2 == 0 {
            size / 2 * 3
        } else {
            size / 3 * 4
        };

        let mut new_grid = Vec::with_capacity(new_size * new_size);
        unsafe {
            new_grid.set_len(new_size * new_size);
        }
        for i in 0..block_count {
            for j in 0..block_count {
                let mut pattern_vec = vec![];
                for x in 0..block_size {
                    for y in 0..block_size {
                        pattern_vec.push(grid[i * block_size + x + size * (j * block_size + y)])
                    }
                }
                let pattern = pattern_vec.iter().collect::<String>();
                // println!("pattern: {}", pattern);
                let new_pattern: Vec<char> = patterns.get(&pattern).unwrap().chars().collect();

                for x in 0..(block_size + 1) {
                    for y in 0..(block_size + 1) {
                        new_grid
                            [i * (block_size + 1) + x + new_size * (j * (block_size + 1) + y)] =
                            new_pattern[x + (block_size + 1) * y];
                    }
                }
            }
        }
        grid = new_grid;
        size = new_size;
    }

    grid.into_iter()
        .fold(0, |sum, char_| if char_ == '#' { sum + 1 } else { sum })
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");
    let input = parse_input(file_path);

    if is_part_two {
        println!("Result 2 is {}", run(input, 18))
    } else {
        println!("Result 1 is {}", run(input, 5))
    }
}

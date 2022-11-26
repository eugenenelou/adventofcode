use std::env;

fn run1(n: u32) -> u32 {
    // distance is the sum of the distances in both dimensions
    // if m is the highest odd number such that m^2 <= n and m = 2k + 1
    // then k is the distance in one of the dimension.
    // in the other dimension the distance is cyclical for all numbers
    // around the square of the m^2 first numbers, the cycle length is m+1
    // and the value is 0 if n-m^2 mod m+1 = k
    // so the distance in this dimension is ((n-m^2) % m+1)-k
    // and summing both dimensions the result is (n-m^2) % m+1
    let mut k: u32 = (n as f64).sqrt() as u32;
    if k % 2 == 0 {
        k -= 1;
    }
    (n - k.pow(2)) % (k + 1)
}

#[derive(Debug)]
enum Direction {
    UP,
    DOWN,
    LEFT,
    RIGHT,
}

struct Grid {
    values: Vec<Vec<u32>>,
    offset: isize,
}

impl Grid {
    fn set(&mut self, x: isize, y: isize, value: u32) {
        self.values[(x + self.offset) as usize][(y + self.offset) as usize] = value
    }

    fn get(&self, x: isize, y: isize) -> u32 {
        self.values[(x + self.offset) as usize][(y + self.offset) as usize]
    }
}

fn init_grid(edge: usize) -> Grid {
    if edge % 2 != 1 {
        panic!("Expect grid size to be an odd number")
    }
    let mut values: Vec<Vec<u32>> = Vec::with_capacity(edge);
    for _ in 0..edge {
        let row = vec![0u32; edge];
        values.push(row);
    }
    Grid {
        values,
        offset: (edge / 2) as isize,
    }
}

fn run2(n: u32) -> u32 {
    // the side of the square we need to store the values on
    let mut edge = (n as f64).sqrt().ceil() as usize;
    if edge % 2 == 0 {
        edge -= 1;
    }
    // This gris is far too big, it  corresponds to part1 sizing, but it works
    let mut grid = init_grid(edge);

    let mut direction = Direction::RIGHT;
    let mut x: isize = 0;
    let mut y: isize = 0;
    grid.set(x, y, 1);
    for _ in 2..n {
        let value: u32;
        match direction {
            Direction::DOWN => {
                y -= 1;
                value = grid.get(x, y + 1)
                    + grid.get(x + 1, y + 1)
                    + grid.get(x + 1, y)
                    + grid.get(x + 1, y - 1);
                grid.set(x, y, value);
                if grid.get(x + 1, y) == 0 {
                    direction = Direction::RIGHT;
                }
            }
            Direction::LEFT => {
                x -= 1;
                value = grid.get(x + 1, y)
                    + grid.get(x + 1, y - 1)
                    + grid.get(x, y - 1)
                    + grid.get(x - 1, y - 1);
                grid.set(x, y, value);
                if grid.get(x, y - 1) == 0 {
                    direction = Direction::DOWN;
                }
            }
            Direction::UP => {
                y += 1;
                value = grid.get(x - 1, y)
                    + grid.get(x - 1, y - 1)
                    + grid.get(x, y - 1)
                    + grid.get(x - 1, y + 1);
                grid.set(x, y, value);
                if grid.get(x - 1, y) == 0 {
                    direction = Direction::LEFT;
                }
            }
            Direction::RIGHT => {
                x += 1;
                value = grid.get(x - 1, y)
                    + grid.get(x - 1, y + 1)
                    + grid.get(x, y + 1)
                    + grid.get(x + 1, y + 1);
                grid.set(x, y, value);
                if grid.get(x, y + 1) == 0 {
                    direction = Direction::UP;
                }
            }
        }
        println!("value: {}, direction: {:?}", value, direction);
        if value > n {
            return value;
        }
    }
    panic!("Didn't find value larger than the input")
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let n = args[1].parse::<u32>().unwrap();
    let is_part_two = args.len() > 2 && args[2].eq("--two");

    if is_part_two {
        println!("Result 2 is {}", run2(n))
    } else {
        println!("Result 1 is {}", run1(n))
    }
}

use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Debug)]
struct Vector {
    x: i32,
    y: i32,
    z: i32,
}

fn parse_input1(file_path: &String) -> Vec<Vector> {
    let input_regex: Regex = Regex::new(r"a=<(-?\d+),(-?\d+),(-?\d+)>").unwrap();
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
        .lines()
        .map(|line| {
            let accelerations = input_regex.captures(line).unwrap();
            let ax: i32 = accelerations.get(1).unwrap().as_str().parse().unwrap();
            let ay: i32 = accelerations.get(2).unwrap().as_str().parse().unwrap();
            let az: i32 = accelerations.get(3).unwrap().as_str().parse().unwrap();
            Vector {
                x: ax,
                y: ay,
                z: az,
            }
        })
        .collect()
}

fn run1(_input: Vec<Vector>) -> usize {
    // max of Ax^2 + Ay^2 + Az^2
    let distances: Vec<(usize, i32)> = _input
        .iter()
        .enumerate()
        .map(|(idx, vector)| (idx, vector.x.abs() + vector.y.abs() + vector.z.abs()))
        .collect();
    let mini = _input
        .iter()
        .enumerate()
        .map(|(idx, vector)| (idx, vector.x.abs() + vector.y.abs() + vector.z.abs()))
        .min_by_key(|(_, d)| *d)
        .unwrap();
    for (idx, distance) in distances {
        if distance == mini.1 {
            println!("idx: {} is mini", idx);
        }
    }
    // we can try the few solutions one by one.
    // if we wanted to be exact we could just compute the distance for a high value of time
    // and take the smaller one.
    mini.0
}

struct Particle {
    p: Vector,
    v: Vector,
    a: Vector,
    dead: bool,
}

fn parse_input2(file_path: &String) -> Vec<Particle> {
    let input_regex: Regex = Regex::new(
        r"p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>",
    )
    .unwrap();
    fs::read_to_string(file_path)
        .expect("Cannot read file")
        .trim()
        .to_owned()
        .lines()
        .map(|line| {
            let groups = input_regex.captures(line).unwrap();
            let numbers: Vec<i32> = (1..10)
                .into_iter()
                .map(|idx| groups.get(idx).unwrap().as_str().parse().unwrap())
                .collect();
            Particle {
                p: Vector {
                    x: numbers[0],
                    y: numbers[1],
                    z: numbers[2],
                },
                v: Vector {
                    x: numbers[3],
                    y: numbers[4],
                    z: numbers[5],
                },
                a: Vector {
                    x: numbers[6],
                    y: numbers[7],
                    z: numbers[8],
                },
                dead: false,
            }
        })
        .collect()
}

fn run2(mut _input: Vec<Particle>) -> u32 {
    let mut particles: Vec<Particle> = _input;

    println!(
        "pre {} {}",
        particles.len(),
        particles
            .iter()
            .fold(0, |sum, particle| sum + (if particle.dead { 0 } else { 1 }))
    );
    for _ in 0..1000 {
        let mut positions: HashMap<i32, HashMap<i32, HashMap<i32, Vec<usize>>>> = HashMap::new();
        particles = particles
            .into_iter()
            .enumerate()
            .map(|(idx, particle)| {
                if particle.dead {
                    return particle;
                }
                let vx = particle.v.x + particle.a.x;
                let vy = particle.v.y + particle.a.y;
                let vz = particle.v.z + particle.a.z;
                let px = particle.p.x + vx;
                let py = particle.p.y + vy;
                let pz = particle.p.z + vz;

                let two_dim = positions.entry(px).or_insert(HashMap::new());
                let one_dim = two_dim.entry(py).or_insert(HashMap::new());
                let particles_at_position = one_dim.entry(pz).or_insert(Vec::new());
                particles_at_position.push(idx);

                Particle {
                    p: Vector {
                        x: px,
                        y: py,
                        z: pz,
                    },
                    v: Vector {
                        x: vx,
                        y: vy,
                        z: vz,
                    },
                    a: particle.a,
                    dead: false,
                }
            })
            .collect();

        // resolve collisions
        for two_dims in positions.values() {
            for one_dims in two_dims.values() {
                for colliding_particles in one_dims.values() {
                    if colliding_particles.len() > 1 {
                        for idx in colliding_particles {
                            particles[*idx].dead = true;
                        }
                    }
                }
            }
        }
        println!(
            "remaining {}",
            particles
                .iter()
                .fold(0, |sum, particle| sum + (if particle.dead { 0 } else { 1 }))
        )
    }
    particles
        .iter()
        .fold(0, |sum, particle| sum + (if particle.dead { 0 } else { 1 }))
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let is_part_two = args.len() > 2 && args[2].eq("--two");

    if is_part_two {
        println!("Result 2 is {}", run2(parse_input2(file_path)))
    } else {
        println!("Result 1 is {}", run1(parse_input1(file_path)))
    }
}

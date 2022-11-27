package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

// The example can be summed up in an equation:
// Disc #1 has 5 positions; at time=0, it is at position 4.
// Disc #2 has 2 positions; at time=0, it is at position 1.

// t + 1 == 1 % 5
// t + 2 == 1 % 2
// so we'll just check every values of t until we find one that matches all disk equations

type Disk struct {
	index     int
	n_pos     int
	known_t   int
	known_pos int
}

func (d Disk) check_time(time int) bool {
	return (time+d.index)%d.n_pos == d.n_pos-d.known_pos+d.known_t
}

func parseInput() []Disk {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var disks []Disk
	for _, rawInstruction := range strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n") {
		if rawInstruction == "" {
			break
		}

		RectRegex := regexp.MustCompile(".*#(\\d+)\\s.*\\s(\\d+)\\s.*=(\\d+),.*\\s(\\d+)\\.")
		match := RectRegex.FindStringSubmatch(rawInstruction)
		if match == nil {
			panic("Failed to parse instruction")
		}
		index, _ := strconv.Atoi(match[1])
		n_pos, _ := strconv.Atoi(match[2])
		known_t, _ := strconv.Atoi(match[3])
		known_pos, _ := strconv.Atoi(match[4])
		disks = append(disks, Disk{index, n_pos, known_t, known_pos})
	}
	return disks
}

func run(disks []Disk) int {
	for t := 0; ; t++ {
		if t%100000 == 0 {
			fmt.Printf("%d\r\n", t)
		}
		check := true
		for _, disk := range disks {
			if !disk.check_time(t) {
				check = false
			}
		}
		if check {
			fmt.Printf("The first time to press is t=%d", t)
			return t
		}
	}
}

func part1() {
	disks := parseInput()
	run(disks)
}

// For part 2, adding the 7th disk increase the complexity by too much
// We'll solve it mathematically instead of bruteforcing
// Equations for each disk:
// E1 t + 1 = 13k1 + 12
// E2 t + 2 = 19k2 + 9
// E3 t + 3 = 3k3 + 1
// E4 t + 4 = 7k4 + 6
// E5 t + 5 = 5k5 + 2
// E6 t + 6 = 17k6 + 12
// As all the period of disks are prime together
// the diophantian equations of combining any 2 equations  together
// has a solution.
// We'll combine the first two, resulting in a new equation
// that we'll combine with the third and repeat until all equations are solved

func extended_gcd(a int, b int) (int, int, int) {
	if a == 0 {
		return b, 0, 1
	}
	gcd, x1, y1 := extended_gcd(b%a, a)
	x := y1 - (b/a)*x1
	y := x1
	return gcd, x, y
}

func solve_diophantian(a int, b int, c int) (x int, y int) {
	gcd, x1, y1 := extended_gcd(a, b)
	if c%gcd != 0 {
		panic(fmt.Sprintf("gcd=%d is not a multiple of c=%d", gcd, c))
	}
	x = x1 * c / gcd
	y = y1 * (c / gcd)
	return x, y
}

func (d Disk) compute_pos(t int) int {
	// compute the pos of the disk when the ball reaches
	// it when launched at time t
	return (d.known_pos - d.known_t + d.index + t) % d.n_pos
}

func (d Disk) to_equation_params() (p int, c int) {
	// Disk #n has p positions, is at position p0 at time t0
	// gives the equation t = p*k + p - p0 - t0 - n
	// let's define c such that t = p * k + c
	p = d.n_pos
	c = (d.n_pos - d.known_pos - d.known_t - d.index) % d.n_pos
	c = (d.n_pos + c) % d.n_pos
	return p, c
}

func (d1 Disk) merge(d2 Disk) Disk {
	// combine both disk equations into a diophantian equation
	// deduce an equation for t that fulfills both
	// create a fake disk that is caracterized by this new equation
	p1, c1 := d1.to_equation_params()
	p2, c2 := d2.to_equation_params()
	// p1 * k1 + p2 * (-k2) = c2 - c1
	gcd, _, _ := extended_gcd(p1, p2)
	x0, _ := solve_diophantian(p1, p2, c2-c1)

	p3 := p1 * p2 / gcd
	c3 := c1 + p1*x0
	c3 = (p3 + c3%p3) % p3 // simplify c3 to be in [0, p3[

	new_disk := Disk{0, p3, 0, p3 - c3}
	return new_disk
}

func (d Disk) find_smallest_solution() int {
	_, c := d.to_equation_params()
	return (c%d.n_pos + d.n_pos) % d.n_pos
}

func part2() {
	disks := parseInput()
	disk := Disk{len(disks) + 1, 11, 0, 0}

	for _, next_disk := range disks {
		new_disk := disk.merge(next_disk)
		disk = new_disk
	}
	solution := disk.find_smallest_solution()
	fmt.Printf("Final disk: %v\r\n", disk)
	fmt.Printf("The first time to press is t=%d\r\n", solution)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

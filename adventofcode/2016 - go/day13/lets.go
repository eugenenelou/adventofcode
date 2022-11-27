package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

var pop8tab = [256]uint8{
	0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4,
	1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
	1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
	1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
	3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
	4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8,
}

func OnesCount32(x uint32) int {
	return int(pop8tab[x>>24] + pop8tab[x>>16&0xff] + pop8tab[x>>8&0xff] + pop8tab[x&0xff])
}

type Case struct {
	x int
	y int
}

func (c Case) equals(other Case) bool {
	return c.x == other.x && c.y == other.y
}

type Problem struct {
	fav_number int
	target     Case
}

type Grid struct {
	fav_number int
	x_max      int
	y_max      int
	values     [][]bool // true if empty space
	costs      [][]int
}

func (g Grid) compute(x int, y int) bool {
	return (OnesCount32(uint32(x*(x+3+2*y)+y*(1+y)+g.fav_number)) % 2) == 0
}

func (g *Grid) extend_x(n int) {
	for j := 0; j < n; j++ {
		x_row := make([]bool, g.y_max)
		x_costs := make([]int, g.y_max)
		for i := 0; i < g.y_max; i++ {
			x_row[i] = g.compute(g.x_max, i)
			x_costs[i] = -1
		}
		g.values = append(g.values, x_row)
		g.costs = append(g.costs, x_costs)
		g.x_max += 1
	}
}

func (g *Grid) extend_y(n int) {
	for j := 0; j < n; j++ {
		for i := 0; i < g.x_max; i++ {
			g.values[i] = append(g.values[i], g.compute(i, g.y_max))
			g.costs[i] = append(g.costs[i], -1)
		}
		g.y_max += 1
	}
}

func (g Grid) print() {
	fmt.Printf("Spaces:\r\n")
	for _, x_row := range g.values {
		for _, value := range x_row {
			var display string
			if value {
				display = " "
			} else {
				display = "#"
			}
			fmt.Printf(display)
		}
		fmt.Printf("\r\n")
	}
	fmt.Printf("Cost:\r\n")
	for _, x_row := range g.costs {
		for _, value := range x_row {
			fmt.Printf(" %02d", value)
		}
		fmt.Printf("\r\n")
	}
}

func (g *Grid) next_cases(case_ Case) []Case {
	cases := make([]Case, 0)
	if case_.x > 0 && g.values[case_.x-1][case_.y] {
		cases = append(cases, Case{case_.x - 1, case_.y})
	}
	if case_.y > 0 && g.values[case_.x][case_.y-1] {
		cases = append(cases, Case{case_.x, case_.y - 1})
	}
	if case_.x+1 >= g.x_max {
		g.extend_x(case_.x + 2 - g.x_max)
	}
	if case_.y+1 >= g.y_max {
		g.extend_y(case_.y + 2 - g.y_max)
	}
	if g.values[case_.x+1][case_.y] {
		cases = append(cases, Case{case_.x + 1, case_.y})
	}
	if g.values[case_.x][case_.y+1] {
		cases = append(cases, Case{case_.x, case_.y + 1})
	}
	return cases
}

func parseInput() Problem {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	numbers := strings.Split(strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n")[0], ",")
	fav_number, _ := strconv.Atoi(numbers[0])
	x_dest, _ := strconv.Atoi(numbers[1])
	y_dest, _ := strconv.Atoi(numbers[2])
	return Problem{fav_number, Case{x_dest, y_dest}}
}

func part1() {
	problem := parseInput()
	grid := Grid{problem.fav_number, 0, 0, make([][]bool, 0), make([][]int, 0)}
	grid.extend_x(problem.target.x + 1)
	grid.extend_y(problem.target.y + 1)

	grid.costs[1][1] = 0
	last_visited := []Case{Case{1, 1}}

	for step := 1; step < 1000; step++ {
		fmt.Printf("Step %d\r\n", step)
		next_last_visited := make([]Case, 0)
		for _, case_ := range last_visited {
			for _, next_case := range grid.next_cases(case_) {
				if grid.costs[next_case.x][next_case.y] != -1 {
					continue
				}
				next_last_visited = append(next_last_visited, next_case)
				grid.costs[next_case.x][next_case.y] = step
				if next_case.equals(problem.target) {
					grid.print()
					fmt.Printf("Solution takes %d steps to reach", step)
					return
				}
			}
		}
		last_visited = next_last_visited
	}
}

func part2() {
	problem := parseInput()
	grid := Grid{problem.fav_number, 0, 0, make([][]bool, 0), make([][]int, 0)}
	grid.extend_x(problem.target.x + 1)
	grid.extend_y(problem.target.y + 1)

	grid.costs[1][1] = 0
	last_visited := []Case{Case{1, 1}}

	visited_count := 1

	for step := 1; step <= 50; step++ {
		fmt.Printf("Step %d\r\n", step)
		next_last_visited := make([]Case, 0)
		for _, case_ := range last_visited {
			for _, next_case := range grid.next_cases(case_) {
				if grid.costs[next_case.x][next_case.y] != -1 {
					continue
				}
				next_last_visited = append(next_last_visited, next_case)
				grid.costs[next_case.x][next_case.y] = step
				visited_count += 1
			}
		}
		last_visited = next_last_visited
	}
	grid.print()
	fmt.Printf("Visited %d locations in 50 steps", visited_count)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

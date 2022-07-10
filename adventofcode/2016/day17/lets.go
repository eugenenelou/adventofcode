package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"os"
	"strings"
)

func parseInput() string {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	return strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n")[0]
}

type Position struct {
	input      string
	directions string
	hash       []rune
	pos_x      int
	pos_y      int
}

var ALLOWED_HASH_RUNES = "bcdef"
var GRID_SIZE = 4

func (p *Position) set_hash() {
	hash := []rune(fmt.Sprintf("%x", md5.Sum([]byte(p.input+p.directions))))[:4]
	p.hash = hash
}

func (p Position) can_go(direction string) bool {
	if direction == "U" && (p.pos_y == 0 || !strings.ContainsRune(ALLOWED_HASH_RUNES, p.hash[0])) {
		return false
	}
	if direction == "D" && (p.pos_y >= GRID_SIZE-1 || !strings.ContainsRune(ALLOWED_HASH_RUNES, p.hash[1])) {
		return false
	}
	if direction == "L" && (p.pos_x == 0 || !strings.ContainsRune(ALLOWED_HASH_RUNES, p.hash[2])) {
		return false
	}
	if direction == "R" && (p.pos_x >= GRID_SIZE-1 || !strings.ContainsRune(ALLOWED_HASH_RUNES, p.hash[3])) {
		return false
	}
	return true
}

func (p Position) go_to(direction string) Position {
	directions := p.directions + direction
	pos_x := p.pos_x
	pos_y := p.pos_y
	if direction == "U" {
		pos_y -= 1
	} else if direction == "R" {
		pos_x += 1
	} else if direction == "D" {
		pos_y += 1
	} else if direction == "L" {
		pos_x -= 1
	}
	new_p := Position{p.input, directions, []rune{}, pos_x, pos_y}
	new_p.set_hash()
	return new_p
}

func (p Position) possible_directions() []string {
	directions := []string{}
	if p.can_go("U") {
		directions = append(directions, "U")
	}
	if p.can_go("D") {
		directions = append(directions, "D")
	}
	if p.can_go("L") {
		directions = append(directions, "L")
	}
	if p.can_go("R") {
		directions = append(directions, "R")
	}
	return directions
}

func run(longest bool) {
	input := parseInput()
	initial_pos := Position{input, "", []rune{}, 0, 0}
	initial_pos.set_hash()
	fmt.Printf("initial_pos %s\n", string(initial_pos.hash))
	positions := []Position{initial_pos}

	longest_solution := initial_pos
	for step := 0; step < 1000; step++ {
		fmt.Printf("step %d, n positions: %d\n", step, len(positions))
		new_positions := []Position{}
		for _, position := range positions {
			for _, direction := range position.possible_directions() {

				new_position := position.go_to(direction)
				if new_position.pos_x == GRID_SIZE-1 && new_position.pos_y == GRID_SIZE-1 {
					if longest {
						if len(new_position.directions) > len(longest_solution.directions) {
							longest_solution = new_position
						}
					} else {
						fmt.Printf("Reached the vault with directions: %s", new_position.directions)
						return
					}
				} else {
					new_positions = append(new_positions, new_position)
				}
			}
		}
		if longest && len(new_positions) == 0 {
			fmt.Printf("Reached the vault with longest path: len: %d, path:%s", len(longest_solution.directions), longest_solution.directions)
			return
		}
		positions = new_positions
	}

}

func part1() {
	run(false)
}

func part2() {
	run(true)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

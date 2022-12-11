package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

func parseInput() []string {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var instructions []string
	for _, rawInstruction := range strings.Split(string(content), "\n") {
		instructions = append(instructions, rawInstruction)
	}
	return instructions
}

type Point struct {
	x int
	y int
}

func (p Point) getNumber() int {
	return 3*(-p.y+1) + p.x + 1 + 1
}

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a int, b int) int {
	if a < b {
		return b
	}
	return a
}

func part1() {
	instructions := parseInput()
	var code []string
	for _, inst := range instructions {
		x, y := 0, 0
		for i := 0; i < len(inst); i++ {
			switch inst[i] {
			case 'U':
				y = min(1, y+1)
			case 'R':
				x = min(1, x+1)
			case 'D':
				y = max(-1, y-1)
			case 'L':
				x = max(-1, x-1)
			}
		}
		code = append(code, fmt.Sprint(Point{x, y}.getNumber()))
	}
	fmt.Println("Code is: ", strings.Join(code, ""))
}

func (p Point) getKey() string {
	switch {
	case p.x == 2 && p.y == 2:
		return "1"
	case p.x == 1 && p.y == 1:
		return "2"
	case p.x == 2 && p.y == 1:
		return "3"
	case p.x == 3 && p.y == 1:
		return "4"
	case p.x == 0 && p.y == 0:
		return "5"
	case p.x == 1 && p.y == 0:
		return "6"
	case p.x == 2 && p.y == 0:
		return "7"
	case p.x == 3 && p.y == 0:
		return "8"
	case p.x == 4 && p.y == 0:
		return "9"
	case p.x == 1 && p.y == -1:
		return "A"
	case p.x == 2 && p.y == -1:
		return "B"
	case p.x == 3 && p.y == -1:
		return "C"
	case p.x == 2 && p.y == -2:
		return "D"
	default:
		panic(fmt.Sprintf("Unexpected point %+v", p))
	}
}

func topLeftConstraint(x int, y int, vertical bool) (int, int) {
	// line y = x, so constraint is y <= x
	if vertical {
		return x, min(x, y)
	}
	return max(x, y), y
}

func topRightConstraint(x int, y int, vertical bool) (int, int) {
	// line y = 4 - x so constraint is y <= 4 - x
	if vertical {
		return x, min(4-x, y)
	}
	return min(x, 4-y), y
}

func bottomLeftConstraint(x int, y int, vertical bool) (int, int) {
	// line y = - x so constraint is y >= - x
	if vertical {
		return x, max(-x, y)
	}
	return max(x, -y), y

}

func bottomRightConstraint(x int, y int, vertical bool) (int, int) {
	// line y = x - 4 so constraint is y >= x - 4
	if vertical {
		return x, max(x-4, y)
	}
	return min(x, y+4), y
}

func part2() {
	instructions := parseInput()
	var code []string
	x, y := 0, 0
	for _, inst := range instructions {
		fmt.Println(inst)
		for i := 0; i < len(inst); i++ {
			switch inst[i] {
			case 'U':
				x, y = topRightConstraint(x, y+1, true)
				x, y = topLeftConstraint(x, y, true)
			case 'R':
				x, y = topRightConstraint(x+1, y, false)
				x, y = bottomRightConstraint(x, y, false)
			case 'D':
				x, y = bottomLeftConstraint(x, y-1, true)
				x, y = bottomRightConstraint(x, y, true)
			case 'L':
				x, y = topLeftConstraint(x-1, y, false)
				x, y = bottomLeftConstraint(x, y, false)
			}
		}
		code = append(code, Point{x, y}.getKey())
	}
	fmt.Println("Code is: ", strings.Join(code, ""))
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

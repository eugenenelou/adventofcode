package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Instruction struct {
	type_ string
	A     int
	B     int
}

func parseInput() []Instruction {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var instructions []Instruction
	for _, rawInstruction := range strings.Split(string(content), "\n") {
		if rawInstruction == "" {
			break
		}
		if strings.HasPrefix(rawInstruction, "rect") {
			RectRegex := regexp.MustCompile("rect (\\d+)x(\\d+)")
			match := RectRegex.FindStringSubmatch(rawInstruction)
			if match == nil {
				panic("Failed to parse instruction")
			}
			A, _ := strconv.Atoi(match[1])
			B, _ := strconv.Atoi(match[2])
			instructions = append(instructions, Instruction{"rect", A, B})
		} else if strings.HasPrefix(rawInstruction, "rotate column") {
			RotateColumnRegex := regexp.MustCompile("rotate column x=(\\d+) by (\\d+)")
			match := RotateColumnRegex.FindStringSubmatch(rawInstruction)
			if match == nil {
				panic("Failed to parse instruction")
			}
			A, _ := strconv.Atoi(match[1])
			B, _ := strconv.Atoi(match[2])
			instructions = append(instructions, Instruction{"rotateColumn", A, B})
		} else if strings.HasPrefix(rawInstruction, "rotate row") {
			RotateRowRegex := regexp.MustCompile("rotate row y=(\\d+) by (\\d+)")
			match := RotateRowRegex.FindStringSubmatch(rawInstruction)
			if match == nil {
				panic("Failed to parse instruction")
			}
			A, _ := strconv.Atoi(match[1])
			B, _ := strconv.Atoi(match[2])
			instructions = append(instructions, Instruction{"rotateRow", A, B})
		} else {
			panic("Failed to recognize instruction")
		}
	}
	return instructions
}

type Screen [][]bool

// Test variables
// const H = 3
// const W = 7

const H = 6
const W = 50

func (s Screen) rect(A, B int) {
	for i := 0; i < B; i++ {
		row := s[i]
		for j := 0; j < A; j++ {
			row[j] = true
		}
	}
}

func (s Screen) rotateRow(A, B int) {
	oldRow := s[A]
	newRow := make([]bool, W)
	for i := 0; i < W; i++ {
		newRow[(i+B)%W] = oldRow[i]
	}
	s[A] = newRow
}

func (s Screen) rotateColumn(A, B int) {
	newColumn := make([]bool, H)
	for i := 0; i < H; i++ {
		newColumn[(i+B)%H] = s[i][A]
	}
	for i := 0; i < H; i++ {
		s[i][A] = newColumn[i]
	}
}

func (s Screen) countLit() int {
	count := 0
	for _, row := range s {
		for _, lit := range row {
			if lit {
				count += 1
			}
		}
	}
	return count
}

func (s Screen) print() {
	for _, row := range s {
		for _, light := range row {
			var char string
			if light {
				char = "#"
			} else {
				char = "."
			}
			fmt.Printf(char)
		}
		fmt.Println("")
	}
}

func part1() Screen {
	var screen Screen
	for i := 0; i < H; i++ {
		screen = append(screen, make([]bool, W))
	}
	for _, instruction := range parseInput() {
		switch instruction.type_ {
		case "rect":
			screen.rect(instruction.A, instruction.B)
		case "rotateColumn":
			screen.rotateColumn(instruction.A, instruction.B)
		case "rotateRow":
			screen.rotateRow(instruction.A, instruction.B)
		default:
			panic(fmt.Sprintf("Unexpected instruction: %s", instruction.type_))
		}
	}
	fmt.Println("There are ", screen.countLit(), " lit lights")
	return screen
}

func part2() {
	part1().print()
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

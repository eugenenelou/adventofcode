package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type Instruction struct {
	direction string
	distance  int
}

func parseInput() []Instruction {
	content, err := io.ReadAll(os.Stdin)
	fmt.Println(string(content))
	if err != nil {
		panic(err)
	}
	var instructions []Instruction
	for _, rawInstruction := range strings.Split(string(content), ", ") {
		direction := string(rawInstruction[0])
		distance, _ := strconv.Atoi(rawInstruction[1:])
		instructions = append(instructions, Instruction{direction, distance})
	}
	return instructions
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func newDirection(x int, y int, direction string) (int, int) {
	if x == 0 {
		if direction == "R" {
			return y, 0
		}
		return -y, 0
	}
	if direction == "R" {
		return 0, -x
	}
	return 0, x
}

func part1() {
	instructions := parseInput()
	distX, distY := 0, 0
	coeffX, coeffY := 1, 0
	for _, instruction := range instructions {
		coeffX, coeffY = newDirection(coeffX, coeffY, instruction.direction)
		distX += instruction.distance * coeffX
		distY += instruction.distance * coeffY
	}
	fmt.Println(fmt.Sprint(Abs(distX) + Abs(distY)))
}

type Point struct {
	x int
	y int
}
type void struct{}

var empty void

func sign(x int) int {
	if x < 0 {
		return -1
	}
	return 1
}

func part2() {
	instructions := parseInput()
	distX, distY := 0, 0
	coeffX, coeffY := 0, 1
	visitedPoints := make(map[Point]void)
	var resultX, resultY int
	found := false
	for _, instruction := range instructions {
		// fmt.Println("Instruction", instruction)
		coeffX, coeffY = newDirection(coeffX, coeffY, instruction.direction)
		diffX := instruction.distance * coeffX
		diffY := instruction.distance * coeffY

		for i := 0; i < Abs(diffX); i++ {
			coordinate := Point{distX + i*sign(diffX), distY}
			_, alreadyVisited := visitedPoints[coordinate]
			if alreadyVisited {
				resultX = coordinate.x
				resultY = coordinate.y
				found = true
				break
			}
			// fmt.Println("Walked ", coordinate)
			visitedPoints[coordinate] = empty
		}
		for i := 0; i < Abs(diffY); i++ {
			coordinate := Point{distX, distY + i*sign(diffY)}
			_, alreadyVisited := visitedPoints[coordinate]
			if alreadyVisited {
				resultX = coordinate.x
				resultY = coordinate.y
				found = true
				break
			}
			// fmt.Println("Walked ", coordinate)
			visitedPoints[coordinate] = empty
		}
		if found {
			break
		}

		distX += diffX
		distY += diffY
		// fmt.Println("Visited (", distX, ", ", distY, ")")
	}
	fmt.Println("Stopped at (", resultX, ", ", resultY, ")")
	fmt.Println(fmt.Sprint(Abs(resultX) + Abs(resultY)))
}

func main() {
	if os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

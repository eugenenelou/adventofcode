package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Triangle struct {
	a int
	b int
	c int
}

func (t Triangle) isValid() bool {
	return t.a+t.b > t.c && t.a+t.c > t.b && t.b+t.c > t.a
}

func parseInput() []Triangle {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var instructions []Triangle
	for _, rawInstruction := range strings.Split(string(content), "\n") {
		if rawInstruction == "" {
			break
		}
		regex := regexp.MustCompile("\\s+")
		edges := regex.Split(strings.Trim(rawInstruction, " "), -1)
		a, _ := strconv.Atoi(edges[0])
		b, _ := strconv.Atoi(edges[1])
		c, _ := strconv.Atoi(edges[2])
		instructions = append(instructions, Triangle{a, b, c})
	}
	return instructions
}

func parseInput2() []Triangle {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var instructions []Triangle
	i := 0
	var edges [9]int
	for _, rawInstruction := range strings.Split(string(content), "\n") {
		if rawInstruction == "" {
			break
		}
		regex := regexp.MustCompile("\\s+")
		rowEdges := regex.Split(strings.Trim(rawInstruction, " "), -1)
		a, _ := strconv.Atoi(rowEdges[0])
		b, _ := strconv.Atoi(rowEdges[1])
		c, _ := strconv.Atoi(rowEdges[2])
		edges[3*i] = a
		edges[3*i+1] = b
		edges[3*i+2] = c

		i += 1
		if i == 3 {
			i = 0
			instructions = append(instructions, Triangle{edges[0], edges[3], edges[6]})
			instructions = append(instructions, Triangle{edges[1], edges[4], edges[7]})
			instructions = append(instructions, Triangle{edges[2], edges[5], edges[8]})
		}
	}
	return instructions
}

func part1() {
	count := 0
	for _, triangle := range parseInput() {
		if triangle.isValid() {
			count += 1
		}
	}
	fmt.Printf("There are %d valid triangles\n", count)
}

func part2() {
	count := 0
	for _, triangle := range parseInput2() {
		if triangle.isValid() {
			count += 1
		}
	}
	fmt.Printf("There are %d valid triangles\n", count)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

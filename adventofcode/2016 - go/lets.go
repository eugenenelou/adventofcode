package main

import (
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
		if rawInstruction == "" {
			break
		}
		instructions = append(instructions, rawInstruction)
	}
	return instructions
}

func part1() {
	panic(true)
}

func part2() {
	panic(true)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

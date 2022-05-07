package main

import (
	"os"
)

func part1() {
	panic(true)
}

func part2() {
	panic(true)
}

func main() {
	if os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

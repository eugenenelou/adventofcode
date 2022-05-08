package main

import (
	"fmt"
	"io"
	"math"
	"os"
	"strings"
)

func parseInput() []string {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var instructions []string
	for _, rawInstruction := range strings.Split(string(content), "\r\n") {
		if rawInstruction == "" {
			break
		}
		instructions = append(instructions, rawInstruction)
	}
	return instructions
}

type Counter map[rune]int

func (c Counter) mostCommon() rune {
	mostCommonLetter := 'a'
	count := 0
	for k, v := range c {
		if v > count {
			count = v
			mostCommonLetter = k
		}
	}
	return mostCommonLetter
}

func (c Counter) leastCommon() rune {
	leastCommonLetter := 'a'
	count := math.MaxInt
	for k, v := range c {
		if 0 < v && v < count {
			count = v
			leastCommonLetter = k
		}
	}
	return leastCommonLetter
}

func countLetters() []Counter {
	var counters []Counter
	for i := 0; i < 8; i++ {
		counters = append(counters, Counter{})
	}
	for _, word := range parseInput() {
		for i, letter := range word {
			counters[i][letter] += 1 // should not work
		}
	}
	return counters
}

func part1() {
	counters := countLetters()
	var word [8]string
	for i, counter := range counters {
		word[i] = string(counter.mostCommon())
	}
	fmt.Printf("The corrected message is: %s", strings.Join(word[:], ""))
}

func part2() {
	counters := countLetters()
	var word [8]string
	for i, counter := range counters {
		word[i] = string(counter.leastCommon())
	}
	fmt.Printf("The corrected message is: %s", strings.Join(word[:], ""))
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

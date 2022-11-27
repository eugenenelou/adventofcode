package main

import (
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Range struct {
	lower int
	upper int
}

func parseInput() []Range {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var ranges []Range
	for _, rawInstruction := range strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n") {
		if rawInstruction == "" {
			break
		}
		bounds := strings.Split(rawInstruction, "-")
		lower, _ := strconv.Atoi(bounds[0])
		upper, _ := strconv.Atoi(bounds[1])
		ranges = append(ranges, Range{lower, upper})
	}
	return ranges
}

func part1() {
	ranges := parseInput()

	// sort the ranges by lower bound
	// the result is the first time, when iterating sorted ranges,
	// a lower bound is superior to the previous upper bound + 1
	sort.Slice(ranges, func(i, j int) bool {
		return ranges[i].lower < ranges[j].lower
	})

	if ranges[0].lower > 0 {
		fmt.Printf("Result is 0")
	}
	last_upper := 0
	for _, range_ := range ranges {
		if range_.lower > last_upper+1 {
			fmt.Printf("Result is %d", last_upper+1)
			return
		}
		if range_.upper > last_upper {
			last_upper = range_.upper
		}
	}
	panic("Result not found")
}

const MAX = 4294967295

func part2() {
	ranges := parseInput()

	// sort the ranges by lower bound
	// the result is the first time, when iterating sorted ranges,
	// a lower bound is superior to the previous upper bound + 1
	sort.Slice(ranges, func(i, j int) bool {
		return ranges[i].lower < ranges[j].lower
	})

	count := 0
	last_upper := -1
	for _, range_ := range ranges {
		if range_.lower > last_upper+1 {
			count += range_.lower - last_upper - 1
		}
		if range_.upper > last_upper {
			last_upper = range_.upper
		}
	}
	if last_upper < MAX {
		count += MAX - last_upper
	}
	fmt.Printf("Result is %d", count)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

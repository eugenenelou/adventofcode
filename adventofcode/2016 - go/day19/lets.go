package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func parseInput() int {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var n int
	rawN := strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n")[0]
	n, _ = strconv.Atoi(rawN)
	return n
}

func part1() {
	n := parseInput()
	list := make([]int, n)
	for i := 0; i < n; i++ {
		list[i] = i + 1
	}

	start_at_one := true
	for len(list) > 1 {
		remaining := len(list)
		if start_at_one {
			// no need to start at 0, 0==2*0
			for i := 1; 2*i < remaining; i++ {
				list[i] = list[2*i]
			}
			list = list[:(remaining+1)/2]
		} else {
			for i := 0; 2*i+1 < remaining; i++ {
				list[i] = list[2*i+1]
			}
			list = list[:remaining/2]
		}
		// start at one changes if the remaining number was odd
		start_at_one = (remaining%2 == 0) == start_at_one
	}
	fmt.Printf("Elf %d takes all presents", list[0])
}

func get_opposite_idx(list_length int, idx int) int {
	res := idx + list_length/2
	if res >= list_length {
		res -= list_length
	}
	return res
}

func part2() {
	// when taking the opposites in the circle, eliminated positions are always
	// 2 consecutive, then spare one, then 2 consecutive ... in a pattern.
	// to avoid recreating slices at every elimination, we eleminate all the positions
	// in the second half of the slice, before reconstructing the slice with the remaining
	// positions
	// and rotating the slice so that the next position to eliminato its opposite is at index 0
	n := parseInput()

	list := make([]int, n)
	for i := 0; i < n; i++ {
		list[i] = i + 1
	}
	for len(list) > 1 {
		current_length := len(list)
		first_opposite := get_opposite_idx(current_length, 0)
		var first_kept int
		if current_length%2 == 0 {
			first_kept = first_opposite + 2
		} else {
			first_kept = first_opposite + 1
		}
		elements_kept := 0
		for i := first_kept; i < current_length; i += 3 {
			list[first_opposite+elements_kept] = list[i]
			elements_kept += 1
		}
		elements_removed := (current_length - first_opposite - elements_kept)
		list = append(list[elements_removed:first_opposite+elements_kept], list[:elements_removed]...)

	}
	fmt.Printf("Elf %d takes all presents", list[0])
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

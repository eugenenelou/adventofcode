package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
)

func parseInput() string {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	return string(content)
}

func part1() {
	length := 0
	in_marker := false
	marker_x_found := false
	marker_a := ""
	marker_b := ""
	input := parseInput()
	for i := 0; i < len(input); i++ {
		char := input[i]
		switch char {
		case '(':
			in_marker = true
			marker_x_found = false
			marker_a = ""
			marker_b = ""
		case ')':
			in_marker = false
			a, _ := strconv.Atoi(marker_a)
			b, _ := strconv.Atoi(marker_b)
			length += a * b
			i += a
		default:
			if in_marker {
				if char == 'x' {
					marker_x_found = true
				} else if marker_x_found {
					marker_b = marker_b + string(char)
				} else {
					marker_a = marker_a + string(char)
				}
			} else {
				length += 1
			}
		}
	}
	fmt.Printf("The final length is %d\n", length)
}

// just go recursive
func get_decompressed_length(input string) int {
	length := 0
	in_marker := false
	marker_x_found := false
	marker_a := ""
	marker_b := ""
	for i := 0; i < len(input); i++ {
		char := input[i]
		switch char {
		case '(':
			in_marker = true
			marker_x_found = false
			marker_a = ""
			marker_b = ""
		case ')':
			in_marker = false
			a, _ := strconv.Atoi(marker_a)
			b, _ := strconv.Atoi(marker_b)
			length += b * get_decompressed_length(input[i+1:i+1+a])
			i += a
		default:
			if in_marker {
				if char == 'x' {
					marker_x_found = true
				} else if marker_x_found {
					marker_b = marker_b + string(char)
				} else {
					marker_a = marker_a + string(char)
				}
			} else {
				length += 1
			}
		}
	}
	return length
}

func part2() {
	fmt.Printf("The final length is %d\n", get_decompressed_length(parseInput()))
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

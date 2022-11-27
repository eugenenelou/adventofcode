package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Operation struct {
	op string
	a  rune
	b  rune
	x  int
	y  int
}

func parseUnaryInt(raw string) int {
	unary_int_regex := regexp.MustCompile(".*\\s(\\d+)(\\s.*)?")
	rawX := unary_int_regex.FindStringSubmatch(raw)[1]
	x, _ := strconv.Atoi(rawX)
	return x
}

func parseUnaryString(raw string) rune {
	unary_int_regex := regexp.MustCompile(".*\\s([a-z])(\\s.*)?")
	a := rune(unary_int_regex.FindStringSubmatch(raw)[1][0])
	return a
}

func parseBinaryInt(raw string) (int, int) {
	unary_int_regex := regexp.MustCompile(".*\\s(\\d+)\\s.*\\s(\\d+)")
	rawX := unary_int_regex.FindStringSubmatch(raw)[1]
	rawY := unary_int_regex.FindStringSubmatch(raw)[2]
	x, _ := strconv.Atoi(rawX)
	y, _ := strconv.Atoi(rawY)
	return x, y
}

func parseBinaryString(raw string) (rune, rune) {
	unary_int_regex := regexp.MustCompile(".*\\s([a-z])\\s.*\\s([a-z])")
	a := rune(unary_int_regex.FindStringSubmatch(raw)[1][0])
	b := rune(unary_int_regex.FindStringSubmatch(raw)[2][0])
	return a, b
}

func parseOperation(raw string) Operation {
	fmt.Printf("Parsing operation %s\r\n", raw)
	if strings.HasPrefix(raw, "swap position") {
		x, y := parseBinaryInt(raw)
		return Operation{"swap_position", '0', '0', x, y}
	}
	if strings.HasPrefix(raw, "swap letter") {
		a, b := parseBinaryString(raw)
		return Operation{"swap_letter", a, b, 0, 0}
	}
	if strings.HasPrefix(raw, "rotate left") {
		x := parseUnaryInt(raw)
		return Operation{"rotate_left", '0', '0', x, 0}
	}
	if strings.HasPrefix(raw, "rotate right") {
		x := parseUnaryInt(raw)
		return Operation{"rotate_right", '0', '0', x, 0}
	}
	if strings.HasPrefix(raw, "rotate based") {
		a := parseUnaryString(raw)
		return Operation{"rotate", a, '0', 0, 0}
	}
	if strings.HasPrefix(raw, "reverse") {
		x, y := parseBinaryInt(raw)
		return Operation{"reverse", '0', '0', x, y}
	}
	if strings.HasPrefix(raw, "move") {
		x, y := parseBinaryInt(raw)
		return Operation{"move", '0', '0', x, y}
	}
	panic(fmt.Sprintf("Unrecognized operation: %s", raw))

}

func parseInput() (starting_string []rune, operations []Operation) {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	operations = make([]Operation, 0)
	for i, rawInstruction := range strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n") {
		if rawInstruction == "" {
			break
		}
		if i == 0 {
			starting_string = []rune(rawInstruction)
		} else {
			operations = append(operations, parseOperation(rawInstruction))
		}
	}
	return starting_string, operations
}

func (o Operation) apply(input []rune) []rune {
	if o.op == "swap_position" {
		input[o.x], input[o.y] = input[o.y], input[o.x]
		return input
	}
	if o.op == "swap_letter" {
		for i, char := range input {
			if char == o.a {
				input[i] = o.b
			} else if char == o.b {
				input[i] = o.a
			}
		}
		return input
	}
	if o.op == "rotate_left" {
		return append(input[o.x:], input[:o.x]...)
	}
	if o.op == "rotate_right" {
		anchor := len(input) - o.x
		return append(input[anchor:], input[:anchor]...)
	}
	if o.op == "rotate" {
		var anchor_index int
		for i, char := range input {
			if char == o.a {
				anchor_index = i
				break
			}
		}
		rotate_times := 1 + anchor_index
		if anchor_index >= 4 {
			rotate_times += 1
		}
		anchor := len(input) - (rotate_times % len(input))
		return append(input[anchor:], input[:anchor]...)
	}
	if o.op == "reverse" {
		slice_copy := make([]rune, o.y+1-o.x)
		copy(slice_copy, input[o.x:o.y+1])
		for i, char := range slice_copy {
			input[o.y-i] = char
		}
		return input
	}
	if o.op == "move" {
		if o.x == o.y {
			return input
		}
		if o.x < o.y {
			res := make([]rune, 0)
			res = append(res, input[:o.x]...)
			res = append(res, input[o.x+1:o.y+1]...)
			res = append(res, input[o.x])
			res = append(res, input[o.y+1:]...)
			return res
		}
		res := make([]rune, 0)
		res = append(res, input[:o.y]...)
		res = append(res, input[o.x])
		res = append(res, input[o.y:o.x]...)
		res = append(res, input[o.x+1:]...)
		return res
	}
	if o.op == "reverse_rotate" {
		var anchor_index int
		for i, char := range input {
			if char == o.a {
				anchor_index = i
				break
			}
		}
		var target_index int
		if anchor_index == 0 {
			target_index = len(input) - 1
		} else if anchor_index%2 == 0 {
			// it comes from an index > 4
			target_index = (anchor_index+len(input))/2 - 1
		} else {
			target_index = (anchor_index - 1) / 2
		}
		var rotate_times int
		if target_index > anchor_index {
			rotate_times = len(input) - target_index + anchor_index
		} else {
			rotate_times = anchor_index - target_index
		}
		return append(input[rotate_times:], input[:rotate_times]...)
	}
	panic(fmt.Sprintf("Unrecognized operation %s", o.op))
}

func part1() {
	password, operations := parseInput()
	for _, op := range operations {
		old_password := string(password)
		new_password := op.apply(password)
		fmt.Printf("%s -> %s  : operations: %v\r\n", old_password, string(new_password), op)
		password = new_password
	}
	fmt.Printf("Resulting password is: %s", string(password))
}

func (o Operation) reverseOp() Operation {
	if o.op == "swap_position" || o.op == "swap_letter" || o.op == "reverse" {
		return o
	}
	if o.op == "rotate_left" {
		return Operation{"rotate_right", o.a, o.b, o.x, o.y}
	}
	if o.op == "rotate_right" {
		return Operation{"rotate_left", o.a, o.b, o.x, o.y}
	}
	if o.op == "rotate" {
		return Operation{"reverse_rotate", o.a, o.b, o.x, o.y}
	}
	if o.op == "move" {
		return Operation{"move", o.a, o.b, o.y, o.x}
	}
	panic(fmt.Sprintf("Unrecognized operation %s", o.op))
}

func part2() {
	password, operations := parseInput()
	password = []rune("fbgdceah")
	n_operations := len(operations)
	reversed_operations := make([]Operation, n_operations)
	for i, op := range operations {
		reversed_operations[n_operations-i-1] = op.reverseOp()
	}
	for _, op := range reversed_operations {
		old_password := string(password)
		new_password := op.apply(password)
		fmt.Printf("%s -> %s  : operations: %v\r\n", old_password, string(new_password), op)
		password = new_password
	}
	fmt.Printf("Resulting unscrambled password is: %s", string(password))
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

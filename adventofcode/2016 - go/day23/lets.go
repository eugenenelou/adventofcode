package main

import (
	"errors"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func hasOneArgument(instruction string) bool {
	return strings.HasPrefix(instruction, "inc") || strings.HasPrefix(instruction, "dec") || strings.HasPrefix(instruction, "tgl")
}

func parseInput() []string {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var instructions []string
	for _, rawInstruction := range strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n") {
		if rawInstruction == "" {
			break
		}
		instructions = append(instructions, rawInstruction)
	}
	return instructions
}

func get_value(registries map[string]int, value string) int {
	cmp, err := strconv.Atoi(value)
	if err != nil {
		return registries[value]
	}
	return cmp
}

func toggleInstruction(instruction string) string {
	values := strings.Split(instruction, " ")
	if strings.HasPrefix(instruction, "cpy ") {
		return strings.Join([]string{"jnz", values[1], values[2]}, " ")
	} else if strings.HasPrefix(instruction, "jnz ") {
		return strings.Join([]string{"cpy", values[1], values[2]}, " ")
	} else if strings.HasPrefix(instruction, "inc ") {
		return strings.Join([]string{"dec", values[1]}, " ")
	} else if strings.HasPrefix(instruction, "dec ") || strings.HasPrefix(instruction, "tgl ") {
		return strings.Join([]string{"inc", values[1]}, " ")
	} else {
		panic(fmt.Sprintf("Unrecognized instruction: %s\n", instruction))
	}
}

// We simplify the multipiclation instruction:
// cpy b c
// inc a
// dec c
// jnz c -2
// dec d
// jnz d -5
//
// becomes:
//
// cpy b*d a
// cpy 0 c
// cpy 0 d

func isMultiply(instructions []string) (string, string, string, string, error) {
	// this does not have all the verifications but is enough for our input
	if len(instructions) >= 6 && strings.HasPrefix(instructions[0], "cpy ") && strings.HasPrefix(instructions[1], "inc ") && strings.HasPrefix(instructions[2], "dec ") && strings.HasPrefix(instructions[3], "jnz ") && strings.HasPrefix(instructions[4], "dec ") && strings.HasPrefix(instructions[5], "jnz ") {
		values := strings.Split(instructions[0], " ")
		r_b := values[1]
		r_c := values[2]
		r_a := strings.Split(instructions[1], " ")[1]
		r_d := strings.Split(instructions[4], " ")[1]

		return r_a, r_b, r_c, r_d, nil
	}
	return "", "", "", "", errors.New("Not a multiplication")
}

func run(registries map[string]int) {
	instructions := parseInput()
	fmt.Printf("instructions: %v\n", instructions)
	fmt.Println()

	j := 0
	for i := 0; i < len(instructions) && j < 10000000000; j++ {
		instruction := instructions[i]
		r_a, r_b, r_c, r_d, err := isMultiply(instructions[i:])
		if i+5 < len(instructions) && err == nil {
			registries[r_a] += get_value(registries, r_b) * get_value(registries, r_d)
			registries[r_c] = 0
			registries[r_d] = 0
			i += 6
		} else if strings.HasPrefix(instruction, "cpy ") {
			values := strings.Split(instruction, " ")
			registry := values[2]
			_, err := strconv.Atoi(registry)
			if err != nil {
				// registry is not a valid registry, it's an integer
				registries[registry] = get_value(registries, values[1])
			}
			i++
		} else if strings.HasPrefix(instruction, "inc ") {
			registry := strings.Split(instruction, " ")[1]
			registries[registry] += 1
			i++
		} else if strings.HasPrefix(instruction, "dec ") {
			registry := strings.Split(instruction, " ")[1]
			registries[registry] -= 1
			i++
		} else if strings.HasPrefix(instruction, "jnz ") {
			values := strings.Split(instruction, " ")
			cmp := get_value(registries, values[1])
			if cmp == 0 {
				i++
			} else {
				i += get_value(registries, values[2])
			}
		} else if strings.HasPrefix(instruction, "tgl") {
			values := strings.Split(instruction, " ")
			x := get_value(registries, values[1])
			idx := x + i
			if idx >= 0 && idx < len(instructions) {
				instructions[idx] = toggleInstruction(instructions[idx])
			}
			i++
		} else {
			panic(fmt.Sprintf("Unrecognized instruction: %s\n", instruction))
		}
	}
	fmt.Println("a: ", registries["a"])
	fmt.Println("b: ", registries["b"])
	fmt.Println("c: ", registries["c"])
	fmt.Println("d: ", registries["d"])
}

func part1() {
	registries := map[string]int{
		"a": 7,
		"b": 0,
		"c": 0,
		"d": 0,
	}
	run(registries)
}

func part2() {
	registries := map[string]int{
		"a": 12,
		"b": 0,
		"c": 0,
		"d": 0,
	}
	run(registries)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

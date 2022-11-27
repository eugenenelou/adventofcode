package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

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

func run(registries map[string]int) {
	instructions := parseInput()
	fmt.Println()

	j := 0
	for i := 0; i < len(instructions); j++ {
		instruction := instructions[i]
		if strings.HasPrefix(instruction, "cpy ") {
			values := strings.Split(instruction, " ")
			// fmt.Printf("values: %v\n", values)
			registry := values[2]
			// fmt.Println("cpy registry", registry, get_value(registries, values[1]))
			registries[registry] = get_value(registries, values[1])
			i++
		} else if strings.HasPrefix(instruction, "inc ") {
			registry := strings.Split(instruction, " ")[1]
			// fmt.Println("inc registry", registry)
			registries[registry] += 1
			i++
		} else if strings.HasPrefix(instruction, "dec ") {
			registry := strings.Split(instruction, " ")[1]
			// fmt.Println("dec registry", registry)
			registries[registry] -= 1
			i++
		} else if strings.HasPrefix(instruction, "jnz ") {
			values := strings.Split(instruction, " ")
			cmp := get_value(registries, values[1])
			// fmt.Println("cmp:", cmp, "jump: ", get_value(registries, values[2]))
			if cmp == 0 {
				i++
			} else {
				i += get_value(registries, values[2])
			}

		} else {
			panic(fmt.Sprintf("Unrecognized instruction: %s\n", instruction))
		}
		// fmt.Println("j: ", j)
		// fmt.Println("i: ", i)
		// fmt.Println("a: ", registries["a"])
		// fmt.Println("b: ", registries["b"])
		// fmt.Println("c: ", registries["c"])
		// fmt.Println("d: ", registries["d"])
		// fmt.Println()
	}
	fmt.Println("a: ", registries["a"])
	fmt.Println("b: ", registries["b"])
	fmt.Println("c: ", registries["c"])
	fmt.Println("d: ", registries["d"])
}

func part1() {
	registries := map[string]int{
		"a": 0,
		"b": 0,
		"c": 0,
		"d": 0,
	}
	run(registries)
}

func part2() {
	registries := map[string]int{
		"a": 0,
		"b": 0,
		"c": 1,
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

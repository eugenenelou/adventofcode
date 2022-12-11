package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

func supportTLS(ipv7 string) bool {
	inBracket := false
	abbaOutsideHypernet := false
	for i, char := range ipv7 {
		if char == '[' {
			inBracket = true
		} else if char == ']' {
			inBracket = false
		} else if i >= 3 && ipv7[i] == ipv7[i-3] && ipv7[i] != ipv7[i-2] && ipv7[i-2] == ipv7[i-1] {
			if inBracket {
				return false
			}
			abbaOutsideHypernet = true
		}
	}
	return abbaOutsideHypernet
}

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
	count := 0
	for _, ipv7 := range parseInput() {
		if supportTLS(ipv7) {
			count += 1
		}
	}
	fmt.Println("IPs that support TLS: ", count)
}

type void struct{}

var empty void

type Set map[string]void

func supportSSL(ipv7 string) bool {
	ABAs := make(Set)
	BABs := make(Set)
	inBracket := false
	for i, char := range ipv7 {
		if char == '[' {
			inBracket = true
		} else if char == ']' {
			inBracket = false
		} else if i >= 2 && ipv7[i] == ipv7[i-2] && ipv7[i] != ipv7[i-1] {
			if inBracket {
				BABs[fmt.Sprintf("%s%s", string(ipv7[i-1]), string(ipv7[i]))] = empty // store AB to allow comparison with ABAs
			} else {
				ABAs[fmt.Sprintf("%s%s", string(ipv7[i]), string(ipv7[i-1]))] = empty
			}
		}
	}
	for ab, _ := range ABAs {
		_, foundMatch := BABs[ab]
		if foundMatch {
			return true
		}
	}
	return false
}

func part2() {
	count := 0
	for _, ipv7 := range parseInput() {
		if supportSSL(ipv7) {
			count += 1
		}
	}
	fmt.Println("IPs that support SSL: ", count)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

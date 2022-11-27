package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func parseInput() (disk int, input string) {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	rows := strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n")
	disk, _ = strconv.Atoi(rows[0])
	input = rows[1]
	return disk, input
}

func dragon_curve(disk int, input string) string {
	var string_builder strings.Builder
	string_builder.WriteString(input)
	string_builder.WriteByte('0')
	l := len(input)
	for i := len(input) - 1; i >= 0 && 2*l+1-i <= disk; i-- {
		char := input[i]
		if char == '0' {
			string_builder.WriteByte('1')
		} else {
			string_builder.WriteByte('0')
		}
	}
	data := string_builder.String()
	if len(data) >= disk {
		return data[:disk]
	}
	fmt.Printf("too short curve: %d/%d\r\n", len(data), disk)
	return dragon_curve(disk, data)
}

func checksum(input string) string {
	if len(input)%2 == 1 {
		panic("Checksum only work on even length string")
	}
	var string_builder strings.Builder
	for i := 0; 2*i < len(input); i++ {
		if input[2*i] == input[2*i+1] {
			string_builder.WriteByte('1')
		} else {
			string_builder.WriteByte('0')
		}
	}
	sum := string_builder.String()
	if len(sum)%2 == 1 {
		return sum
	} else {
		fmt.Printf("Even length checksum: %s, recomputing\r\n", sum)
		return checksum(sum)
	}
}

func part1() {
	disk, input := parseInput()
	data := dragon_curve(disk, input)
	fmt.Printf("curve (len: %d): %s\r\n", len(data), data)
	fmt.Printf("checksum: %s", checksum(data))
}

func part2() {
	disk := 35651584
	_, input := parseInput()
	data := dragon_curve(disk, input)
	fmt.Printf("curve len: %d", len(data))
	fmt.Printf("checksum: %s", checksum(data))
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

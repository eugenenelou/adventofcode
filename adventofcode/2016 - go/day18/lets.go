package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

func parseInput() Row {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	tiles := make([]bool, 0)
	for _, char := range strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n")[0] {
		tiles = append(tiles, char == '^')
	}
	return Row{tiles}
}

type Row struct {
	tiles []bool
}

func (r Row) count_safe_tiles() int {
	count := 0
	for _, tile := range r.tiles {
		if !tile {
			count += 1
		}
	}
	return count
}

func (r Row) next_row() Row {
	// the tile is a trap if on the previous row: left XOR right
	tiles := make([]bool, 0)
	tiles = append(tiles, r.tiles[1])
	n := len(r.tiles)
	for i := 0; i < n-2; i++ {
		tiles = append(tiles, r.tiles[i] != r.tiles[i+2])
	}
	tiles = append(tiles, r.tiles[n-2])
	return Row{tiles}
}

func (r Row) print() {
	var string_builder strings.Builder
	for _, trap := range r.tiles {
		if trap {
			string_builder.WriteByte('^')
		} else {
			string_builder.WriteByte('.')
		}
	}
	fmt.Println(string_builder.String())
}

func run(n int) {
	row := parseInput()
	// row.print()
	count := row.count_safe_tiles()
	for i := 1; i < n; i++ {
		row = row.next_row()
		// row.print()
		count += row.count_safe_tiles()
	}
	fmt.Printf("There are %d safe tiles", count)
}

func part1() {
	run(40)
}

func part2() {
	run(400000)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

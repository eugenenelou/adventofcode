package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

func parseInput() ([]Node, int, int) {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var nodes []Node
	maxX := 0
	maxY := 0
	var wantedNode int
	for i, rawNode := range strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n")[2:] {
		if rawNode == "" {
			break
		}
		node := parseNode(rawNode)
		if node.x > maxX {
			maxX = node.x
			if node.y == 0 {
				wantedNode = i
			}
		}
		if node.y > maxY {
			maxY = node.y
		}
		nodes = append(nodes, node)
	}
	nodes[wantedNode].wanted = true
	return nodes, maxX, maxY
}

type Node struct {
	x      int
	y      int
	size   int
	used   int
	avail  int
	wanted bool
}

func (n Node) isDest() bool {
	return n.x == 0 && n.y == 0
}

func parseNode(raw string) Node {
	node_regex := regexp.MustCompile(".*-x(\\d+)-y(\\d+)\\s+(\\d+)T\\s+(\\d+)T\\s+\\d+T\\s+\\d+%")
	match := node_regex.FindStringSubmatch(raw)
	if match == nil {
		panic("Failed to parse instruction")
	}
	x, _ := strconv.Atoi(match[1])
	y, _ := strconv.Atoi(match[2])
	size, _ := strconv.Atoi(match[3])
	used, _ := strconv.Atoi(match[4])
	return Node{
		x:      x,
		y:      y,
		size:   size,
		used:   used,
		avail:  size - used,
		wanted: false,
	}
}

func part1() {
	nodes, _, _ := parseInput()

	nodes_by_avail := make([]Node, len(nodes))
	copy(nodes_by_avail, nodes)
	sort.Slice(nodes_by_avail, func(i, j int) bool {
		return nodes_by_avail[i].avail < nodes_by_avail[j].avail
	})

	fmt.Printf("Avail")
	for _, node := range nodes_by_avail {
		fmt.Printf("%d\r\n", node.avail)
	}
	nodes_by_used := make([]Node, len(nodes))
	copy(nodes_by_used, nodes)
	sort.Slice(nodes_by_used, func(i, j int) bool {
		return nodes_by_used[i].used < nodes_by_used[j].used
	})

	fmt.Printf("Used")
	for _, node := range nodes_by_used {
		fmt.Printf("%d\r\n", node.used)
	}

	avail_index := 0
	count_pairs := 0
	for _, node := range nodes_by_used {
		if node.used == 0 {
			continue
		}
		for nodes_by_avail[avail_index].avail < node.used {
			avail_index += 1
			if avail_index >= len(nodes) {
				break
			}
		}
		if avail_index >= len(nodes) {
			break
		}
		count_pairs += len(nodes) - avail_index
		if node.used <= node.avail {
			fmt.Printf("1: %d \n", 1)
			count_pairs -= 1
		}
	}
	fmt.Printf("There are %d valid pairs", count_pairs)
}

type NodeType int8

const (
	Empty NodeType = iota
	BigAndFull
	Movable
)

// Test
// const MovableLimit = 6
// const BigLimit = 15

const MovableLimit = 75
const BigLimit = 100

func (n Node) getType() NodeType {
	if n.size > MovableLimit {
		if n.size > BigLimit {
			if n.avail > MovableLimit {
				panic(fmt.Sprintf("Cannot handle big and not full: %v", n))
			} else {
				return BigAndFull
			}
		}
		if n.avail > MovableLimit {
			return Empty
		}
		return Movable
	}
	panic(fmt.Sprintf("Cannot handle small nodes: %v", n))
}

func (n NodeType) String() string {
	switch n {
	case Empty:
		return "_"
	case BigAndFull:
		return "#"
	case Movable:
		return "."
	}
	return "?"
}

func (n Node) String() string {
	var typeString string
	if n.wanted {
		typeString = "G"
	} else {
		typeString = n.getType().String()
	}

	if n.isDest() {
		return fmt.Sprintf("(%s)", typeString)
	}
	return fmt.Sprintf(" %s ", typeString)
}

type Direction int8

const (
	Down Direction = iota
	Right
	Up
	Left
)

type Grid [][]Node

func (g Grid) print() {
	for _, row := range g {
		for _, node := range row {
			fmt.Printf("%s", node.String())
		}
		fmt.Printf("\r\n")
	}
}

func (g Grid) getStartingCoords() (int, int) {
	emptyNodes := make([]Node, 0)
	for _, row := range g {
		for _, node := range row {
			if node.getType() == Empty {
				emptyNodes = append(emptyNodes, node)
			}
		}
	}
	if len(emptyNodes) != 1 {
		panic(fmt.Sprintf("Did not find exactly 1 empty node, found %d", len(emptyNodes)))
	}
	return emptyNodes[0].x, emptyNodes[0].y
}

func (g Grid) canMove(direction Direction, currentX int, currentY int) bool {
	switch direction {
	case Up:
		return currentX > 0 && g[currentX-1][currentY].getType() == Movable
	case Right:
		return currentY < len(g[0])-1 && g[currentX][currentY+1].getType() == Movable
	case Down:
		return currentX < len(g)-1 && g[currentX+1][currentY].getType() == Movable
	case Left:
		return currentY > 0 && g[currentX][currentY-1].getType() == Movable
	}
	panic("Unrecognized direction")
}

func (n *Node) add(used int) {
	n.used += used
	n.avail -= used
	if n.avail < 0 {
		panic("Added more to node than available")
	}
}

func (n *Node) empty() {
	n.used = 0
	n.avail = n.size
}

func (g Grid) move(direction Direction, currentX int, currentY int) Grid {
	newGrid := make(Grid, len(g))
	copy(newGrid, g)
	ySize := len(g[0])
	switch direction {
	case Up:
		newRow1 := make([]Node, ySize)
		newRow2 := make([]Node, ySize)
		copy(newRow1, g[currentX-1])
		copy(newRow2, g[currentX])
		newGrid[currentX-1] = newRow1
		newGrid[currentX] = newRow2
		newRow1[currentY].add(newRow2[currentY].used)
		newRow2[currentY].empty()
	case Right:
		newRow := make([]Node, ySize)
		copy(newRow, g[currentX])
		newRow[currentY+1].add(newRow[currentY].used)
		newRow[currentY].empty()
		newGrid[currentX] = newRow
	case Down:
		newRow1 := make([]Node, ySize)
		newRow2 := make([]Node, ySize)
		copy(newRow1, g[currentX])
		copy(newRow2, g[currentX+1])
		newGrid[currentX] = newRow1
		newGrid[currentX+1] = newRow2
		newRow2[currentY].add(newRow1[currentY].used)
		newRow1[currentY].empty()
	case Left:
		newRow := make([]Node, ySize)
		copy(newRow, g[currentX])
		newRow[currentY-1].add(newRow[currentY].used)
		newRow[currentY].empty()
		newGrid[currentX] = newRow
	}
	return newGrid
}

func getUserInput() Direction {
	arr := make([]string, 0)
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("Enter Text: ")
		// Scans a line from Stdin(Console)
		scanner.Scan()
		// Holds the string that scanned
		text := scanner.Text()
		if len(text) != 0 {
			fmt.Println(text)
			arr = append(arr, text)
		} else {
			break
		}

	}
	// Use collected inputs
	fmt.Println(arr)
	return Up
	// for {
	// consoleReader := bufio.NewReaderSize(os.Stdin, 1)
	// fmt.Print("Direction? >")
	// input, _ := consoleReader.ReadString('\r')

	// fmt.Println("Input: ", input)
	// switch input {
	// case "37": // left
	// 	return Left
	// case "38": // up
	// 	return Up
	// case "39": // right
	// 	return Right
	// case "40": // down
	// 	return Down
	// default:
	// 	fmt.Println("Unrecognized direction")
	// }
	// time.Sleep(time.Second)
	// }
	// return Up
}

func part2() {
	// 1. categorize nodes by: empty, big and full, movable
	nodes, maxX, _ := parseInput()

	grid := make(Grid, 0)
	x := -1
	var row []Node
	for i, node := range nodes {
		if node.x > x {
			x += 1
			if x != node.x {
				panic("Missing some nodes")
			}
			if i > 0 {
				grid = append(grid, row)

			}
			row = make([]Node, 0)
		}
		row = append(row, node)
	}
	grid = append(grid, row)

	for _, row := range grid {
		for _, node := range row {
			fmt.Printf("%s", node.String())
		}
		fmt.Printf("\r\n")
	}

	grid.print()
	maxX += 1
	return

	// // This is simple enough, let's make it a game:
	// // control the empty slot
	// currentX, currentY := grid.getStartingCoords()
	// goalX, goalY := maxX, 0

	// steps := 0
	// for goalX != 0 || goalY != 0 {
	// 	direction := getUserInput()
	// 	grid.print()
	// 	if grid.canMove(direction, currentX, currentY) {
	// 		grid = grid.move(direction, currentX, currentY)
	// 		steps += 1
	// 	} else {
	// 		fmt.Printf("Cannod move in this direction\r\n")
	// 	}
	// 	fmt.Sprintf("Steps: %d\r\n", steps)
	// }
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

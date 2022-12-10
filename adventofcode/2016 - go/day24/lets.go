package main

import (
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
	"strings"
)

type Point struct {
	x, y int
}

type Labyrinth struct {
	grid [][]rune
	n    int
	m    int
}

func parseInput() (Labyrinth, map[int]Point) {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var grid [][]rune
	pois := make(map[int]Point)
	for i, rawInstruction := range strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n") {
		if rawInstruction == "" {
			break
		}
		grid = append(grid, []rune(rawInstruction))
		for j, cell := range rawInstruction {
			if cell != '#' && cell != '.' {
				number, err := strconv.Atoi(string(cell))
				if err != nil {
					panic("failed to parse cell")
				}
				pois[number] = Point{i, j}
			}
		}
	}
	return Labyrinth{grid, len(grid), len(grid[0])}, pois
}

type Pair struct {
	a, b int
}

func get_next_paths(labyrinth Labyrinth, visited map[Point]bool, point Point) []Point {
	nexts := make([]Point, 0)
	up := Point{point.x - 1, point.y}
	if point.x > 0 && !visited[up] && labyrinth.grid[up.x][up.y] != '#' {
		nexts = append(nexts, up)
	}
	left := Point{point.x, point.y - 1}
	if point.y > 0 && !visited[left] && labyrinth.grid[left.x][left.y] != '#' {
		nexts = append(nexts, left)
	}
	down := Point{point.x + 1, point.y}
	if point.x < labyrinth.n-1 && !visited[down] && labyrinth.grid[down.x][down.y] != '#' {
		nexts = append(nexts, down)
	}
	right := Point{point.x, point.y + 1}
	if point.y < labyrinth.m-1 && !visited[right] && labyrinth.grid[right.x][right.y] != '#' {
		nexts = append(nexts, right)
	}
	return nexts

}

func score_route(route []int, distances map[Pair]int) int {
	sum := 0
	for i := 0; i < len(route)-1; i++ {
		sum += distances[Pair{route[i], route[i+1]}]
	}
	return sum
}

// Permutation generation algorithm from:
// https://stackoverflow.com/questions/30226438/generate-all-permutations-in-go
func nextPerm(p []int) {
	for i := len(p) - 1; i >= 0; i-- {
		if i == 0 || p[i] < len(p)-i-1 {
			p[i]++
			return
		}
		p[i] = 0
	}
}

func shortest_route(distances map[Pair]int, numbers []int, second_part bool) int {
	result := math.MaxInt

	// iterate all permutations of the numbers that start with 0
	orig := make([]int, len(numbers)-1)
	i := 0
	for _, number := range numbers {
		if number > 0 {
			orig[i] = number
			i++
		}
	}
	for p := make([]int, len(orig)); p[0] < len(p); nextPerm(p) {
		perm := getPerm(orig, p)
		// as we go through every permutation, putting 0 at the end
		// is equivalent to putting it at the start
		perm = append(perm, 0)
		if second_part {
			perm = append([]int{0}, perm...)
		}
		steps := score_route(perm, distances)
		if steps < result {
			result = steps
			fmt.Println("steps", steps, perm)
		}
	}
	return result
}

func getPerm(orig, p []int) []int {
	result := append([]int{}, orig...)
	for i, v := range p {
		result[i], result[i+v] = result[i+v], result[i]
	}
	return result
}

func run(second_part bool) int {
	// 1. parse the input
	labyrinth, pois := parseInput()
	poi_numbers := make(map[Point]int)
	numbers := []int{}
	for key, value := range pois {
		poi_numbers[value] = key
		numbers = append(numbers, key)
	}
	// for _, row := range labyrinth.grid {
	// 	fmt.Println(row)
	// }
	// fmt.Println(pois)
	// 2. compute the distance between each couple of numbers
	distances := make(map[Pair]int)
	for number, poi := range pois {
		visited := make(map[Point]bool)
		distance := 0
		to_visit := []Point{poi}
		i := 0
		for len(to_visit) > 0 {
			i += 1
			// fmt.Println("i", i, to_visit, len(visited))
			distance += 1
			next_to_visit := make([]Point, 0)
			for _, point := range to_visit {
				for _, next := range get_next_paths(labyrinth, visited, point) {
					visited[next] = true
					visited_number, found := poi_numbers[next]
					if found {
						distances[Pair{visited_number, number}] = distance
						distances[Pair{number, visited_number}] = distance
					}
					next_to_visit = append(next_to_visit, next)
				}
			}
			to_visit = next_to_visit
		}
	}
	fmt.Println("Distances:", distances)
	// 3. compute the distance of each possible route (n! with n < 10 is ok)
	return shortest_route(distances, numbers, second_part)
}

func part2() int {
	return 0
}

func main() {
	// visited := make(map[Point]int)
	// visited[Point{1, 1}] = 32
	// print(visited[Point{1, 1}])
	// return
	second_part := len(os.Args) > 1 && os.Args[1] == "--two"
	fmt.Println("result: ", run(second_part))
}

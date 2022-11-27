package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strings"
)

type Element struct {
	rock  string
	index int
}

const MAX_FLOOR = 4
const MAX_ITERS = 1000

type State struct {
	elevator int
	chips    []int
	gens     []int
	elements []Element
}

func contains(a []int, n int) bool {
	for _, elt := range a {
		if elt == n {
			return true
		}
	}
	return false
}

func (s State) isValid() bool {
	for i := 0; i < len(s.chips); i++ {
		floor := s.chips[i]
		if s.gens[i] != floor && (contains(s.gens[:i], floor) || contains(s.gens[i+1:], floor)) {
			return false
		}
	}
	return true
}

func (s State) isSolution() bool {
	for _, chip := range s.chips {
		if chip != MAX_FLOOR-1 {
			return false
		}
	}
	for _, gen := range s.gens {
		if gen != MAX_FLOOR-1 {
			return false
		}
	}
	return true
}

func (s State) id() int {
	id := s.elevator
	i := 4
	for _, chip := range s.chips {
		id += chip * i
		i *= MAX_FLOOR
	}
	for _, gen := range s.gens {
		id += gen * i
		i *= MAX_FLOOR
	}
	return id
}

func object_name(element_name string, is_gen bool) string {
	var type_display string
	if is_gen {
		type_display = "G"
	} else {
		type_display = "M"
	}
	return fmt.Sprintf("%s%s", strings.ToUpper(element_name[:1]), type_display)
}

func (s State) print() {
	for floor := MAX_FLOOR - 1; floor > -1; floor-- {
		obj_names := make([]string, 0)
		for i := 0; i < len(s.chips); i++ {
			if s.chips[i] == floor {
				obj_names = append(obj_names, object_name(s.elements[i].rock, false))
			} else {
				obj_names = append(obj_names, "  ")
			}
			if s.gens[i] == floor {
				obj_names = append(obj_names, object_name(s.elements[i].rock, true))
			} else {
				obj_names = append(obj_names, "  ")
			}
		}
		var elevator_display string
		if floor == s.elevator {
			elevator_display = "E"
		} else {
			elevator_display = "."
		}
		fmt.Printf("%d %s %s\n", floor+1, elevator_display, strings.Join(obj_names, " "))
	}
}

type Object struct {
	element Element
	is_gen  bool
}

func parseFloorName(name string) int {
	switch name {
	case "first":
		return 0
	case "second":
		return 1
	case "third":
		return 2
	case "fourth":
		return 3
	default:
		panic(fmt.Sprintf("Unrecognized floor name '%s'", name))
	}
}

func parseLine(elements map[string]Element, line string) (int, []Object) {
	object_regex := regexp.MustCompile("an? ([a-z]+)( generator|-compatible microchip)")
	floor_regex := regexp.MustCompile("The ([a-z]+) floor")
	if !floor_regex.MatchString(line) {
		panic(fmt.Sprintf("Cannot find floor for line '%s'", line))
	}
	floor := parseFloorName(floor_regex.FindStringSubmatch(line)[1])
	objects := make([]Object, 0)
	for _, match := range object_regex.FindAllStringSubmatch(line, -1) {
		element_name := match[1]
		element, ok := elements[element_name]
		if !ok {
			element = Element{element_name, len(elements)}
			elements[element_name] = element
		}
		object := Object{element, match[2] == " generator"}
		objects = append(objects, object)
	}
	return floor, objects
}

func parseInput() State {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	elements := make(map[string]Element)
	state := State{0, make([]int, 0), make([]int, 0), make([]Element, 0)}
	for _, rawInstruction := range strings.Split(string(content), "\n") {
		if rawInstruction == "" {
			break
		}
		floor, objects := parseLine(elements, rawInstruction)

		n_elements := len(elements)
		if len(state.chips) < n_elements {
			state.chips = append(state.chips, make([]int, n_elements-len(state.chips))...)
		}
		if len(state.gens) < n_elements {
			state.gens = append(state.gens, make([]int, n_elements-len(state.gens))...)
		}
		if len(state.elements) < n_elements {
			state.elements = append(state.elements, make([]Element, n_elements-len(state.elements))...)
		}
		for _, object := range objects {
			if object.is_gen {
				state.gens[object.element.index] = floor
			} else {
				state.chips[object.element.index] = floor
			}
			state.elements[object.element.index] = object.element
		}
	}
	if !state.isValid() {
		panic("Invalid initial state")
	}
	return state
}

type void struct{}

var empty void

func (s State) copy() State {
	chips_copy := make([]int, len(s.chips))
	copy(chips_copy, s.chips)
	gens_copy := make([]int, len(s.gens))
	copy(gens_copy, s.gens)
	return State{s.elevator, chips_copy, gens_copy, s.elements}
}

func (s State) possibleNextStates(known_states map[int]void) []State {
	// Combination of 1 or 2 elt from the current floor taken 1 floor up or 1 floor down
	nextStates := make([]State, 0)
	n_elements := len(s.elements)
	for i_up := 0; i_up < 2; i_up++ {
		up := i_up != 0
		if up && s.elevator == MAX_FLOOR-1 {
			continue
		}
		if !up && s.elevator == 0 {
			continue
		}
		var diff int
		if up {
			diff = 1
		} else {
			diff = -1
		}
		for i := 0; i < 2*n_elements; i++ {
			if i < n_elements {
				if s.chips[i] != s.elevator {
					continue
				}
			} else if s.gens[i-n_elements] != s.elevator {
				continue
			}
			// 1 elt combination
			newState := s.copy()
			newState.elevator += diff
			if i < n_elements {
				newState.chips[i] += diff
			} else {
				newState.gens[i-n_elements] += diff
			}
			if newState.isValid() {
				id := newState.id()
				_, known := known_states[id]
				if !known {
					nextStates = append(nextStates, newState)
					known_states[id] = empty
				}
			}

			for j := i + 1; j < 2*n_elements; j++ {
				if j < n_elements {
					if s.chips[j] != s.elevator {
						continue
					}
				} else if s.gens[j-n_elements] != s.elevator {
					continue
				}
				// 2 elt combination, move another element
				newState2 := newState.copy()
				if j < n_elements {
					newState2.chips[j] += diff
				} else {
					newState2.gens[j-n_elements] += diff
				}
				if newState2.isValid() {
					id := newState2.id()
					_, known := known_states[id]
					if !known {
						nextStates = append(nextStates, newState2)
						known_states[id] = empty
					}
				}
			}
		}
	}
	return nextStates
}

func part1() {
	initial_state := parseInput()
	states := []State{initial_state}
	known_states := make(map[int]void)
	known_states[initial_state.id()] = empty

	fmt.Println("Initial state:")
	initial_state.print()
	fmt.Println("")
	for i := 0; i < MAX_ITERS; i++ {
		fmt.Printf("Computing step %d\n", i)
		for _, state := range states {
			if state.isSolution() {
				state.print()
				fmt.Printf("Best solution takes %d steps\n", i)
				return
			}
		}
		nextStates := make([]State, 0)
		for _, state := range states {
			nextStates = append(nextStates, state.possibleNextStates(known_states)[:]...)
		}
		fmt.Printf("%d states found\n\n", len(nextStates))
		states = nextStates
	}
}

func main() {
	part1() // use input2 for part2
}

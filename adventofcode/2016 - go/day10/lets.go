package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Instruction struct {
	type_ string // comp or input

	bot             int
	value           int
	output_bot_low  int
	output_bot_high int
	low_is_output   bool
	high_is_output  bool
}

type Bot struct {
	id             int
	input_a        int // value
	input_b        int // value
	output_high    int // bot ID
	output_low     int // bot ID
	high_is_output bool
	low_is_output  bool
}

type Output struct {
	id    int
	input int
}

const VALUE_A = 17
const VALUE_B = 61

func instruction_from_string(s string) Instruction {
	input_regex := regexp.MustCompile("value (\\d+) goes to bot (\\d+)")
	comp_regex := regexp.MustCompile("bot (\\d+) gives low to (bot|output) (\\d+) and high to (bot|output) (\\d+)")

	if input_regex.MatchString(s) {
		match := input_regex.FindStringSubmatch(s)
		value, _ := strconv.Atoi(match[1])
		bot, _ := strconv.Atoi(match[2])
		return Instruction{"input", bot, value, -1, -1, false, false}
	} else if comp_regex.MatchString(s) {
		match := comp_regex.FindStringSubmatch(s)
		bot, _ := strconv.Atoi(match[1])
		bot_low := -1
		bot_low, _ = strconv.Atoi(match[3])
		bot_high := -1
		bot_high, _ = strconv.Atoi(match[5])
		return Instruction{"comp", bot, -1, bot_low, bot_high, match[2] == "output", match[4] == "output"}
	} else {
		panic(fmt.Sprintf("Cannot match pattern for input '%s'", s))
	}
}

func (b Bot) isReadyToCompare() bool {
	return b.input_a >= 0 && b.input_b >= 0
}

func parseInput() []Instruction {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var instructions []Instruction
	for _, rawInstruction := range strings.Split(string(content), "\r\n") {
		if rawInstruction == "" {
			break
		}
		instructions = append(instructions, instruction_from_string(rawInstruction))
	}
	return instructions
}

func (b *Bot) send(value int) {
	if b.input_a >= 0 {
		b.input_b = value
	} else {
		b.input_a = value
	}
}

func (o *Output) send(value int) {
	o.input = value
}

func (b *Bot) isSolution() bool {
	return (b.input_a == VALUE_A && b.input_b == VALUE_B) || (b.input_b == VALUE_A && b.input_a == VALUE_B)
}

func init_bots(instructions []Instruction) (map[int]*Bot, []*Bot, map[int]*Output) {
	bots := make(map[int]*Bot)
	outputs := make(map[int]*Output)
	bots_ready_to_compare := make([]*Bot, 0)
	for _, instruction := range instructions {
		if instruction.type_ == "input" {
			bot, ok := bots[instruction.bot]
			if !ok {
				bot = &Bot{instruction.bot, -1, -1, -1, -1, false, false}
				bots[instruction.bot] = bot
			}
			bot.send(instruction.value)
			if bot.isReadyToCompare() {
				bots_ready_to_compare = append(bots_ready_to_compare, bot)
			}
		} else {
			bot1, ok1 := bots[instruction.bot]
			if !ok1 {
				bot1 = &Bot{instruction.bot, -1, -1, -1, -1, false, false}
				bots[instruction.bot] = bot1
			}
			bot1.output_high = instruction.output_bot_high
			bot1.high_is_output = instruction.high_is_output
			bot1.output_low = instruction.output_bot_low
			bot1.low_is_output = instruction.low_is_output

			if instruction.high_is_output {
				_, ok2 := outputs[instruction.output_bot_high]
				if !ok2 {
					output2 := &Output{instruction.output_bot_high, -1}
					outputs[instruction.output_bot_high] = output2
				}
			} else {
				_, ok2 := bots[instruction.output_bot_high]
				if !ok2 {
					bot2 := &Bot{instruction.output_bot_high, -1, -1, -1, -1, false, false}
					bots[instruction.output_bot_high] = bot2
				}
			}

			if instruction.low_is_output {
				_, ok3 := outputs[instruction.output_bot_low]
				if !ok3 {
					output3 := &Output{instruction.output_bot_low, -1}
					outputs[instruction.output_bot_low] = output3
				}
			} else {
				_, ok3 := bots[instruction.output_bot_low]
				if !ok3 {
					bot3 := &Bot{instruction.output_bot_low, -1, -1, -1, -1, false, false}
					bots[instruction.output_bot_low] = bot3
				}
			}

		}
	}
	return bots, bots_ready_to_compare, outputs
}

func (b Bot) values() (int, int) {
	if b.input_a > b.input_b {
		return b.input_a, b.input_b
	}
	return b.input_b, b.input_a
}

func part1() {
	instructions := parseInput()
	bots, bots_ready_to_compare, _ := init_bots(instructions)

	for len(bots_ready_to_compare) > 0 {
		new_ready_to_compare := make([]*Bot, 0)
		for _, bot := range bots_ready_to_compare {
			high, low := bot.values()
			if bot.output_high >= 0 {
				bot_high, _ := bots[bot.output_high]
				bot_high.send(high)
				if bot_high.isSolution() {
					fmt.Printf("Solution is bot %d", bot_high.id)
					return
				}
				if bot_high.isReadyToCompare() {
					new_ready_to_compare = append(new_ready_to_compare, bot_high)
				}
			}
			if bot.output_low >= 0 {
				bot_low, _ := bots[bot.output_low]
				bot_low.send(low)
				if bot_low.isSolution() {
					fmt.Printf("Solution is bot %d", bot_low.id)
					return
				}
				if bot_low.isReadyToCompare() {
					new_ready_to_compare = append(new_ready_to_compare, bot_low)
				}
			}
		}
		bots_ready_to_compare = new_ready_to_compare
	}
}

func part2() {
	instructions := parseInput()
	bots, bots_ready_to_compare, outputs := init_bots(instructions)

	for len(bots_ready_to_compare) > 0 {
		new_ready_to_compare := make([]*Bot, 0)
		for _, bot := range bots_ready_to_compare {
			high, low := bot.values()
			if bot.high_is_output {
				output := outputs[bot.output_high]
				output.send(high)
			} else {
				bot_high := bots[bot.output_high]
				bot_high.send(high)
				if bot_high.isReadyToCompare() {
					new_ready_to_compare = append(new_ready_to_compare, bot_high)
				}
			}
			if bot.low_is_output {
				output, ok := outputs[bot.output_low]
				if !ok {
					panic(fmt.Sprintf("cannot find output %d", bot.output_low))
				}
				output.send(low)
			} else {
				bot_low, _ := bots[bot.output_low]
				bot_low.send(low)
				if bot_low.isReadyToCompare() {
					new_ready_to_compare = append(new_ready_to_compare, bot_low)
				}
			}
		}
		bots_ready_to_compare = new_ready_to_compare
	}
	fmt.Printf("product of outputs 0, 1 and 2 is %d", (outputs[0].input)*(outputs[1].input)*(outputs[2].input))
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

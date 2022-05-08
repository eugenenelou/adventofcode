package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

type Room struct {
	data          string
	encryptedName string
	id            int
	checksum      string
}

type LetterCount struct {
	letter rune
	count  int
}

// Implement a custom ordered collections of letter+count
// that respect the alphebetical ordering for same count letters
type LetterCounter []LetterCount

func (c LetterCounter) Len() int {
	return len(c)
}

func (c LetterCounter) Less(i, j int) bool {
	a, b := c[i], c[j]
	return a.count < b.count || (a.count == b.count && a.letter > b.letter)
}

func (c LetterCounter) Swap(i, j int) {
	c[i], c[j] = c[j], c[i]
}

func getChecksum(encryptedName string) string {
	letterMap := make(map[rune]int)
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	for _, letter := range alphabet {
		letterMap[letter] = 0
	}
	for _, letter := range strings.Replace(encryptedName, "-", "", -1) {
		letterMap[letter] += 1
	}
	var counter_ [26]LetterCount
	counter := counter_[:]
	for i, letter := range alphabet {
		counter[i] = LetterCount{letter, letterMap[letter]}
	}
	sort.Sort(sort.Reverse(LetterCounter(counter[:])))
	var letters [5]string
	for i := 0; i < 5; i++ {
		letters[i] = string(counter[i].letter)
	}
	return strings.Join(letters[:], "")
}

func (r Room) isValid() bool {
	return getChecksum(r.encryptedName) == r.checksum
}

func makeRoom(data string) Room {
	regex := regexp.MustCompile("(?P<encryptedName>[a-z-]*)(?P<id>[0-9]+)\\[(?P<checksum>[a-z]+)\\]")
	match := regex.FindStringSubmatch(data)
	encryptedName := match[1]
	id, _ := strconv.Atoi(match[2])
	r := Room{data, encryptedName, id, match[3]}
	return r
}

func parseInput() []Room {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	var instructions []Room
	for _, rawInstruction := range strings.Split(string(content), "\n") {
		if rawInstruction == "" {
			break
		}
		instructions = append(instructions, makeRoom(rawInstruction))
	}
	return instructions
}

func part1() {
	count := 0
	for _, r := range parseInput() {
		if r.isValid() {
			count += r.id
		}
	}
	fmt.Printf("Sum of IDs is %d", count)
}

func decryptRune(r rune, shift int) rune {
	if r == '-' {
		return ' '
	}
	return rune((int(r)-int('a')+shift)%26 + int('a'))
}

func (r Room) decryptName() string {
	var letters []string
	for _, letter := range r.encryptedName {
		letters = append(letters, string(decryptRune(letter, r.id)))
	}
	return strings.Join(letters, "")
}

func part2() {
	var suspiciousRooms []Room
	for _, r := range parseInput() {
		if r.isValid() {
			name := r.decryptName()
			fmt.Printf("[%d] %s\n", r.id, name)
			if strings.Contains(name, "northpole") {
				suspiciousRooms = append(suspiciousRooms, r)
			}
		}
	}
	fmt.Println("Suspicious rooms:")
	for _, r := range suspiciousRooms {
		fmt.Printf("  - [%d] %s\n", r.id, r.decryptName())
	}
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

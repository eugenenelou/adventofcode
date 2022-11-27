package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func parseInput() string {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	input := strings.SplitN(string(content), "\n", 2)[0]
	return input
}

func getHexaHash(i int, doorId string) string {
	hash := md5.Sum([]byte(fmt.Sprintf("%s%d", doorId, i)))
	return hex.EncodeToString(hash[:])
}

func part1() {
	doorId := parseInput()
	var password []string
	n := 0
	for i := 0; n < 8; i++ {
		hexaHash := getHexaHash(i, doorId)
		if hexaHash[:5] == "00000" {
			n += 1
			password = append(password, string(hexaHash[5]))
		}
	}
	fmt.Printf("Password is: %s", strings.Join(password, ""))
}

func part2() {
	doorId := parseInput()
	var password [8]string
	var filledIndexes [8]bool
	n := 0
	for i := 0; n < 8; i++ {
		hexaHash := getHexaHash(i, doorId)
		if hexaHash[:5] == "00000" {
			rawJ := hexaHash[5]
			j, err := strconv.Atoi(string(rawJ))
			if err == nil && 0 <= j && j < 8 && !filledIndexes[j] {
				n += 1
				filledIndexes[j] = true
				password[j] = string(hexaHash[6])
			}
		}
	}
	fmt.Printf("Password is: %s", strings.Join(password[:], ""))
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

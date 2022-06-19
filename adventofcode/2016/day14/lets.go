package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"os"
	"sort"
	"strings"
)

func parseInput() string {
	content, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	return strings.Split(strings.ReplaceAll(string(content), "\r", ""), "\n")[0]

}

func hex_md5(i int, salt string) string {
	hash := md5.Sum([]byte(fmt.Sprintf("%s%d", salt, i)))
	return hex.EncodeToString(hash[:])
}

func hex_md5_stretched(i int, salt string) string {
	hash := fmt.Sprintf("%s%d", salt, i)
	for i := 0; i < 2017; i++ {
		raw_hash := md5.Sum([]byte(hash))
		hash = hex.EncodeToString(raw_hash[:])
	}
	return hash
}

func parse_hash_triplet(hash string) (char rune, ok bool) {
	last_char := 'g' // not possible
	count := 0
	for _, char := range hash {
		if char == last_char {
			count += 1
			if count == 3 {
				return char, true
			}
		} else {
			last_char = char
			count = 1
		}
	}
	return 'g', false
}

func parse_hash_quintuplet(hash string) (chars []rune, found bool) {
	last_char := 'g' // not possible
	found = false
	chars = make([]rune, 0)
	count := 0
	for _, char := range hash {
		if char == last_char {
			count += 1
			if count == 5 {
				chars = append(chars, char)
				found = true
			}
		} else {
			last_char = char
			count = 1
		}
	}
	return chars, found
}

func run(stretched bool) {
	salt := parseInput()
	total := 0
	char_by_index_found := make(map[rune][]int)

	// do more iterations after finding 64 keys
	// in case we validate a smaller index.
	// we have to do go to the index of the 64th found key + 999
	max_iterations := 100000
	found_keys_indexes := make([]int, 0)
	for i := 0; i < max_iterations; i++ {
		var hash string
		if stretched {
			hash = hex_md5_stretched(i, salt)
		} else {
			hash = hex_md5(i, salt)
		}
		triplet_char, has_triplet := parse_hash_triplet(hash)

		if has_triplet {
			// cannot have quintuplet without a triplet
			quintuplets, ok := parse_hash_quintuplet(hash)
			if ok {
				for _, quintuplet := range quintuplets {
					previous_triplets, ok2 := char_by_index_found[quintuplet]
					if ok2 {
						for _, previous_triplet := range previous_triplets {
							total += 1
							fmt.Printf("Found the matching of index %d at index %d (total: %d, diff %d)\r\n", previous_triplet, i, total, i-previous_triplet)
							found_keys_indexes = append(found_keys_indexes, previous_triplet)
							if total == 64 {
								max_iterations = previous_triplet + 999
							}
						}
					}
					char_by_index_found[quintuplet] = make([]int, 0)
				}
			}

			// schedule check for quintuplet later
			_, ok3 := char_by_index_found[triplet_char]
			if ok3 {
				char_by_index_found[triplet_char] = append(char_by_index_found[triplet_char], i)
			} else {
				char_by_index_found[triplet_char] = []int{i}
			}
		}

		// clean indexes older than 1000 steps
		for key, indexes := range char_by_index_found {
			n := 0
			for _, index := range indexes {
				if i <= index+1000 {
					indexes[n] = index
					n++
				}
			}
			char_by_index_found[key] = indexes[:n]
		}
	}
	sort.Ints(found_keys_indexes)
	fmt.Printf("Found the 64th key at index %d", found_keys_indexes[63])
}
func part1() {
	run(false)
}

func part2() {
	run(true)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--two" {
		part2()
	} else {
		part1()
	}
}

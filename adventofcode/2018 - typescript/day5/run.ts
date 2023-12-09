type Data = string[]

function parseInput(input: string): Data {
  return Array.from(input.trimEnd())
}
const alphabet = Array.from("abcdefghijklmnopqrstuvwxyz")

const mapping = alphabet.reduce((acc, char) => {
  const upper = char.toUpperCase()
  acc[char] = upper
  acc[upper] = char
  return acc
}, {} as Record<string, string>)

function solve(polymer: string[]) {
  let i = 0
  while(i < polymer.length-1) {
    if (polymer[i] == mapping[polymer[i+1]]) {
      polymer.splice(i, 2)
      i -= 1
    } else {
      i+= 1
    }
  }
  return polymer.length
}

function main1(input: string) {
  return solve(parseInput(input))
}

function main2(input: string) {
  let res = input.length
  const data = parseInput(input)
  alphabet.forEach(char => {
    const upper = mapping[char]
    const value = solve(data.filter(item => item !== char && item !== upper))
    if (value < res){
      res = value
    }
  })
  return res
}


const decoder = new TextDecoder()
let input = ""
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk)
}
const main = Deno.args.includes( "--two") ? main2 : main1
console.log(`The result is: ${main(input)}`)
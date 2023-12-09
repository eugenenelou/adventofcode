type Data = number[]

function parseInput(input: string): Data {
  return input.trimEnd().split('\n').map(Number)
}


function main1(input: string) {
  const data = parseInput(input)
  console.log('data', data)
}

function main2(input: string) {
  const data = parseInput(input)
  console.log('data', data)
}


const decoder = new TextDecoder()
let input = ""
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk)
}
const main = Deno.args.includes( "--two") ? main2 : main1
console.log(`The result is: ${main(input)}`)
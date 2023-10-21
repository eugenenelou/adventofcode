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
for await (const chunk of Deno.stdin.readable) {
  const main = Deno.args.includes( "--two") ? main2 : main1
  console.log(`The result is: ${main(decoder.decode(chunk))}`)
}
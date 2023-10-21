type Data = number[]

function parseInput(input: string): Data {
  return input.trimEnd().split('\n').map(Number)
}


function main1(input: string) {
  const data = parseInput(input)
  return data.reduce((acc, value) => acc+value, 0)
}

function main2(input: string) {
  const data = parseInput(input)
  let frequency = 0
  const seen = new Set()
  console.log('toto')
  while(true){
    for (const value of data) {
      frequency += value
      if (seen.has(frequency)) {
        return frequency
      }
      seen.add(frequency)
    }
  }
}

const decoder = new TextDecoder()
for await (const chunk of Deno.stdin.readable) {
  const main = Deno.args.includes( "--two") ? main2 : main1
  console.log(`The result is: ${main(decoder.decode(chunk))}`)
}
type Data = string[]

function parseInput(input: string): Data {
  return input.trimEnd().split('\n')
}

function checkExactCount(lettersCount:  Map<string, number>, exactCount: number): boolean {
  for (const [,value] of lettersCount) {
    if (value === exactCount) {
      return true
    }
  }
  return false
}

type d = Object

function main1(input: string) {
  const data = parseInput(input)
  const counts= data.reduce((acc, boxId) => {
    const lettersCount = new Map<string, number>
    for (const char of boxId) {
      const current = lettersCount.get(char)
      if(current) {
        lettersCount.set(char, current + 1)
      } else {
        lettersCount.set(char, 1)
      }
    }
    if (checkExactCount(lettersCount, 2)) {
      acc.twos += 1
    }
    if (checkExactCount(lettersCount, 3)) {
      acc.threes += 1
    }
    return acc
  }, {twos: 0, threes: 0})
  return counts.twos * counts.threes
}

function main2(input: string) {
  const data = parseInput(input)
  for (let idx = 0; idx < data.length; idx++) {
    const boxId = data[idx]
    for (const boxId2 of data.slice(idx)) {
      let diffCount = 0
      let lastDiffIndex = -1
      for (let jdx = 0; jdx < boxId.length; jdx++) {
        if(boxId[jdx] !== boxId2[jdx]) {
          diffCount +=1
          lastDiffIndex = jdx
        }
      }
      if (diffCount === 1) {
        console.log('boxId', boxId)
        console.log('boxId2', boxId2)
        return boxId.slice(0, lastDiffIndex) + boxId.slice(lastDiffIndex+1)
      }
    }
  }
}


const decoder = new TextDecoder()
for await (const chunk of Deno.stdin.readable) {
  const main = Deno.args.includes( "--two") ? main2 : main1
  console.log(`The result is: ${main(decoder.decode(chunk))}`)
}
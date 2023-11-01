type Data = Claim[]

const inputRe = /#(\d+) @ (\d+),(\d+): (\d+)x(\d+)/

type Claim = {
  id: number
  top: number
  left: number
  width: number
  height: number
}

function parseInput(input: string): Data {
  return input.trimEnd().split('\n').map(claim => {
    const matches = claim.match(inputRe)
    // console.log(matches, claim)
    if(matches == null) {
      throw new Error('claim did not match')
    }
    return {
      id: parseInt(matches[1], 10),
      left: parseInt(matches[2], 10),
      top: parseInt(matches[3], 10),
      width: parseInt(matches[4], 10),
      height: parseInt(matches[5], 10)
    }
  })
}


function main1(input: string) {
  const data = parseInput(input)
  const grid: number[][] = new Array(1000)
  for(let i = 0; i < 1000; i++) {
    grid[i] = new Array(1000).fill(0)
  }

  data.forEach(claim => {
    for(let rowIdx = 0; rowIdx < claim.height; rowIdx++) {
      const row = grid[claim.top + rowIdx]
      for(let colIdx = 0; colIdx < claim.width; colIdx ++) {
        row[claim.left + colIdx] += 1
      }
    }
  })

  return grid.reduce((acc, row) => acc + row.reduce((acc2, count) => acc2 + (count > 1 ? 1 : 0), 0), 0)
}

function main2(input: string) {
  const data = parseInput(input)
  const grid: number[][] = new Array(1000)
  for(let i = 0; i < 1000; i++) {
    grid[i] = new Array(1000).fill(0)
  }

  const nonOverlappingClaims = new Set()

  // for each claime, keep it as non overlapping if it does not
  // overlap when first claiming it
  // else if it overlaps, remove the overlapping claims from potential
  // candidates. At the end there is only 1 candidate

  data.forEach(claim => {
    let overlapping = false
    for(let rowIdx = 0; rowIdx < claim.height; rowIdx++) {
      const row = grid[claim.top + rowIdx]
      for(let colIdx = 0; colIdx < claim.width; colIdx ++) {
        const value = row[claim.left + colIdx]
        if(value == 0) {
          row[claim.left + colIdx] = claim.id
        } else if (value == -1) {
          overlapping = true
        } else {
          nonOverlappingClaims.delete(value)
          overlapping = true
          row[claim.left + colIdx] = -1
        }
      }
    }
    if (!overlapping) {
      nonOverlappingClaims.add(claim.id)
    }
  })

  const candidates = [...nonOverlappingClaims]
  if (candidates.length !== 1) {
    throw new Error(`The number of candidates is not 1: ${candidates}`)
  }

  return candidates[0]
}


const decoder = new TextDecoder()
let input = ""
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk)
}
const main = Deno.args.includes( "--two") ? main2 : main1
console.log(`The result is: ${main(input)}`)
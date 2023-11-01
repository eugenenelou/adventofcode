type Shift = boolean[] // True if sleeping
type Data = Record<number, Shift[]>

const begingShiftRe = /\d+:\d+\] Guard #(\d+)/
const fallsAsleepRe = /(\d+):(\d+)\] falls/
const wakesRe = /00:(\d+)\] wakes/

function parseInput(input: string): Data {
  const data: Data = {}
  let guardId = 0
  let shift: Shift  = []
  let asleepAt: null | number = null
  const rows = input.trimEnd().split('\n').sort((a, b) => a.localeCompare(b))
  rows.push('[0000-00-00 00:00] Guard #0 begins shift') // to end the last shift
  rows.forEach(row => {
    let matches = row.match(begingShiftRe)
    if (matches != null) {
      if (guardId != 0) {
        if (asleepAt != null) { // sleeps until the end of the shift
        shift.fill(true, asleepAt, 60)
        }
        data[guardId].push(shift)
      }
      guardId = parseInt(matches[1], 10)
      if(!data[guardId]) {
        data[guardId] = []
      }
      shift = new Array(60).fill(false)
      asleepAt = null
      return
    }
    matches = row.match(fallsAsleepRe)
    if(matches != null) {
      const hour = parseInt(matches[1], 10)
      asleepAt = hour != 0 ? 0 : parseInt(matches[2], 10)
      return
    }
    matches = row.match(wakesRe)
    if(matches != null) {
      if (asleepAt == null) {
        throw new Error('awaking but not sleeping')
      }
      shift.fill(true, asleepAt, parseInt(matches[1], 10))
      asleepAt = null
      return
    }
    throw new Error(`No regex match for row: ${row}`)
    })
  return data
  }



function main1(input: string) {
  const data = parseInput(input)
  let mostAsleepCount = 0
  let mostAsleepId = 0
  Object.entries(data).forEach(([guardId, shifts]) => {
    const sleepingCount = (shifts as Shift[]).reduce((acc, shift) => acc + shift.reduce((acc2, sleeping) => acc2 + (sleeping ? 1 : 0), 0), 0)
    if (sleepingCount > mostAsleepCount) {
      mostAsleepCount = sleepingCount
      mostAsleepId = parseInt(guardId, 10)
    }
  })
  const minutes = new Array(60).fill(0)
  data[mostAsleepId].forEach(shift => {
    for(let i = 0; i < 60; i++) {
      if (shift[i]) {
      minutes[i] += 1
      }
    }
  })
  return mostAsleepId * minutes.indexOf(Math.max.apply(Math, minutes))
}

function main2(input: string) {
  const data = parseInput(input)
  let mostFrequent = 0
  let mostFrequentMinute = 0
  let mostAsleepId = 0
  Object.entries(data).forEach(([guardId, shifts]) => {
    const minutes = new Array(60).fill(0)
    shifts.forEach(shift => {
      for(let i = 0; i < 60; i++) {
        if (shift[i]) {
        minutes[i] += 1
        }
      }
    })
    const mostFrequentMinuteForGuard = Math.max.apply(Math, minutes)
    if (mostFrequentMinuteForGuard > mostFrequent) {
      mostFrequent = mostFrequentMinuteForGuard
      mostFrequentMinute = minutes.indexOf(mostFrequentMinuteForGuard)
      mostAsleepId = parseInt(guardId,10)
    }
  })
  console.log('mostFrequent', mostFrequent)
  console.log('mostFrequentMinute', mostFrequentMinute)
  console.log('mostAsleepId', mostAsleepId)
  return mostAsleepId * mostFrequentMinute
}


const decoder = new TextDecoder()
let input = ""
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk)
}
const main = Deno.args.includes( "--two") ? main2 : main1
console.log(`The result is: ${main(input)}`)
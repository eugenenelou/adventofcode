type Data = [number, number][];

const regex = /\d+/g;
function parseInput(input: string): Data {
  return input
    .trimEnd()
    .split("\n")
    .map(
      (row) =>
        (row.match(regex) as [string, string]).map((x) => parseInt(x, 10)) as [
          number,
          number
        ]
    );
}

function main1(input: string) {
  const data = parseInput(input);
  for (const [players, marblesMax] of data) {
    const scores = [...Array(players)].fill(0);
    const marbles = [0];
    let current = 0;
    for (let i = 1; i < marblesMax + 1; i++) {
      // if (i % 10000 === 0) {
      //   console.log("i", i);
      // }
      if (i % 23 == 0) {
        const player = i % players;
        current = (current - 7 + marbles.length) % marbles.length;
        scores[player] = scores[player] + i + marbles.splice(current, 1)[0];
      } else {
        current = (current + 2) % marbles.length;
        marbles.splice(current, 0, i);
      }
    }
    const result = Math.max(...scores);
    console.log(`Max score: ${result}`);
  }
}

class LinkedList {
  next: LinkedList | null = null;
  prev: LinkedList | null = null;
  constructor(public value: number, selfLinked: boolean = false) {
    this.value = value;
    if (selfLinked) {
      this.next = this;
      this.prev = this;
    }
  }

  insertRight(link: LinkedList) {
    const right = this.next;
    if (right == null) {
      throw new Error("cannot insert, next is null");
    }
    link.next = right;
    link.prev = this;
    right.prev = link;
    this.next = link;
    return link;
  }

  getPrev(n: number) {
    if (n === 0) {
      return this;
    }
    return this.prev.getPrev(n - 1);
  }
  getNext(n: number) {
    if (n === 0) {
      return this;
    }
    return this.next.getNext(n - 1);
  }

  popLeft() {
    const link = this.prev as LinkedList;
    (link.prev as LinkedList).next = this;
    this.prev = link.prev;
    link.prev = null;
    link.next = null;
    return link;
  }
}
const multiplier = 100;

function main2(input: string) {
  const data = parseInput(input);
  for (const [players, marblesMax] of data) {
    const scores = [...Array(players)].fill(0);
    let marbles = new LinkedList(0, true);
    const maxi = marblesMax * multiplier + 1;
    for (let i = 1; i < maxi; i++) {
      if (i % 23 == 0) {
        marbles = marbles.getPrev(6);
        const player = i % players;
        scores[player] = scores[player] + i + marbles.popLeft().value;
      } else {
        marbles = (marbles.next as LinkedList).insertRight(new LinkedList(i));
      }
    }
    const result = Math.max(...scores);
    console.log(`Max score: ${result}`);
  }
}

const decoder = new TextDecoder();
let input = "";
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk);
}
const secondPart = Deno.args.includes("--two");
const main = secondPart ? main2 : main1;
console.log(`The result is: ${main(input)}`);

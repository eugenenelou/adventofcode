function parseInput(input: string): number {
  return Number(input.trimEnd());
}

// taken from day 9
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

function getNewRecipes(a: number, b: number): number[] {
  return [...(a + b).toString()].map(Number);
}

function main1(input: string) {
  const afterXRecipes = parseInput(input);
  let elf1 = new LinkedList(3, true);
  let elf2 = elf1.insertRight(new LinkedList(7));
  let lastLink = elf2;

  let count = 2;
  while (count < afterXRecipes + 10) {
    getNewRecipes(elf1.value, elf2.value).forEach((recipe) => {
      lastLink = lastLink.insertRight(new LinkedList(recipe));
      count += 1;
    });
    elf1 = elf1.getNext(1 + elf1.value);
    elf2 = elf2.getNext(1 + elf2.value);
  }
  let resultLink = lastLink.getPrev(count - afterXRecipes - 1);
  const result: number[] = [];
  for (let i = 0; i < 10; i++) {
    result.push(resultLink.value);
    resultLink = resultLink.getNext(1);
  }
  return result.map((x) => x.toString()).join("");
}

function checkResult(
  expectedSequence: number[],
  lastLink: LinkedList,
): boolean {
  for (let i = 0; i < expectedSequence.length; i++) {
    if (expectedSequence[i] !== lastLink.value) {
      return false;
    }
    lastLink = lastLink.getPrev(1);
  }
  return true;
}

function main2(input: string) {
  const inputData = parseInput(input);
  const expectedSequence = inputData.toString().split("").reverse().map(Number);
  let elf1 = new LinkedList(3, true);
  let elf2 = elf1.insertRight(new LinkedList(7));
  let lastLink = elf2;

  let count = 2;
  while (true) {
    for (const recipe of getNewRecipes(elf1.value, elf2.value)) {
      lastLink = lastLink.insertRight(new LinkedList(recipe));
      count += 1;
      if (checkResult(expectedSequence, lastLink)) {
        return count - expectedSequence.length;
      }
    }
    elf1 = elf1.getNext(1 + elf1.value);
    elf2 = elf2.getNext(1 + elf2.value);
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

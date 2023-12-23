type Data = number[];

function parseInput(input: string): Data {
  return input.trimEnd().split(" ").map(Number);
}

function countMetadata1(data: Data): [number[], number] {
  if (data.length > 2) {
    const [childCount, metadataCount, ...rest] = data;
    let queue = rest;
    let count = 0;
    let subcount: number;
    for (let i = 0; i < childCount; i++) {
      [queue, subcount] = countMetadata1(queue);
      count = count + subcount;
    }
    const metadatas = queue.splice(0, metadataCount);
    count = metadatas.reduce((acc, v) => acc + v, count);
    return [queue, count];
  }
  return [[], 0];
}

function main1(input: string) {
  const data = parseInput(input);
  return countMetadata1(data)[1];
}

function countMetadata2(data: Data): [number[], number] {
  if (data.length > 2) {
    const [childCount, metadataCount, ...rest] = data;
    let queue = rest;
    let subcount: number;
    const childrenCounts: number[] = [];
    for (let i = 0; i < childCount; i++) {
      [queue, subcount] = countMetadata2(queue);
      childrenCounts.push(subcount);
    }
    const metadatas = queue.splice(0, metadataCount);
    let count: number;
    if (childCount > 0) {
      count = metadatas.reduce(
        (acc, idx) => acc + (childrenCounts[idx - 1] ?? 0),
        0
      );
    } else {
      count = metadatas.reduce((acc, v) => acc + v, 0);
    }
    return [queue, count];
  }
  return [[], 0];
}

function main2(input: string) {
  const data = parseInput(input);
  return countMetadata2(data)[1];
}

const decoder = new TextDecoder();
let input = "";
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk);
}
const secondPart = Deno.args.includes("--two");
const main = secondPart ? main2 : main1;
console.log(`The result is: ${main(input)}`);

class Point {
  x: number;
  y: number;
  dx: number;
  dy: number;

  constructor(x: number, y: number, dx: number, dy: number) {
    this.x = x;
    this.y = y;
    this.dx = dx;
    this.dy = dy;
  }

  getAtTime(t: number): [number, number] {
    return [this.x + t * this.dx, this.y + t * this.dy];
  }

  distance(other: Point, t: number): number {
    const [x1, y1] = this.getAtTime(t);
    const [x2, y2] = other.getAtTime(t);
    return Math.abs(x1 - x2) + Math.abs(y1 - y2);
  }
}

type Data = Point[];
const regex =
  /position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>/;

function parseInput(input: string): Data {
  return input
    .trimEnd()
    .split("\n")
    .map((row) => {
      const match = row.match(regex);
      if (match == null) {
        throw new Error("did not match");
      }
      return new Point(
        parseInt(match[1], 10),
        parseInt(match[2], 10),
        parseInt(match[3], 10),
        parseInt(match[4], 10)
      );
    });
}

function printAtTime(data: Data, t: number) {
  const points = data.map((point) => new Point(...point.getAtTime(t), 0, 0));
  const xMin = Math.min(...points.map((p) => p.x));
  const xMax = Math.max(...points.map((p) => p.x));
  const yMin = Math.min(...points.map((p) => p.y));
  const yMax = Math.max(...points.map((p) => p.y));
  const grid = new Array(yMax - yMin + 1)
    .fill(0)
    .map(() => new Array(xMax - xMin + 1).fill(" "));
  points.forEach((point) => {
    grid[point.y - yMin][point.x - xMin] = "#";
  });
  console.log("\n");
  console.log(grid.map((row) => row.join("")).join("\n"));
}

function main1(input: string) {
  const data = parseInput(input);
  let t = 0;

  function getDistance(data: Data, t: number) {
    return data.reduce((acc, value) => value.distance(data[0], t), 0);
  }

  let lastDistance = Infinity;
  while (true) {
    t++;
    // console.log("t", t);
    // printAtTime(data, t);
    const newDistance = getDistance(data, t);
    if (newDistance > lastDistance) {
      break;
    }
    lastDistance = newDistance;
  }

  for (let i = 0; i < 15; i++) {
    printAtTime(data, t + i);
    console.log("t", t + i);
  }
}

function main2(input: string) {
  const data = parseInput(input);
}

const decoder = new TextDecoder();
let input = "";
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk);
}
const secondPart = Deno.args.includes("--two");
const main = secondPart ? main2 : main1;
console.log(`The result is: ${main(input)}`);

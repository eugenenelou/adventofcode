type Data = number;

function parseInput(input: string): Data {
  return parseInt(input.trimEnd(), 10);
}

function getPower(x: number, y: number, serialNumber: number): number {
  let p = ((x + 10) * y + serialNumber) * (x + 10);
  p = Math.floor((p / 100) % 10);
  return p - 5;
}

const gridSize = 300;

function main1(
  input: string,
  squareSize: number = 3
): [number, [number, number]] {
  const serialNumber = parseInput(input);
  const grid: number[][] = new Array(gridSize)
    .fill(0)
    .map(() => new Array(gridSize).fill(0));
  for (let x = 0; x < gridSize; x++) {
    for (let y = 0; y < gridSize; y++) {
      grid[x][y] = getPower(x + 1, y + 1, serialNumber);
    }
  }

  function getValue(x: number, y: number) {
    if (x < 0 || y < 0 || x >= gridSize || y >= gridSize) {
      return 0;
    }
    return grid[x][y];
  }

  let maxi = 0;
  let result: [number, number] = [-1, -1];

  grid.forEach((row, x) =>
    row.forEach((_, y) => {
      let total = 0;
      for (let i = 0; i < squareSize; i++) {
        for (let j = 0; j < squareSize; j++) {
          total += getValue(x + i, y + j);
        }
      }
      if (total > maxi) {
        maxi = total;
        result = [x + 1, y + 1];
      }
    })
  );
  return [maxi, result];
}

function maxForSquareSize(
  grid: number[][],
  squareSize: number
): [number, [number, number]] {
  function getValue(x: number, y: number) {
    if (x < 0 || y < 0 || x >= gridSize || y >= gridSize) {
      return 0;
    }
    return grid[x][y];
  }
  // each cell contains the sum of the power of the next "squareSize" cells
  // including itself
  const rowPowers: number[][] = new Array(gridSize)
    .fill(0)
    .map(() => new Array(gridSize).fill(0));

  grid.forEach((row, x) => {
    const cellPowers = grid[x];
    const rowPower = rowPowers[x];
    for (let y = 0; y < squareSize; y++) {
      rowPower[0] = rowPower[0] + cellPowers[y];
    }
    for (let y = 1; y < gridSize; y++) {
      rowPower[y] =
        rowPower[y - 1] -
        cellPowers[y - 1] +
        (cellPowers[y + squareSize - 1] ?? 0);
    }
  });

  let maxi = 0;
  let result: [number, number] = [-1, -1];
  const squarePowers: number[][] = new Array(gridSize)
    .fill(0)
    .map(() => new Array(gridSize).fill(0));
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < squareSize; x++) {
      squarePowers[0][y] = squarePowers[0][y] + rowPowers[x][y];
    }
    const value = squarePowers[0][y];
    if (value > maxi) {
      maxi = value;
      result = [1, y + 1];
    }
  }
  for (let x = 1; x < gridSize; x++) {
    for (let y = 0; y < gridSize; y++) {
      const value =
        squarePowers[x - 1][y] -
        rowPowers[x - 1][y] +
        (rowPowers[x + squareSize - 1]?.[y] ?? 0);
      squarePowers[x][y] = value;
      if (value > maxi) {
        maxi = value;
        result = [x + 1, y + 1];
      }
    }
  }
  return [maxi, result];
}

function main2(input: string) {
  const serialNumber = parseInput(input);
  const grid: number[][] = new Array(gridSize)
    .fill(0)
    .map(() => new Array(gridSize).fill(0));
  for (let x = 0; x < gridSize; x++) {
    for (let y = 0; y < gridSize; y++) {
      grid[x][y] = getPower(x + 1, y + 1, serialNumber);
    }
  }

  let maxi = 0;
  let result: [number, number, number] = [-1, -1, -1];
  for (let squareSize = 1; squareSize <= gridSize; squareSize++) {
    const [power, itemResult] = maxForSquareSize(grid, squareSize);
    if (power > maxi) {
      maxi = power;
      result = [...itemResult, squareSize];
    }
  }
  console.log("maxi", maxi);
  return result;
}

const decoder = new TextDecoder();
let input = "";
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk);
}
const secondPart = Deno.args.includes("--two");
const main = secondPart ? main2 : main1;
console.log(`The result is: ${main(input)}`);

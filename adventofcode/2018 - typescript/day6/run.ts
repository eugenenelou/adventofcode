type Coordinate = [number, number];
type Data = Coordinate[];

function parseInput(input: string): Data {
  return input.trimEnd().split("\n").map((row) => {
    const [a, b] = row.split(", ");
    return [parseInt(a, 10), parseInt(b, 10)];
  });
}

const alphabet = Array.from("abcdefghijklmnopqrstuvwxyz");
function displayGrid(grid: ([number | null, number] | null)[][]) {
  grid.forEach((row) => {
    console.log(
      row.map((value) => {
        if (value == null || value[0] == null) {
          return ".";
        }
        const [id, step] = value;
        const char = alphabet[id];
        return step === 0 ? char.toUpperCase() : char;
      }).join(""),
    );
  });
}

const deltas: [number, number][] = [[-1, 0], [1, 0], [0, -1], [0, 1]];
function main1(input: string) {
  const coordinates = parseInput(input);
  // limit the size of the grid to consider.
  const offsetX = Math.min(...coordinates.map(([x]) => x));
  const offsetY = Math.min(...coordinates.map(([, y]) => y));
  const width = Math.max(...coordinates.map(([x]) => x)) - offsetX + 1;
  const height = Math.max(...coordinates.map(([, y]) => y)) - offsetY + 1;

  const grid: ([number | null, number] | null)[][] = [...Array(width)].map(
    () => Array(height).fill(null),
  );
  console.log("width", width);
  console.log("height", height);
  console.log("[offsetX, offsetY]", [offsetX, offsetY]);
  coordinates.forEach(([x, y], idx) => {
    grid[x - offsetX][y - offsetY] = [idx, 0];
  });

  let starts: [number, Coordinate][] = coordinates.map((
    [x, y],
    id,
  ) => [id, [x - offsetX, y - offsetY]]);
  let i = 0;
  while (starts.length) {
    i++;
    let newStarts: typeof starts = [];
    starts.forEach(([id, coordinate]) => {
      const [x, y] = coordinate;
      deltas.forEach(([deltaX, deltaY]) => {
        const currentX = x + deltaX;
        const currentY = y + deltaY;
        if (
          currentX < 0 || currentX >= width || currentY < 0 ||
          currentY >= height
        ) {
          return;
        }
        const value = grid[currentX][currentY];
        if (value == null) {
          grid[currentX][currentY] = [id, i];
          newStarts.push([id, [currentX, currentY]]);
        } else if (value[0] !== id && value[1] === i) {
          // i cannot be lower due to i increasing every loop
          grid[currentX][currentY] = [null, i];
          // this can add several times the same origin coordinates
          newStarts.push([id, [currentX, currentY]]);
        }
      });
    });
    starts = newStarts;
  }

  const idsTouchingBorder = new Set([
    ...grid[0].map(([id]) => id),
    ...grid[grid.length - 1].map(([id]) => id),
    ...grid.map((row) => row[0]?.[0]),
    ...grid.map((row) => row[row.length - 1]?.[0]),
  ]);

  console.log(
    "idsTouchingBorder",
    [...idsTouchingBorder].map((id) => alphabet[id]),
  );

  return Math.max(
    ...grid.reduce(
      (acc, row) =>
        row.reduce((acc, [coord]) => {
          if (coord != null) {
            acc[coord] += 1;
          }
          return acc;
        }, acc),
      Array<number>(coordinates.length).fill(0),
    ).filter((_, id) => !idsTouchingBorder.has(id)),
  );
}

const N = 10000;
function main2(input: string) {
  const coordinates = parseInput(input);
  // limit the size of the grid to consider.
  const offsetX = Math.min(...coordinates.map(([x]) => x));
  const offsetY = Math.min(...coordinates.map(([, y]) => y));
  const width = Math.max(...coordinates.map(([x]) => x)) - offsetX + 1;
  const height = Math.max(...coordinates.map(([, y]) => y)) - offsetY + 1;
  const countCoordPerColumn = coordinates.reduce((acc, [, y]) => {
    acc[y - offsetY] += 1;
    return acc;
  }, [...Array(height)].fill(0));

  let res = 0;
  // height * 2 because coordinates outside of the original grid can
  // still verify the distance condition
  for (let i = 0; i < height * 2; i++) {
    // manhattan distance from (i, 0) to each of the coordinate
    let distance = coordinates.reduce(
      (acc, [x, y]) => acc + Math.abs(x - offsetX - i) + y - offsetY,
      0,
    );
    if (distance < N) {
      res += 1;
    }
    let countLeft = 0;
    let countRight = coordinates.length;
    let found = false;
    for (let j = 1; j < width * 2; j++) {
      const rowLeft = (j > 0) ? countCoordPerColumn[j - 1] : 0;
      countLeft += rowLeft;
      countRight -= rowLeft;
      distance = distance + countLeft - countRight;
      if (distance < N) {
        res += 1;
        found = true;
      } else if (countLeft >= countRight) {
        // the distance can only increase for this row
        break;
      }
    }
    if (i > height && !found) {
      break;
    }
  }
  return res;
}

const decoder = new TextDecoder();
let input = "";
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk);
}
const main = Deno.args.includes("--two") ? main2 : main1;
console.log(`The result is: ${main(input)}`);

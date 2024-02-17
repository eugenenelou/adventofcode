const leftTurn: Record<string, string> = {
  "^": "<",
  ">": "^",
  "v": ">",
  "<": "v",
};
const rightTurn: Record<string, string> = {
  "<": "^",
  "^": ">",
  ">": "v",
  "v": "<",
};

const newDirections: Record<string, string> = {
  "/^": ">",
  "/<": "v",
  "/v": "<",
  "/>": "^",
  "\\v": ">",
  "\\<": "^",
  "\\>": "v",
  "\\^": "<",
};

function display(grid: string[], cars: Car[]) {
  const g = grid.map((row) => row.split(""));
  cars.forEach((car) => {
    if ("^>v^<".includes(g[car.x][car.y])) {
      g[car.x][car.y] = "X";
    } else {
      g[car.x][car.y] = car.direction;
    }
  });
  g.forEach((row) => console.log(row.join("")));
}

class Car {
  x: number;
  y: number;
  direction: string;
  turnCounter: number;
  crashed: boolean;

  constructor(x: number, y: number, direction: string) {
    this.x = x;
    this.y = y;
    this.direction = direction;
    this.turnCounter = 0;
    this.crashed = false;
  }

  tick(grid: string[]) {
    this.move();
    this.updateDirection(grid);
    // console.log(this.positionIdentifier());
  }

  move() {
    switch (this.direction) {
      case "^":
        this.x -= 1;
        break;
      case ">":
        this.y += 1;
        break;
      case "v":
        this.x += 1;
        break;
      case "<":
        this.y -= 1;
        break;
      default:
        throw new Error(`Unexpected value ${this.direction}`);
    }
  }

  updateDirection(grid: string[]) {
    const trackValue = grid[this.x][this.y];
    if (trackValue === "-" || trackValue === "|") {
      return;
    }
    if (trackValue === "+") {
      switch (this.turnCounter) {
        case 0:
          this.direction = leftTurn[this.direction];
          break;
        case 2:
          this.direction = rightTurn[this.direction];
      }
      this.turnCounter = (this.turnCounter + 1) % 3;
      return;
    }
    this.direction = newDirections[`${trackValue}${this.direction}`];
  }

  positionIdentifier() {
    return this.y.toString().padStart(3, "0") + "," +
      this.x.toString().padStart(3, "0");
  }
}

function parseInput(input: string): [string[], Car[]] {
  const rawGrid = input.trimEnd().split("\n");
  const grid: string[] = rawGrid.map((row) =>
    row.replace(/[<>]/g, "-").replace(/[\^v]/g, "|").replace("\r", "")
  );
  const cars: Car[] = [];
  rawGrid.forEach((row, x) => {
    [...row].forEach((char, y) => {
      if ("^>v<".includes(char)) {
        cars.push(new Car(x, y, char));
      }
    });
  });
  return [grid, cars];
}

function main1(input: string) {
  let [grid, cars] = parseInput(input);
  const carPositions = new Set<string>(
    cars.map((car) => car.positionIdentifier()),
  );
  while (true) {
    for (const car of cars) {
      const oldPos = car.positionIdentifier();
      car.tick(grid);
      const pos = car.positionIdentifier();
      if (carPositions.has(pos)) {
        // Crash
        return pos;
      }
      carPositions.delete(oldPos);
      carPositions.add(pos);
    }
    cars = cars.sort((a: Car, b: Car) =>
      a.positionIdentifier().localeCompare(b.positionIdentifier())
    );
  }
}

function main2(input: string) {
  let [grid, cars] = parseInput(input);
  const carPositions = new Set<string>(
    cars.map((car) => car.positionIdentifier()),
  );
  while (true) {
    for (const car of cars) {
      if (car.crashed) {
        continue;
      }
      const oldPos = car.positionIdentifier();
      car.tick(grid);
      const pos = car.positionIdentifier();
      if (carPositions.has(pos)) {
        // Crash
        cars.forEach((car) => {
          if (car.positionIdentifier() === pos) {
            car.crashed = true;
          }
        });
        carPositions.delete(pos);
        carPositions.delete(oldPos);
      } else {
        carPositions.add(pos);
        carPositions.delete(oldPos);
      }
    }
    cars = cars.sort((a: Car, b: Car) =>
      a.positionIdentifier().localeCompare(b.positionIdentifier())
    ).filter((car) => !car.crashed);
    if (cars.length < 2) {
      return cars[0].positionIdentifier();
    }
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

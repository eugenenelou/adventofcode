type Data = Record<string, Set<string>>;

function parseInput(input: string): Data {
  const dependencies = input
    .trimEnd()
    .split("\n")
    .map((row) => {
      const words = row.split(" ");
      const node_1 = words[1];
      const node_2 = words[7];
      return [node_1, node_2];
    });
  const requiredNodes: Data = dependencies.reduce((acc, [from, to]) => {
    if (to in acc) {
      acc[to].add(from);
    } else {
      acc[to] = new Set([from]);
    }
    if (!(from in acc)) {
      acc[from] = new Set();
    }
    return acc;
  }, {});
  return requiredNodes;
}

function main1(input: string) {
  const requiredNodes = parseInput(input);

  const result: string[] = [];
  let lastCanditate: string | null = null;
  const nodeCount = Object.keys(requiredNodes).length;
  const candidates: string[] = [];
  while (result.length < nodeCount) {
    for (const node in requiredNodes) {
      const froms = requiredNodes[node];
      if (lastCanditate != null) {
        froms.delete(lastCanditate);
      }
      if (froms.size === 0) {
        candidates.push(node);
        delete requiredNodes[node];
      }
    }
    candidates.sort();
    lastCanditate = candidates.shift();
    result.push(lastCanditate);
  }
  return result.join("");
}

const OFFSET = 60;
const WORKERS = 5;

const timeByNode: Record<string, number> = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  .split("")
  .reduce((acc, char, idx) => {
    acc[char] = idx + OFFSET + 1;
    return acc;
  }, {});

function main2(input: string) {
  const requiredNodes = parseInput(input);
  const workers: number[] = [...Array(WORKERS)].fill(0);
  const workerTasks: (string | null)[] = [...Array(WORKERS)].fill(null);
  let t = 0;
  let finishedCount = 0;

  function tick() {
    const dt = Math.min(...workers.filter((v) => v > 0));
    if (dt !== Infinity) {
      for (let i = 0; i < workers.length; i++) {
        const newValue = Math.max(0, workers[i] - dt);
        if (isNaN(newValue)) {
          throw new Error("NaN");
        }
        workers[i] = newValue;
        const task = workerTasks[i];
        if (newValue === 0 && task != null) {
          finishedCount++;
          workerTasks[i] = null;
          Object.values(requiredNodes).forEach((froms) => froms.delete(task));
        }
      }
      t += dt;
    }
  }

  const nodeCount = Object.keys(requiredNodes).length;
  const candidates: string[] = [];
  while (finishedCount < nodeCount) {
    for (const node in requiredNodes) {
      const froms = requiredNodes[node];
      if (froms.size === 0) {
        candidates.push(node);
        delete requiredNodes[node];
      }
    }
    candidates.sort();
    if (workers.every((v) => v > 0) || !candidates.length) {
      tick();
    } else {
      workers.forEach((v, idx) => {
        if (v === 0 && candidates.length) {
          const candidate = candidates.shift() as string;
          workers[idx] = timeByNode[candidate];
          workerTasks[idx] = candidate;
        }
      });
    }
  }
  return t;
}

const decoder = new TextDecoder();
let input = "";
for await (const chunk of Deno.stdin.readable) {
  input += decoder.decode(chunk);
}
const secondPart = Deno.args.includes("--two");
const main = secondPart ? main2 : main1;
console.log(`The result is: ${main(input)}`);

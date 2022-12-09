import sys
from collections import defaultdict


def split_atoms(molecule):
    result = []
    current = ""
    for atom in molecule:
        if atom.islower():
            result.append(f"{current}{atom}")
            current = ""
        elif current:
            result.append(current)
            current = atom
        else:
            current = atom
    if current:
        result.append(current)
    return result


def parse_input(input_):
    i = iter(input_)
    operations = defaultdict(list)
    while line := next(i).rstrip():
        from_, to = line.split(" => ")
        operations[from_].append(split_atoms(to))
    molecule = next(i).rstrip()
    return operations, split_atoms(molecule)


def main1(input_):
    operations, molecule = parse_input(input_)
    results = set()
    for i, atom in enumerate(molecule):
        for result in operations[atom]:
            results.add("".join(molecule[:i] + result + molecule[i + 1 :]))
    return len(results)


def main2(input_):
    """
    all operations that return 8 atoms contain (in that order): Y, Y, Ar
    all operations that return 6 atoms contain  (in that order): Y, Ar
    all operations that return 4 atoms contain: Ar
    all other operations return 2 atoms.

    So if we had only operations returning 2 atoms, the number of operations needed
    would be the number of atoms in the resulting molecule minus one (the starting e)
    and each Y and Ar each allow to skip 2 operations
    """
    _, molecule = parse_input(input_)
    return len(molecule) - 1 - 2 * sum(atom == "Y" or atom == "Ar" for atom in molecule)


if __name__ == "__main__":
    input_ = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input_), file=sys.stdout)

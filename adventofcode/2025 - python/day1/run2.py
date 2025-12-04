n = 50
pwd = 0


def count_zeros(a: int, b: int) -> int:
    return abs(a // 100 - b // 100)


try:
    while line := input():
        if n == 0 and line.startswith("L"):
            pwd -= 1
        new_n = n + (-1 if line.startswith("L") else 1) * int(line[1:])
        pwd += (delta := count_zeros(n, new_n))
        n = new_n % 100
        if n == 0 and line.startswith("L"):
            pwd += 1
except EOFError:
    pass
print(pwd)

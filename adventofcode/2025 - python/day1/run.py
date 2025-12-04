n = 50
pwd = 0
try:
    while line := input():
        n = (n + (-1 if line.startswith("L") else 1) * int(line[1:])) % 100
        if n == 0:
            pwd += 1
except EOFError:
    pass
print(pwd)

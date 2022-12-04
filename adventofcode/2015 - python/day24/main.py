import sys


def parse_input(input_):
    return [int(line.rstrip()) for line in input_]


def group_complexity(group):
    res = 1
    for weight in group:
        res *= weight
    return res


class Solver:
    def __init__(self, data, n_groups):
        self.data = data
        self.n_groups = n_groups
        self.weights_set = set(data)
        self.max_group_size = len(data) - 2
        self.group_weight = sum(data) // n_groups

    def can_achieve_weight(self, weights, weight, acc, depth):
        """
        Return whether a group a weight totalling **weight** can be extracted
        from **weights**
        """
        if not weights:
            return False
        a, *b = weights
        if a == weight:
            new_acc = {*acc, a}
            if depth == 1 or self.can_achieve_weight(
                self.weights_set - new_acc, self.group_weight, new_acc, depth=depth - 1
            ):
                return True
        if not b:
            return False
        return self.can_achieve_weight(b, weight, acc, depth=depth) or (
            a < weight and self.can_achieve_weight(b, weight - a, [*acc, a], depth=depth)
        )

    def iter_possible_groups(self, weights, grouped_weights, target_weight, group_size):
        """
        Expect weights to be sorted in desc order
        """
        if not weights or group_size + 1 > self.max_group_size:
            return
        a, *b = weights
        group_weights_with_a = [*grouped_weights, a]
        if a == target_weight:
            yield group_weights_with_a
        if not b:
            return
        if a < target_weight and group_size < self.max_group_size:
            yield from self.iter_possible_groups(
                b, group_weights_with_a, target_weight - a, group_size + 1
            )
        yield from self.iter_possible_groups(b, grouped_weights, target_weight, group_size)

    def run(self):
        weights = sorted(self.data, reverse=True)
        valid_groups = []
        for group in self.iter_possible_groups(weights, [], self.group_weight, 0):
            if self.can_achieve_weight(
                self.weights_set - set(group), self.group_weight, group, depth=self.n_groups - 2
            ):
                l = len(group)
                if self.max_group_size > l:
                    self.max_group_size = l  # this way the iterator will not even generate the group worst than the current best solution
                    valid_groups = [group]
                elif self.max_group_size < l:
                    continue
                else:
                    valid_groups.append(group)
        return min(group_complexity(group) for group in valid_groups)


if __name__ == "__main__":
    input_ = sys.stdin
    second_part = "--two" in sys.argv
    solver = Solver(parse_input(input_), n_groups=4 if second_part else 3)
    print(solver.run(), file=sys.stdout)

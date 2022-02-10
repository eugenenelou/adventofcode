import sys


def parse_input(input):
    ingredients = {}
    for ingredient in input:
        name, values = ingredient.rstrip().split(": ")
        ingredients.setdefault(name, {})
        for property in values.split(", "):
            k, v = property.split(" ")
            ingredients[name][k] = int(v)
    return ingredients


def score1(ingredients, quantities):
    def score_property(property):
        return max(
            0,
            sum(
                ingredient[property] * quantity
                for ingredient, quantity in zip(ingredients, quantities)
            ),
        )

    return (
        score_property("capacity")
        * score_property("durability")
        * score_property("flavor")
        * score_property("texture")
        * (0 if score_property("calories") == 0 else 1)
    )


def score2(ingredients, quantities, aimed_calories):
    def score_property(property):
        return max(
            -1,
            sum(
                ingredient[property] * quantity
                for ingredient, quantity in zip(ingredients, quantities)
            ),
        )

    return (
        max(0, score_property("capacity"))
        * max(0, score_property("durability"))
        * max(0, score_property("flavor"))
        * max(0, score_property("texture"))
        * (1 if score_property("calories") == aimed_calories else 0)
    )


MAX_TEASPOONS = 100


def generate_quantities(n, maxi, acc=None):
    if n == 1:
        if acc is None:
            yield [maxi]
        else:
            yield [*acc, maxi]
    else:
        for i in range(maxi):
            if acc is None:
                sub_acc = [i]
            else:
                sub_acc = [*acc, i]
            yield from generate_quantities(n - 1, maxi - i, sub_acc)


def main1(input):
    ingredients = parse_input(input)
    return max(
        score1(ingredients.values(), quantities)
        for quantities in generate_quantities(len(ingredients), MAX_TEASPOONS)
    )


def main2(input):
    ingredients = parse_input(input)
    return max(
        score2(ingredients.values(), quantities, 500)
        for quantities in generate_quantities(len(ingredients), MAX_TEASPOONS)
    )


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)

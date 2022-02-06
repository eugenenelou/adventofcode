import sys

from string import hexdigits


def main(input):
    result = 0
    for base_string in input:
        cleaned_string = []
        string = list(base_string.rstrip())
        while string:
            match string:
                case "\\", "\\", *rest:
                    cleaned_string.append("\\")
                    string = rest
                case "\\", '"', *rest:
                    cleaned_string.append('"')
                    string = rest
                case "\\", "x", a, b, *rest:
                    if a in hexdigits and b in hexdigits:
                        cleaned_string.append("'")
                        string = rest
                    else:
                        cleaned_string.extend(["\\", "x"])
                        string = [a, b, *rest]
                case a, *rest:
                    cleaned_string.append(a)
                    string = rest
                case _:
                    raise Exception("Did not match anything")
        result += 2 + len(base_string.rstrip()) - len(cleaned_string)
    return result


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)

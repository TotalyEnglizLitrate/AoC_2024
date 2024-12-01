def run(input: str) -> None:
    from collections import Counter
    from functools import reduce

    column1: list[int] = []
    column2: list[int] = []
    
    for line in input.splitlines():
        if line:
            e1, e2 = map(int, line.split())
            column1.append(e1)
            column2.append(e2)
    
    column1.sort()
    column2.sort()

    part_one_sum = reduce(lambda acc, elems: acc + abs(elems[0] - elems[1]), zip(column1, column2), 0)
    part_two_count = Counter(column2)
    part_two_sum = sum((x * part_two_count.get(x, 0)) for x in column1)

    print(f"Part 1 - {part_one_sum}")
    print(f"Part 2 - {part_two_sum}")
    
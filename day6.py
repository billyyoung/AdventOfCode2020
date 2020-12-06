from collections import defaultdict
import re

with open("day6.input") as infile:
    lines = [l for l in infile.read().split("\n")]

index = 0
group_size = 0
total1 = 0
total2 = 0
values = set()
counts = defaultdict(int)

while index < len(lines):

    if lines[index]:
        for s in lines[index]:
            values.add(s)
            counts[s] += 1
        group_size += 1

    else:
        total1 += len(values)

        for v in counts.values():
            if v == group_size:
                total2 += 1

        values = set()
        counts = defaultdict(int)
        group_size = 0
    index += 1

print total1
print total2

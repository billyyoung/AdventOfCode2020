from collections import defaultdict
import re

with open("day10.input") as infile:
    lines = [int(l) for l in infile.read().split("\n") if l]

need = max(lines) + 3

lines = sorted(lines)
lines.append(need)

# part 1
diffs_to_count = defaultdict(int)

prev = 0
for j in lines:
    diff = j - prev
    diffs_to_count[diff] += 1
    prev = j

print diffs_to_count[1] * diffs_to_count[3]

# part 2
combos_for_n = defaultdict(int)
combos_for_n[0] = 1

for n in lines:
    combos = combos_for_n[n-1] + combos_for_n[n-2] + combos_for_n[n-3]
    combos_for_n[n] = combos

print combos_for_n[need]

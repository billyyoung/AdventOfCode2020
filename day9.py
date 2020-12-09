from collections import defaultdict
import re

with open("day9.input") as infile:
    lines = [int(l) for l in infile.read().split("\n") if l]

def is_valid(num, preamble):
    val_to_count = defaultdict(int)
    for n in preamble:
        val_to_count[n] += 1

    for n in preamble:
        if num-n in val_to_count:
            val_to_count[num-n] -= 1
            if val_to_count[n] > 0:
                return True
            val_to_count[num-n] += 1

    return False

for i in range(25, len(lines)):
    if not is_valid(lines[i], lines[i-25:i]):
        print i, lines[i]
        break

target = 23278925  # index 514
for i in range(514):
    tracker = i
    subsum = 0
    min_num = 1000000000000
    max_num = 0
    while subsum < target:
        min_num = min(min_num, lines[tracker])
        max_num = max(max_num, lines[tracker])
        subsum += lines[tracker]
        tracker += 1

    if subsum == target:
        print min_num + max_num
        break

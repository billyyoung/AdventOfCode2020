from collections import defaultdict
import re

with open("day8.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

# return total, final_line
def part1(lines):
    current = 0
    total = 0

    seen = set()

    while current < len(lines):
        if current in seen:
            return total, current

        if current < 0:
            return -1, None

        seen.add(current)

        op, val_str = lines[current].split(" ")
        val = int(val_str[1:])
        if '-' in val_str:
            val *= -1

        if op == 'nop':
            current += 1

        elif op == 'acc':
            total += val
            current += 1

        else:  # jmp
            current += val

    return total, current

total, current = part1(lines)
print total

for i in range(len(lines)):
    if 'acc' in lines[i]:
        continue
    if lines[i] == 'nop +0':
        continue

    original_line = lines[i]

    if 'nop' in original_line:
        new_line = 'jmp' + original_line[3:]
    else:  # jmp
        new_line = 'nop' + original_line[3:]

    # try fix
    lines[i] = new_line
    total, final_line = part1(lines)
    if final_line == len(lines):
        print total
        break

    # undo
    lines[i] = original_line

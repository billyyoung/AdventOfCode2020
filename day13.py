from collections import defaultdict
import re

with open("day13.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

start_time = int(lines[0])
busses = lines[1].split(",")

min_mins = 100000000
min_id = None
for bus in busses:
    if bus == 'x':
        continue

    bus = int(bus)
    mod = start_time % bus
    if bus - mod < min_mins:
        min_mins = min(min_mins, bus - mod)
        min_id = bus

print min_mins * min_id

# part 2
# find first N that satisfies 2 equations
# N % a_0 == 0
# (N + offset_1) % a_1 == 0 -> N % a_1 == (a_1 - offset_1)

# Once you have N, you can only add (a_0 * a_1) to it to maintain the above
# so keep adding (a_0 * a_1) until you find a value that satisfies
# N % a_2 == (a_2 - offset_a2)

# then repeat with (a_0 * a_1 * a_2), etc

current_ans = None
multiplier = None
for i in range(len(busses)):
    bus = busses[i]
    if bus == 'x':
        continue
    bus = int(bus)

    if current_ans is None:
        current_ans = bus + i
        multiplier = bus
        continue

    while (current_ans + i) % bus != 0:
        current_ans += multiplier

    multiplier *= bus

print current_ans

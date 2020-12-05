import re

with open("day5.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

max_res = 0
all_seats = []
for line in lines:
    # F/B
    row = 0
    for i in range(7):
        if line[i] == 'B':
            row += 2 ** (6-i)

    # L/R
    seat = 0
    for i in range(3):
        if line[i+7] == 'R':
            seat += 2 ** (2-i)

    res = row * 8 + seat
    all_seats.append(res)
    max_res = max(max_res, res)

print max_res

all_seats = sorted(all_seats)
for i in range(len(all_seats)-1):
    if all_seats[i] + 2 == all_seats[i+1]:
        print all_seats[i] + 1

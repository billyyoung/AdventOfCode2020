from collections import defaultdict
import re
from pprint import pprint

with open("day11.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

def num_empty(seats, row, seat):
    empty = 0
    occupied = 0
    for r in [-1, 0, 1]:
        for s in [-1, 0, 1]:
            if r == 0 and s == 0:
                continue

            if 0 <= row + r < len(seats) and 0 <= seat + s < len(seats[0]):
                if seats[row + r][seat + s] == 'L':
                    empty += 1
                if seats[row + r][seat + s] == '#':
                    occupied += 1

    return empty, occupied

seats = [[c for c in line] for line in lines]

while True:
    new_seats = [[c for c in row] for row in seats]

    for row in range(len(seats)):
        for seat in range(len(seats[0])):

            if seats[row][seat] == '.':
                continue

            empty, occupied = num_empty(seats, row, seat)
            if seats[row][seat] == 'L':
                if occupied == 0 and empty > 0:
                    new_seats[row][seat] = '#'

            if seats[row][seat] == '#':
                if occupied >= 4:
                    new_seats[row][seat] = 'L'

    if seats == new_seats:
        break
    seats = new_seats

count = 0
for row in seats:
    for s in row:
        if s == '#':
            count += 1
print count

# part 2
def num_empty2(seats, row, seat):
    empty = 0
    occupied = 0

    for r in [-1, 0, 1]:
        for s in [-1, 0, 1]:
            if r == 0 and s == 0:
                continue

            r_extend = r
            s_extend = s

            while 0 <= row + r_extend < len(seats) and 0 <= seat + s_extend < len(seats[0]):
                if seats[row + r_extend][seat + s_extend] == '.':
                    r_extend += r
                    s_extend += s
                    continue

                if seats[row + r_extend][seat + s_extend] == 'L':
                    empty += 1
                    break
                if seats[row + r_extend][seat + s_extend] == '#':
                    occupied += 1
                    break

    return empty, occupied

seats = [[c for c in line] for line in lines]

while True:
    new_seats = [[c for c in row] for row in seats]

    for row in range(len(seats)):
        for seat in range(len(seats[0])):

            if seats[row][seat] == '.':
                continue

            empty, occupied = num_empty2(seats, row, seat)
            if seats[row][seat] == 'L':
                if occupied == 0 and empty > 0:
                    new_seats[row][seat] = '#'

            if seats[row][seat] == '#':
                if occupied >= 5:
                    new_seats[row][seat] = 'L'

    if seats == new_seats:
        break
    seats = new_seats

count = 0
for row in seats:
    for s in row:
        if s == '#':
            count += 1
print count

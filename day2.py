from collections import defaultdict

with open("day2.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

def is_valid1(line):
    # format: 8-11 l: qllllqllklhlvtl

    rule, pw = line.split(": ")
    interval, letter = rule.split(" ")
    min_req, max_req = [int(v) for v in interval.split("-")]

    letter_counts = defaultdict(int)
    for i in range(len(pw)):
        letter_counts[pw[i]] += 1

    return min_req <= letter_counts[letter] <= max_req

def solve_part1():
    count = 0
    for line in lines:
        if is_valid1(line):
            count += 1

    print count


def is_valid2(line):
    rule, pw = line.split(": ")
    interval, letter = rule.split(" ")
    i1, i2 = [int(v) for v in interval.split("-")]

    i1_valid = pw[i1-1] == letter
    i2_valid = pw[i2-1] == letter
    return any([i1_valid, i2_valid]) and not all([i1_valid, i2_valid])

def solve_part2():
    count = 0
    for line in lines:
        if is_valid2(line):
            count += 1

    print count

solve_part1()
solve_part2()

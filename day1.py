with open("day1.input") as infile:
    vals = [int(l) for l in infile.read().split("\n") if l]

def solve_part1():
    for i in range(len(vals)):
        for j in range(i+1, len(vals)):
            if vals[i] + vals[j] == 2020:
                print vals[i] * vals[j]
                return

def solve_part2():
    for i in range(len(vals)):
        for j in range(i+1, len(vals)):
            for k in range(j+1, len(vals)):
                if vals[i] + vals[j] + vals[k] == 2020:
                    print vals[i] * vals[j] * vals[k]
                    return

solve_part2()

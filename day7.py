from collections import defaultdict
import re

with open("day7.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

inner_to_outers = defaultdict(set)
outer_to_inner_and_count = defaultdict(set)

for line in lines:
    # dull crimson bags contain 3 mirrored plum bags, 2 dotted orange bags, 3 faded brown bags.

    if 'no other bags' in line:
        continue

    line = line[:-1]  # remove '.'
    outer, inners = line.split(" contain ")

    outer_colour = outer[:-5]  # remove ' bags'

    for inner in inners.split(", "):
        parts = inner.split(" ")
        num = parts[0]
        inner_colour = parts[1] + " " + parts[2]

        inner_to_outers[inner_colour].add(outer_colour)

        outer_to_inner_and_count[outer_colour].add((inner_colour, int(num)))

# BFS 1
seen = set()
queue = {'shiny gold'}

while len(queue) > 0:
    item = queue.pop()

    for o in inner_to_outers[item]:
        if o not in seen:
            seen.add(o)
            queue.add(o)

print len(seen)

# recursive DFS 1 (after the fact)
seen = set()
def count_containers(item, seen, inner_to_outers):
    for outer in inner_to_outers[item]:
        if outer not in seen:
            seen.add(outer)
            count_containers(outer, seen, inner_to_outers)

count_containers('shiny gold', seen, inner_to_outers)
print len(seen)

# DFS 2
def count_bags(item, outer_to_inner_and_count):
    count = 0
    for inner, num in outer_to_inner_and_count[item]:
        count += num + num * count_bags(inner, outer_to_inner_and_count)

    return count

print count_bags('shiny gold', outer_to_inner_and_count)

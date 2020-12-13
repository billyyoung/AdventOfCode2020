from collections import defaultdict
import re

with open("day12.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

pos = [0, 0]
dir = [1, 0]

dir_to_vector = {
    'N' : [0, 1],
    'S' : [0, -1],
    'W' : [-1, 0],
    'E' : [1, 0],
}

for line in lines:
    action = line[0]
    val = int(line[1:])

    if action in dir_to_vector:
        vector = dir_to_vector[action]
        pos[0] += val * vector[0]
        pos[1] += val * vector[1]

    elif action in ['L', 'R']:
        rotation = val / 90
        # [a,b] -L90-> x1 becomes y2, y1 becomes -x2
        # [a,b] -R90-> x1 becomes -y2, y1 becomes x2

        for i in range(rotation):
            if action == 'L':
                dir = [-1 * dir[1], dir[0]]
            elif action == 'R':
                dir = [dir[1], -1 * dir[0]]

    elif action == 'F':
        pos[0] += val * dir[0]
        pos[1] += val * dir[1]

print abs(pos[0]) + abs(pos[1])

# part 2
pos = [0, 0]
waypoint_vector = [10, 1]

for line in lines:
    action = line[0]
    val = int(line[1:])

    if action in dir_to_vector:
        vector = dir_to_vector[action]
        waypoint_vector[0] += val * vector[0]
        waypoint_vector[1] += val * vector[1]

    elif action in ['L', 'R']:
        rotation = val / 90
        # [a,b] -L90-> x1 becomes y2, y1 becomes -x2
        # [a,b] -R90-> x1 becomes -y2, y1 becomes x2

        for i in range(rotation):
            if action == 'L':
                waypoint_vector = [-1 * waypoint_vector[1], waypoint_vector[0]]
            elif action == 'R':
                waypoint_vector = [waypoint_vector[1], -1 * waypoint_vector[0]]

    elif action == 'F':
        pos[0] += val * waypoint_vector[0]
        pos[1] += val * waypoint_vector[1]

print abs(pos[0]) + abs(pos[1])

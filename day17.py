from collections import defaultdict
import re
from copy import deepcopy

with open("day17.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

cube = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(str))))

for x in range(len(lines)):
    line = lines[x]

    for y in range(len(line)):
        cube[x][y][0][0] = line[y]

def num_neighbours_active(cube, x, y, z, w):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):

                    if not (dx == dy == dz == dw == 0):
                        if cube[x + dx][y + dy][z + dz][w + dw] == '#':
                            count += 1
                            if count > 3:
                                return count
    return count

# find the min/max indices of the cube, to get the bounding planes
# (then will iterate over min-1, max+1 bounds
# to check all the points in the cube and surrounding the cube)
def get_dims(cube):
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    minz = 0
    maxz = 0
    minw = 0
    maxw = 0

    minx = min(cube.keys())
    maxx = max(cube.keys())

    for x in cube:
        miny = min(miny, min(cube[x].keys()))
        maxy = max(maxy, max(cube[x].keys()))

        for y in cube[x]:
            minz = min(minz, min(cube[x][y].keys()))
            maxz = max(maxz, max(cube[x][y].keys()))

            for z in cube[x][y]:
                minw = min(minw, min(cube[x][y][z].keys()))
                maxw = max(maxw, max(cube[x][y][z].keys()))


    return [[minx, maxx], [miny, maxy], [minz, maxz], [minw, maxw]]

def iterate(cube):
    next_cube = deepcopy(cube)
    count = 0

    rx, ry, rz, rw = get_dims(cube)

    for x in range(rx[0]-1, rx[1]+1 +1):
        for y in range(ry[0]-1, ry[1]+1 +1):
            for z in range(rz[0]-1, rz[1]+1 +1):
                # for w in [0]:  # for part 1
                for w in range(rw[0]-1, rw[1]+1 +1):  # for part 2

                    actives = num_neighbours_active(cube, x, y, z, w)

                    if cube[x][y][z][w] == '#':
                        if 2 <= actives <= 3:
                            next_cube[x][y][z][w] = '#'
                        else:
                            next_cube[x][y][z][w] = '.'

                    else: #if cube[x][y][z][w] == '.':
                        if actives == 3:
                            next_cube[x][y][z][w] = '#'
                        else:
                            next_cube[x][y][z][w] = '.'

                    if next_cube[x][y][z][w] == '#':
                        count += 1

    print count
    return next_cube

for i in range(6):
    cube = iterate(cube)

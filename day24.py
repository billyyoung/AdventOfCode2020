import re
from collections import defaultdict
from copy import deepcopy

with open("day24.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

def parse(dir_str):
    res = []
    i = 0
    while i < len(dir_str):
        if dir_str[i] in ['e', 'w']:
            res.append(dir_str[i])
            i += 1
        else:  # n*, s*
            res.append(dir_str[i:i+2])
            i += 2
    return res

def get_neighbours(tile):
    neighbours = []
    # E,W
    for dx in [-1, 1]:
        new_tile = (tile[0] + dx, tile[1])
        neighbours.append(new_tile)

    # N*, S*
    for dx in [-0.5, 0.5]:
        for dy in [-1, 1]:
            new_tile = (tile[0] + dx, tile[1] + dy)
            neighbours.append(new_tile)

    return neighbours

hex_map = defaultdict(str)
black_count = 0

for line in lines:
    directions = parse(line)

    posx = 0
    posy = 0
    for d in directions:
        if 'n' in d:
            posy += 1
        elif 's' in d:
            posy -= 1

        ew_modifier = 1 if len(d) == 1 else 0.5
        if 'e' in d:
            posx += ew_modifier
        elif 'w' in d:
            posx -= ew_modifier

        key = (posx, posy)
        if key not in hex_map:
            hex_map[key] = 'white'

    key = (posx, posy)
    if key in hex_map:
        colour = hex_map[key]
        if colour == 'black':
            hex_map[key] = 'white'
            black_count -= 1
        else:
            hex_map[key] = 'black'
            black_count += 1

            # add all adjacent neighbours to hex_map for part 2
            for neighbour_tile in get_neighbours(key):
                if neighbour_tile not in hex_map:
                    hex_map[neighbour_tile] = 'white'
    else:
        hex_map[key] = 'black'
        black_count += 1

        # add all adjacent neighbours to hex_map for part 2
        for neighbour_tile in get_neighbours(key):
            if neighbour_tile not in hex_map:
                hex_map[neighbour_tile] = 'white'

print black_count

# part 2
def get_adjacent_black_count(tile, hex_map):
    count = 0

    for neighbour_tile in get_neighbours(tile):
        if neighbour_tile in hex_map and hex_map[neighbour_tile] == 'black':
            count += 1
    return count

for i in range(100):
    new_map = defaultdict(str)

    queue = hex_map.keys()
    for tile in queue:
        colour = hex_map[tile]

        new_map[tile] = colour

        adj_black_count = get_adjacent_black_count(tile, hex_map)
        if colour == 'black' and (adj_black_count == 0 or adj_black_count > 2):
            new_map[tile] = 'white'
            black_count -= 1

        elif colour == 'white' and adj_black_count == 2:
            new_map[tile] = 'black'
            black_count += 1

            # add all adjacent neighbours to hex_map for part 2
            for neighbour_tile in get_neighbours(tile):
                if neighbour_tile not in hex_map:
                    queue.append(neighbour_tile)
                    hex_map[neighbour_tile] = 'white'

    print 'Day %d: %d' % (i+1, black_count)
    hex_map = new_map

print black_count

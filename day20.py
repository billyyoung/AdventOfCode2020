from collections import defaultdict
import re
from copy import deepcopy
from pprint import pprint
import math

with open("day20.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

tile_id_to_tile = {}

for i in range(0, len(lines), 11):
    _, num_str = lines[i].split(" ")
    num = int(num_str[:-1])  # remove ':'

    grid = [
        [lines[i+j][k] for k in range(len(lines[i+1]))]
        for j in range(1, 11)
    ]

    tile_id_to_tile[num] = grid

# setup a N x N grid
# for each position in the grid, starting at top-left, try a piece
# for the adjacent pieces, specify a "required edges"
# search among the remaining pieces for any takers, try adding them
# if no more takers, then this is not a valid setup, bubble up and try anotherpiece
# go until you fill all units in the grid

# need
# 1) some concept of a piece, its orientation and flippedness
# 2) for an empty neighbour, specify which edges are needed where
# 3) be able to look at pieces and select them based on ^

# encode the edge into binary
# ordered list for requirement of edges?  top is 0, right is 1, etc?
# -- then each piece only needs 4 lists: original, xflip, yflip, xyflip
#    and rotaions are handled by list subsets

# read top from L->R, right from T->B, bottom from R->L, left from B->T
# (like a snake going around the tile)
# so rotation is easy
def get_raw_edges(tile):
    raw_edges = [
        ''.join(tile[0]),  # top
        ''.join(tile[i][-1] for i in range(len(tile))),  # right
        ''.join(tile[-1][::-1]),  # bottom
        ''.join(tile[i][0] for i in range(len(tile)-1,-1,-1)),  # left
    ]
    return raw_edges

def img_to_bin(line):
    # convert '.' = 0, '#' = 1
    line = line.replace('.', '0')
    line = line.replace('#', '1')
    return line

def img_to_int(line):
    line = '0b' + img_to_bin(line)
    return int(line, 2)

def flip(tile, axes_str):
    new_tile = deepcopy(tile)
    if 'x' in axes_str:
        new_tile = [
            [new_tile[row][col] for col in range(len(new_tile[0]))]
            for row in range(len(new_tile)-1, -1, -1)
        ]

    if 'y' in axes_str:
        new_tile = [
            [new_tile[row][col] for col in range(len(new_tile[0])-1, -1, -1)]
            for row in range(len(new_tile))
        ]

    return new_tile

def tile_to_all_edge_combos(tile):
    # only need Original + Flip-on-X-axis
    # then rotations cover the other 2 flip cases (Y-flip, XY-flip)
    edges = [img_to_bin(e) for e in get_raw_edges(tile)]
    edges_xflip = [img_to_bin(e) for e in get_raw_edges(flip(tile, 'x'))]

    return [edges, edges_xflip]  # , edges_yflip, edges_xyflip]

def get_next(row, col, col_size):
    if col == col_size-1:
        return row+1, 0
    else:
        return row, col+1

def recurse(layout, ids_seen, tile_id_to_tile, next_row, next_col):
    if len(ids_seen) == len(tile_id_to_tile):
        return layout
    next_next_row, next_next_col = get_next(next_row, next_col, len(layout[0]))

    # we are filling in tiles from L->R, top->bottom
    # so requirements are L and Above
    left_req = None
    if next_col != 0:

        # RIGHT side is generated from T->B
        # we want our next tile's LEFT side to match the same orientation
        # but LEFT is usually read from B->T
        # so convert RIGHT side of prev tile from T->B to B->T
        left_req = layout[next_row][next_col-1][1][RIGHT][::-1]


    top_req = None
    if next_row != 0:

        # BOTTOM side is generated from R->L
        # we want our next tile's TOP side to match the same orientation
        # but TOP is usually read from L->R
        # so convert BOTTOM side of prev tile from R->L to L->R
        top_req = layout[next_row-1][next_col][1][BOTTOM][::-1]

    for tile_id, tile in tile_id_to_tile.iteritems():
        if tile_id in ids_seen:
            continue

        # if this tile meets our reqs, add it and move on
        all_combos = tile_to_all_edge_combos(tile)
        for combo in all_combos:
            if top_req and top_req not in combo:
                continue
            if left_req and left_req not in combo:
                continue
            for i in range(4):
                attempt = [combo[(i+j) % 4] for j in range(4)]
                fail = (
                    (top_req and attempt[TOP] != top_req) or
                    (left_req and attempt[LEFT] != left_req)
                )
                if not fail:
                    layout[next_row][next_col] = (tile_id, attempt)
                    ids_seen.add(tile_id)
                    res = recurse(
                        layout, ids_seen, tile_id_to_tile, next_next_row,
                        next_next_col
                    )

                    if res:
                        return res
                    else:
                        # undo
                        layout[next_row][next_col] = (0,0)
                        ids_seen.remove(tile_id)

    return None

# actual part 1
size = int(math.sqrt(len(tile_id_to_tile)))
final_layout = [
    [(0,0) for i in range(size)]
    for j in range(size)
]
ids_done = 0
# for tile_id, tile in tile_id_to_tile.iteritems():
# for tile_id, tile in [(1951, tile_id_to_tile[1951])]:  # seed answer to sample
for tile_id, tile in [(2099, tile_id_to_tile[2099])]:  # seed answer
    # test out each tile in each orientation...

    # get all orientations
    all_combos = tile_to_all_edge_combos(tile)
    ids_seen = {tile_id}

    found = False
    for combo in all_combos:
        for i in range(4):
            attempt = [combo[(i+j) % 4] for j in range(4)]

            final_layout[0][0] = (tile_id, attempt)

            layout = recurse(final_layout, ids_seen, tile_id_to_tile, 0, 1)
            if layout:
                found = True
                final_layout = layout
                break
        if found:
            break

    ids_done += 1
    print ids_done

# debug, seed sample
#final_layout = [[(0,0) for i in range(size)] for j in range(size)]
#final_layout[0][0] = (1951, ['1000110100', '0100111110', '0110001101', '1101001001'])
#final_layout = recurse(final_layout, {1951}, tile_id_to_tile, 0, 1)
#print final_layout[0][0][0] * final_layout[0][size-1][0] * \
#        final_layout[size-1][0][0] * final_layout[size-1][size-1][0]

# part 2
def rotate(tile, cc_rotations):

    res = deepcopy(tile)
    for i in range(cc_rotations):
        # right side becomes top
        res = [
            [res[row][col] for row in range(len(res))]
            for col in range(len(res[0])-1, -1, -1)
        ]

    return res

def get_tile_from_orientation(tile, orientation):
    combo = [img_to_bin(e) for e in get_raw_edges(tile)]
    # rotate
    for i in range(4):
        attempt = [combo[(i+j) % 4] for j in range(4)]

        if orientation == attempt:
            # i = 1 == right side became TOP == CC rotation
            return rotate(tile, cc_rotations=i)

    combo = [img_to_bin(e) for e in get_raw_edges(flip(tile, 'x'))]
    # flip, then rotate
    for i in range(4):
        attempt = [combo[(i+j) % 4] for j in range(4)]

        if orientation == attempt:
            res = flip(tile, 'x')
            return rotate(res, cc_rotations=i)

def get_tile_removed_borders(tile):
    temp = tile[1:len(tile)-1]
    result = [
        [row[c] for c in range(1, len(row)-1)]
        for row in temp
    ]
    return result

# construct image from layout
picture_grid = [
    [None for i in range(size)]
    for j in range(size)
]
for row in range(size):
    for col in range(size):

        tile_id, orientation = final_layout[row][col]
        oriented_tile = get_tile_from_orientation(
            tile_id_to_tile[tile_id], orientation
        )

        picture_grid[row][col] = get_tile_removed_borders(oriented_tile)

# construct final image
final_image = []
for row in picture_grid:
    for img_row in range(len(row[0])):  # row[0] is a picture
        metadata = [''.join(row[i][img_row]) for i in range(len(row))]
        final_image.append(''.join(metadata))

sea_monster = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

total_hits = 0
for row in range(len(final_image)):
    for col in range(len(final_image[0])):
        if final_image[row][col] == '#':
            total_hits += 1
sea_monster_size = 0
for row in range(len(sea_monster)):
    for col in range(len(sea_monster[0])):
        if sea_monster[row][col] == '#':
            sea_monster_size += 1

# generate monster flips and rotations to go through
monster_grid = [
    [row[c] for c in range(len(row))]
    for row in sea_monster
]
monster_mod_grids = [
    monster_grid,
    flip(monster_grid, 'x'),
    flip(monster_grid, 'y'),
    flip(monster_grid, 'xy'),

    rotate(monster_grid, cc_rotations=1),
    flip(rotate(monster_grid, cc_rotations=1), 'x'),
    flip(rotate(monster_grid, cc_rotations=1), 'y'),
    flip(rotate(monster_grid, cc_rotations=1), 'xy'),
]
max_count = 0
for mod in monster_mod_grids:

    monster_count = 0
    for row in range(len(final_image)-len(mod)):
        for col in range(len(final_image[0])-len(mod[0])):

            # check if this space has a monster
            monster_hits = 0
            for dr in range(len(mod)):
                for dc in range(len(mod[0])):

                    if mod[dr][dc] == '#' and final_image[row + dr][col + dc] == '#':
                        monster_hits += 1
            if monster_hits == sea_monster_size:
                import pdb;pdb.set_trace()
                monster_count += 1
                # do I need to shift my window intelligently?

    if monster_count > 0:
        max_count = max(max_count, monster_count)

print total_hits - max_count * sea_monster_size

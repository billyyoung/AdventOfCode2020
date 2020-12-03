from collections import defaultdict

with open("day3.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

def slide(dx, dy):
    posx, posy = 0, 0

    tree_hit_count = 0
    while posy < len(lines)-1:
        posx = (posx + dx) % len(lines[0])
        posy = posy + dy

        if posy >= len(lines):
            break
        if lines[posy][posx] == '#':
            tree_hit_count += 1

    return tree_hit_count

print slide(1,1) * slide(3,1) * slide(5,1) * slide(7,1) * slide(1,2)

import re
from collections import defaultdict

with open("day21.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

ingr_count = defaultdict(int)
allergens_to_possible_ingrs = defaultdict(set)

for line in lines:
    match = re.search(r"(?<=\(contains ).+(?=\)$)", line)
    allergens = match.group().split(", ")

    match = re.search(r".+(?= \()", line)
    ingredients = match.group().split(" ")

    for a in allergens:
        if a in allergens_to_possible_ingrs:
            allergens_to_possible_ingrs[a] = \
                allergens_to_possible_ingrs[a].intersection(ingredients)
        else:
            allergens_to_possible_ingrs[a] = set(ingredients)

    for ingr in ingredients:
        ingr_count[ingr] += 1

# part 1
# for each allergen, guess a possibility
# and only the correct solution will have each allergen be left with 1 match
# (failed solution will have an allergen with 0 options)

def solve(a_to_i, allergens_to_possible_ingrs):

    solved_ingredients = set(a_to_i.values())

    # see if there are still solutions
    remaining_a = set(allergens_to_possible_ingrs.keys()).difference(
        a_to_i.keys()
    )
    if len(remaining_a) == 0:
        return a_to_i  # done!

    for a in remaining_a:
        # exclude the solved ingrs, see how many remain
        remaining_i = set(allergens_to_possible_ingrs[a]).difference(
            solved_ingredients
        )
        if len(remaining_i) == 0:
            return None  # no solution

    new_a = remaining_a.pop()
    remaining_i = set(allergens_to_possible_ingrs[new_a]).difference(
        solved_ingredients
    )

    # try: i causes a
    for new_i in remaining_i:
        a_to_i[new_a] = new_i
        res_a_to_i = solve(a_to_i, allergens_to_possible_ingrs)
        if res_a_to_i:
            return res_a_to_i
        del a_to_i[new_a]

    return None  # no solution

res = solve(defaultdict(str), allergens_to_possible_ingrs)

bad_ingrs = set(res.values())
total = 0
for ingr, count in ingr_count.iteritems():
    if ingr not in bad_ingrs:
        # good boi
        total += count
print total

# part 2
sorted_bad_i = [res[a] for a in sorted(res.keys())]
print ','.join(sorted_bad_i)

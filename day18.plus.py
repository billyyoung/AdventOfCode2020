from collections import defaultdict
import re
from copy import deepcopy

with open("day18.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

def isint(s):
    try:
        int(s)
        return True
    except:
        return False

def calc(val1, op, val2):
    if op == '*':
        return val1 * val2
    else:
        return val1 + val2

def evaluate(items, desired_op):
    prev_val = 0
    prev_i = 0
    op = None

    i = 0
    while i < len(items):
        item = items[i]
        if isint(item):
            val = int(item)

            if op is None:
                prev_val = val
                prev_i = i
            else:
                # val op val
                total = calc(prev_val, op, val)

                new_items = items[:prev_i] + [str(total)] + items[i+1:]
                items = new_items

                i = prev_i  # continue from 'total'
                op = None
                continue

        elif items[i] in desired_op:
            op = items[i]
            i += 1
            continue

        i += 1

    return items

# part 1
# returns a collapsed list of items: if there are brackets: recurse inside
# otherwise, do any op that comes first

def collapse(items):
    # clear brackets
    i = 0
    while i < len(items):
        item = items[i]

        if '(' in item:
            # get result of brackets
            start_index = i
            brackets = item.count('(')
            for j in range(i+1, len(items)):
                if '(' in items[j]:
                    brackets += items[j].count('(')
                if ')' in items[j]:
                    brackets -= items[j].count(')')

                if brackets == 0:
                    break
            end_index = j

            subset = items[start_index:end_index+1]
            subset[0] = subset[0][1:]  # remove (
            subset[-1] = subset[-1][:-1]  # remove )

            result = collapse(subset)

            # replace array
            new_items = items[:i] + result + items[end_index+1:]
            items = new_items

        i += 1

    items = evaluate(items, '+*')
    return items

total = 0
for line in lines:
    ans = int(collapse(line.split(" "))[0])
    total += ans
print total

# part 2
# returns a collapsed list of items: if there are brackets: recurse inside
# otherwise, do + first, then *
def collapse2(items):
    # clear brackets
    i = 0
    while i < len(items):
        item = items[i]

        if '(' in item:
            # get result of brackets
            start_index = i
            brackets = item.count('(')
            for j in range(i+1, len(items)):
                if '(' in items[j]:
                    brackets += items[j].count('(')
                if ')' in items[j]:
                    brackets -= items[j].count(')')

                if brackets == 0:
                    break
            end_index = j

            subset = items[start_index:end_index+1]
            subset[0] = subset[0][1:]  # remove (
            subset[-1] = subset[-1][:-1]  # remove )

            result = collapse2(subset)

            # replace array
            new_items = items[:i] + result + items[end_index+1:]
            items = new_items

        i += 1

    items = evaluate(items, '+')
    items = evaluate(items, '*')
    return items

total = 0
for line in lines:
    ans = int(collapse2(line.split(" "))[0])
    total += ans
print total

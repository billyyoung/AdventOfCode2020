from collections import defaultdict
import re
from copy import deepcopy

with open("day18.sample") as infile:
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

def parse(items, level):
    total = 0

    op = None
    i = 0
    while i < len(items):

        if isint(items[i]):
            val = int(items[i])

            if op is None:
                total = val
            else:
                total = calc(total, op, val)

        elif items[i] in ['*', '+']:
            op = items[i]
            i += 1
            continue

        elif items[i][0] == '(':
            sub_items = [items[i][1:]]  # remove the bracket
            for j in range(i+1, len(items)):
                sub_items.append(items[j])

            val = parse(sub_items, level + 1)

            total = calc(total, op, val)

            # update items with sub-results
            brackets = items[i].count('(')
            for j in range(i+1, len(items)):
                if '(' in items[j]:
                    brackets += 1
                elif ')' in items[j]:
                    brackets -= items[j].count(')')

                if brackets <= 0:
                    break

            if brackets < 0:
                # we reached the end of a higher level bracket-expr
                # so bubble up the value right away
                return total

            # otherwise it's a (expr) so just collapse it
            new_items = [items[k] for k in range(i)]
            new_val = str(val)
            new_items.append(new_val)
            new_items += [items[k] for k in range(j+1, len(items))]
            print ' ' * level, new_items

            items = new_items

        elif ')' in items[i]:
            # (a + b)
            # (a + (b + c))

            val = int(items[i].replace(')', ''))
            total = calc(total, op, val)
            print ' ' * level, 'return total = %d' % total
            return total

        i += 1
        print ' ' * level, 'total = %d' % total
    return total

total = 0
for line in lines:
    print line
    items = line.split(" ")
    ans = parse(items, 1)
    print ans
    print
    total += ans

print total

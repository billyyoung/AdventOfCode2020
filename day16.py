from collections import defaultdict
import re

with open("day16.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

rules = []
rules_and_names = []
tickets = []

for i in range(len(lines)):
    if lines[i] == 'your ticket:':
        tickets = [
            [int(n) for n in l.split(',')]
            for l in [lines[i+1]] + lines[i+3:]
        ]
        break

    match = re.search(r"(?<=: )\d+-\d+(?= or)", lines[i])
    interval1 = [int(n) for n in match.group().split('-')]

    match = re.search(r"(?<= )\d+-\d+(?=$)", lines[i])
    interval2 = [int(n) for n in match.group().split('-')]

    rule = [interval1, interval2]
    rules.append(rule)
    name = lines[i][:lines[i].index(':')]
    rules_and_names.append([name, rule])

def get_errors(rules, ticket):
    errors = []
    for n in ticket:
        matched = 0
        for rule in rules:
            if rule[0][0] <= n <= rule[0][1] or rule[1][0] <= n <= rule[1][1]:
                matched += 1
                break

        if matched == 0:
            errors.append(n)

    return errors

name_to_possibilities = {
    name : {i for i in range(len(rules))}
    for name, _ in rules_and_names
}

error_total = 0
for ticket in tickets[1:]:
    errors = get_errors(rules, ticket)
    if errors:
        error_total += sum(errors)

    else:

        for i in range(len(ticket)):
            n = ticket[i]

            for name, [i1, i2] in rules_and_names:
                if not (i1[0] <= n <= i1[1] or i2[0] <= n <= i2[1]):

                    # then this name cannot correspond to the ith value
                    name_to_possibilities[name].discard(i)

print error_total

name_to_index = defaultdict(int)
for i in range(len(rules)):

    for name, s in name_to_possibilities.items():
        if len(s) == 1:
            answer = s.pop()
            name_to_index[name] = answer
            break

    for name in name_to_possibilities:
        name_to_possibilities[name].discard(answer)

product = 1
for name, i in name_to_index.items():
    if 'departure' in name:
        product *= tickets[0][i]

print product

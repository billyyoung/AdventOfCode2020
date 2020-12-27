from collections import defaultdict
import re
from copy import deepcopy

with open("day19.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

rules = {}
for i in range(len(lines)):
    if ':' not in lines[i]:
        break

    # parse rule: "N: <rule>"
    rule_num, rule = lines[i].split(": ")
    if '"' in rule:
        parsed_rule = rule[1]  # "a"
    else:
        rule_list = rule.split(" | ")
        parsed_rule = [
            [int(n) for n in r.split(" ")]
            for r in rule_list
        ]
    rules[int(rule_num)] = parsed_rule

messages = lines[i:]

def is_valid(msg, rules, debug=False):
    # if any msg was fully consumed by a ruleset
    return '' in consume(msg, rules, 0, 1, debug)

def consume(msg, rules, rule_num, level, debug):
    if msg == '':  # trying to consume with nothing left...
        return set()

    if rules[rule_num] in ['a', 'b']:
        return {msg[1:]} if msg[0] == rules[rule_num] else set()

    # possible success paths after feeding 'msg' through the rule lists
    possibilities = set()

    rule_list = rules[rule_num]
    # rule_list = [ [1, 2, 3, ...], [... ]

    for rule in rule_list:  # e.g. [1, 2, 3, ...]

        # try 'msg' on this particular ruleset
        test_msgs = {msg}

        # see what possible consumptions there are
        success = True
        for r in rule:  # e.g. 42 of [42, 11, 31]

            temp = set()
            for t in test_msgs:

                if debug:
                    print "%s [try] - [%s] -> %s" % (
                        " " * level,
                        ','.join([str(x) for x in rule]),
                        test_msgs
                    )

                results = consume(t, rules, r, level+1, debug)
                for res in results:
                    temp.add(res)

            # if none of the possibilities passed 't':
            # then this entire rule is a failure, break early
            if not temp:
                success = False
                break

            # some possibilities passed 't', move them forward to the next 'r'
            test_msgs = temp

        if success:  # found some things that passed this ruleset

            if debug:
                print "%s [result] - [%s] -> %s" % (
                    " " * level,
                    ','.join([str(x) for x in rule]),
                    test_msgs
                )

            # test_msgs are the results of the consumption, move forward
            possibilities = possibilities.union(test_msgs)

    return possibilities

count = 0
for i in range(len(messages)):
    msg = messages[i]

    valid = is_valid(msg, rules)
    if valid:
        count += 1
print count

# part 2
rules[8] = [[42, 8], [42]]
rules[11] = [[42, 11, 31], [42, 31]]

count = 0
for i in range(len(messages)):
    msg = messages[i]

    valid = is_valid(msg, rules)
    if valid:
        count += 1
print count

from collections import defaultdict
import re
from copy import deepcopy

with open("day19.sample2") as infile:
    lines = [l for l in infile.read().split("\n") if l]

rules = {}
i = 0
while True:
    if ':' not in lines[i]:
        break

    # parse rule:
    # N: rule
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
    i += 1

messages = lines[i:]

def is_valid(msg, rules):
    if consume(msg, rules, 0) == '':  # fully consumed
        return True
    return False

def consume(msg, rules, rule_num):
    if msg == '':  # trying to consume with nothing left...
        return 'fail'

    if rules[rule_num] in ['a', 'b']:
        return msg[1:] if msg[0] == rules[rule_num] else 'fail'

    rule_list = rules[rule_num]
    # if 2222 in rules and rule_num in [8, 11]:
    #     import pdb;pdb.set_trace()

    # rule_list = [ [1, 2, 3, ...], [... ]
    # rule = [1, 2, 3, ...]
    for rule in rule_list:
        test_msg = msg

        success = True
        for r in rule:
            res = consume(test_msg, rules, r)
            if res == test_msg or res == 'fail':  # rule failed, get out
                success = False
                break

            else:  # rule worked, keep going with res
                test_msg = res

        if success:
            return test_msg  # all r's succeeded, return consumed msg

    return msg  # nothing succeeded, this msg failed

count = 0
for i in range(len(messages)):
    msg = messages[i]

    valid = is_valid(msg, rules)
    if valid:
        count += 1

print count
print

# part 2
rules[2222] = 1  # hack to flag part 2
rules[8] = [[42, 8], [42]]
rules[11] = [[42, 11, 31], [42, 31]]

count = 0
for i in range(len(messages)):
    msg = messages[i]

    # msg = 'babbbbaabbbbbabbbbbbaabaaabaaa'
    valid = is_valid(msg, rules)
    if valid:
        count += 1
    print "%s - %s" % (msg, valid)  # debug

print count

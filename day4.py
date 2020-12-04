import re

with open("day4.input") as infile:
    lines = [l for l in infile.read().split("\n")]

def is_valid1(values):
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for f in required_fields:
        if f not in values:
            return False

    return True

def is_valid2(values):
    required_fields_to_checks = {
        'byr' : [
            lambda v: re.search('^\d{4}$', v) is not None,
            lambda v: 1920 <= int(v) <= 2002,
        ],
        'iyr' : [
            lambda v: re.search('^\d{4}$', v) is not None,
            lambda v: 2010 <= int(v) <= 2020,
        ],
        'eyr' : [
            lambda v: re.search('^\d{4}$', v) is not None,
            lambda v: 2020 <= int(v) <= 2030,
        ],
        'hgt' : [
            lambda v: v[-2:] in ['cm', 'in'],
            lambda v: (v[-2:] == 'cm' and
                re.search('^\d{3}', v[:-2]) is not None and
                150 <= int(v[:-2]) <= 193) or
                (v[-2:] == 'in' and
                re.search('^\d{2}', v[:-2]) is not None and
                59 <= int(v[:-2]) <= 76),
        ],
        'hcl' : [
            lambda v: re.search('^#[0-9a-f]{6}$', v) is not None,
        ],
        'ecl' : [
            lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        ],
        'pid' : [
            lambda v: re.search('^\d{9}$', v) is not None,
        ],
    }
    for key, checks in required_fields_to_checks.items():
        if key not in values:
            return False

        value = values[key]
        for check in checks:
            if not check(value):
                return False

        if key == 'hgt':
            if value[-2:] not in ['cm', 'in']:
                return False
            if value[-2:] == 'cm':
                prefix = value[:-2]

    return True

index = 0
valid = 0
values = {}
while index < len(lines):

    if lines[index]:
        for s in lines[index].split(" "):
            key, value = s.split(":")
            values[key] = value
    else:
        print values
        if is_valid2(values):
            valid += 1
        values = {}
    index += 1

print valid

from collections import defaultdict
import re

with open("day14.input") as infile:
    lines = [l for l in infile.read().split("\n") if l]

memory1 = defaultdict(int)
memory2 = defaultdict(int)

def expand_float(masked_addr):
    if 'X' not in masked_addr:
        return [int(masked_addr, 2)]
    else:
        for i in range(len(masked_addr)):
            if masked_addr[i] == 'X':
                new_addr = masked_addr[:i] + '0' + masked_addr[i+1:]
                sublist1 = expand_float(new_addr)

                new_addr = masked_addr[:i] + '1' + masked_addr[i+1:]
                sublist2 = expand_float(new_addr)

                break

        return sublist1 + sublist2

def run_program(bitmask, writes, memory1, memory2):
    for addr, value in writes:
        # part 1
        bin_value = bin(value)[2:]  # remove '0b' prefix
        # fill out 0s
        bin_value = '0' * (len(bitmask) - len(bin_value)) + bin_value

        masked_value = ''
        for i in range(len(bin_value)):
            if bitmask[i] == 'X':
                masked_value += bin_value[i]
            else:
                masked_value += bitmask[i]

        new_value = int(masked_value, 2)

        memory1[addr] = new_value

        # part 2
        bin_addr = bin(addr)[2:]  # remove '0b' prefix
        # fill out 0s
        bin_addr = '0' * (len(bitmask) - len(bin_addr)) + bin_addr

        masked_addr = ''
        for i in range(len(bin_value)):
            if bitmask[i] == '0':
                masked_addr += bin_addr[i]
            else:
                masked_addr += bitmask[i]

        new_addrs = expand_float(masked_addr)
        for a in new_addrs:
            memory2[a] = value

i = 0
while i < len(lines):
    bitmask = lines[i][7:]  # get rid of 'mask = '
    i += 1

    writes = []
    while i < len(lines) and 'mask' not in lines[i]:
        match = re.search(r"(?<=\[)\d+(?=\])", lines[i])
        addr = int(match.group())

        match = re.search(r"(?<= )\d+(?=$)", lines[i])
        value = int(match.group())

        writes.append((addr, value))
        i += 1

    run_program(bitmask, writes, memory1, memory2)

print sum(memory1.values())
print sum(memory2.values())

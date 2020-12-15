from collections import defaultdict

input = [13,16,0,12,15,1]

last_index = defaultdict(int)

for i in range(len(input)):
    last_index[input[i]] = i

count = len(input)
next_num = 0  # 4th num, index = 3
while count < 30000000-1: # 2019:
    prev_num = next_num

    if next_num in last_index:
        next_num = count - last_index[next_num]

    else:
        next_num = 0

    last_index[prev_num] = count
    count += 1

print next_num

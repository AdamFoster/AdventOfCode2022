#answer = STHGRZZFR

import functools as ft
import re

filename = 'sample01.txt'
filename = 'input.txt'

score = 0
stackcount = 0
stacks = [[]]
with open(filename, "r") as f:
    while len(line := f.readline().rstrip('\n')) > 0:
        if stackcount == 0:
            stackcount = (len(line)-3)//4+1
            stacks = [[] for i in range(stackcount)]
        for i in range(stackcount):
            if line[4*i+1] != " ":
                stacks[i].insert(0, line[4*i+1])
        #print("*" + line + "*")
    while (line := f.readline().strip()):
        matches = re.match("move ([0-9]+) from ([0-9]+) to ([0-9]+)", line)

        repeats = int(matches.group(1))
        source = int(matches.group(2))
        target = int(matches.group(3))
        print(f"{repeats} {source} {target}")
        for i in range(repeats):
            stacks[target-1].append(stacks[source-1].pop(i-repeats))

print(stackcount)
print(stacks)
print(ft.reduce(lambda a, b: a+b[-1], stacks, ""))
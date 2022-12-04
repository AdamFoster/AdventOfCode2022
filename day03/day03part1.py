#answer = 8139

import re

#filename = 'sample01.txt'
filename = 'input.txt'

def priority(c : chr) -> int:
    if re.match("[A-Z]", c):
        return ord(c)-ord('A')+27
    elif re.match("[a-z]", c):
        return ord(c)-ord('a')+1
    else:
        print("Invalid character found: " + c + "!")

score = 0
with open(filename, "r") as f:
    for line in f:
        line = line.strip()
        c1 = line[:len(line)//2]
        c2 = line[len(line)//2:]
        s1 = {c for c in c1}
        s2 = {c for c in c2}
        intersection = s1.intersection(s2)
        if len(intersection) != 1:
            print("Set too big")
            print(intersection)
            print(s1)
            print(s2)
            exit(1)
        for e in intersection:
            score += priority(e)
        #print(intersection)
print(score)


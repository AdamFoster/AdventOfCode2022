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
    while (line := f.readline().strip()):
        s1 = {c for c in line}
        s2 = {c for c in f.readline().strip()}
        s3 = {c for c in f.readline().strip()}

        intersection = s1.intersection(s2).intersection(s3)
        if len(intersection) != 1:
            print("Set too big")
            print(intersection)
            print(s1)
            print(s2)
            print(s3)
            exit(1)

        for e in intersection:
            score += priority(e)
print(score)


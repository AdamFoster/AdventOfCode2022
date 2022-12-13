#answer = 21276

from copy import deepcopy
import functools


filename = 'sample01.txt'
filename = 'input.txt'

def parse(s: str):
    #s = s.strip()[1:-1]
    list = []
    currentstack = [list]
    while len(s) > 0:
        if s[0] == ",":
            s = s[1:]
        if s[0].isdigit():
            num = ""
            while s[0].isdigit():
                num += s[0]
                s = s[1:]
            currentstack[-1].append(int(num))
        elif s[0] == "[":
            newlist = []
            currentstack[-1].append(newlist)
            currentstack.append(newlist)
            s = s[1:]
        elif s[0] == "]":
            currentstack.pop()
            s = s[1:]
        else:
            print("Unknown string", s, list, currentstack)
    return list[0]



def compare(first, second):
    fcurrentstack = [deepcopy(first)]
    scurrentstack = [deepcopy(second)]
    rightorder = False
    done = False
    print("FIRST_SECOND", first, second, sep=" * ")
    while not done:
        print("Comparing", fcurrentstack[-1], scurrentstack[-1], sep=" *** ")
        if len(fcurrentstack[-1]) == 0 and len(scurrentstack[-1]) == 0:
            fcurrentstack.pop()
            scurrentstack.pop()
        elif len(fcurrentstack[-1]) == 0 and len(scurrentstack[-1]) > 0:
            done = True
            rightorder = True
        elif len(fcurrentstack[-1]) > 0 and len(scurrentstack[-1]) == 0:
            done = True
            rightorder = False
            #print("Too long")
            #print(fcurrentstack[-1])
            #print(scurrentstack[-1])
        elif isinstance(fcurrentstack[-1][0], int) and isinstance(scurrentstack[-1][0], int):
            if fcurrentstack[-1][0] < scurrentstack[-1][0]:
                done = True
                rightorder = True
            elif fcurrentstack[-1][0] > scurrentstack[-1][0]:
                done = True
                rightorder = False
                #print(fcurrentstack)
                #print(scurrentstack)
            else:
                fcurrentstack[-1].pop(0)
                scurrentstack[-1].pop(0)
        elif isinstance(fcurrentstack[-1][0], int):
            fcurrentstack[-1][0] = [fcurrentstack[-1][0]]
        elif isinstance(scurrentstack[-1][0], int):
            scurrentstack[-1][0] = [scurrentstack[-1][0]]
        else: # both lists
            fcurrentstack.append(fcurrentstack[-1].pop(0))
            scurrentstack.append(scurrentstack[-1].pop(0))

    return -1 if rightorder else 1

packets = []
    
with open(filename, "r") as f:
    line = f.readline()
    while line:
        if len(line.strip()) > 0:
            #print(line)
            packets.append(parse(line.strip()))
        line = f.readline()

packets.append(parse("[[2]]"))
packets.append(parse("[[6]]"))
two = str(packets[-2])
six = str(packets[-1])

sortedpackets = sorted(packets, key=functools.cmp_to_key(compare))
decoder = 1
for i,p in enumerate(sortedpackets):
    print(p)
    if str(p) == six or str(p) == two:
        decoder *= (i+1)
print(decoder)


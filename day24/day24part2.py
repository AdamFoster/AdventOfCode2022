#answer = 843 # too high

import math
from queue import PriorityQueue

filename = 'sample02.txt'
filename = 'input.txt'

UP = (-1,0)
DOWN = (1,0)
LEFT = (0,-1)
RIGHT = (0,1)
WAIT = (0,0)
dirs = [UP,DOWN,LEFT,RIGHT]
dirsandwait = [UP,DOWN,LEFT,RIGHT,WAIT]
dirfromicon = {"^":UP, "v":DOWN, "<":LEFT, ">":RIGHT}
iconfromdir = {dir:icon for icon,dir in dirfromicon.items()}

BlizzardType = tuple[int,int,tuple[int,int]]

blizzards: set[BlizzardType] = set() # row, column, (dir)
blizzardcache: list[set[BlizzardType]] = []
blizzardcachesimple: list[set[tuple[int,int]]] = []
startpos: int = -1
endpos: int = -1
width = 0
height = 0
with open(filename, "r") as f:
    line = f.readline().strip()
    startpos = (-1,line.index(".")-1)
    line = f.readline().strip()
    linecount = 0
    width = len(line)-2
    while line.count("#") == 2:
        for i,c in enumerate(line):
            if c in dirfromicon.keys():
                blizzards.add((linecount, i-1, dirfromicon[c]))

        linecount += 1
        line = f.readline().strip()
    endpos = (linecount,line.index(".")-1)
    height = linecount
    blizzardcache.append(blizzards)
    blizzardcachesimple.append(set([(r,c) for (r,c,(dr,dc)) in blizzards]))
lcm = math.lcm(width,height)

print(startpos, "->", endpos)
#print(blizzards)
print("Height=",height, "width=", width, "lcm=", lcm)
#exit(0)

def getBlizzard(time: int) -> set[BlizzardType]:
    t = len(blizzardcache)
    while t < (time+1)%(lcm+1):
        newblizzardset: set[BlizzardType] = set()
        for b in blizzardcache[t-1]:
            newblizzard = [b[0]+b[2][0], b[1]+b[2][1], b[2]]
            newblizzard[0] = newblizzard[0] % height
            newblizzard[1] = newblizzard[1] % width
            newblizzardset.add(tuple(newblizzard))
        blizzardcache.append(newblizzardset)
        blizzardcachesimple.append(set([(r,c) for (r,c,(dr,dc)) in newblizzardset]))

        t = len(blizzardcache)

    return blizzardcachesimple[time%lcm]

def printblizzard(bs: set[BlizzardType]) -> None:
    pbs = {}
    for (r,c,(dr,dc)) in bs:
        if (r,c) in pbs:
            if isinstance(pbs[(r,c)], int):
                pbs[(r,c)] += 1
            else:
                pbs[(r,c)] = 2
        else:
            pbs[(r,c)] = iconfromdir[(dr,dc)]
    for r in range(height):
        for c in range(width):
            if (r,c) in pbs:
                print(pbs[(r,c)], end="")
            else:
                print(".", end="")
        print()

#for i in range(6):
#    printblizzard(getBlizzard(i))
#    print(blizzardcache[i])
#    print("------------------")

def getcachekey(state: tuple[tuple[int,int], int], end) -> int:
    #return state[1] + abs(end[0]-state[0][0]) + abs(end[1]-state[0][1])
    return abs(end[0]-state[0][0]) + abs(end[1]-state[0][1])

nextopentimecache = [{},{},{}]
def nextopentime(time: int, target: tuple[int,int], stage: int) -> int:
    if target == startpos:
        target = (target[0]+1, target[1])
    elif target == endpos:
        target = (target[0]-1, target[1])
    else:
        assert False
    preptime = time - 1
    if time in nextopentimecache[stage]:
        return nextopentimecache[stage][time]
    else:
        i = 0
        while True:
            bs = getBlizzard(preptime+i)
            if target in bs:
                i += 1
            else:
                for j in range(i+1):
                    nextopentimecache[stage][time+j] = time+i
                break
    return nextopentimecache[stage][time]
    

def search(start,end,starttime,stage):
    print("Searching",start,"->",end,"t0=",starttime)
    besttime = 999999999999999999
    #queue: list[tuple[tuple[int,int], int]] = [] #(location, time)
    pqueue = PriorityQueue() #(priority,location,time)
    explored: set[tuple[tuple[int,int], int]] = set()
    root = (start, starttime)
    #queue.append(root)
    pqueue.put((getcachekey(root,end), root[0], root[1]))
    explored.add(root)
    
    while not pqueue.empty():
        #queue.sort(key=lambda s: s[1] + abs(end[0]-s[0][0]) + abs(end[1]-s[0][1]))
        #queue.sort(key=lambda s: )
        #print(queue)
        #(row,column), time = queue.pop(0)
        _,(row,column), time = pqueue.get()
        #if stage==2: print("R,c,t",row,column,time)
        #exit(0)

        if (row, column) in getBlizzard(time):
            #print("Hit blizzard")
            continue
        
        if (row,column) == end:
            print("At the end. Time=", time," Best=", besttime,"cache=",len(blizzardcache), len(blizzardcachesimple))
            besttime = min(time, besttime)
            #print()
            continue

        if besttime < nextopentime(time + abs(end[0]-row) + abs(end[1]-column), end, stage):
            print("Cull",besttime,"already better than",time + abs(end[0]-row) + abs(end[1]-column))
            continue

        for d in dirsandwait: #testconnections: #alldistances[state.location]:
            newlocation = (row+d[0], column+d[1])
            if ((0 <= newlocation[0] < height) and (0 <= newlocation[1] < width)) or newlocation == end or newlocation == start:
                s = (newlocation, time+1)
                exploredstate = (s[0], s[1]%lcm)
                if exploredstate not in explored: # not in explored[s.time]:
                    explored.add(exploredstate)
                    #queue.append(s)
                    pqueue.put((getcachekey(s,end), s[0], s[1]))
                    #if stage==2: print("Exploring", s)
        
        #if len(queue) > 5: break

    return besttime

there=search(start=startpos,end=endpos,starttime=0,stage=0)
print("There:",there)
back=search(start=endpos,end=startpos,starttime=there,stage=1)
print("Back:",back)
thereagain=search(start=startpos,end=endpos,starttime=back,stage=2)
print("Thereagain:",thereagain)

#thereagain=search(start=startpos,end=endpos,starttime=528,stage=2)
#print("Thereagain:",thereagain)

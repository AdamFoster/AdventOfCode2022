#answer = 1570434782634

from dataclasses import dataclass
from copy import deepcopy
from functools import reduce

@dataclass
class Rock:
    parts: tuple
    width: int
    height: int


#filename = 'sample01.txt'
filename = 'input.txt'

data = []
jets = []
with open(filename, "r") as f:
    jets = [-1 if c == "<" else 1 for c in f.readline().strip()]

chamberwidth = 7

# changing to up +ve
rocks = [Rock(parts=((0,0), (0,1), (0,2), (0,3)), width=4, height=1), 
         Rock(((-1,0), (0,1), (-1,1), (-2,1), (-1,2)), width=3, height=3),
         Rock(((-2,0), (-2,1), (0,2), (-1,2), (-2,2)), width=3, height=3),
         Rock(((0,0), (-1,0), (-2,0), (-3,0)), width=1, height=4),
         Rock(((0,0), (0,1), (-1,0), (-1,1)), width=2, height=2)] #r,c
#print(jets)
#print(rocks)
#exit(0)

orthodirs = [(0,-1), (0,1), (-1,0), (1,0)] 

def cull2(pile: set[tuple], added: tuple[int], maxheight: int) -> set[tuple]: #assumes added is at the top of a column
    flood = set()
    flood.add(added)
    outer: set[tuple[int, int]] = set()
    edge: set[tuple[int, int]] = set()
    first = (maxheight-1, 0)
    outer.add(first) # = edge + inner # (added[0]+1, added[1])
    edge.add(first) #(added[0]+1, added[1])
    #print("Edge", edge)
    debug = False#added == (-14, 0)
    #print("Debug", debug)
    canexpand = True
    while canexpand:
        canexpand = False
        if debug: print("Can expand", canexpand)
        newedge = set()
        for o in edge:
            for dir in orthodirs:
                candidate = (o[0]+dir[0], o[1]+dir[1])
                if debug: print("Candidate", candidate)
                if candidate in pile:
                    flood.add(candidate)
                elif candidate in outer:
                    pass
                elif candidate in edge:
                    pass
                else:
                    if 0 <= candidate[1] < chamberwidth and candidate[0]<maxheight: 
                        newedge.add(candidate)
                        canexpand = True
        outer = outer | newedge
        edge = newedge
    if debug: print("Flood", flood)
    return flood

cache: dict[tuple, tuple] = {} #rock phase, tick phase, height

culledheight: int = 0
heightoffset: int = 0
rockcount: int = 0
tick: int = 0
pile: set[tuple] = set([(0,c) for c in range(chamberwidth)])
keepers: set[tuple] = set()
targetrocks = 1000000000000 #2022
while rockcount < targetrocks:
    rockcount += 1
    #print("Rock #", rockcount)
    rockphase = (rockcount-1) % len(rocks)
    r = rocks[rockphase]
    rr, rc = culledheight+3+r.height, 2
    falling = True
    if rockcount % 100000 == 0: print("Rock #", rockcount, len(pile)) #print("Spawn at",rr,rc)
    while falling:

        #apply jets
        tickphase = tick%len(jets)
        dir = jets[tickphase]

        move = True
        for part in r.parts:
            newloc = (part[0]+rr, part[1]+rc+dir)
            if newloc[1] == -1 or newloc[1] == chamberwidth or newloc in pile:
                #no move
                move = False
        if move: rc += dir

        #try to fall
        for part in r.parts:
            newloc = (part[0]+rr-1, part[1]+rc)
            if newloc in pile:
                #no fall
                falling = False
        #add to pile
        if not falling:
            for part in r.parts:
                parttoadd = (part[0]+rr, part[1]+rc)
                pile.add(parttoadd)
            if culledheight < rr:
                culledheight = rr
            #if rockcount != 84:
            oldmin = reduce(lambda a,b: min(a, b[0]), pile, 9999999999999999)
            keepers = cull2(pile, (r.parts[0][0]+rr, r.parts[0][1]+rc), culledheight+2)
            minkeepers = reduce(lambda a,b: min(a, b[0]), keepers, 9999999999999999)
            shrinkfactor = minkeepers - oldmin
            #print("Mins", oldmin, minkeepers)
            pile = set([(r-minkeepers,c) for (r,c) in keepers]) #reset keepers to 0
            heightoffset = heightoffset + (minkeepers-oldmin)
            culledheight = culledheight - (minkeepers-oldmin)

            cachekey = ((rockphase, tickphase), tuple(pile))
            if cachekey in cache and True:
                #print("Been here:", "rockcount:", rockcount, cache[cachekey], "culledheight:", culledheight, "heightoffset:", heightoffset)
                heightoffsetdifference = heightoffset - cache[cachekey][3]
                rockcountdifference = rockcount - cache[cachekey][4]
                multipler = (targetrocks-cache[cachekey][4])//rockcountdifference
                multipler -= 1
                #print("Mid ff:", "heightoffsetdifference:", heightoffsetdifference, "rockcountdifference", rockcountdifference, "multipler", multipler)
                heightoffset = heightoffset + heightoffsetdifference*multipler
                rockcount = rockcount + rockcountdifference*multipler 
                #print("Complete ff:", "rockcount:", rockcount, cache[cachekey], "culledheight:", culledheight, "heightoffset:", heightoffset)
                cache.clear() #don't try caching again
                #exit(0)
                    
            else:
                cache[cachekey] = (rockphase, tickphase, culledheight, heightoffset, rockcount)
                #print("Not Been here", rockcount, cache[cachekey], culledheight, heightoffset)

            #print("Scales", heightoffset, height, height+heightoffset)
                #print("New height: ", height, rr)
            #else: print("No change: ", height, rr)
        else:
            #print("Falling")
            rr -= 1
        tick += 1
        if tick > len(jets):
            tick -= len(jets)

#print(pile)
print("Keepers", keepers)
if True:
    for r in range(culledheight+3, -1, -1):
        for c in range(chamberwidth):
            if (r,c) in keepers:
                print("X", end="")
            elif (r,c) in pile:
                print("#", end="")
            else:
                print(".", end="")
        print("|", r)

print(culledheight+heightoffset)

        
    
#answer = 3181

from dataclasses import dataclass

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


rocks = [Rock(parts=((0,0), (0,1), (0,2), (0,3)), width=4, height=1), 
         Rock(((1,0), (0,1), (1,1), (2,1), (1,2)), width=3, height=3),
         Rock(((2,0), (2,1), (0,2), (1,2), (2,2)), width=3, height=3),
         Rock(((0,0), (1,0), (2,0), (3,0)), width=1, height=4),
         Rock(((0,0), (0,1), (1,0), (1,1)), width=2, height=2)] #r,c
#print(jets)
#print(rocks)
#exit(0)

height: int = 0
rockcount: int = 0
tick: int = 0
pile: set[tuple] = set()
while rockcount < 2022:
    rockcount += 1
    print("Rock #", rockcount)
    r = rocks[(rockcount-1) % len(rocks)]
    rr, rc = -height-3-r.height, 2
    falling = True
    #print("Spawn at",rr,rc)
    while falling:

        #apply jets
        dir = jets[tick%len(jets)]

        move = True
        for part in r.parts:
            newloc = (part[0]+rr, part[1]+rc+dir)
            if newloc[1] == -1 or newloc[1] == chamberwidth or newloc in pile:
                #no move
                move = False
        if move: rc += dir

        #if dir == -1 and rc > 0:
        #    rc -= 1
        #    print("<")
        #elif dir == 1 and rc+r.width < chamberwidth:
        #    rc += 1
        #    print(">")

        #try to fall
        for part in r.parts:
            newloc = (part[0]+rr+1, part[1]+rc)
            if newloc[0] == 0 or newloc in pile:
                #no fall
                falling = False
        #add to pile
        if not falling:
            for part in r.parts:
                pile.add((part[0]+rr, part[1]+rc))
            if height < -rr:
                height = -rr
                #print("New height: ", height, rr)
            #else: print("No change: ", height, rr)
        else:
            #print("Falling")
            rr += 1
        tick += 1
        if tick > len(jets):
            tick -= len(jets)

print(pile)
for r in range(-height-3, 1, 1):
    for c in range(chamberwidth):
        print("#" if (r,c) in pile else ".", end="")
           
    print("|")


print(height)

        
    
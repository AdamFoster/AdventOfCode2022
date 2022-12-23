#answer = 4241

#filename = 'sample01.txt'
filename = 'input.txt'

dirs = ["N","S","W","E"]
scans = {"N":((-1,-1), (-1,0), (-1,1)),
         "S":((1,-1), (1,0), (1,1)),
         "W":((-1,-1), (0,-1), (1,-1)),
         "E":((-1,1), (0,1), (1,1))}
adjacents = [(-1,-1), (-1,0), (-1,1), (1,-1), (1,0), (1,1),(0,-1),(0,1)]
diroffset = {"N":(-1,0),"S":(1,0),"W":(0,-1),"E":(0,1)}
elves: set[tuple[int,int]] = set()
with open(filename, "r") as f:
    for r,line in enumerate(f):
        for c,char in enumerate(line.strip()):
            if char == "#":
                elves.add((r,c))

def printelves(es):
    minr,maxr,minc,maxc = 0,0,0,0
    for e in es:
        minr = min(minr, e[0])
        maxr = max(maxr, e[0])
        minc = min(minc, e[1])
        maxc = max(maxc, e[1])
    print("-"*(maxc-minc+3))
    for r in range(minr,maxr+1):
        for c in range(minc,maxc+1):
            if (r,c) in es:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print("-"*(maxc-minc+3))
def rectsize(es):
    minr,maxr,minc,maxc = 0,0,0,0
    for e in es:
        minr = min(minr, e[0])
        maxr = max(maxr, e[0])
        minc = min(minc, e[1])
        maxc = max(maxc, e[1])
    return (maxr-minr+1)*(maxc-minc+1)


for round in range(10):
    #plan
    #printelves(elves)
    plan: dict[tuple,object] = {}
    plannedspaces: dict[tuple,int] = {}
    for elf in elves:
        lonely = True
        for adj in adjacents:
            if (elf[0]+adj[0], elf[1]+adj[1]) in elves:
                lonely = False
        if lonely:
            plan[elf] = None
            continue

        for dir in dirs:
            canmove = True
            for scanoffset in scans[dir]:
                if (elf[0]+scanoffset[0], elf[1]+scanoffset[1]) in elves:
                    #no move
                    canmove = False
            if canmove:
                plan[elf] = dir
                target = (elf[0]+diroffset[dir][0],elf[1]+diroffset[dir][1])
                if target in plannedspaces:
                    plannedspaces[target] += 1
                else:
                    plannedspaces[target] = 1
                break
        if elf not in plan:
            plan[elf] = None

    #print("Plan =",plan)
    #print("Space=",plannedspaces)

    #move
    newelves:set[tuple[int,int]] = set() 
    for elf in elves:
        if plan[elf] is not None:
            target = (elf[0]+diroffset[plan[elf]][0],elf[1]+diroffset[plan[elf]][1])
            if plannedspaces[target] == 1:
                #make the move
                newelves.add(target)
            else:
                newelves.add(elf)
        else:
            newelves.add(elf)
    elves = newelves

    dir = dirs.pop(0)
    dirs.append(dir)
printelves(elves)

rs = rectsize(elves)
print(rs, len(elves), rs-len(elves))
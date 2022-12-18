#answer = 2106

#filename = 'sample01.txt'
filename = 'input.txt'

xs = [999,-1]
ys = [999,-1]
zs = [999,-1]
data = set()
with open(filename, "r") as f:
    for line in f:
        cube = tuple([int(x) for x in line.strip().split(",")])
        data.add(cube)
        xs = [min(xs[0], cube[0]), max(xs[1], cube[0])]
        ys = [min(ys[0], cube[1]), max(ys[1], cube[1])]
        zs = [min(zs[0], cube[2]), max(zs[1], cube[2])]

#print (data)

dirs = [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]

#print (dirs)

#flood outside
def floodfill(start=(xs[0]-1,ys[0]-1,zs[0]-1)) -> set():
    outer: set[tuple[int, int]] = set()
    edge: set[tuple[int, int]] = set()
    outer.add(start) # = edge + inner # (added[0]+1, added[1])
    edge.add(start) #(added[0]+1, added[1])
    #print("Edge", edge)

    debug = False#added == (-14, 0)
    #print("Debug", debug)
    canexpand = True
    while canexpand:
        canexpand = False
        if debug: print("Can expand", canexpand)
        newedge = set()
        for o in edge:
            for dir in dirs:
                candidate = (o[0]+dir[0], o[1]+dir[1], o[2]+dir[2])
                if debug: print("Candidate", candidate)
                if candidate in data:
                    pass
                elif candidate in outer:
                    pass
                elif candidate in edge:
                    pass
                else:
                    if xs[0]-1 <= candidate[0] <= xs[1]+1 and ys[0]-1 <= candidate[1] <= ys[1]+1 and zs[0]-1 <= candidate[2] <= zs[1]+1: 
                        newedge.add(candidate)
                        canexpand = True
            if debug: print("New edge", newedge)
        outer = outer | newedge
        edge = newedge
    if debug: print("Outer", outer)
    return outer


outer = floodfill()
#print("Outer", outer)
exposed = 0
for cube in data:
    for dir in dirs:
        if (cube[0]+dir[0], cube[1]+dir[1], cube[2]+dir[2]) in outer:
            exposed += 1            


print(exposed)
print(xs, ys, zs)
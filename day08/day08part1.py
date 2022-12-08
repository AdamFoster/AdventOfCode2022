#answer = 1703

from functools import reduce


#filename = 'sample01.txt'
filename = 'input.txt'

trees = []
visibletotal = 0

with open(filename, "r") as f:
    for line in f:
        trees.append([int(x) for x in line.strip()])

visibletop = []
visibleleft = []
visiblebottom = []
visibleright = []
for y in range(len(trees)):
    visibletop.append([])
    visibleleft.append([])
    visiblebottom.append([])
    visibleright.append([])

    for x in range(len(trees[0])):
        if y == 0:
            visibletop[y].append(True)
        elif max([trees[yv][x] for yv in range(y)])<trees[y][x]:
            visibletop[y].append(True)
        else:
            visibletop[y].append(False)

        if x == 0:
            visibleleft[y].append(True)
        elif max([trees[y][xv] for xv in range(x)])<trees[y][x]:
            visibleleft[y].append(True)
        else:
            visibleleft[y].append(False)

        if y == len(trees)-1:
            visiblebottom[y].append(True)
        elif max([trees[yv][x] for yv in range(y+1,len(trees))])<trees[y][x]:
            visiblebottom[y].append(True)
        else:
            visiblebottom[y].append(False)

        if x == len(trees[0])-1:
            visibleright[y].append(True)
        elif max([trees[y][xv] for xv in range(x+1,len(trees[0]))])<trees[y][x]:
            visibleright[y].append(True)
        else:
            visibleright[y].append(False)

        if visibletop[y][x] or visibleleft[y][x] or visiblebottom[y][x] or visibleright[y][x]:
            visibletotal += 1

print(trees)
print(visibletop)
print(visibleleft)
print(visiblebottom)
print(visibleright)

print(visibletotal)

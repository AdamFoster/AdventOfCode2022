#answer = 3564

#filename = 'sample01.txt'
filename = 'input.txt'

data = set()
with open(filename, "r") as f:
    for line in f:
        cube = tuple([int(x) for x in line.strip().split(",")])
        data.add(cube)


#print (data)

dirs = [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]

#print (dirs)

exposed = 0
for cube in data:
    for dir in dirs:
        if (cube[0]+dir[0], cube[1]+dir[1], cube[2]+dir[2]) in data:
            pass
        else:
            exposed += 1

print(exposed)

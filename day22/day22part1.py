#answer = 89224

import re


#filename = 'sample01.txt'
filename = 'input.txt'

map = []
instructions = []
LEFT = (0,-1)
RIGHT = (0,1)
UP = (-1,0)
DOWN = (1,0)
facing = (0,1) #r,c. Right, down +ve
location = (0,0)
facingtostring = {RIGHT:">", DOWN:"V", LEFT:"<", UP:"^"}
facingtovalue = {RIGHT:0, DOWN:1, LEFT:2, UP:3}
turnleft =  {(0,1):(-1,0), (-1,0):(0,-1), (0,-1):( 1,0), ( 1,0):(0,1)}
turnright = {(0,1):( 1,0), ( 1,0):(0,-1), (0,-1):(-1,0), (-1,0):(0,1)}
with open(filename, "r") as f:
    line = f.readline().rstrip()
    location = (1, line.index(".")+1)
    mapmax = 0
    while len(line) > 0:
        mapmax = max(mapmax,len(line))
        map.append(line)
        line = f.readline().rstrip()
    for i in range(len(map)):
        map[i] = " " + map[i].ljust(mapmax) + " "
    map.insert(0, " " * (mapmax+2))
    map.append(" " * (mapmax+2))
    line = f.readline().rstrip()
    while len(line) > 0:
        rx = "([0-9]+)([RL])?"
        m = re.match(rx, line)
        g = m.groups()
        instructions.append(int(g[0]))
        #print(g)
        if g[1] is not None:
            instructions.append(g[1])
            line = line[line.index(g[1])+1:]
        else:
            break
        #print(line)

print(instructions)
print(map)

def printmap():
    for i,r in enumerate(map):
        if i == 0:
            print("-"*len(r))
        print("|", end="")
        for j,c in enumerate(r):
            if i == location[0] and j == location[1]:
                print(facingtostring[facing], end="")
            else:
                print(map[i][j], end="")
        print("|")
        if i == len(map)-1:
            print("-"*len(r))

printmap()

for ind,i in enumerate(instructions):
    #print(i)
    #assert 
    if map[location[0]][location[1]] == " ":
        printmap()
        print("instruction", i, ind)
        assert False
    if i == "L":
        facing = turnleft[facing]
    elif i == "R":
        facing = turnright[facing]
    else:
        #print(i, type(i))
        for _ in range(i):
            nl = (location[0]+facing[0], location[1]+facing[1])
            #print("New location", location, "->", nl)
            if map[nl[0]][nl[1]] == ".":
                location = nl
                #print("Moved")
            elif map[nl[0]][nl[1]] == "#": #wall
                #print("Walled")
                pass
            else: #wrap
                #print("Wrapping")
                if facing == LEFT:
                    nl = (location[0], len(map[location[0]].rstrip())-1)
                    assert map[nl[0]][nl[1]] != " "
                    assert map[nl[0]][nl[1]+1] == " "
                elif facing == RIGHT:
                    nl = (location[0], len(map[location[0]]) - len(map[location[0]].lstrip()))
                    assert map[nl[0]][nl[1]] != " "
                    assert map[nl[0]][nl[1]-1] == " "
                elif facing == UP:
                    t = location[0]
                    while map[t][location[1]] != " ":
                        t += 1
                    nl = (t-1, location[1])
                    assert map[nl[0]][nl[1]] != " "
                    assert map[nl[0]+1][nl[1]] == " "
                elif facing == DOWN:
                    t = location[0]
                    while map[t][location[1]] != " ":
                        t -= 1
                    nl = (t+1, location[1])
                    assert map[nl[0]][nl[1]] != " "
                    assert map[nl[0]-1][nl[1]] == " "
                else:
                    assert False
                if map[nl[0]][nl[1]] == "#":
                    pass
                elif map[nl[0]][nl[1]] == " ":
                    assert False
                else:
                    location = nl
    #printmap()

printmap()
print(location[0], location[1], facing)
print(1000*(location[0]) + 4*(location[1]) + facingtovalue[facing])

#answer = 2120, 81312, 24401, 13381 # too low
# 81362, 45423 # wrong

import re


#filename = 'sample02.txt'
filename = 'input.txt'

#  01
#  2
# 34
# 5

instructions = []
LEFT = (0,-1)
RIGHT = (0,1)
UP = (-1,0)
DOWN = (1,0)
SS = 50 if filename == "input.txt" else 6
SSM1 = SS-1
facing = (0,1) #r,c. Right, down +ve
location = (0,0,0) #square,row,column
facingtostring = {RIGHT:">", DOWN:"V", LEFT:"<", UP:"^"}
facingtovalue = {RIGHT:0, DOWN:1, LEFT:2, UP:3}
squares = [[] for _ in range(6)]
turnleft =  {(0,1):(-1,0), (-1,0):(0,-1), (0,-1):( 1,0), ( 1,0):(0,1)}
turnright = {(0,1):( 1,0), ( 1,0):(0,-1), (0,-1):(-1,0), (-1,0):(0,1)}
squareoffsets = [(0,SS), (0,SS*2), (SS,SS), (SS*2,0), (SS*2,SS), (SS*3,0)]
with open(filename, "r") as f:
    for _ in range(SS):
        line = f.readline()
        squares[0].append(line[SS:SS*2])
        squares[1].append(line[SS:SS*2])
    for _ in range(SS):
        line = f.readline()
        squares[2].append(line[SS:SS*2])
    for _ in range(SS):
        line = f.readline()
        squares[3].append(line[0:SS])
        squares[4].append(line[SS:SS*2])
    for _ in range(SS):
        line = f.readline()
        squares[5].append(line[0:SS])
    
    f.readline()
    line = f.readline().rstrip()
    while len(line) > 0:
        rx = "([0-9]+)([RLX])?"
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

#print(instructions)
print(squares)

def printsquare():
    #print("-"*len(squares[0]))
    for y,r in enumerate(squares[location[0]]):
        for x,c in enumerate(r):
            if location == (location[0], y, x):
                print(facingtostring[facing], end="")
            else:
                print(squares[location[0]][y][x], end="")
        print()


#location=(5,1,1)
#facing=DOWN
#instructions=[1]

for ind,i in enumerate(instructions):
    #if ind>5: break
    DEBUG = False
    if DEBUG:
        print(facing, location)
        printsquare()
        print()
        print(ind, "=", i)
    assert 0 <= location[0] < 6
    assert 0 <= location[1] < SS
    assert 0 <= location[2] < SS
    assert squares[location[0]][location[1]][location[2]] == "."
    if i == "L":
        facing = turnleft[facing]
    elif i == "R":
        facing = turnright[facing]
    elif i == "X":
        pass
    else:
        #print(i, type(i), range(i))
        for _ in range(i):
            nl = (location[0], location[1]+facing[0], location[2]+facing[1])
            #print(location, "->", nl)
            #print("New location", location, "->", nl)
            if 0 <= nl[1] < SS and 0 <= nl[2] < SS:
                if squares[nl[0]][nl[1]][nl[2]] == ".":
                    location = nl
                    #print("Moved")
                elif squares[nl[0]][nl[1]][nl[2]] == "#": #wall
                    #print("Walled")
                    pass
            else: #other face
                nl = location
                nf = facing
                #  01
                #  2
                # 34
                # 5
                if location[0] == 0:
                    if facing == UP:
                        nl = (5, location[2], 0)
                        nf = RIGHT
                    elif facing == LEFT:
                        nl = (3, SSM1-location[1], 0)
                        nf = RIGHT
                    elif facing == DOWN:
                        nl = (2, 0, location[2])
                    elif facing == RIGHT:
                        nl = (1, location[1], 0)
                elif location[0] == 1:
                    if facing == UP:
                        nl = (5, SSM1, location[2])
                    elif facing == LEFT:
                        nl = (0, location[1], SSM1)
                    elif facing == DOWN:
                        nl = (2, location[2], SSM1)
                        nf = LEFT
                    elif facing == RIGHT:
                        nl = (4, SSM1-location[1], SSM1)
                        nf = LEFT
                elif location[0] == 2:
                    if facing == UP:
                        nl = (0, SSM1, location[2])
                    elif facing == LEFT:
                        nl = (3, 0, location[1])
                        nf = DOWN
                    elif facing == DOWN: 
                        nl = (4, 0, location[2])
                    elif facing == RIGHT:
                        nl = (1, SSM1, location[1])
                        nf = UP
                elif location[0] == 3:
                    if facing == UP:
                        nl = (2, location[2], 0)
                        nf = RIGHT
                    elif facing == LEFT:
                        nl = (0, SSM1-location[1], 0)
                        nf = RIGHT
                    elif facing == DOWN:
                        nl = (5, 0, location[2])
                    elif facing == RIGHT:
                        nl = (4, location[1], 0)
                elif location[0] == 4:
                    if facing == UP:
                        nl = (2, SSM1, location[2])
                    elif facing == LEFT:
                        nl = (3, location[1], SSM1)
                    elif facing == DOWN:
                        nl = (5, location[2], SSM1)
                        nf = LEFT
                    elif facing == RIGHT:
                        nl = (1, SSM1-location[1], SSM1)
                        nf = LEFT
                elif location[0] == 5:
                    if facing == UP:
                        nl = (3, SSM1, location[2])
                    elif facing == LEFT:
                        nl = (0, 0, location[1])
                        nf = DOWN
                    elif facing == DOWN: #todo
                        nl = (1, 0, location[2])
                        nf = DOWN
                    elif facing == RIGHT: #todo
                        nl = (4, SSM1, location[1])
                        nf = UP
                else:
                    assert False
                if squares[nl[0]][nl[1]][nl[2]] == ".":
                    print(facingtostring[facing], location[0], "to", facingtostring[nf], nl[0])
                    print(location, "to", nl)
                    location = nl
                    facing = nf
                    #print("New square", location, facing)
                    #exit(0)
                elif squares[nl[0]][nl[1]][nl[2]] == "#":
                    print("Walled cube")
                    pass
                else:
                    assert False

print(facing, location)
printsquare()
realrow = location[1] + squareoffsets[location[0]][0] + 1
realcol = location[2] + squareoffsets[location[0]][1] + 1
print(realrow, realcol)
print(1000*realrow + 4*realcol + facingtovalue[facing])

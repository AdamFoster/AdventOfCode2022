#answer = 1016

#filename = 'sample01.txt'
filename = 'input.txt'

maxy = 0
rocks=set()
with open(filename, "r") as f:
    for line in f:
        parts = line.strip().split(" -> ")
        for i in range(1,len(parts)):
            s = [int(x) for x in parts[i-1].split(",")]
            e = [int(x) for x in parts[i].split(",")]

            if s[0] == e[0]:
                for y in range(min(s[1], e[1]), max(s[1], e[1])):
                    rocks.add((s[0], y))
            else:
                for x in range(min(s[0], e[0]), max(s[0], e[0])):
                    rocks.add((x, s[1]))
            
            rocks.add((s[0], s[1]))
            rocks.add((e[0], e[1]))
            if s[1] > maxy:
                maxy = s[1]
            if e[1] > maxy:
                maxy = e[1]

#sand = set()
done = False
count = 0
while not done:
    s = (500, 0)
    falling = True
    while falling:
        if s[1] > maxy:
            done = True
            falling = False
        else:
            if (s[0], s[1]+1) not in rocks:
                s = (s[0], s[1]+1)
            elif (s[0]-1, s[1]+1) not in rocks:
                s = (s[0]-1, s[1]+1)
            elif (s[0]+1, s[1]+1) not in rocks:
                s = (s[0]+1, s[1]+1)
            else:
                falling = False
                rocks.add(s)
                count += 1
print(rocks)

print(count)

#for y in range(0, 10):
#    for x in range(494, 504):
#        if (x,y) in rocks:
#            print("#", end="")
#        else:
#            print(".", end="")
#    print()
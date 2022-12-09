#answer = 2487

#filename = 'sample01.txt'
filename = 'input.txt'

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def tailtostring(tail): f"{tail[0]},{tail[1]}"

knots = [[0,0] for t in range(10)]
dirs = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}
tailsites = set([tailtostring(knots[len(knots)-1])])

with open(filename, "r") as f:
    for line in f:
        dir, stepss = line.strip().split()
        steps = int(stepss)
        for s in range(steps):
            knots[0][0] += dirs[dir][0]
            knots[0][1] += dirs[dir][1]

            for k in range(1, len(knots)):
                if abs(knots[k-1][0] - knots[k][0]) <=1 and abs(knots[k-1][1] - knots[k][1]) <= 1:
                    pass #nomove
                    #print("NOMOVE", head, tail, tailsites)
                else:
                    m0 = clamp(knots[k-1][0] - knots[k][0], -1, 1)
                    m1 = clamp(knots[k-1][1] - knots[k][1], -1, 1)
                    knots[k][0] += m0
                    knots[k][1] += m1
                    if k == len(knots)-1: 
                        tailsites.add(f"{knots[k][0]},{knots[k][1]}")
                    #print(head, tail, tailsites)

print(tailsites)
print(len(tailsites))

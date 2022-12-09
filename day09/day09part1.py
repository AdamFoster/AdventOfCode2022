#answer = 6081

#filename = 'sample01.txt'
filename = 'input.txt'

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

head = [0,4]
tail = [0,4]
dirs = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}
tailsites = set([f"{tail[0]},{tail[1]}"])
with open(filename, "r") as f:
    for line in f:
        dir, stepss = line.strip().split()
        steps = int(stepss)
        for s in range(steps):
            head[0] += dirs[dir][0]
            head[1] += dirs[dir][1]
            if abs(head[0] - tail[0]) <=1 and abs(head[1] - tail[1]) <= 1:
                pass #nomove
                #print("NOMOVE", head, tail, tailsites)
            else:
                m0 = clamp(head[0] - tail[0], -1, 1)
                m1 = clamp(head[1] - tail[1], -1, 1)
                tail[0] += m0
                tail[1] += m1
                tailsites.add(f"{tail[0]},{tail[1]}")
                #print(head, tail, tailsites)

print(tailsites)
print(len(tailsites))

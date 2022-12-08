#answer = 496650

from functools import reduce


#filename = 'sample01.txt'
filename = 'input.txt'

trees = []
visibletotal = 0

with open(filename, "r") as f:
    for line in f:
        trees.append([int(x) for x in line.strip()])

scenics = [[0 for x in trees[0]] for y in trees]

for y in range(1, len(trees)-1):
    for x in range(1, len(trees[0])-1):
        scores = [1,1,1,1]
        i = y-1
        while i>-1 and trees[y][x] > trees[i][x]:
            scores[0] += 1
            i -= 1
        if i == -1:
            scores[0] -= 1
        i = y+1
        while i<len(trees) and trees[y][x] > trees[i][x]:
            scores[1] += 1
            i += 1
        if i == len(trees):
            scores[1] -= 1        

        i = x-1
        while i>-1 and trees[y][x] > trees[y][i]:
            scores[2] += 1
            i -= 1
        if i == -1:
            scores[2] -= 1        
        i = x+1
        while i<len(trees[0]) and trees[y][x] > trees[y][i]:
            scores[3] += 1
            i += 1
        if i == len(trees[0]):
            scores[3] -= 1
        
        #print (scores)
        scenics[y][x] = reduce(lambda a,b: a*b, scores)

print(scenics)

print(max([max(s) for s in scenics]))

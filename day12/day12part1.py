#answer = 350

from collections import defaultdict


filename = 'sample01.txt'
filename = 'input.txt'

heights = []
start = (-1, -1) #row,col
end = (-1, -1)
with open(filename, "r") as f:
    for line in f:
        if "S" in line:
            start = (len(heights), line.index("S"))
        if "E" in line:
            end = (len(heights), line.index("E")) 
        heights.append([0 if a == "S" else 25 if a == "E" else ord(a)-ord('a') for a in line.strip()])

def h(current, end) -> int:
    return abs(current[0]-end[0]) + abs(current[1]-end[1])

print(heights)
print(start, end)

# From wikipedia https://en.wikipedia.org/wiki/A*_search_algorithm
def reconstruct_path(cameFrom: dict, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path

# A* finds a path from start to goal. 
# h is the heuristic function. h(n) estimates the cost to reach goal from node n.
def A_Star(start, goal):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet = {start}

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    cameFrom = dict()

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = defaultdict(lambda: 999999999) # map with default value of Infinity
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore = defaultdict(lambda: 999999999) # map with default value of Infinity
    fScore[start] = h(start, goal)

    while len(openSet) > 0:
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        ss = sorted(openSet, key=lambda k: fScore[k])
        print(ss)
        current = ss[0] #:= the node in openSet having the lowest fScore[] value
        if current == goal:
            return reconstruct_path(cameFrom, current)

        openSet.remove(current)
        for dir in [(-1,0), (1,0), (0,-1), (0,1)]:
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            neighbor = (current[0]+dir[0], current[1]+dir[1])
            if neighbor[0] < 0 or neighbor[0] == len(heights):
                continue
            if neighbor[1] < 0 or neighbor[1] == len(heights[0]):
                continue
            if heights[neighbor[0]][neighbor[1]] - heights[current[0]][current[1]] > 1:
                continue
            tentative_gScore = gScore[current] + 1 #d(current, neighbor)
            if tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + h(neighbor, goal)
                if neighbor not in openSet:
                    openSet.add(neighbor)

    # Open set is empty but goal was never reached
    assert False #return failure

path = A_Star(start, end)
print(path)
print(len(path)-1)
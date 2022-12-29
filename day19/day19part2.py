#answer = 1480 (too low)

from dataclasses import dataclass, field
from copy import deepcopy
from functools import reduce
from queue import PriorityQueue

#filename = 'sample01.txt'
filename = 'input.txt'

MAXTIME = 24

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"
TYPES = [ORE, CLAY, OBSIDIAN, GEODE]
TYPES_R = [GEODE, OBSIDIAN, CLAY, ORE]

@dataclass
class Robot:
    minetype: str
    costs: dict[str, int] #ore -> amount

@dataclass
class Blueprint:
    index: int
    robots: dict[str, Robot]
    maxes: dict[str, bool]

@dataclass
class State:
    resources: dict[str, int]  #type -> number
    robots: dict[str, int]  #type -> number
    timeleft: int
    couldhavebuilt: dict[str, bool] #robottype -> bool

    def canafford(self, robot: Robot):
        for costtype,costvalue in robot.costs.items():
            if self.resources[costtype] < costvalue:
                return False
        return True
    
    def amountcanmine(self, robot: Robot):
        return {t:self.robots[t]*self.timeleft for t in self.robots}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)): return NotImplemented
        if self.timeleft != other.timeleft:
            return False
        for t in TYPES:
            if self.resources[t] != other.resources[t]:
                return False
            if self.robots[t] != other.robots[t]:
                return False
            if self.couldhavebuilt[t] != other.couldhavebuilt[t]:
                return False
        return True

    def __hash__(self) -> int:
        return hash((self.timeleft, tuple([self.resources[t] for t in TYPES]), tuple([self.robots[t] for t in TYPES]), tuple([self.couldhavebuilt[t] for t in TYPES])))

    def __lt__(self, other):
        if self.timeleft != other.timeleft:
            return self.timeleft < other.timeleft
        return tuple([(self.robots[t], self.resources[t]) for t in TYPES_R]) < tuple([(other.robots[t], other.resources[t]) for t in TYPES_R])

blueprints = []
with open(filename, "r") as f:
    for i,line in enumerate(f):
        b = Blueprint(index=i, robots={}, maxes={t:0 for t in TYPES})
        for robotstr in line.strip().split(":")[1].strip()[:-1].split("."):
            #print("*",robotstr,"*")
            roboparts = robotstr.strip().split(" ")
            t = roboparts[1].strip()
            costs = {}
            costs[roboparts[5].strip()] = int(roboparts[4].strip())
            
            if len(roboparts) > 6:
                costs[roboparts[8].strip()] = int(roboparts[7].strip())
            b.robots[t] = Robot(minetype=t, costs=costs)
        #maxes = {t:max([b.robots[r].costs[t] for r in b.robots if t in b.robots[r].costs]) for t in TYPES}
        for rid,r in b.robots.items():
            for cid,c in r.costs.items():
                b.maxes[cid] = max(b.maxes[cid], c)
        
        blueprints.append(b)

print(blueprints)


def statevalue(s: State) -> int:
    v = s.resources[GEODE]
    v += s.robots[GEODE] * s.timeleft
    return v

def beststatevalue(s: State) -> int:
    v = statevalue(s)
    v += (s.timeleft * (s.timeleft-1) // 2)
    return v

def getqueuekey(state: State):
    return ((state.timeleft, state.resources[GEODE]), state.robots[GEODE], state.robots[OBSIDIAN])


def search(bp: Blueprint):
    maxgeodes = 0
    #queue: list[State] = []
    pqueue = PriorityQueue()
    #explored: list[set[State]] = [set() for _ in range(MAXTIME)]
    explored: set[State] = set()

    robots = {t: 0 for t in TYPES}
    resources = {t: 0 for t in TYPES}
    robots["ore"] = 1
    root = State(robots=robots, resources=resources, timeleft=MAXTIME, couldhavebuilt={t:False for t in TYPES})
    #queue.append(root)
    pqueue.put((getqueuekey(root), root))

    explored.add(root)
    while not pqueue.empty():
        #print("DFS", dfs)
        
        #state = queue.pop(0)
        _,state = pqueue.get()
        #print("Expl",len(explored),"Q",pqueue.qsize(),"State:",state)
        currentvalue = statevalue(state)
        if currentvalue > maxgeodes:
            maxgeodes = currentvalue
            print("Max improved", maxgeodes)
            #print(state)
            #print("Best estimate", beststatevalue(state))

        if state.timeleft == 1:
            #print("At the end")
            continue

        if maxgeodes >= beststatevalue(state):
            continue

        saturated = True
        for geoderobotcosttype,geoderobotcostvalue in bp.robots[GEODE].costs.items():
            if state.robots[geoderobotcosttype] < geoderobotcostvalue:
                #can make more robots to make more geode robots
                saturated = False
        if saturated:
            #no need to make more
            maxgeodes = max(maxgeodes, beststatevalue(state))
            print("Saturated",state,"=",beststatevalue(state),"vs", maxgeodes)
            continue

        for robottype,robot in bp.robots.items():
            if state.canafford(robot) and ((bp.maxes[robottype] > state.robots[robottype] and state.couldhavebuilt[robottype] is False) or robottype == GEODE):
                #if robottype == GEODE:
                #    print("Exit from here")
                #    exit(0)
                if state.timeleft < 3 and (robottype == ORE or robottype == CLAY):
                    continue
                #make a robot
                s: State = deepcopy(state)
                s.timeleft -= 1
                s.robots[robottype] += 1
                s.couldhavebuilt = {t:False for t in TYPES}
                for costtype,costvalue in robot.costs.items():
                    s.resources[costtype] -= costvalue
                for srt,src in state.robots.items():
                    s.resources[srt] += src
                if s not in explored:
                    explored.add(s)
                    #queue.append(s)
                    pqueue.put((getqueuekey(s), s))
        
        #try also not making a robot
        couldhavebuilt = {t:(state.canafford(bp.robots[t]) or state.couldhavebuilt[t]) for t in TYPES}
        if True: # not reduce(lambda a,b: a and b, couldhavebuilt.values()):
            s: State = deepcopy(state)
            s.timeleft -= 1
            s.couldhavebuilt = couldhavebuilt
            for srt,src in state.robots.items():
                s.resources[srt] += src
            if s not in explored:
                explored.add(s)
                pqueue.put((getqueuekey(s), s))
            #else:
                #print("Already explored", s)
    return maxgeodes


quality = 0
for i,bp in enumerate(blueprints):
    #if i>3: break
    v = search(bp=bp)
    quality += (i+1)*v
    print (i+1,v,quality)


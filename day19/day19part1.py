#answer = 1480

from dataclasses import dataclass, field
from copy import deepcopy

#filename = 'sample01.txt'
filename = 'input.txt'

TYPES = ["ore", "clay", "obsidian", "geode"]
TYPES_R = ["geode", "obsidian", "clay", "ore"]

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
        return True

    def __hash__(self) -> int:
        return hash((self.timeleft, tuple([self.resources[t] for t in TYPES]), tuple([self.robots[t] for t in TYPES])))

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

MAXTIME = 24

def prunekey(resources):
    return tuple([resources[t] for t in TYPES])

def bestgeodes(currentgeodes, currentgeodesrobots, timeleft):
    return currentgeodes + currentgeodesrobots * timeleft + timeleft*(timeleft+1)//2

def geodes_collected(blueprint: Blueprint, state: State, cache: dict, prune: dict):
    #if state == None:
    #    assert False
    #if dict != None:
    #    assert False

    #print("STATE", state, len(cache))
    if state.timeleft == 0:
        #exit(0)
        return 0
    if state in cache:
        #print("HIT")
        return cache[state]
    if prunekey(state.resources) in prune:
        previous = prune[prunekey(state.resources)]
        prevbetter = True
        if previous[0] <= state.timeleft:
            prevbetter = False
        else:
            for t in TYPES:
                if previous[1][t] <= state.robots[t]:
                    prevbetter = False
        if prevbetter:
            #print("PRUNE")
            return 0
    maxsubgeodes = 0

    #for t in TYPES[:-1]: # reject if too many resources
    #    if state.resources[t] > 2*(sum([r.costs[t] for _,r in blueprint.robots.items() if t in r.costs])):
    #        #print("PRUNE 3")
    #        return 0

    couldmakeall = True
    for t in TYPES_R: #make robot
        if state.canafford(blueprint.robots[t]) and (t == "geode" or blueprint.maxes[t] > state.robots[t]):
            s = deepcopy(state)
            for t2 in TYPES:
                s.resources[t2] += s.robots[t2]
            for costtype,costamount in blueprint.robots[t].costs.items():
                #print("R1", s.resources, blueprint)
                s.resources[costtype] -= costamount
                #print("R2", s.resources)
            s.robots[t] += 1
            s.timeleft -= 1
            #print("NEW STATE", s)
            subgeodes = geodes_collected(blueprint, s, cache, prune)
            maxsubgeodes = max(maxsubgeodes, subgeodes)
        else:
            for costtype,costamount in blueprint.robots[t].costs.items():
                if state.resources[costtype] < costamount and state.robots[costtype] > 0:
                    couldmakeall = False

    if not couldmakeall:
        s = deepcopy(state) # no make robot, just reduce time
        s.timeleft -= 1
        for t in TYPES:
            s.resources[t] += s.robots[t]
        maxsubgeodes = max(maxsubgeodes, geodes_collected(blueprint, s, cache, prune))
    #else: print("PRUNE 2")
    geodes = maxsubgeodes + state.robots["geode"]
    cache[state] = geodes
    #print(cache[state])
    prune[prunekey(state.resources)] = (state.timeleft, state.robots)
    return geodes #amount mined in subticks + this tick

def geodes_collected_starter(blueprint: Blueprint):
    cache = {}
    robots = {t: 0 for t in TYPES}
    resources = {t: 0 for t in TYPES}
    robots["ore"] = 1
    state = State(robots=robots, resources=resources, timeleft=MAXTIME)
    return geodes_collected(blueprint=blueprint, state=state, cache=cache, prune={})

quality = 0
for i,bp in enumerate(blueprints):
    v = geodes_collected_starter(blueprint=bp)
    quality += (i+1)*v
    print (i,v,quality)


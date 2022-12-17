#answer = 1638

from dataclasses import dataclass, field
from copy import deepcopy


#filename = 'sample01.txt'
filename = 'input.txt'
maxtime = 30


@dataclass
class Valve:
    id: str = field(default="")
    rate: int = field(default=0)
    connections: list[str] = field(default=lambda: [])
    #maxamount: int = field(default=0)
    amount: int = field(default=0)
    ison: bool = field(default=False)
    timeon: int = field(default=0)

valvesmaster: dict[str, Valve] = {}
alldistances: dict[str, dict[str, int]] = {}


@dataclass()
class State:
    time: int = field(default=0)
    location: str = field(default="AA")
    valves: dict[str, Valve] = field(default=lambda: {})
    comefrom: str = field(default="AA")

    def __hash__(self):
        return hash((self.location, tuple([(v.id, v.amount) for v in self.valves.values()]))) #self.time, 

    def __eq__(self, other): #assumes same ids
        if not isinstance(other, type(self)): return NotImplemented
        #if self.time != other.time:
        #    return False
        if self.location != other.location:
            return False
        else:
            for vid in self.valves:
                if self.valves[vid].amount != other.valves[vid].amount:
                    return False
        return True


with open(filename, "r") as f:
    for line in f:
        line = line.strip().split()
        id = line[1]
        rate = int(line[4].split("=")[1][:-1])
        connections = [x[:-1] for x in line[9:-1]]
        connections.append(line[-1])
        v = Valve(id, rate, connections)
        #print(v)
        valvesmaster[id] = v


def distances(source:str) -> dict[str,int]:
    dist = {vid: 9999999 for vid in valvesmaster}
    prev = {vid: None for vid in valvesmaster}
    Q = [vid for vid in valvesmaster]
    dist[source] = 0

    while len(Q) > 0:
        Q.sort(key=lambda a: dist[a])
        u = Q.pop(0)

        for v in valvesmaster[u].connections:
            if v in Q:
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    return dist


#print(alldistances)
#exit(0)


def search(dfs=True):
    max = 0
    queue: list[State] = []
    explored: list[set[State]] = [set() for _ in range(maxtime+1)]
    root = State(time=maxtime, location="AA", valves=deepcopy(valvesmaster))
    queue.append(root)
    explored[root.time].add(root)
    while len(queue) > 0:
        #print("DFS", dfs)
        state = queue.pop() if dfs else queue.pop(0)
        currentvalue = calc(state)
        if currentvalue > max:
            max = currentvalue
            print("Max improved", max)
            print(state)
            print("Best estimate", best(state))

        if state.time == 1:
            #print("At the end")
            continue

        if max >= best(state):
            continue

        #descend into on/off
        if not state.valves[state.location].ison and state.valves[state.location].rate > 0:
            s: State = deepcopy(state)
            s.time -= 1
            s.valves[state.location].ison = True
            s.valves[state.location].timeon = maxtime - s.time
            s.valves[state.location].amount = s.time * s.valves[state.location].rate
            s.comefrom = ""
            if not hasexplored(s, explored): #s not in explored[s.time]:
                explored[s.time].add(s)
                queue.append(s)
                #print("Adding valve on/off")

        #try greedy
        testconnections = sorted(alldistances[state.location].keys(), key=lambda k: state.valves[k].rate * (state.time-alldistances[state.location][k]) * (1 if state.valves[k].ison else 0))
        if not dfs:
            testconnections.reverse()
        
        for connection in state.valves[state.location].connections: #testconnections: #alldistances[state.location]:
            if connection == state.comefrom:
                continue
            s: State = deepcopy(state)
            s.time -= 1 #alldistances[state.location][connection]
            if s.time < 2:
                continue
            s.comefrom = state.location
            s.location = connection
            if not hasexplored(s, explored): # not in explored[s.time]:
                explored[s.time].add(s)
                queue.append(s)
                #print("Exploring", connection)

def hasexplored(state: State, explored: list[set[State]]) -> bool:
    for t in range(state.time, maxtime):
        if state in explored[t]:
            return True
    return False

def calc(state: State) -> int:
    total = 0
    for valve in state.valves.values():
        total += valve.amount
    return total

def best(state: State) -> int:
    total = 0
    for valve in state.valves.values():
        if valve.ison:
            total += valve.amount
        else:
            if valve.rate > 0:
                timeleftaftermove = state.time - 1 - alldistances[state.location][valve.id]
                if timeleftaftermove > 0:
                    total += valve.rate * timeleftaftermove
                #total += valve.rate*state.time
                #s.valves[state.location].amount = s.time * s.valves[state.location].rate
    return total


for vid in valvesmaster:
    alldistances[vid] = {k:d for (k,d) in distances(vid).items() if valvesmaster[k].rate>0}
#for vid in valvesmaster:
#    valvesmaster[vid].connections = [] #just to make sure we don't use these accidentally
#valvesmaster = {k:v for (k,v) in valvesmaster.items() if (v.rate != 0 or k == "AA")}

print(alldistances)
#exit(0)
search(dfs=True)

#root = State(time=30, location="AA", valves=deepcopy(valvesmaster))
#print(root)
#rc = deepcopy(root)
#rc.valves["AA"].amount = 500
#print(root)
#print(rc)
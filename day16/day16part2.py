#answer = 1638

from dataclasses import dataclass, field
from copy import deepcopy


#filename = 'sample01.txt'
filename = 'input.txt'
maxtime = 26


@dataclass
class Valve:
    id: str = field(default="")
    rate: int = field(default=0)
    connections: list[str] = field(default=lambda: [])

valvesmaster: dict[str, Valve] = {}
alldistances: dict[str, dict[str, int]] = {}


@dataclass()
class State:
    time: int = field(default=0)
    locations: tuple = field(default=())
    valveamounts: dict[str, int] = field(default=lambda: {})
    comefroms: tuple = field(default=("AA", "AA"))

    def __hash__(self):
        return hash((self.locations[0], self.locations[1], tuple([(vid, self.valveamounts[vid]) for vid in self.valveamounts]))) #self.time, 

    def __eq__(self, other): #assumes same ids
        if not isinstance(other, type(self)): return NotImplemented
        #if self.time != other.time:
        #    return False
        if self.locations[0] != other.locations[0]:
            return False
        if self.locations[1] != other.locations[1]:
            return False
        else:
            for vid in self.valveamounts:
                if self.valveamounts[vid] != other.valveamounts[vid]:
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
        #connections.sort(key=lambda c: va)
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

def move1(state: State) -> list[State]: #time has already been decremented by person
    states: list[State] = []

    if state.valveamounts[state.locations[1]] == 0 and valvesmaster[state.locations[1]].rate > 0:
        s: State = deepcopy(state)
        s.valveamounts[state.locations[1]] =  s.time * valvesmaster[state.locations[1]].rate
        s.comefroms = (s.comefroms[0], "")
        if s.locations[1] < s.locations[0]:
            s.locations = (s.locations[1], s.locations[0])
            s.comefroms = (s.comefroms[1], s.comefroms[0])
            
        states.append(s)
            
    for connection in valvesmaster[state.locations[1]].connections:
        if connection == state.comefroms[1]:
            continue
        s: State = deepcopy(state)
        s.comefroms = (s.comefroms[0], s.locations[1])
        s.locations = (s.locations[0], connection)
        if s.locations[1] < s.locations[0]:
            s.locations = (s.locations[1], s.locations[0])
            s.comefroms = (s.comefroms[1], s.comefroms[0])
        states.append(s)

    return states

def search(dfs=True):
    max = 0
    queue: list[State] = []
    explored: list[set[State]] = [set() for _ in range(maxtime+1)]
    root = State(time=maxtime, locations=("AA", "AA"), valveamounts={vid:0 for vid in valvesmaster})
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
        if state.valveamounts[state.locations[0]] == 0 and valvesmaster[state.locations[0]].rate > 0:
            s: State = deepcopy(state)
            s.time -= 1
            s.valveamounts[state.locations[0]] = s.time * valvesmaster[state.locations[0]].rate
            s.comefroms = ("", s.comefroms[1])
            emoves = move1(s)
            for m in emoves:
                if not hasexplored(m, explored): 
                    explored[m.time].add(m)
                    queue.append(m)
        
        for connection in valvesmaster[state.locations[0]].connections:
            if connection == state.comefroms[0]:
                continue
            s: State = deepcopy(state)
            s.time -= 1 #alldistances[state.location][connection]
            if s.time < 2:
                continue
            s.comefroms = (state.locations[0], s.comefroms[1])
            s.locations = (connection, state.locations[1])
            emoves = move1(s)
            for m in emoves:
                if not hasexplored(m, explored): 
                    explored[m.time].add(m)
                    queue.append(m)

def hasexplored(state: State, explored: list[set[State]]) -> bool:
    for t in range(state.time, maxtime):
        if state in explored[t]:
            return True
    return False

def calc(state: State) -> int:
    total: int = 0
    for valveamount in state.valveamounts.values():
        total += valveamount
    return total

def best(state: State) -> int:
    total: int = 0
    for vid in state.valveamounts.keys():
        if state.valveamounts[vid] > 0:
            total += state.valveamounts[vid]
        else:
            if valvesmaster[vid].rate > 0:
                timeleftaftermove = state.time - 1 - min(alldistances[state.locations[0]][vid], alldistances[state.locations[1]][vid])
                if timeleftaftermove > 0:
                    total += valvesmaster[vid].rate * timeleftaftermove
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
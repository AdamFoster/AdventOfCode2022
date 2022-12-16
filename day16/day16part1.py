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

valvesmaster: dict[str, Valve] = {}

@dataclass()
class State:
    time: int = field(default=0)
    location: str = field(default="AA")
    valves: dict[str, Valve] = field(default=lambda: {})
    comefrom: str = field(default="AA")

    def __hash__(self):
        return hash((self.location, tuple([(v.id, v.ison, v.amount) for v in self.valves.values()]))) #self.time, 

    def __eq__(self, other): #assumes same ids
        if not isinstance(other, type(self)): return NotImplemented
        #if self.time != other.time:
        #    return False
        if self.location != other.location:
            return False
        else:
            for vid in self.valves:
                if self.valves[vid].ison != other.valves[vid].ison:
                    return False
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
        print(v)
        valvesmaster[id] = v


def bfs():
    max = 0
    queue: list[State] = []
    explored: list[set[State]] = [set() for _ in range(maxtime+1)]
    root = State(time=maxtime, location="AA", valves=deepcopy(valvesmaster))
    queue.append(root)
    explored[root.time].add(root)
    while len(queue) > 0:
        state = queue.pop(0)
        currentvalue = calc(state)
        if currentvalue > max:
            max = currentvalue
            print("Max improved", max)
            print(state)

        if state.time < 0:
            #print("At the end")
            continue

        #allon = True
        #for v in state.valves.values():
        #    if v.rate > 0 and not v.ison:
        #        allon = False
        #if allon:
        #    continue

        if currentvalue >= best(state):
            continue

        #descend into on/off
        if not state.valves[state.location].ison and state.valves[state.location].rate > 0:
            s: State = deepcopy(state)
            s.time -= 1
            s.valves[state.location].ison = True
            s.valves[state.location].amount = s.time * s.valves[state.location].rate
            if not hasexplored(s, explored): #s not in explored[s.time]:
                explored[s.time].add(s)
                queue.append(s)
                #print("Adding valve on/off")
        for connection in state.valves[state.location].connections:
            #if state.location == "CC" and state.time == 26:
                #print ("Moving", connection, state)
            s: State = deepcopy(state)
            s.time -= 1
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
            total += valve.rate*state.time
    return total

def calcmaxammount(time: int, location: str, valves: dict[str, Valve]):
    if valves[location].ison:
        max = 0
        for c in valves[location].connections:
            candidate = calcmaxammount(time=time-1, location=c, valves=deepcopy(valves))
            if c > max:
                max = c
        return max
    else:
        valves[location].ison = True
        valves[location].amount = time * valves[location].rate
        return calcmaxammount(time=time-1, location=location, valves=deepcopy(valves)) + valves[location].amount

#print(calcmaxammount(time=maxtime, location="AA", valves=valvesmaster))
bfs()
#root = State(time=30, location="AA", valves=deepcopy(valvesmaster))
#print(root)
#rc = deepcopy(root)
#rc.valves["AA"].amount = 500
#print(root)
#print(rc)
#answer = 5962

from dataclasses import dataclass
from copy import deepcopy


#filename = 'sample01.txt'
filename = 'input.txt'

@dataclass()
class ACNumber:
    value: int
    originalposition: int
    currentposition: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)): return NotImplemented
        return self.value == other.value and self.originalposition == other.originalposition and self.currentposition == other.currentposition

    def __hash__(self) -> int:
        return hash((self.value, self.originalposition, self.currentposition))

ZERO = None

data: list[ACNumber] = []
with open(filename, "r") as f:
    for i,line in enumerate(f):
        n = int(line.strip())
        data.append(ACNumber(n, i, i))
        if n == 0:
            ZERO = data[-1]

#print(data)
SIZE = len(data)
newdata: list[ACNumber] = [acn for acn in data]
#print(newdata)

def printlist(acnlist: list[ACNumber]):
    print(", ".join([str(acn.value) for acn in acnlist]))

#print(newdata)
#printlist(newdata)
for i,acn in enumerate(data):
    loc = newdata.index(acn)
    newloc = loc + acn.value
    if newloc >= SIZE: #+ve wrap
        newloc = (newloc + newloc//SIZE) % SIZE
    elif newloc < 0: #-ve wrap
        newloc = (newloc + newloc//SIZE + 2*SIZE) % SIZE
    if newloc == 0:
        newloc = SIZE-1
    #print(newloc)
    newdata.pop(loc)
    newdata.insert(newloc, acn)
    #printlist(newdata)

#for acn in newdata:
#    print(acn.value)

#print(newdata)
offset = newdata.index(ZERO)
items = [newdata[(i+offset)%SIZE].value for i in [1000, 2000, 3000]]
print(items)
total = sum(items)
print(total)

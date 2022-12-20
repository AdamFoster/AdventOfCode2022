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
KEY = 811589153

data: list[ACNumber] = []
with open(filename, "r") as f:
    for i,line in enumerate(f):
        n = int(line.strip()) * KEY
        data.append(ACNumber(n, i, i))
        if n == 0:
            ZERO = data[-1]

#print(data)
SIZE = len(data)
SM1 = SIZE-1
newdata: list[ACNumber] = [acn for acn in data]
#print(newdata)

def printlist(acnlist: list[ACNumber]):
    print(", ".join([str(acn.value) for acn in acnlist]))

#print(newdata)
printlist(newdata)
for round in range(10):
    for i,acn in enumerate(data):
        loc = newdata.index(acn)
        newdata.pop(loc)
        newloc = loc + acn.value
        newloc %= SM1
        if newloc <= 0: newloc += SM1
        #print(newloc)
        newdata.insert(newloc, acn)
        #printlist(newdata)
    printlist(newdata)
    #break

#for acn in newdata:
#    print(acn.value)

#print(newdata)
offset = newdata.index(ZERO)
items = [newdata[(i+offset)%SIZE].value for i in [1000, 2000, 3000]]
print(items)
total = sum(items)
print(total)

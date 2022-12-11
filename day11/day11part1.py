#answer = 112221

from dataclasses import dataclass, field
import operator
from typing import List


#filename = 'sample01.txt'
filename = 'input.txt'

monkeys = []

@dataclass
class Monkey():
    items: List[int] = field(default_factory=lambda: [])
    operator: str = field(default="")
    operand: int = field(default="")
    test: int = field(default=-1)
    throw: List[int] = field(default_factory=lambda: [-1, -1])
    inspections: int = field(default=0)

operators = {'*': operator.mul, '+': operator.add, '/': operator.floordiv, '-': operator.sub}

data = []
with open(filename, "r") as f:
    line = f.readline()
    while line:
        m = Monkey()
        line = f.readline().strip().split()
        for i in range(2, len(line)):
            if (line[i].endswith(",")):
                line[i] = line[i][:-1]
            m.items.append(int(line[i]))

        line = f.readline().strip().split()
        print(line)
        m.operator = line[4]
        if (line[5] == "old"):
            m.operand = -1
        else:
            m.operand = int(line[5])
        
        line = f.readline().strip().split()
        m.test = int(line[3])

        line = f.readline().strip().split()
        m.throw[0] = (int(line[-1]))
        line = f.readline().strip().split()
        m.throw[1] = (int(line[-1]))

        line = f.readline()
        line = f.readline()
        print(m)
        monkeys.append(m)

#exit(0)
for round in range(20):
    for m in monkeys:
        while len(m.items) > 0:
            m.inspections += 1
            item = m.items.pop(0)
            level = operators[m.operator](item, m.operand if m.operand > -1 else item)
            level = level // 3
            if level % m.test == 0:
                monkeys[m.throw[0]].items.append(level)
            else:
                monkeys[m.throw[1]].items.append(level)
            #print(m)

for m in monkeys:
    print(m)
            #exit(0)

monkeys.sort(key=lambda e: e.inspections, reverse=True)
print(monkeys[0].inspections * monkeys[1].inspections)

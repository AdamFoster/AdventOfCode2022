#answer = 3378273370680

from dataclasses import dataclass, field
import operator


#filename = 'sample01.txt'
filename = 'input.txt'

ops = {'*': operator.mul, '+': operator.add, '/': operator.floordiv, '-': operator.sub}

@dataclass
class Node:
    name: str = field(default="")
    operation: callable = field(default=None)
    opcode: str = field(default="")
    value: int = field(default=None)
    leftname: str = field(default="")
    rightname: str = field(default="")
    dep: bool = field(default=False)

data: dict[str, Node] = {}
root = None
with open(filename, "r") as f:
    for line in f:
        name, rest = line.strip().split(":")
        n = Node(name=name)
        rest = rest.strip().split(" ")
        if len(rest) == 1:
            n.value = int(rest[0])
        else:
            n.leftname = rest[0]
            n.rightname = rest[2]
            n.operation = ops[rest[1]]
            n.opcode = rest[1]
        if name == "root":
            root = n
        data[name] = n

print(len(data))
#print(data)

def calc(node):
    if node.name == "humn":
        node.value = None
        return None

    if node.value is not None:
        return node.value
    l = calc(data[node.leftname])
    r = calc(data[node.rightname])

    if l == None or r == None:
        node.dep = True
        return None
    node.value = node.operation(l, r)

    data.pop(node.leftname)
    data.pop(node.rightname)
    return node.value

calc(root)
print("**************")
print(len(data))
#print(data)

def recalc(node: Node, target: int):
    if node.name == "humn":
        node.value = target
        return target

    if node.opcode == "+":
        if data[node.leftname].value == None:
            return recalc(data[node.leftname], target - data[node.rightname].value)
        else:
            return recalc(data[node.rightname], target - data[node.leftname].value)
    elif node.opcode == "*":
        if data[node.leftname].value == None:
            return recalc(data[node.leftname], target // data[node.rightname].value)
        else:
            return recalc(data[node.rightname], target // data[node.leftname].value)
    elif node.opcode == "-":
        if data[node.leftname].value == None:
            return recalc(data[node.leftname], target + data[node.rightname].value)
        else:
            return recalc(data[node.rightname], data[node.leftname].value - target)
    elif node.opcode == "/":
        if data[node.leftname].value == None:
            return recalc(data[node.leftname], target * data[node.rightname].value)
        else:
            return recalc(data[node.rightname], data[node.leftname].value // target)
    assert False




if data[root.leftname].value == None:
    print(recalc(data[root.leftname], data[root.rightname].value))
else:
    print(recalc(data[root.rightname], data[root.leftname].value))
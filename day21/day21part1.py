#answer = 331120084396440

from dataclasses import dataclass, field
import operator


#filename = 'sample01.txt'
filename = 'input.txt'

ops = {'*': operator.mul, '+': operator.add, '/': operator.floordiv, '-': operator.sub}

@dataclass
class Node:
    name: str = field(default="")
    operation: callable = field(default=None)
    value: int = field(default=None)
    leftname: str = field(default="")
    left: object = field(default=None)
    rightname: str = field(default="")
    right: object = field(default=None)

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
        if name == "root":
            root = n
        data[name] = n

print(data)

def calc(node):
    if node.value is not None:
        return node.value
    l = calc(data[node.leftname])
    r = calc(data[node.rightname])
    return node.operation(l, r)

print(calc(root))

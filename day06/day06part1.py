#answer = 1480

import functools as ft
import re

#filename = 'sample01.txt'
filename = 'input.txt'

score = 0
last4 = ""
last4set = {}
index = 3
with open(filename, "r") as f:
    line = f.readline().strip()
    while len(last4set) < 4:
        index += 1
        last4 = line[index-4:index]
        last4set = {c for c in last4}
    print(index)   
    print(last4)


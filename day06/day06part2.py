#answer = 2746

import functools as ft
import re

#filename = 'sample01.txt'
filename = 'input.txt'

markerlen = 14
score = 0
last = ""
lastset = {}
index = markerlen-1
with open(filename, "r") as f:
    line = f.readline().strip()
    while len(lastset) < markerlen:
        index += 1
        last = line[index-markerlen:index]
        lastset = {c for c in last}
    print(index)   
    print(last)


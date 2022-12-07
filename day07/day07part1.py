#answer = 1307902

from functools import reduce


#filename = 'sample01.txt'
filename = 'input.txt'

threshold = 100000

currentlocation = []
structure = {"directories": {}, "files": {}, "size": 0}
currentstructure = [structure]
with open(filename, "r") as f:
    for line in f:
        line = line.strip()
        #print(line)
        if line[0] == '$':
            if line[2:4] == "ls":
                #print("Listing")
                pass
            elif line[2:4] == "cd":
                targetdir = line[5:]
                #print("Moving to ", targetdir)
                if targetdir == "/":
                    currentlocation = []
                    currentstructure = [structure]
                elif targetdir == "..":
                    currentlocation.pop()
                    currentstructure.pop() 
                else:
                    currentlocation.append(targetdir)
                    currentstructure.append(currentstructure[-1]["directories"][targetdir])
                #print(currentlocation)
            else:
                print("Uh oh", line)
        else:
            size, location = line.split()
            #print(currentstructure)
            if size == "dir":
                currentstructure[-1]["directories"][location] = {"directories": {}, "files": {}, "size": 0}
            else:
                currentstructure[-1]["files"][location] = int(size)

def calcsize(d):
    total = reduce(lambda a,b: a+b, d["files"].values(), 0)
    for subd in d["directories"]:
        total += calcsize(d["directories"][subd])
    d["size"] = total
    #print(total)
    return total

size = calcsize(structure)
#print(size)


def calcanswer(d):
    total = 0
    for subd in d["directories"]:
        if d["directories"][subd]["size"] <= threshold:
            total += d["directories"][subd]["size"]
        total += calcanswer(d["directories"][subd])
    return total

print(calcanswer(structure))
    


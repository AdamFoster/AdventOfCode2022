#answer = 13639962836448

#filename = 'sample01.txt'
filename = 'input.txt'

distress = (-1,-1)
scanners: dict[tuple, int] = {}
#targetline = 2000000 if filename == 'input.txt' else 10
maxrange = 4000000 if filename == 'input.txt' else 20

with open(filename, "r") as f:
    for line in f:
        s, b = line.strip().split(":")
        s = s.split()
        s = (int(s[2][2:-1]), int(s[3][2:]))
        b = b.split()
        b = (int(b[4][2:-1]), int(b[5][2:]))
        #print(b)

        d = abs(s[0]-b[0]) + abs(s[1]-b[1])
        scanners[s] = d
        
        #print(s, b, d)
#print(beacons)

for y in range(maxrange):
    #if y%1000 == 0:
    #    print("Y=",y)
    coverage = []
    for sx,sy in scanners:
        scanner = (sx,sy)
        distance = scanners[(sx,sy)]
        #print(scanner, distance)
        if scanner[1]-distance <= y <= scanner[1]+distance:
            d = distance-abs(scanner[1]-y)
            ss = scanner[0]-d
            se = scanner[0]+d
            newcoverage = []
            #if y == 11:
            #    print(ss, se, coverage)
            for interval in coverage:
                if interval[1]+1 < ss or se+1 < interval[0]:
                    newcoverage.append(interval)
                else:
                    ss = min(interval[0], ss)
                    se = max(interval[1], se)
            newcoverage.append((ss, se))
            coverage = newcoverage
    #print(coverage, y)
    if len(coverage) > 1:
        print(coverage, y)
        print((max(coverage[0][0],coverage[1][0])-1)*4000000 + y)
        break


#print(used)
#print(len(used))



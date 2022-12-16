#answer = 4907780

#filename = 'sample01.txt'
filename = 'input.txt'

beacons = set()
targetline = 2000000 if filename == 'input.txt' else 10
used = set()
with open(filename, "r") as f:
    for line in f:
        s, b = line.strip().split(":")
        s = s.split()
        s = (int(s[2][2:-1]), int(s[3][2:]))
        b = b.split()
        b = (int(b[4][2:-1]), int(b[5][2:]))
        beacons.add(b)

        d = abs(s[0]-b[0]) + abs(s[1]-b[1])

        if s[1]-d <= targetline <= s[1]+d:
            for i in range(d-abs(s[1]-targetline)+1):
                used.add(s[0]+i)
                used.add(s[0]-i)

        #print(s, b, d)

for beacon in beacons:
    if beacon[1] == targetline:
        used.discard(beacon[0])

#print(used)
print(len(used))



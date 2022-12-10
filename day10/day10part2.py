#answer = PLPAFBCL
###..#....###...##..####.###...##..#...#
#..#.#....#..#.#..#.#....#..#.#..#.#....
#..#.#....#..#.#..#.###..###..#....#....
###..#....###..####.#....#..#.#....#....
#....#....#....#..#.#....#..#.#..#.#....
#....####.#....#..#.#....###...##..####.

#filename = 'sample02.txt'
filename = 'input.txt'

def draw(c, x):
    if x <= c%40 <= x+2: #screen coordinates 0 indexed, cycles 1 indexed
        print("#", end="")
    else:
        print(".", end="")
    if (c%40 == 0):
        print("")

x = 1
cycle = 0

with open(filename, "r") as f:
    for line in f:
        if line.strip() == "noop":
            cycle += 1
            draw(cycle, x)

        else:
            amount = int(line.strip().split()[1])
            cycle += 1
            draw(cycle, x)
            cycle += 1
            draw(cycle, x)
            x += amount




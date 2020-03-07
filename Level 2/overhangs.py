import parser

def find_overhangs(map):
    supported = set()
    def visit_supported(x, y, z):
        if (x, y, z) in supported: return
        if x < 0 or y < 0 or z < 0: return
        if max(x, y, z) >= len(map): return
        if map[x][y][z] == None: return
        supported.add((x, y, z))
        ddx = [0, 0, 0, 1, -1]
        ddy = [0, -1, 1, 0, 0]
        ddz = [1, 0, 0, 0, 0]
        for (dx, dy, dz) in zip(ddx, ddy, ddz):
            visit_supported(x+dx, y+dy, z+dz)

    all_blocks = set()

    for x in range(len(map)):
        for y in range(len(map[0])):
            visit_supported(x, y, 0)
            for z in range(len(map[0][0])):
                if map[x][y][z]:
                    all_blocks.add((x, y, z))

    overhangs = all_blocks - supported
    return overhangs

if __name__ == '__main__':
    good, bad = parser.parse_file("../data/hard.txt")
    print(find_overhangs(good))

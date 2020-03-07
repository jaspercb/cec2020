import parser

def find_overhangs(map):
    def sample(x, y, z):
        if x < 0 or y < 0 or z < 0: return None
        if x >= len(map) or y >= len(map) or z >= len(map): return None
        return map[x][y][z]
    overhangs = set()
    for x in range(len(map)):
        for y in range(len(map[x])):
            for z in range(len(map[x][y])):
                if z == 0: continue
                if (sample(x, y, z+1) is not None and 
                    sample(x, y, z-1) is None and
                    sample(x+1, y, z) is None and
                    sample(x-1, y, z) is None and
                    sample(x, y+1, z) is None and
                    sample(x, y-1, z) is None):
                    overhangs.add((x, y, z))
    return overhangs

if __name__ == '__main__':
    good, bad = parser.parse_file("../data/overhang.txt")
    print(find_overhangs(good))

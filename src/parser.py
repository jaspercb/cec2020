import sys

import render

class VoxelArray:
    def __init__(self, size):
        self.arr = [[[None]*size for _ in range(size)] for _ in range(size)]
        assert(len(self.arr) == size)
        assert(len(self.arr[1]) == size)
        assert(len(self.arr[2]) == size)

    def __getitem__(self, idx):
        return self.arr[idx]

    def getArr(self):
        return self.arr
    
    def place(self, color, x, y, z):
        for val in [x, y, z]:
            assert(0 <= val)
            assert(val < len(self.arr))

        assert(self[x][y][z] is None)

        def clamp(val):
            if val < 0:
                return 0
            if val >= len(self.arr):
                return len(self.arr) - 1
            return val
        
        ddx = [0, 0, -1, 1]
        ddy = [-1, 1, 0, 0]
        has_support = False
        for dx, dy in zip(ddx, ddy):
            if self[x + dx][y + dy][z] is not None:
                has_support = True
                break

        assert(has_support)
        self[x][y][z] = color

def parse(lines):
    # returns [unscrambled, scrambled]
    assert(lines[0] == 'unscrambled_image')
    size = int(lines[1][5:])

    def make_array(lines):
        assert(len(lines) == size**3)
        voxels = VoxelArray(size)
        for lineno in range(size**3):
            line = lines[lineno]
            pos, color = line.split('=')
            pos = tuple([int(n) for n in pos.split(',')])
            # strip quotes
            color = color[1:-1]
            if color:
                color = tuple([int(channel) for channel in color.split('_')])
            else:
                color = None
            voxels[pos[0]][pos[1]][pos[2]] = color
        return voxels

    voxel_dim = size**3
    unscrambled = make_array(lines[2:2+voxel_dim])
    scrambled = make_array(lines[5+voxel_dim:5+2*voxel_dim])
    return unscrambled, scrambled

def parse_file(filename):
    with open(filename) as f:
        return parse([line.strip() for line in f.readlines()])

def main(filename):
    with open(filename) as f:
        [unscrambled, scrambled] = parse([line.strip() for line in f.readlines()])
        render.render(unscrambled.getArr())
        render.render(scrambled.getArr())

if __name__ == '__main__':
    main(sys.argv[1])


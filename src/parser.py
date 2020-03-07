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

def main(filename):
    with open(filename) as f:
        [unscrambled, scrambled] = parse([line.strip() for line in f.readlines()])
        render.render(unscrambled.getArr())
        render.render(scrambled.getArr())

if __name__ == '__main__':
    main(sys.argv[1])


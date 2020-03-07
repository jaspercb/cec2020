import sys

from renderer import Renderer

def vec3sum(a, b):
    return tuple(map(sum, zip(a, b)))


class VoxelArray:
    def __init__(self, size):
        self.arr = [[[None]*size for _ in range(size)] for _ in range(size)]
        assert(len(self.arr) == size)
        assert(len(self.arr[1]) == size)
        assert(len(self.arr[2]) == size)

    def __getitem__(self, idx):
        return self.arr[idx]

    def __len__(self):
        return len(self.arr)

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
        has_support = z == 0
        for dx, dy in zip(ddx, ddy):
            if self[x + dx][y + dy][z] is not None:
                has_support = True
                break
        if self[x][y][z-1] is not None:
            has_support = True

        assert(has_support)
        self[x][y][z] = color

    def apply_gravity_to_unsupported_blocks(self):
        """
        Say we have

        YZ
        X
        -----

        and we remove X

        This should fall to
        YZ
        -----

        Pos: the (x, y, z) of the removed block (X, in this case)
        """
        ddx = [0, 0, 0, -1, 1, 0]
        ddy = [0, -1, 1, 0, 0, 0]
        ddz = [-1, 0, 0, 0, 0, 1]

        supported_blocks = set()

        def visit(pos):
            if pos in supported_blocks:
                return
            size = len(self[0])
            x, y, z = pos
            if min(x, y, z) < 0: return
            if max(x, y, z) >= size: return
            color = self[x][y][z]
            if color is None:
                return

            supported_blocks.add(pos)
            for offset in zip(ddx, ddy, ddz):
                adjacent = vec3sum(pos, offset)
                visit(adjacent)

        all_blocks = set()
        for x in range(len(self[0])):
            for y in range(len(self[0])):
                visit((x, y, 0))
                for z in range(len(self[0])):
                    if self[x][y][z] is not None:
                        all_blocks.add((x, y, z))

        unsupported = all_blocks - supported_blocks

        if unsupported:
            new_pos = {}
            for (x, y, z) in unsupported:
                new_pos[(x, y, z-1)] = self[x][y][z]
                self[x][y][z] = None
            for ((x, y, z), color) in new_pos.items():
                self[x][y][z] = color

            self.apply_gravity_to_unsupported_blocks()

    def remove(self, x, y, z):
        self[x][y][z] = None
        self.apply_gravity_to_unsupported_blocks()


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
        renderer = Renderer()
        renderer.animate([scrambled.getArr(), unscrambled.getArr()])

if __name__ == '__main__':
    main(sys.argv[1])

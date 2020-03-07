import copy
import sys
import traceback

import parser
import brain
import drone
import renderer

def main(filename):
    [unscrambled, scrambled] = parser.parse_file(filename)

    frames = []
    def callback(pos, world):
        world = copy.deepcopy(world)
        for x in range(len(world)):
            for y in range(len(world[x])):
                world[x][y].append(None)
        x, y, z = pos
        world[x][y][z] = (0, 255, 0)
        frames.append(world)

    d = drone.Drone(scrambled, 0, 0, callback)
    b = brain.Brain(d, unscrambled)
    try:
        b.mainloop()
    except AssertionError:
        traceback.print_exc()

    r = renderer.Renderer()
    r.animate(frames[::20])

if __name__ == '__main__':
    main(sys.argv[1])

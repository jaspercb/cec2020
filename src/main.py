import copy
import sys
import traceback

import parser
import brain
import drone
import renderer

def main(filename, num_frames=None):
    [unscrambled, scrambled] = parser.parse_file(filename)

    frames = []
    def callback(pos, world, ticks, hopper_contents, capacity):
        world = copy.deepcopy(world)
        for x in range(len(world)):
            for y in range(len(world[x])):
                world[x][y].append(None)
        x, y, z = pos
        world[x][y][z] = (0, 255, 0)
        frames.append((ticks, world, hopper_contents, capacity))

    d = drone.Drone(scrambled, 0, 0, callback)
    b = brain.Brain(d, unscrambled)
    try:
        b.mainloop()
    except AssertionError:
        traceback.print_exc()

    r = renderer.Renderer()
    if num_frames is None:
      r.animate(frames)
    else:
      r.animate(frames[::len(frames)//int(num_frames)] + [frames[-1]])

if __name__ == '__main__':
    main(*sys.argv[1:])

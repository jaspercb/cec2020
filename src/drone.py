from collections import Counter

class Drone(object):
    UNKNOWN = "?"

    def __init__(self, world, x, y, callback=lambda pos, world:None):
        """
        Parameters:
            callback: a function called as f((self.x, self.y, self.z), self.world)
            called every time the worldstate or our position changes
        """
        size = len(world[0])

        self.callback = callback
        self.world = world
        self.capacity = int((size**1.5)/2)

        self.hopper = Counter()
        self.lastColor = None
        self.x = x
        self.y = y
        self.updateZ()

        # Part B
        self.knowledge = [[[Drone.UNKNOWN]*size for _ in range(size)] for _ in range(size)]
        self.ticks = 0

    def fireCallback(self):
        self.callback((self.x, self.y, self.z), self.world)

    def updateZ(self):
        height = 0
        for h, block in enumerate(self.world[self.x][self.y]):
            if block:
                height = max(h, height)
        self.z = height + 1
        self.fireCallback()

    def move(self, dx, dy):
        moving_x = dx != 0
        moving_y = dy != 0

        assert(moving_x ^ moving_y)
        assert(dx in [-1, 0, 1])
        assert(dy in [-1, 0, 1])

        self.x += dx
        self.y += dy

        self.updateZ()
        self.ticks += 1

    def scan(self):
        """
        Returns: (height, color) of the highest block at (self.x, self.y)
        """
        for h, block in list(enumerate(self.world[self.x][self.y]))[::-1]:
            if block:
                self.knowledge[self.x][self.y][h] = block
                return h, block
            self.knowledge[self.x][self.y][h] = None
        return -1, None

    def pickup(self):
        assert(sum(self.hopper.values()) < self.capacity)
        h, color = self.scan()

        if color == self.lastColor:
            self.ticks += 2
        else:
            self.ticks += 3

        self.hopper[color] += 1
        self.lastColor = color
        self.world.remove(self.x, self.y, h)
        self.knowledge[self.x][self.y][self.z-1] = None
        self.z -= 1
        self.fireCallback()

    def dropoff(self, color, z):
        # Check we have the block.
        assert(self.hopper[color] > 0)

        if color == self.lastColor:
            self.ticks += 2
        else:
            self.ticks += 3

        self.lastColor = color

        h, _ = self.scan()
        if z <= h:
            import pdb; pdb.set_trace()
        assert(z > h)
        assert(z < len(self.world))

        self.z = z + 1

        self.world.place(color, self.x, self.y, z)
        self.knowledge[self.x][self.y][z] = color
        self.hopper[color] -= 1
        if self.hopper[color] == 0:
            del self.hopper[color]
        self.fireCallback()

    def space_left(self):
        return self.capacity - sum(self.hopper.values())

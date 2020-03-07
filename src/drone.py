from collections import Counter

class Drone(object):
    def __init__(self, world, x, y):
        self.world = world
        self.capacity = int((len(world[0])**0.5)/2)
        self.hopper = Counter()
        self.lastColour = None
        self.x = x
        self.y = y
        self.updateZ()

    def updateZ(self):
        height = 0
        for h, block in enumerate(self.world[self.x][self.y]):
            if block:
                height = max(h, height)
        self.z = height + 1

    def moveX(self, dx):
        assert(dx in [-1, 1])
        self.x += dx
        self.updateZ()

    def moveY(self, dy):
        assert(dy in [-1, 1])
        self.y += dy
        self.updateZ()

    def scan(self):
        # returns: height, color
        for h, block in list(enumerate(self.world[self.x][self.y]))[::-1]:
            if block:
                return h, block
        return None

    def pickup(self):
        assert(sum(self.hopper.values()) < self.capacity)
        h, color = self.scan()
        self.hopper[color] += 1
        self.lastColor = color
        self.world[self.x][self.y][self.z-1] = None
        self.z -= 1

    def dropoff(self, color, z):
        # Check we have the block.
        assert(self.hopper[color] > 0)
        self.world.place(color, self.x, self.y, z)
        self.hopper[color] -= 1
        if self.hopper[color] == 0:
            del self.hopper[color]


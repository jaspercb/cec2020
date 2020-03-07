import functools

import deps
import renderer

class Brain:
    def __init__(self, drone, unscrambled):
        assert(drone.x == 0 and drone.y == 0)
        self.n = len(unscrambled.getArr())
        self.drone = drone
        self.unscrambled = unscrambled
        self.deps = deps.Deps(unscrambled)
        self.clearedColumns = set()
        self.unclearedColumns = set((i, j) for i in range(self.n) for j in range(self.n))
        self.prevColumn = None

    def satisfyDependencies(self):
        while True:
            cpos = self.drone.x, self.drone.y
            doable = self.deps.getNext(self.clearedColumns)
            closest = None
            dropColour = None
            dropZ = None
            def dist(a, b):
                return abs(a[0]-b[0]) + abs(a[1]-b[1])
            for (i, j, k) in doable:
                colour = self.unscrambled[i][j][k]
                assert(colour)
                if colour not in self.drone.hopper:
                    continue
                if not closest or dist(cpos, (i, j)) < dist(cpos, closest):
                    closest = (i, j)
                    dropColour = colour
                    dropZ = k
            if not closest:
                break

            self.travelTo(closest)
            self.drone.dropoff(dropColour, dropZ)
            self.deps.place((closest[0], closest[1], dropZ))

    def clearColumn(self):
        # get an upper bound on the number of blocks in this column
        h, _ = self.drone.scan()
        space = self.drone.space_left()
        h += 1

        ox, oy = self.drone.x, self.drone.y
        while h > self.drone.space_left():
            good = False
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                nx, ny = self.drone.x + dx, self.drone.y + dy
                if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                    continue
                good = True
                break
            assert(good)
            # need to dump blocks off
            self.drone.move(dx, dy)
            self.dump(h)
        self.travelTo((ox, oy))
        while True:
            h, c = self.drone.scan()
            if h == -1:
                break        
            self.drone.pickup()
        self.unclearedColumns.remove((ox, oy))

    def mainloop(self):
        while True:
            col = (self.drone.x, self.drone.y)
            (cx, cy) = col
            assert(col in self.unclearedColumns)
            self.clearColumn()
            if self.prevColumn:
                self.clearedColumns.add(self.prevColumn)
            self.prevColumn = col
            self.satisfyDependencies()
            ncol = None
            if ((cx == 0 and (cx+1, cy) in self.clearedColumns) 
                    or (cx == self.n-1 and (cx-1, cy) in self.clearedColumns)):
                cy += 1
                # todo: don't need buffer column if we're at an edge
                if cy == self.n:
                    break
            else:
                good = False
                for nx in [cx-1, cx+1]:
                    if nx < 0 or nx >= self.n:
                        continue
                    if (nx, cy) in self.clearedColumns:
                        continue
                    good = True
                    break
                assert(good)
                cx = nx
            self.travelTo((cx, cy))
            print('New pos: {}, hopper: {}'.format((cx, cy), self.drone.hopper))
            # renderer.Renderer().singleFrame(self.drone.world)
        self.clearedColumns.add(self.prevColumn)
        self.satisfyDependencies()

    def dump(self, needed):
        while self.drone.space_left() < needed:
            h, c = self.drone.scan()
            if h >= self.n - 1:
                break
            dropC = None
            if c and self.drone.hopper[c] > 0:
                dropC = c
            else:
                dropC = next(self.drone.hopper.elements())
            self.drone.dropoff(dropC, h+1)

    ###################
    # Utility methods #
    ###################

    def maxInformationPath(self, start, end):
        def predecessors(pos):
            ret = []
            if start[0] < pos[0]:
                ret.append((pos[0]-1, pos[1]))
            elif start[0] > pos[0]:
                ret.append((pos[0]+1, pos[1]))

            if start[1] < pos[1]:
                ret.append((pos[0], pos[1] - 1))
            elif start[1] > pos[1]:
                ret.append((pos[0], pos[1] + 1))

            return ret

        @functools.lru_cache(maxsize=None)
        def maxInformation(pos):
            if pos == start:
                return 0
            info = int(self.drone.knowledge[pos[0]][pos[1]][-1] == self.drone.UNKNOWN)
            return info + max(maxInformation(pred) for pred in predecessors(pos))

        # Backtrack to construct the path
        path = []

        def recurse(pos):
            if pos == start:
                return
            pred = max(predecessors(pos), key=maxInformation)
            recurse(pred)
            path.append(pred)

        recurse(end)
        path.append(end)

        return maxInformation(end), path

    def travelPath(self, path):
        for i, pos in enumerate(path[1:]):
            prev = path[i]
            dx = pos[0] - prev[0]
            dy = pos[1] - prev[1]

            self.drone.move(dx, dy)

    def travelTo(self, destination):
        """
        Large-scale travelling is an opportunity to explore our surroundings.
        Given a desired final location (x, y), take the shortest path that
        maximizes how many new blocks we see.
        """

        _, path = self.maxInformationPath((self.drone.x, self.drone.y), destination)
        self.travelPath(path)

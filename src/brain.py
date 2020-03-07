import functools

class Brain:
    def __init__(self, drone, unscrambled):
        self.drone = drone
        self.unscrambled = unscrambled

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
                path.append(pos)
                return
            pred = max(predecessors(pos), key=maxInformation)
            recurse(pred)
            path.append(pred)

        recurse(end)

        return maxInformation(end), path

    def travelPath(self, path):
        for i, pos in enumerate(path):
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

        path = self.maxInformationPath((self.drone.x, self.drone.y), destination)
        self.travelPath(path)

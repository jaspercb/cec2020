class Deps(object):
    def __init__(self, stacked):
        stacked = stacked.getArr()
        n = len(stacked)
        self.n = n
        
        self.needsAdjacent = [[[False for k in range(n)] for j in range(n)] for i in range(n)]
        self.hasAdjacent = [[[False for k in range(n)] for j in range(n)] for i in range(n)]
        self.hasBelow = [[[False for k in range(n)] for j in range(n)] for i in range(n)]

        self.stacked = stacked
        self.next = set()
        self.done = set()
        for i in range(n):
            for j in range(n):
                prev = None
                for k in range(n):
                    c = stacked[i][j][k]
                    if not c:
                        continue
                    if not prev and k == 0:
                        self.next.add((i,j,k))
                        self.hasBelow[i][j][k] = True
                    if prev != None and prev != k-1:
                        # dependencies on blocks around us
                        self.needsAdjacent[i][j][k] = True
                    prev = k


    def place(self, pos):
        assert(pos in self.next)
        self.next.remove(pos)
        self.done.add(pos)

        i, j, k = pos
        for di, dj in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= self.n or nj < 0 or nj >= self.n:
                continue
            if self.needsAdjacent[ni][nj][k]:
                self.hasAdjacent[ni][nj][k] = True
                npos = ni, nj, k
                if npos not in self.done and self.hasBelow[ni][nj][k]:
                    self.next.add(npos)
        for nk in range(k+1, self.n):
            if self.stacked[i][j][nk]:
                self.hasBelow[i][j][nk] = True
                if (not self.needsAdjacent[i][j][nk] or self.hasAdjacent[i][j][nk]):
                    self.next.add((i, j, nk))
                break

    def getNext(self, freeColumns):
        return set((i, j, k) for (i, j, k) in self.next if (i, j) in freeColumns)

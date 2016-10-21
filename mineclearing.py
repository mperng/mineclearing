class Game(object):
    def __init__(self, cuboidStr):
        self.scriptSteps = []
        self.volleysFired = 0
        self.cuboid = Cuboid(cuboidStr)
        self.score = (10 * self.cuboid.numMines)


class Cuboid(object):
    def __init__(self, cuboidStr):
        # assuming the same number of cols for each row,
        # otherwise invalid cuboid given
        self.grid, self.numMines = [], 0
        for line in cuboidStr.split():
            l = list(line)
            self.numMines += len(l) - l.count('.')
            self.grid.append(l)

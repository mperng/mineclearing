class Game(object):
    def __init__(self, numMines):
        self.cuboid = Cuboid()
        self.steps = []
        self.volleysFired = 0
        self.shipPosition = None
        self.numMines = numMines
        self.score = (10 * numMines)


class Cuboid(object):
    def __init__(self):
        pass

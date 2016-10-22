class Simulation(object):
    '''
    A class representing a simulation of a mine-clearing script
    '''
    def __init__(self, cuboidStr):
        self.scriptSteps = []
        self.volleysFired = 0
        self.cuboid = Cuboid(cuboidStr)
        self.score = 10 * self.cuboid.numMines

    def run(self):
        '''
        Run the script until an end condition has been reached
        '''
        pass

    def evaluate(self):
        '''
        Evaluate if an end condition has been reached.
        '''
        pass


class Cuboid(object):
    '''
    A class representing a cuboid view in the simulation
    '''
    def __init__(self, cuboidStr):
        self.matrix = [list(l) for l in cuboidStr.split()]
        self.mines = self._getMinePositions()
        self.numRows = len(self.matrix)
        self.numCols = len(self.matrix[0])
        self.shipPos = [self.numRows / 2, self.numCols / 2]
        self.minesRemaining = len(self.mines)

    def _getMinePositions(self):
        '''
        Return a list of positions (row_num, col_num) where mines are located
        '''
        mines = []
        for x_pos, row in enumerate(self.matrix):
            mines += reduce(lambda l, t: l + [[x_pos, t[0]]],
                            filter(lambda t: t[1] != '.', enumerate(row)),
                            [])
        return mines

    def inBounds(self, x, y):
        '''
        Return True if the given x, y values
        are within the bounds of the cuboid
        '''
        if x < 0 or y < 0 or x >= self.numRows or y >= self.numCols:
            return False
        return True

    def __str__(self):
        '''
        return the string representation of the Cuboid
        '''
        return '\n'.join([''.join(x) for x in self.matrix ]) + '\n'

    def executeFireCmd(self, firePositions):
        '''
        modify the cuboid to reflect the result of a fire command
        '''
        pass

    def executeMoveCmd(self, offset_x, offset_y):
        '''
        modify the ship position to reflect the result of a move command
        '''
        pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python mineclearing.py \
                         /path/to/cuboid_file.txt /path/to/script_file.txt')

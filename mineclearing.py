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
        self.grid = [list(l) for l in cuboidStr.split()]
        self.minePosList = self._getMinePositions()
        self.numRows = len(self.grid)
        self.numCols = len(self.grid[0])

    def _getMinePositions(self):
        '''
        Return a list of positions (row_num, col_num) where mines are located
        '''
        minePosList = []
        for x_pos, row in enumerate(self.grid):
            minePosList += reduce(lambda l, t: l + [[x_pos, t[0]]],
                                  filter(lambda t: t[1] != '.', enumerate(row)),
                                  [])
        return minePosList

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

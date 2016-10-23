class Simulation(object):
    '''
    A class representing a simulation of a mine-clearing script
    '''
    def __init__(self, cuboid, scriptSteps):
        self.script_steps = []
        self.volleys_fired = 0
        self.cuboid = cuboid
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
    def __init__(self, cuboid_str=None):
        self.matrix, self.mine_positions = [], []
        self.num_rows, self.num_cols = 0, 0
        self.mines_remaining = 0
        self.ship_position = None

    def add_row(self, row):
        '''
        Add a row to the underlying matrix representation of this cuboid.
        '''
        self.matrix.append(row)
        mines = [(self.num_rows, y[0]) for y in enumerate(row) if y[1] != '.']
        self.mine_positions += mines
        self.num_rows += 1
        self.num_cols = max(self.num_cols, len(row))
        self.mines_remaining += len(mines)
        self.ship_position = [self.num_rows / 2, self.num_cols / 2]

    def in_bounds(self, x, y):
        '''
        Return True if the given x, y values
        are within the bounds of the cuboid
        '''
        if x < 0 or y < 0 or x >= self.num_rows or y >= self.num_cols:
            return False
        return True

    def decrement_mine_distance(self, value):
        '''
        decrement one mine's distance value
        '''
        pass

    def fire(self, firePositions):
        '''
        modify the cuboid to reflect the result of a fire command
        '''
        pass

    def move(self, offset_x, offset_y):
        '''
        modify the ship position to reflect the result of a move command
        '''
        pass

    def __str__(self):
        '''
        return the string representation of the Cuboid
        '''
        return '\n'.join([''.join(x) for x in self.matrix]) + '\n'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python mineclearing.py \
                         /path/to/cuboid_file.txt /path/to/script_file.txt')
    with open(sys.argv[0], 'r'), open(sys.argv[1]) as cuboid_file, script_file:
        c = Cuboid()
        cuboid_row = next(cuboid_file, None)
        while cuboid_row:
            c.add_row(cuboid_row)
            cuboid_row = next(cuboid_file, None)
        s = Simulation(c)
        script_step = next(script_file, None)
        while script_step:
            s.run(script_step.split(' '))
            script_step = next(script_file, None)

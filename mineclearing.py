import operator


class Simulation(object):
    '''
    A class representing a simulation of a mine-clearing script
    '''
    def __init__(self, cuboid):
        self.volleys_fired = 0
        self.cuboid = cuboid
        self.score = 10 * self.cuboid.num_mines()
        self.move_dict = {'north': (-1, 0), 'south': (1, 0),
                          'east': (0, 1), 'west': (0, -1)}
        self.fire_dict = {'alpha': [(-1, -1), (1, -1), (1, 1), (-1, 1)],
                          'beta': [(-1, 0), (1, 0), (0, -1), (0, 1)],
                          'gamma': [(0, -1), (0, 0), (0, 1)],
                          'delta': [(-1, 0), (0, 0), (1, 0)]}

    def run(self, script_step):
        '''
        Run the script until an end condition has been reached
        '''
        for cmd in list(script_steps):
            self.run_cmd(cmd)

    def run_cmd(self, cmd):
        if cmd in move_dict:
            c.move(move_dict[cmd])
        elif cmd in fire_dict:
            c.fire(*fire_dict[cmd])
            self.volleys_fired += 1
        else:
            print 'invalid command'

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
        self.matrix, self.mines = [], []
        self.num_rows, self.num_cols = 0, 0
        self.ship_position = None

    def add_row(self, row):
        '''
        Add a row to the underlying matrix representation of this cuboid.
        '''
        self.matrix.append(row)
        self.mines += [(self.num_rows, y[0])
                       for y in enumerate(row) if y[1] != '.']
        self.num_rows += 1
        self.num_cols = max(self.num_cols, len(row))
        self.ship_position = [self.num_rows / 2, self.num_cols / 2]

    def in_bounds(self, x, y):
        '''
        Return True if the given x, y values
        are within the bounds of the cuboid
        '''
        return not (x < 0 or y < 0 or x >= self.num_rows or y >= self.num_cols)

    def update(self):
        '''
        decrement all mine distances on the matrix
        '''
        for x, y in iter(self.mines):
            self.matrix[x][y] = self.update_mine_distance(self.matrix[x][y])

    def update_mine_distance(self, value):
        '''
        update a mine's distance char to be 1km less than before
        assuming valid mine values (a to z, A to Z)
        '''
        if ord(value) == 65:
            return 'z'
        elif ord(value) == 97:
            return '*'
        return chr(ord(value) - 1)

    def fire(self, fire_positions):
        '''
        Remove mines that fall into the positions specified by a fire command.
        '''
        ship_x, ship_y = self.ship_position
        removed_mines = []
        for x, y in [(t[0] + ship_x, t[1] + ship_y) for t in fire_positions]:
            if self.in_bounds(x, y) and self.matrix[x][y] != '.':
                self.matrix[x][y] = '.'
                removed_mines.append((x, y))
        self.mines = filter(lambda x: x not in removed_mines, self.mines)

    def move(self, offset_x, offset_y):
        '''
        Modify the ship position to reflect the result of a move command.
        '''
        self.ship_position[0] += offset_x
        self.ship_position[1] += offset_y

    def gen_mine_values(self):
        '''
        A generator that yields all mine values.
        '''
        for x, y in iter(self.mines):
            yield self.matrix[x][y]

    def mine_missed(self):
        '''
        Return True if a mine was passed.
        '''
        if filter(lambda x: x == '*', self.gen_mine_values()):
            return True
        return False

    def num_mines(self):
        '''
        Return the number of mines remaining in the Cuboid.
        '''
        return len(self.mines)

    def get_vert_limits(self):
        '''
        Return the first and last rows that contain a mine
        Assuming that all rows contain same number of columns
        '''
        return self.mines[0][0], self.mines[-1][0]

    def get_hor_limits(self):
        '''
        Return the first and last columns that contain a mine
        Assuming that all rows contain same number of columns
        '''
        hor_sorted_mines = sorted(self.mines, key=operator.itemgetter(1))
        return hor_sorted_mines[0][1], hor_sorted_mines[-1][1]

    def _get_offset(self, index, center_index, pad_value):
        if index < center_index:
            return (pad_value - 1) / 2 - index
        else:
            return 0

    def __str__(self):
        '''
        Return the string representation of the Cuboid.
        '''
        s_x, s_y = self.ship_position
        c_x, c_y = self.num_rows / 2, self.num_cols / 2
        hor_limits, vert_limits = self.get_hor_limits(), self.get_vert_limits()
        true_num_rows = (max(abs(vert_limits[0] - s_x),
                         abs(vert_limits[1] - s_x)) * 2) + 1
        true_num_cols = (max(abs(hor_limits[0] - s_y),
                         abs(hor_limits[1] - s_y)) * 2) + 1
        x_offset = self._get_offset(s_x, c_x, true_num_rows)
        y_offset = self._get_offset(s_y, c_y, true_num_cols)
        result = [['.' for j in xrange(true_num_cols)]
                  for i in xrange(true_num_rows)]
        for x, y in self.mines:
            result[x + x_offset][y + y_offset] = self.matrix[x][y]
        return '\n'.join(''.join(r) for r in result)


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

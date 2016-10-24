import operator


class Cuboid(object):
    '''
    A class representing a cuboid view in the simulation
    '''
    def __init__(self, cuboid_str=''):
        self.matrix, self.mines = [], []
        self.num_rows, self.num_cols = 0, 0
        self.ship_position = None
        for row in map(list, cuboid_str.split()):
            self.add_row(row)

    def add_row(self, row):
        '''
        Add a row to the underlying matrix representation of this cuboid.
        Assuming row is a list of chars representing values in the cuboid.
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

    def num_mines(self):
        '''
        Return the number of mines remaining in the Cuboid.
        '''
        return len(self.mines)

    def mine_missed(self):
        '''
        Return True if a the zero distance value for a mine ('*')
        is found in the mine distance values list.
        '''
        return '*' in (self.matrix[x][y] for x, y in iter(self.mines))

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
        def _is_valid(t):
            return self.in_bounds(t[0], t[1]) and \
                   self.matrix[t[0]][t[1]] != '.'

        def _add_offsets(t):
            return (t[0] + self.ship_position[0], t[1] + self.ship_position[1])
        removed_mines = []
        for x, y in filter(_is_valid, map(_add_offsets, fire_positions)):
            self.matrix[x][y] = '.'
            removed_mines.append((x, y))
        self.mines = filter(lambda x: x not in removed_mines, iter(self.mines))

    def move(self, offset_x, offset_y):
        '''
        Modify the ship position to reflect the result of a move command.
        '''
        self.ship_position[0] += offset_x
        self.ship_position[1] += offset_y

    def get_vert_limits(self):
        '''
        Return the first and last rows in the matrix that contain a mine.
        Assuming that all rows contain same number of columns
        and that all mines are sorted by x index.
        '''
        return self.mines[0][0], self.mines[-1][0]

    def get_hor_limits(self):
        '''
        Return the first and last columns in the matrix that contain a mine.
        Assuming that all rows contain same number of columns.
        '''
        hor_sorted_mines = sorted(self.mines, key=operator.itemgetter(1))
        return hor_sorted_mines[0][1], hor_sorted_mines[-1][1]

    def _get_offset(self, index, center_index, pad_value):
        '''
        Used by __str__ function to calculate the offset from
        the index value (x or y value) that mine
        locations need to be adjusted for.
        '''
        if index >= center_index:
            return 0
        return pad_value - index

    def __str__(self):
        '''
        Return the string representation of the Cuboid.
        '''
        s_x, s_y = self.ship_position
        c_x, c_y = self.num_rows / 2, self.num_cols / 2
        hor_limits, vert_limits = self.get_hor_limits(), self.get_vert_limits()
        extra_rows = max(abs(vert_limits[0] - s_x), abs(vert_limits[1] - s_x))
        extra_cols = max(abs(hor_limits[0] - s_y), abs(hor_limits[1] - s_y))
        x_offset = self._get_offset(s_x, c_x, extra_rows)
        y_offset = self._get_offset(s_y, c_y, extra_cols)
        result = [['.' for j in xrange(extra_cols * 2 + 1)]
                  for i in xrange(extra_rows * 2 + 1)]
        for x, y in self.mines:
            result[x + x_offset][y + y_offset] = self.matrix[x][y]
        return '\n'.join(''.join(r) for r in result)

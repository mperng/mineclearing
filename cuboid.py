import operator


class Cuboid(object):
    '''
    A class representing a cuboid view in the simulation
    cuboid_str: string representing an initial view of a minefield
    '''
    def __init__(self, cuboid_str=''):
        self.matrix, self.mines = [], []
        self.num_rows, self.num_cols = 0, 0
        self.ship_position = None
        for row in map(list, cuboid_str.split()):
            self.add_row(row)
        if self.mines:
            self._resize()

    def add_row(self, row):
        '''
        Add a row to the underlying matrix representation of this cuboid.
        Assuming row is a list of chars representing values in the cuboid.
        row: a list of chars representing either an empty space or a mine in
              the minefield
        '''
        self.matrix.append(row)
        self.mines += [(self.num_rows, y[0])
                       for y in enumerate(row) if y[1] != '.']
        self.num_rows += 1
        self.num_cols = max(self.num_cols, len(row))
        self.ship_position = [self.num_rows / 2, self.num_cols / 2]

    def _resize(self):
        '''
        Resize the matrix to account for improper input from user.
        '''
        vert_limits, hor_limits = self.get_vert_limits(), self.get_hor_limits()
        x_offset, y_offset = 0, 0
        needs_resize = False
        if hor_limits[0] == hor_limits[1] and self.num_cols > 1:
            self.num_cols = 1
            y_offset = hor_limits[0]
            needs_resize = True
        if vert_limits[0] == vert_limits[1] and self.num_rows > 1:
            self.num_rows = 1
            x_offset = vert_limits[0]
            needs_resize = True
        if not needs_resize:
            return
        new_matrix = [['.' for c in xrange(self.num_cols)]
                      for r in xrange(self.num_rows)]
        for x, y in iter(self.mines):
            new_matrix[x - x_offset][y - y_offset] = self.matrix[x][y]
        self.mines = []
        for x, row in enumerate(new_matrix):
            self.mines += reduce(lambda l, t: l + [(x, t[0])],
                                 filter(lambda t: t[1] != '.', enumerate(row)),
                                 [])
        self.matrix = new_matrix
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
        Update all mine chars to show -1km distance than before
        '''
        for x, y in iter(self.mines):
            self.matrix[x][y] = self.update_mine_distance(self.matrix[x][y])

    def update_mine_distance(self, value):
        '''
        Update an individual mine's distance char to -1km distance than before
        value: a valid mine value representing distance of the mine from the
               ship (a to z, A to Z)
        '''
        if ord(value) == 65:
            return 'z'
        elif ord(value) == 97:
            return '*'
        return chr(ord(value) - 1)

    def fire(self, fire_positions):
        '''
        Remove mines that fall into the positions specified by a fire command.
        fire_positions: (x, y) index pairs representing offsets from the ship
                        position to remove mines from
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
        offset_x: the x offset to add to the ship's current x position
        offset_y: the y offset to add to the ship's current y position
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
        index: either an x or y index
        center_index: either an x or y index for the center of this cuboid's
                      matrix
        pad_value: row_padding or col_padding value
        '''
        if index >= center_index:
            return 0
        return pad_value - index

    def _get_dimension(self, limits, ship_pos_index):
        '''
        Get the total number of rows or cols that would be required for the
        string representation of this Cuboid's matrix
        limits: vert_limits or hor_limits
        ship_pos_index: the x or y index of the position of the ship
        '''
        return max(abs(limits[0] - ship_pos_index),
                   abs(limits[1] - ship_pos_index)) * 2 + 1

    def __str__(self):
        '''
        Return the string representation of the Cuboid.
        '''
        if not self.mines:
            return '.'
        s_x, s_y = self.ship_position
        num_print_rows = self._get_dimension(self.get_vert_limits(), s_x)
        num_print_cols = self._get_dimension(self.get_hor_limits(), s_y)
        result = [['.' for j in xrange(num_print_cols)]
                  for i in xrange(num_print_rows)]
        new_center = num_print_rows / 2, num_print_cols / 2
        for x, y in self.mines:
            offsets = (x - s_x, y - s_y)
            result[new_center[0] + offsets[0]][new_center[1] + offsets[1]] = \
                self.matrix[x][y]
        return '\n'.join(''.join(r) for r in result)

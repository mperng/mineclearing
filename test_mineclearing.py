import unittest

from mineclearing import *


class CuboidTest(unittest.TestCase):
    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

    def testCuboidInit1(self):
        c = Cuboid()
        self.assertEqual(c.matrix, [])
        self.assertEqual(c.mine_positions, [])
        self.assertEqual(c.num_rows, 0)
        self.assertEqual(c.num_cols, 0)
        self.assertEqual(c.ship_position, None)

    def testCuboidAddRow1(self):
        cuboid_str = '..Z..\n.Z..Z\n.ZZZ.\n'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(0, 2), (1, 1), (1, 4), (2, 1), (2, 2), (2, 3)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mine_positions, expected_mines)
        self.assertEqual(c.mines_remaining, 6)
        self.assertEqual(c.num_rows, 3)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [1, 2])

    def testCuboidAddRow2(self):
        cuboid_str = '.....\n.Z..Z\n.ZZZ.\n'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(1, 1), (1, 4), (2, 1), (2, 2), (2, 3)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mine_positions, expected_mines)
        self.assertEqual(c.mines_remaining, 5)
        self.assertEqual(c.num_rows, 3)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [1, 2])

    def testCuboidAddRow3(self):
        cuboid_str = '.....\n.a.b.\n.z...\n.d.c.\n..z..\n'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(1, 1), (1, 3), (2, 1), (3, 1), (3, 3), (4, 2)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mine_positions, expected_mines)
        self.assertEqual(c.mines_remaining, 6)
        self.assertEqual(c.num_rows, 5)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [2, 2])

    def testCuboidaddRow4(self):
        cuboid_str = 'a'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(0, 0)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mine_positions, expected_mines)
        self.assertEqual(c.mines_remaining, 1)
        self.assertEqual(c.num_rows, 1)
        self.assertEqual(c.num_cols, 1)
        self.assertEqual(c.ship_position, [0, 0])

    def testCuboidaddRow5(self):
        cuboid_str = 'a...a'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(0, 0), (0, 4)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mine_positions, expected_mines)
        self.assertEqual(c.mines_remaining, 2)
        self.assertEqual(c.num_rows, 1)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [0, 2])

    def testCuboidaddRow6(self):
        cuboid_str = '..Z..\n.....\nZ...Z\n.....\n..Z..\n'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(0, 2), (2, 0), (2, 4), (4, 2)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mine_positions, expected_mines)
        self.assertEqual(c.mines_remaining, 4)
        self.assertEqual(c.num_rows, 5)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [2, 2])

    def testCuboidin_bounds1(self):
        c = self.createCuboid('a')
        self.assertEqual(c.in_bounds(-1, -1), False)
        self.assertEqual(c.in_bounds(-1, 0), False)
        self.assertEqual(c.in_bounds(0, -1), False)
        self.assertEqual(c.in_bounds(0, 1), False)
        self.assertEqual(c.in_bounds(1, 0), False)
        self.assertEqual(c.in_bounds(1, 1), False)
        self.assertEqual(c.in_bounds(0, 0), True)

    def testCuboidin_bounds2(self):
        c = self.createCuboid('..Z..\n.....\nZ...Z\n.....\n..Z..\n')
        for x in xrange(c.num_rows):
            for y in xrange(c.num_cols):
                self.assertEqual(c.in_bounds(x, y), True)
        self.assertEqual(c.in_bounds(-1, -1), False)
        self.assertEqual(c.in_bounds(-1, 0), False)
        self.assertEqual(c.in_bounds(0, -1), False)
        self.assertEqual(c.in_bounds(c.num_rows, 0), False)
        self.assertEqual(c.in_bounds(0, c.num_cols), False)


if __name__ == '__main__':
    unittest.main()

import unittest

from mineclearing import Simulation, Cuboid


class CuboidCreateTest(unittest.TestCase):
    def testCuboidInit1(self):
        c = Cuboid()
        self.assertEqual(c.matrix, [])
        self.assertEqual(c.mines, [])
        self.assertEqual(c.num_rows, 0)
        self.assertEqual(c.num_cols, 0)
        self.assertEqual(c.ship_position, None)


class CuboidAddRowTests(unittest.TestCase):
    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

    def testCuboidAddRow1(self):
        cuboid_str = '..Z..\n.Z..Z\n.ZZZ.\n'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(0, 2), (1, 1), (1, 4), (2, 1), (2, 2), (2, 3)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.num_rows, 3)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [1, 2])

    def testCuboidAddRow2(self):
        cuboid_str = '.....\n.Z..Z\n.ZZZ.\n'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(1, 1), (1, 4), (2, 1), (2, 2), (2, 3)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.num_rows, 3)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [1, 2])

    def testCuboidAddRow3(self):
        cuboid_str = '.....\n.a.b.\n.z...\n.d.c.\n..z..\n'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(1, 1), (1, 3), (2, 1), (3, 1), (3, 3), (4, 2)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.num_rows, 5)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [2, 2])

    def testCuboidaddRow4(self):
        cuboid_str = 'a'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(0, 0)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.num_rows, 1)
        self.assertEqual(c.num_cols, 1)
        self.assertEqual(c.ship_position, [0, 0])

    def testCuboidaddRow5(self):
        cuboid_str = 'a...a'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(0, 0), (0, 4)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.num_rows, 1)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [0, 2])

    def testCuboidaddRow6(self):
        cuboid_str = '..Z..\n.....\nZ...Z\n.....\n..Z..\n'
        c = self.createCuboid(cuboid_str)
        expected_matrix = [list(line) for line in cuboid_str.split()]
        expected_mines = [(0, 2), (2, 0), (2, 4), (4, 2)]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.num_rows, 5)
        self.assertEqual(c.num_cols, 5)
        self.assertEqual(c.ship_position, [2, 2])


class CuboidInBoundsTests(unittest.TestCase):
    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

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


class CuboidUpdateMineDistanceTests(unittest.TestCase):
    def testCuboidUpdateMineDistance1(self):
        self.assertEqual('*', Cuboid().update_mine_distance('a'))

    def testCuboidUpdateMineDistance2(self):
        self.assertEqual('a', Cuboid().update_mine_distance('b'))

    def testCuboidUpdateMineDistance3(self):
        self.assertEqual('z', Cuboid().update_mine_distance('A'))

    def testCuboidUpdateMineDistance4(self):
        self.assertEqual('Y', Cuboid().update_mine_distance('Z'))

    def testCuboidUpdateMineDistance5(self):
        c = Cuboid()
        alpha = list('bcdefghijklmnopqrstuvwxyz')
        expected = list('abcdefghijklmnopqrstuvwxy')
        for i, j in zip(alpha, expected):
            self.assertEqual(c.update_mine_distance(i), j)

    def testCuboidUpdateMineDistance6(self):
        c = Cuboid()
        alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        expected = list('zABCDEFGHIJKLMNOPQRSTUVWXY')
        for i, j in zip(alpha, expected):
            self.assertEqual(c.update_mine_distance(i), j)

    def testCuboidUpdateMineDistance7(self):
        c = Cuboid()
        alpha = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        expected = list('*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY')
        for i, j in zip(alpha, expected):
            self.assertEqual(c.update_mine_distance(i), j)


class CuboidUpdateTests(unittest.TestCase):
    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

    def testCuboidUpdate1(self):
        c = self.createCuboid('a')
        expected = [['*']]
        c.update()
        self.assertEqual(c.matrix, expected)

    def testCuboidUpdate2(self):
        c = self.createCuboid('..Z..\n.....\nZ...Z\n.....\n..Z..\n')
        expected = map(list, '..Y..\n.....\nY...Y\n.....\n..Y..\n'.split())
        c.update()
        self.assertEqual(c.matrix, expected)

    def testCuboidUpdate3(self):
        c = self.createCuboid('a\n.\n.\n.\na\n')
        expected = map(list, '*\n.\n.\n.\n*\n'.split())
        c.update()
        self.assertEqual(c.matrix, expected)

    def testCuboidUpdate4(self):
        c = self.createCuboid('ggZgg\nabcde\nZaaaZ\nABCDE\naaZaa\n')
        expected = map(list, 'ffYff\n*abcd\nY***Y\nzABCD\n**Y**\n'.split())
        c.update()
        self.assertEqual(c.matrix, expected)


class CuboidGenMineValuesTests(unittest.TestCase):
    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

    def testCuboidGenMineValues1(self):
        c = self.createCuboid('a')
        expected = ['a']
        for val, expected in zip(c.gen_mine_values(), expected):
            self.assertEqual(val, expected)

    def testCuboidGenMineValues2(self):
        c = self.createCuboid('a\n.\n.\n.\na\n')
        expected = ['a', 'a']
        for val, expected in zip(c.gen_mine_values(), expected):
            self.assertEqual(val, expected)

    def testCuboidGenMineValues3(self):
        c = self.createCuboid('ggZgg\nabcde\nZaaaZ\nABCDE\naaZaa\n')
        expected = list('ggZggabcdeZaaaZABCDEaaZaa')
        for val, expected in zip(c.gen_mine_values(), expected):
            self.assertEqual(val, expected)


class CuboidMineMissedTests(unittest.TestCase):
    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

    def testCuboidMineMissed1(self):
        c = self.createCuboid('a')
        self.assertEqual(c.mine_missed(), False)

    def testCuboidMineMissed2(self):
        c = self.createCuboid('a..\n*..\n...\n...\n.a.\n')
        self.assertEqual(c.mine_missed(), True)

    def testCuboidMineMissed3(self):
        c = self.createCuboid('a....\n.....\n.....\n.....\n...a..*\n')
        self.assertEqual(c.mine_missed(), True)


class CuboidNumMinesTests(unittest.TestCase):
    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

    def testCuboidNumMines1(self):
        c = self.createCuboid('a')
        self.assertEqual(c.num_mines(), 1)

    def testCuboidNumMines2(self):
        c = self.createCuboid('ggZgg\nabcde\nZaaaZ\nABCDE\naaZaa\n')
        self.assertEqual(c.num_mines(), 25)

    def testCuboidNumMines3(self):
        c = self.createCuboid('..Z..\n.....\nZ...Z\n.....\n..Z..\n')
        self.assertEqual(c.num_mines(), 4)


class CuboidMoveTests(unittest.TestCase):
    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

    def testCuboidMove1(self):
        c = self.createCuboid('a')
        c.move(*(0, -1))
        self.assertEqual(c.ship_position[0], 0)
        self.assertEqual(c.ship_position[1], -1)

    def testCuboidMove2(self):
        c = self.createCuboid('a')
        c.move(*(0, 1))
        self.assertEqual(c.ship_position[0], 0)
        self.assertEqual(c.ship_position[1], 1)

    def testCuboidMove3(self):
        c = self.createCuboid('a')
        c.move(*(1, 0))
        self.assertEqual(c.ship_position[0], 1)
        self.assertEqual(c.ship_position[1], 0)

    def testCuboidMove4(self):
        c = self.createCuboid('a')
        c.move(*(-1, 0))
        self.assertEqual(c.ship_position[0], -1)
        self.assertEqual(c.ship_position[1], 0)

    def testCuboidMove5(self):
        c = self.createCuboid('..Z..\n.....\nZ...Z\n.....\n..Z..\n')
        c.move(*(0, -1))
        self.assertEqual(c.ship_position[0], 2)
        self.assertEqual(c.ship_position[1], 1)

    def testCuboidMove6(self):
        c = self.createCuboid('..Y..\n.....\nY...Y\n.....\n..Y..\n')
        c.ship_position[0], c.ship_position[1] = 2, 1
        c.move(*(0, 1))
        self.assertEqual(c.ship_position[0], 2)
        self.assertEqual(c.ship_position[1], 2)

    def testCuboidMove7(self):
        c = self.createCuboid('.....\n.....\nX...X\n.....\n..X..\n')
        c.ship_position[0], c.ship_position[1] = 2, 2
        c.move(*(1, 0))
        self.assertEqual(c.ship_position[0], 3)
        self.assertEqual(c.ship_position[1], 2)

    def testCuboidMove8(self):
        c = self.createCuboid('.....\n.....\nW...W\n.....\n..W..\n')
        c.ship_position[0], c.ship_position[1] = 2, 2
        c.move(*(-1, 0))
        self.assertEqual(c.ship_position[0], 1)
        self.assertEqual(c.ship_position[1], 2)

class CuboidFireTests(unittest.TestCase):
    def setUp(self):
        self.fire_dict = {'alpha': [(-1, -1), (1, -1), (1, 1), (-1, 1)],
                          'beta': [(-1, 0), (1, 0), (0, -1), (0, 1)],
                          'gamma': [(0, -1), (0, 0), (0, 1)],
                          'delta': [(-1, 0), (0, 0), (1, 0)]}

    def createCuboid(self, cuboid_str):
        c = Cuboid()
        for row in map(list, cuboid_str.split()):
            c.add_row(row)
        return c

    def testFire1(self):
        c = self.createCuboid('a')
        c.fire(self.fire_dict['alpha'])
        expected = [['a']]
        self.assertEqual(c.matrix, expected)

    def testFire2(self):
        c = self.createCuboid('a')
        c.fire(self.fire_dict['beta'])
        expected = [['a']]
        self.assertEqual(c.matrix, expected)

    def testFire3(self):
        c = self.createCuboid('a')
        c.fire(self.fire_dict['gamma'])
        expected = [['.']]
        self.assertEqual(c.matrix, expected)
        self.assertEqual(c.mines, [])

    def testFire4(self):
        c = self.createCuboid('a')
        c.fire(self.fire_dict['delta'])
        expected = [['.']]
        self.assertEqual(c.matrix, expected)
        self.assertEqual(c.mines, [])

    def testFire5(self):
        c = self.createCuboid('..Y..\n.....\nY...Y\n.....\n..Y..\n')
        expected_matrix = map(list,
                              '.....\n.....\nY...Y\n.....\n..Y..\n'.split())
        expected_mines = [(2, 0), (2, 4), (4, 2)]
        c.ship_position[0], c.ship_position[1] = 1, 2
        c.fire(self.fire_dict['delta'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire6(self):
        c = self.createCuboid('.....\n.....\nY...Y\n.....\n..Y..\n')
        expected_matrix = map(list,
                              '.....\n.....\n....Y\n.....\n..Y..\n'.split())
        expected_mines = [(2, 4), (4, 2)]
        c.ship_position[0], c.ship_position[1] = 2, -1
        c.fire(self.fire_dict['gamma'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire7(self):
        c = self.createCuboid('.....\n.....\n....Y\n.....\n..Y..\n')
        expected_matrix = map(list,
                              '.....\n.....\n....Y\n.....\n.....\n'.split())
        expected_mines = [(2, 4)]
        c.ship_position[0], c.ship_position[1] = 5, 2
        c.fire(self.fire_dict['delta'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire8(self):
        c = self.createCuboid('.....\n.....\n....Y\n.....\n..Y..\n')
        expected_matrix = map(list,
                              '.....\n.....\n....Y\n.....\n.....\n'.split())
        expected_mines = [(2, 4)]
        c.ship_position[0], c.ship_position[1] = 5, 3
        c.fire(self.fire_dict['alpha'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire9(self):
        c = self.createCuboid('.....\n.....\n....Y\n.....\n..Y..\n')
        expected_matrix = map(list,
                              '.....\n.....\n....Y\n.....\n.....\n'.split())
        expected_mines = [(2, 4)]
        c.ship_position[0], c.ship_position[1] = 5, 2
        c.fire(self.fire_dict['beta'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire10(self):
        c = self.createCuboid('a.a\n...\na.a\n')
        expected_matrix = map(list, '...\n...\n...\n'.split())
        expected_mines = []
        c.fire(self.fire_dict['alpha'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire11(self):
        c = self.createCuboid('a.a\n...\na.a\n')
        expected_matrix = map(list, '..a\n...\na.a\n'.split())
        expected_mines = [(0, 2), (2, 0), (2, 2)]
        c.ship_position[0], c.ship_position[1] = -1, -1
        c.fire(self.fire_dict['alpha'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire12(self):
        c = self.createCuboid('a.a\n...\na.a\n')
        expected_matrix = map(list, '..a\n...\na.a\n'.split())
        expected_mines = [(0, 2), (2, 0), (2, 2)]
        c.ship_position[0], c.ship_position[1] = -1, 0
        c.fire(self.fire_dict['beta'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire13(self):
        c = self.createCuboid('a.a\n...\na.a\n')
        expected_matrix = map(list, 'a..\n...\na.a\n'.split())
        expected_mines = [(0, 0), (2, 0), (2, 2)]
        c.ship_position[0], c.ship_position[1] = -1, 3
        c.fire(self.fire_dict['alpha'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire14(self):
        c = self.createCuboid('a.a\n...\na.a\n')
        expected_matrix = map(list, 'a..\n...\na..\n'.split())
        expected_mines = [(0, 0), (2, 0)]
        c.ship_position[0], c.ship_position[1] = 1, 2
        c.fire(self.fire_dict['delta'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire15(self):
        c = self.createCuboid('.a.\na.a\n.a.\n')
        expected_matrix = map(list, '...\n...\n...\n'.split())
        expected_mines = []
        c.fire(self.fire_dict['beta'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire16(self):
        c = self.createCuboid('.a.\n.a.\n.a.\n')
        expected_matrix = map(list, '...\n...\n...\n'.split())
        expected_mines = []
        c.fire(self.fire_dict['delta'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)

    def testFire17(self):
        c = self.createCuboid('...\naaa\n...\n')
        expected_matrix = map(list, '...\n...\n...\n'.split())
        expected_mines = []
        c.fire(self.fire_dict['gamma'])
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)



if __name__ == '__main__':
    unittest.main()

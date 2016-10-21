import unittest

from mineclearing import *


class CuboidTest(unittest.TestCase):
    def testCuboidInit1(self):
        cuboidStr = '..Z..\n.Z..Z\n.ZZZ.\n'
        c = Cuboid(cuboidStr)
        expected_grid = [list(line) for line in cuboidStr.split()]
        expected_numMines = 6
        self.assertEqual(c.grid, expected_grid)
        self.assertEqual(c.numMines, expected_numMines)


class GameTest(unittest.TestCase):
    def testGameInit1(self):
        g = Game('')
        self.assertEqual(g.score, 0)

    def testGameInit2(self):
        g = Game('..Z..\n.Z..Z\n.ZZZ.\n')
        self.assertEqual(g.score, 60)

if __name__ == '__main__':
    unittest.main()

import unittest

from mineclearing import *


class CuboidTest(unittest.TestCase):
    def testCuboidInit1(self):
        cuboidStr = '..Z..\n.Z..Z\n.ZZZ.\n'
        c = Cuboid(cuboidStr)
        expected_grid = [list(line) for line in cuboidStr.split()]
        expected_minePosList = [[0, 2], [1, 1], [1, 4], [2, 1], [2, 2], [2, 3]]
        self.assertEqual(c.grid, expected_grid)
        self.assertEqual(c.minePosList, expected_minePosList)
        self.assertEqual(c.numRows, 3)
        self.assertEqual(c.numCols, 5)

    def testCuboidInit2(self):
        cuboidStr = '.....\n.Z..Z\n.ZZZ.\n'
        c = Cuboid(cuboidStr)
        expected_grid = [list(line) for line in cuboidStr.split()]
        expected_minePosList = [[1, 1], [1, 4], [2, 1], [2, 2], [2, 3]]
        self.assertEqual(c.grid, expected_grid)
        self.assertEqual(c.minePosList, expected_minePosList)
        self.assertEqual(c.numRows, 3)
        self.assertEqual(c.numCols, 5)

    def testCuboidInit3(self):
        cuboidStr = '.....\n.a.b.\n.z....\n.d.c.\n..z..\n'
        c = Cuboid(cuboidStr)
        expected_grid = [list(line) for line in cuboidStr.split()]
        expected_minePosList = [[1, 1], [1, 3], [2, 1], [3, 1], [3, 3], [4, 2]]
        self.assertEqual(c.grid, expected_grid)
        self.assertEqual(c.minePosList, expected_minePosList)
        self.assertEqual(c.numRows, 5)
        self.assertEqual(c.numCols, 5)


"""
class SimulationTest(unittest.TestCase):
    def testSimulationInit1(self):
        s = Simulation('a')
        self.assertEqual(s.score, 10)

    def testSimulationInit2(self):
        s = Simulation('..Z..\n.Z..Z\n.ZZZ.\n')
        self.assertEqual(s.score, 60)
"""

if __name__ == '__main__':
    unittest.main()

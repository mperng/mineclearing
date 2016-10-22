import unittest

from mineclearing import *


class CuboidTest(unittest.TestCase):
    def testCuboidInit1(self):
        cuboidStr = '..Z..\n.Z..Z\n.ZZZ.\n'
        c = Cuboid(cuboidStr)
        expected_matrix = [list(line) for line in cuboidStr.split()]
        expected_mines = [[0, 2], [1, 1], [1, 4], [2, 1], [2, 2], [2, 3]]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.numRows, 3)
        self.assertEqual(c.numCols, 5)
        self.assertEqual(c.shipPos, [1, 2])

    def testCuboidInit2(self):
        cuboidStr = '.....\n.Z..Z\n.ZZZ.\n'
        c = Cuboid(cuboidStr)
        expected_matrix = [list(line) for line in cuboidStr.split()]
        expected_mines = [[1, 1], [1, 4], [2, 1], [2, 2], [2, 3]]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.numRows, 3)
        self.assertEqual(c.numCols, 5)
        self.assertEqual(c.shipPos, [1, 2])

    def testCuboidInit3(self):
        cuboidStr = '.....\n.a.b.\n.z...\n.d.c.\n..z..\n'
        c = Cuboid(cuboidStr)
        expected_matrix = [list(line) for line in cuboidStr.split()]
        expected_mines = [[1, 1], [1, 3], [2, 1], [3, 1], [3, 3], [4, 2]]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.numRows, 5)
        self.assertEqual(c.numCols, 5)
        self.assertEqual(c.shipPos, [2, 2])

    def testCuboidInit4(self):
        cuboidStr = 'a'
        c = Cuboid(cuboidStr)
        expected_matrix = [list(line) for line in cuboidStr.split()]
        expected_mines = [[0, 0]]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.numRows, 1)
        self.assertEqual(c.numCols, 1)
        self.assertEqual(c.shipPos, [0, 0])

    def testCuboidInit5(self):
        cuboidStr = 'a...a'
        c = Cuboid(cuboidStr)
        expected_matrix = [list(line) for line in cuboidStr.split()]
        expected_mines = [[0, 0], [0, 4]]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.numRows, 1)
        self.assertEqual(c.numCols, 5)
        self.assertEqual(c.shipPos, [0, 2])

    def testCuboidInit6(self):
        cuboidStr = '..Z..\n.....\nZ...Z\n.....\n..Z..\n'
        c = Cuboid(cuboidStr)
        expected_matrix = [list(line) for line in cuboidStr.split()]
        expected_mines = [[0, 2], [2, 0], [2, 4], [4, 2]]
        self.assertEqual(c.matrix, expected_matrix)
        self.assertEqual(c.mines, expected_mines)
        self.assertEqual(c.numRows, 5)
        self.assertEqual(c.numCols, 5)
        self.assertEqual(c.shipPos, [2, 2])

    def testCuboidInBounds1(self):
        c = Cuboid('a')
        self.assertEqual(c.inBounds(-1, -1), False)
        self.assertEqual(c.inBounds(-1, 0), False)
        self.assertEqual(c.inBounds(0, -1), False)
        self.assertEqual(c.inBounds(0, 1), False)
        self.assertEqual(c.inBounds(1, 0), False)
        self.assertEqual(c.inBounds(1, 1), False)
        self.assertEqual(c.inBounds(0, 0), True)

    def testCuboidInBounds2(self):
        c = Cuboid('..Z..\n.....\nZ...Z\n.....\n..Z..\n')
        for x in xrange(c.numRows):
            for y in xrange(c.numCols):
                self.assertEqual(c.inBounds(x, y), True)
        self.assertEqual(c.inBounds(-1, -1), False)
        self.assertEqual(c.inBounds(-1, 0), False)
        self.assertEqual(c.inBounds(0, -1), False)
        self.assertEqual(c.inBounds(c.numRows, 0), False)
        self.assertEqual(c.inBounds(0, c.numCols), False)




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

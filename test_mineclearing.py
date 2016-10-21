import unittest

from mineclearing import *


class CuboidTest(unittest.TestCase):
    def testCuboidInit1(self):
        c = Cuboid()


class GameTest(unittest.TestCase):
    def testGameInit1(self):
        g = Game(0)
        self.assertEqual(g.numMines, 0)
        self.assertEqual(g.score, 0)

    def testGameInit2(self):
        g = Game(1)
        self.assertEqual(g.numMines, 1)
        self.assertEqual(g.score, 10)

if __name__ == '__main__':
    unittest.main()

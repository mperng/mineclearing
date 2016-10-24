import unittest

from cuboid import Cuboid
from simulation import Simulation


class SimulationCreateTests(unittest.TestCase):
    def setUp(self):
        self.expected_move_dict = {'north': (-1, 0), 'south': (1, 0),
                                   'east': (0, 1), 'west': (0, -1)}
        self.expected_fire_dict = {
                          'alpha': [(-1, -1), (1, -1), (1, 1), (-1, 1)],
                          'beta': [(-1, 0), (1, 0), (0, -1), (0, 1)],
                          'gamma': [(0, -1), (0, 0), (0, 1)],
                          'delta': [(-1, 0), (0, 0), (1, 0)]}

    def testSimulationInit1(self):
        s = Simulation(script='gamma\n', cuboid=Cuboid())
        self.assertIsNotNone(s.cuboid)
        self.assertEqual(s.script, ['gamma'])
        self.assertEqual(s.step_num, 0)
        self.assertEqual(s.num_moves, 0)
        self.assertEqual(s.num_volleys, 0)
        self.assertEqual(s.initial_num_mines, 0)
        self.assertEqual(s.score, 0)
        self.assertEqual(s.move_dict, self.expected_move_dict)
        self.assertEqual(s.fire_dict, self.expected_fire_dict)

    def testSimulationInit2(self):
        s = Simulation(script='gamma\n', cuboid=Cuboid('a\n'))
        self.assertIsNotNone(s.cuboid)
        self.assertEqual(s.script, ['gamma'])
        self.assertEqual(s.step_num, 0)
        self.assertEqual(s.num_moves, 0)
        self.assertEqual(s.num_volleys, 0)
        self.assertEqual(s.initial_num_mines, 1)
        self.assertEqual(s.score, 10)
        self.assertEqual(s.move_dict, self.expected_move_dict)
        self.assertEqual(s.fire_dict, self.expected_fire_dict)

    def testSimulationInit3(self):
        s = Simulation(script='gamma\n', cuboid=Cuboid('.a.\nZ..b\nc..\n'))
        self.assertIsNotNone(s.cuboid)
        self.assertEqual(s.script, ['gamma'])
        self.assertEqual(s.step_num, 0)
        self.assertEqual(s.num_moves, 0)
        self.assertEqual(s.num_volleys, 0)
        self.assertEqual(s.initial_num_mines, 4)
        self.assertEqual(s.score, 40)
        self.assertEqual(s.move_dict, self.expected_move_dict)
        self.assertEqual(s.fire_dict, self.expected_fire_dict)

    def testSimulationInit4(self):
        s = Simulation(script='gamma west\ndelta\n',
                       cuboid=Cuboid('.a.\nZ..b\nc..\n'))
        self.assertIsNotNone(s.cuboid)
        self.assertEqual(s.script, ['gamma west', 'delta'])
        self.assertEqual(s.step_num, 0)
        self.assertEqual(s.num_moves, 0)
        self.assertEqual(s.num_volleys, 0)
        self.assertEqual(s.initial_num_mines, 4)
        self.assertEqual(s.score, 40)
        self.assertEqual(s.move_dict, self.expected_move_dict)
        self.assertEqual(s.fire_dict, self.expected_fire_dict)


class SimulationGetScoreTests(unittest.TestCase):
    def testGetScore1(self):
        s = Simulation('', Cuboid('a'))
        self.assertEqual(s.get_score(), 'fail 0')

    def testGetScore2(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 1
        self.assertEqual(s.get_score(), 'pass 1')

    def testGetScore3(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 2
        s.initial_num_mines = 1
        s.score = 10
        self.assertEqual(s.get_score(), 'pass 10')

    def testGetScore4(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 2
        s.initial_num_mines = 1
        s.score = 10
        s.num_volleys = 10
        self.assertEqual(s.get_score(), 'pass 5')

    def testGetScore5(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_volleys = 2
        self.assertEqual(s.get_score(), 'pass 20')

    def testGetScore6(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_moves = 10
        self.assertEqual(s.get_score(), 'pass 21')

    def testGetScore7(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_moves = 1
        self.assertEqual(s.get_score(), 'pass 28')

    def testGetScore8(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_volleys = 1
        s.num_moves = 1
        self.assertEqual(s.get_score(), 'pass 23')

    def testGetScore9(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_volleys = 2
        s.num_moves = 1
        self.assertEqual(s.get_score(), 'pass 18')

    def testGetScore10(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.'))
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_volleys = 3
        s.num_moves = 4
        self.assertEqual(s.get_score(), 'pass 7')


class SimulationEndConditionTests(unittest.TestCase):
    def testEndCondition1(self):
        s = Simulation('gamma\n', Cuboid('.'))
        s.step_num = 0
        self.assertEqual(s.end_condition(), True)

    def testEndCondition2(self):
        s = Simulation('gamma\n',
                       Cuboid('..a..\n.....\n.....\n.....\n..a..\n'))
        s.step_num = 1
        self.assertEqual(s.end_condition(), True)

    def testEndCondition3(self):
        s = Simulation('gamma\n', Cuboid('*\n.\n.\n.\n*\n'))
        self.assertEqual(s.end_condition(), True)

    def testEndCondition4(self):
        s = Simulation('gamma\ndelta\n', Cuboid('*\n.\n.\n.\na\n'))
        self.assertEqual(s.end_condition(), True)

    def testEndCondition5(self):
        s = Simulation('gamma\ndelta\n', Cuboid('*\n.\n.\n.\na\n'))
        self.assertEqual(s.end_condition(), True)

    def testEndCondition6(self):
        s = Simulation('gamma\ndelta\n', Cuboid('.....\n.....\n.....\n.....\n'
                                                '.....\n'))
        self.assertEqual(s.end_condition(), True)

import unittest

from StringIO import StringIO

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
        s = Simulation('gamma\n', '.')
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
        s = Simulation('gamma\n', 'a\n')
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
        s = Simulation('gamma\n', '.a.\nZ..b\nc..\n')
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
        s = Simulation('gamma west\ndelta\n', '.a.\nZ..b\nc..\n')
        self.assertIsNotNone(s.cuboid)
        self.assertEqual(s.script, ['gamma west', 'delta'])
        self.assertEqual(s.step_num, 0)
        self.assertEqual(s.num_moves, 0)
        self.assertEqual(s.num_volleys, 0)
        self.assertEqual(s.initial_num_mines, 4)
        self.assertEqual(s.score, 40)
        self.assertEqual(s.move_dict, self.expected_move_dict)
        self.assertEqual(s.fire_dict, self.expected_fire_dict)


class SimulationRunScriptTests(unittest.TestCase):
        def testRunScript1(self):
            s = Simulation('gamma\n', 'z\n')
            o = StringIO()
            s.run_script(out=o)
            expected = 'Step 1\n\nz\n\ngamma\n\n.\n\npass (5)\n\n'
            actual = o.getvalue()
            self.assertEqual(expected, actual)

        def testRunScript2(self):
            s = Simulation('gamma\nnorth alpha\n', 'z\n')
            o = StringIO()
            s.run_script(out=o)
            expected = 'Step 1\n\nz\n\ngamma\n\n.\n\npass (1)\n\n'
            actual = o.getvalue()
            self.assertEqual(expected, actual)

        def testRunScript3(self):
            script = 'north\ndelta south\nsouth\nsouth\ndelta\n'
            field = '..a..\n.....\n.....\n.....\n..a..\n'
            s = Simulation(script, field)
            o = StringIO()
            s.run_script(out=o)
            expected = 'Step 1\n\n' \
                       'a\n.\n.\n.\na\n\n' \
                       'north\n\n' \
                       '.\n.\n*\n.\n.\n.\n*\n\n' \
                       'fail (0)\n\n'
            actual = o.getvalue()
            self.assertEqual(expected, actual)

        def testRunScript4(self):
            script = 'north\ndelta south\nwest\ngamma east\neast\ngamma west\n'\
                     'south\ndelta\n'
            field = '..Z..\n.....\nZ...Z\n.....\n..Z..\n'
            s = Simulation(script, field)
            o = StringIO()
            s.run_script(out=o)
            expected = 'Step 1\n\n'\
                       '..Z..\n.....\nZ...Z\n.....\n..Z..\n\n'\
                       'north\n\n'\
                       '.....\n.....\n..Y..\n.....\nY...Y\n.....\n..Y..\n\n'\
                       'Step 2\n\n'\
                       '.....\n.....\n..Y..\n.....\nY...Y\n.....\n..Y..\n\n'\
                       'delta south\n\n'\
                       '.....\n.....\nX...X\n.....\n..X..\n\n'\
                       'Step 3\n\n'\
                       '.....\n.....\nX...X\n.....\n..X..\n\n'\
                       'west\n\n'\
                       '.......\n.......\n..W...W\n.......\n....W..\n\n'\
                       'Step 4\n\n'\
                       '.......\n.......\n..W...W\n.......\n....W..\n\n'\
                       'gamma east\n\n'\
                       '.....\n.....\n....V\n.....\n..V..\n\n'\
                       'Step 5\n\n'\
                       '.....\n.....\n....V\n.....\n..V..\n\n'\
                       'east\n\n'\
                       '...\n...\n..U\n...\nU..\n\n'\
                       'Step 6\n\n'\
                       '...\n...\n..U\n...\nU..\n\n'\
                       'gamma west\n\n'\
                       '.\n.\n.\n.\nT\n\n'\
                       'Step 7\n\n'\
                       '.\n.\n.\n.\nT\n\n'\
                       'south\n\n'\
                       '.\n.\nS\n\n'\
                       'Step 8\n\n'\
                       '.\n.\nS\n\n'\
                       'delta\n\n'\
                       '.\n\n'\
                       'pass (8)\n\n'
            actual = o.getvalue()
            print actual
            self.assertEqual(expected, actual)

        def testRunScript5(self):
            script = 'north\ndelta south\nwest\ngamma east\neast\ngamma west\n'
            field = '..Z..\n.....\nZ...Z\n.....\n..Z..\n'
            s = Simulation(script, field)
            o = StringIO()
            s.run_script(out=o)
            expected = 'Step 1\n\n'\
                       '..Z..\n.....\nZ...Z\n.....\n..Z..\n\n'\
                       'north\n\n'\
                       '.....\n.....\n..Y..\n.....\nY...Y\n.....\n..Y..\n\n'\
                       'Step 2\n\n'\
                       '.....\n.....\n..Y..\n.....\nY...Y\n.....\n..Y..\n\n'\
                       'delta south\n\n'\
                       '.....\n.....\nX...X\n.....\n..X..\n\n'\
                       'Step 3\n\n'\
                       '.....\n.....\nX...X\n.....\n..X..\n\n'\
                       'west\n\n'\
                       '.......\n.......\n..W...W\n.......\n....W..\n\n'\
                       'Step 4\n\n'\
                       '.......\n.......\n..W...W\n.......\n....W..\n\n'\
                       'gamma east\n\n'\
                       '.....\n.....\n....V\n.....\n..V..\n\n'\
                       'Step 5\n\n'\
                       '.....\n.....\n....V\n.....\n..V..\n\n'\
                       'east\n\n'\
                       '...\n...\n..U\n...\nU..\n\n'\
                       'Step 6\n\n'\
                       '...\n...\n..U\n...\nU..\n\n'\
                       'gamma west\n\n'\
                       '.\n.\n.\n.\nT\n\n'\
                       'fail (0)\n\n'
            actual = o.getvalue()
            print actual
            self.assertEqual(expected, actual)


class SimulationRunCmdTests(unittest.TestCase):
    def testRunCmd1(self):
        s = Simulation('gamma\n', 'a')
        self.assertEqual(str(s.cuboid), 'a')
        s.run_cmd('north')
        self.assertEqual(str(s.cuboid), '.\n.\na')

    def testRunCmd2(self):
        s = Simulation('gamma\n', 'a')
        self.assertEqual(str(s.cuboid), 'a')
        s.run_cmd('gamma')
        self.assertEqual(str(s.cuboid), '.')

    def testRunCmd3(self):
        s = Simulation('gamma\n', 'a')
        self.assertEqual(str(s.cuboid), 'a')
        s.run_cmd('gamma')
        self.assertEqual(str(s.cuboid), '.')

    def testRunCmd4(self):
        s = Simulation('gamma\n', 'aaa')
        self.assertEqual(str(s.cuboid), 'aaa')
        s.run_cmd('gamma')
        self.assertEqual(str(s.cuboid), '.')

    def testRunCmd5(self):
        s = Simulation('gamma\n', 'aaa\naaa\naaa')
        self.assertEqual(str(s.cuboid), 'aaa\naaa\naaa')
        s.run_cmd('alpha')
        self.assertEqual(str(s.cuboid), '.a.\naaa\n.a.')

    def testRunCmd6(self):
        s = Simulation('gamma\n', 'aaa\naaa\naaa')
        self.assertEqual(str(s.cuboid), 'aaa\naaa\naaa')
        s.run_cmd('beta')
        self.assertEqual(str(s.cuboid), 'a.a\n.a.\na.a')

    def testRunCmd7(self):
        s = Simulation('gamma\n', 'a')
        self.assertEqual(str(s.cuboid), 'a')
        s.run_cmd('west')
        self.assertEqual(str(s.cuboid), '..a')

    def testRunCmd8(self):
        s = Simulation('gamma\n', 'a')
        self.assertEqual(str(s.cuboid), 'a')
        s.run_cmd('east')
        self.assertEqual(str(s.cuboid), 'a..')

    def testRunCmd9(self):
        s = Simulation('gamma\n', 'a')
        self.assertEqual(str(s.cuboid), 'a')
        s.run_cmd('south')
        self.assertEqual(str(s.cuboid), 'a\n.\n.')

    def testRunCmd10(self):
        script = 'north\ndelta south\nsouth\nsouth\ndelta\n'
        field = '..a..\n.....\n.....\n.....\n..a..\n'
        s = Simulation(script, field)
        self.assertEqual(str(s.cuboid), 'a\n.\n.\n.\na')
        s.run_cmd('north')
        self.assertEqual(str(s.cuboid), '.\n.\na\n.\n.\n.\na')


class SimulationGetScoreTests(unittest.TestCase):
    def testGetScore1(self):
        s = Simulation('west\n', 'a')
        s.step_num = 1
        self.assertEqual(s.get_score(), 'fail (0)')

    def testGetScore2(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 1
        self.assertEqual(s.get_score(), 'pass (1)')

    def testGetScore3(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 2
        s.initial_num_mines = 1
        s.score = 10
        self.assertEqual(s.get_score(), 'pass (10)')

    def testGetScore4(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 2
        s.initial_num_mines = 1
        s.score = 10
        s.num_volleys = 10
        self.assertEqual(s.get_score(), 'pass (5)')

    def testGetScore5(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_volleys = 2
        self.assertEqual(s.get_score(), 'pass (20)')

    def testGetScore6(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_moves = 10
        self.assertEqual(s.get_score(), 'pass (21)')

    def testGetScore7(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_moves = 1
        self.assertEqual(s.get_score(), 'pass (28)')

    def testGetScore8(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_volleys = 1
        s.num_moves = 1
        self.assertEqual(s.get_score(), 'pass (23)')

    def testGetScore9(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_volleys = 2
        s.num_moves = 1
        self.assertEqual(s.get_score(), 'pass (18)')

    def testGetScore10(self):
        s = Simulation('gamma\ndelta\n', '.')
        s.step_num = 2
        s.initial_num_mines = 3
        s.score = 30
        s.num_volleys = 3
        s.num_moves = 4
        self.assertEqual(s.get_score(), 'pass (7)')


class SimulationEndConditionTests(unittest.TestCase):
    def testEndCondition1(self):
        s = Simulation('gamma\n', '.')
        s.step_num = 0
        self.assertEqual(s.end_condition(), True)

    def testEndCondition2(self):
        s = Simulation('gamma\n', '..a..\n.....\n.....\n.....\n..a..\n')
        s.step_num = 1
        self.assertEqual(s.end_condition(), True)

    def testEndCondition3(self):
        s = Simulation('gamma\n', '*\n.\n.\n.\n*\n')
        self.assertEqual(s.end_condition(), True)

    def testEndCondition4(self):
        s = Simulation('gamma\ndelta\n', '*\n.\n.\n.\na\n')
        self.assertEqual(s.end_condition(), True)

    def testEndCondition5(self):
        s = Simulation('gamma\ndelta\n', '*\n.\n.\n.\na\n')
        self.assertEqual(s.end_condition(), True)

    def testEndCondition6(self):
        s = Simulation('gamma\ndelta\n', '.....\n.....\n.....\n.....\n.....\n')
        self.assertEqual(s.end_condition(), True)

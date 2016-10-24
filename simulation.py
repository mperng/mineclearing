from cuboid import Cuboid


class Simulation(object):
    '''
    A class representing a simulation of a mine-clearing script
    '''
    def __init__(self, script, cuboid):
        self.script = script.strip().split('\n')
        self.cuboid = cuboid
        self.step_num = 0
        self.num_moves, self.num_volleys = 0, 0
        self.initial_num_mines = self.cuboid.num_mines()
        self.score = 10 * self.initial_num_mines
        self.move_dict = {'north': (-1, 0), 'south': (1, 0),
                          'east': (0, 1), 'west': (0, -1)}
        self.fire_dict = {'alpha': [(-1, -1), (1, -1), (1, 1), (-1, 1)],
                          'beta': [(-1, 0), (1, 0), (0, -1), (0, 1)],
                          'gamma': [(0, -1), (0, 0), (0, 1)],
                          'delta': [(-1, 0), (0, 0), (1, 0)]}

    def run_script(self, script):
        '''
        Runs the script while printing output and
        prints the Simulation score at the end.
        '''
        def _print_str(self, s):
            print '{}\n'.format(s)
        while not self.end_condition():
            _print_str('Step {}'.format(self.step_num + 1))
            _print_str(self.c)
            _print_str(self.script[self.step_num])
            for cmd in self.script[self.step_num]:
                self.run_cmd(cmd)
            self.step_num += 1
            _print_str(self.c)
        _print_str(self.get_score())

    def run_cmd(self, cmd):
        '''
        Run an individual command against the Cuboid.
        Assuming num_volleys means the number of fire commands issued.
        '''
        if cmd in move_dict:
            self.cuboid.move(move_dict[cmd])
            self.num_moves += 1
        elif cmd in fire_dict:
            self.cuboid.fire(*fire_dict[cmd])
            self.num_volleys += 1
        else:
            print 'invalid command'

    def get_score(self):
        '''
        Calculate score as initial score - volley penalty - move penalty
        '''
        if self.cuboid.num_mines():
            return 'fail 0'
        elif self.step_num < len(self.script):
            return 'pass 1'
        else:
            volley_penalty = min(5 * self.num_volleys,
                                 5 * self.initial_num_mines)
            move_penalty = min(2 * self.num_moves,
                               3 * self.initial_num_mines)
            return 'pass {}'.format(self.score - volley_penalty - move_penalty)

    def end_condition(self):
        '''
        Return True if an end condition for the Simulation is reached.
        '''
        return self.cuboid.mine_missed() or self.cuboid.num_mines() == 0 or \
            self.step_num >= len(self.script)

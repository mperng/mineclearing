from cuboid import Cuboid


class Simulation(object):
    '''
    A class representing a simulation of a mine-clearing script
    '''
    def __init__(self, cuboid):
        self.volleys_fired = 0
        self.cuboid = cuboid
        self.score = 10 * self.cuboid.num_mines()
        self.move_dict = {'north': (-1, 0), 'south': (1, 0),
                          'east': (0, 1), 'west': (0, -1)}
        self.fire_dict = {'alpha': [(-1, -1), (1, -1), (1, 1), (-1, 1)],
                          'beta': [(-1, 0), (1, 0), (0, -1), (0, 1)],
                          'gamma': [(0, -1), (0, 0), (0, 1)],
                          'delta': [(-1, 0), (0, 0), (1, 0)]}

    def run(self, script_step):
        '''
        Run the script until an end condition has been reached
        '''
        for cmd in list(script_steps):
            self.run_cmd(cmd)

    def run_cmd(self, cmd):
        if cmd in move_dict:
            c.move(move_dict[cmd])
        elif cmd in fire_dict:
            c.fire(*fire_dict[cmd])
            self.volleys_fired += 1
        else:
            print 'invalid command'

    def evaluate(self):
        '''
        Evaluate if an end condition has been reached.
        '''
        pass

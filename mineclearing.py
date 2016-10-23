from cuboid import Cuboid
from simulation import Simulation

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python mineclearing.py \
                         /path/to/cuboid_file.txt /path/to/script_file.txt')
    with open(sys.argv[0], 'r'), open(sys.argv[1]) as cuboid_file, script_file:
        c = Cuboid()
        cuboid_row = next(cuboid_file, None)
        while cuboid_row:
            c.add_row(cuboid_row)
            cuboid_row = next(cuboid_file, None)
        s = Simulation(c)
        script_step = next(script_file, None)
        while script_step:
            s.run(script_step.split(' '))
            script_step = next(script_file, None)

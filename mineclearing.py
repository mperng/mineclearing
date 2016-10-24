from cuboid import Cuboid
from simulation import Simulation

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python mineclearing.py \
                         /path/to/cuboid_file.txt /path/to/script_file.txt')
    with open(sys.argv[0], 'r'), open(sys.argv[1]) as cuboid_file, script_file:
        s = Simulation(Cuboid(cuboid_file.read()), script_file.read())
        s.run_script()

import sys

from cuboid import Cuboid
from simulation import Simulation

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python mineclearing.py'
                         '/path/to/field_file.txt /path/to/script_file.txt')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'r') as s:
        s = Simulation(script=s.read(), field=f.read())
        s.run_script()

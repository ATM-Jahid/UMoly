import argparse

parser = argparse.ArgumentParser(description='replicate lammps input files')
parser.add_argument('-x', '--xdim', metavar='', help='half length of x dimension')
parser.add_argument('-y', '--ydim', metavar='', help='half length of y dimension')
parser.add_argument('-z', '--zdim', metavar='', help='half length of z dimension')
parser.add_argument('-l', '--LATT', default='3.14', metavar='', help='lattice constant')
parser.add_argument('-p', '--run', default='3', metavar='', help='tilt run')
parser.add_argument('-q', '--rise', default='1', metavar='', help='tilt rise')
parser.add_argument('-Mo', '--portion', default='0.22', metavar='', help='Molybdenum portion')
parser.add_argument('-s', '--SEED', metavar='', help='random seed')
parser.add_argument('-t', '--temper', default='1200', metavar='', help='temperature in kelvin')
parser.add_argument('-f', '--fileName', default='GB', metavar='', help='replicated file name')
args = parser.parse_args()

with open('in.grain') as f:
    jar = f.read()

jar = jar.replace('xdim', '{}'.format(args.xdim), 1)
jar = jar.replace('ydim', '{}'.format(args.ydim), 1)
jar = jar.replace('zdim', '{}'.format(args.zdim), 1)
jar = jar.replace('LATT', '{}'.format(args.LATT), 1)
jar = jar.replace('run', '{}'.format(args.run), 1)
jar = jar.replace('rise', '{}'.format(args.rise), 1)
jar = jar.replace('portion', '{}'.format(args.portion), 1)
jar = jar.replace('SEED', '{}'.format(args.SEED), 1)
jar = jar.replace('temper', '{}'.format(args.temper), 1)

with open('in.{}'.format(args.fileName), 'w') as f:
    f.write(jar)

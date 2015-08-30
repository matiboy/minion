"""mode2 to binary.

Usage:
  mode2_to_binary.py <source>

"""
from docopt import docopt

def closest(test, low, high):
    if abs(low - test) < abs(high - test):
      return low
    return high

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Mode2 to binary')
    source = arguments['<source>']
    with open(source, 'r') as f:
        zeroes = []
        ones = []

        for r in f.readlines():
            values = r.strip().split()
            for i, v in enumerate(values):
                v = int(v)
                if i % 2:
                    ones.append(v)
                else:
                    zeroes.append(v)
    a_zero = int(sum(zeroes, 0.0) / len(zeroes))

    real_ones = filter(lambda x: x < 0.75*a_zero or x>1.25*a_zero, ones)

    a_one = int(sum(real_ones, 0.0) / len(real_ones))

    print real_ones

    print a_zero, a_one


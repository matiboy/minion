"""Binary to mode2.

Usage:
  binary_to_mode2.py <value> [--low=530] [--high=1100] [--columnwidth=9]

"""
from docopt import docopt

def closest(test, low, high):
    if abs(low - test) < abs(high - test):
      return low
    return high

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Binary to mode2')
    if arguments['--low'] is None:
        low = '530'
    else:
        low = arguments['--low']
    if arguments['--high'] is None:
        high = '1100'
    else:
        high = arguments['--high']
    if arguments['--columnwidth'] is None:
        width = 9
    else:
        width = arguments['--columnwidth']

    binary = arguments['<value>']

    first_line = binary[:2]

    rest = binary[2:]

    n = 3

    lines = [rest[i:i+n] for i in range(0, len(rest), n)]

    output = []

    for line in [first_line] + lines:
        output.append('\n')
        for bit in line:
            output.append(' '*(width-len(low))+low)
            if int(bit) == 1:
                output.append(' '*(width-len(high))+high)
            else:
                output.append(' '*(width-len(low))+low)

    print ''.join(output)


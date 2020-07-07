# The argparse is a recommended command-line parsing module in the Python standard library.
# All materials here are from https://docs.python.org/3/howto/argparse.html


import argparse


'''
Script arg_parse.py accepts positional and optional command-line arguments and print a result to screen.

Examples:

>>> python arg_parse.py 4
16

>>> python arg_parse.py 4 -v
4^2 == 16

>>> python arg_parse.py 4 -vv
the square of 4 equals 16

>>> python arg_square.py -h
usage: arg_parse.py [-h] [-v] square

positional arguments:
  square           display a square of a given number

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity  increase output verbosity
  
'''

parser = argparse.ArgumentParser()

parser.add_argument('-v',
                    '--verbosity',
                    action='count',
                    default=0,
                    help='increase output verbosity',
                    )

parser.add_argument('square',
                    type=int,
                    help='display a square of a given number'
                    )

args = parser.parse_args()
answer = args.square ** 2

if args.verbosity >= 2:
    print('the square of {} equals {}'.format(args.square, answer))
elif args.verbosity >= 1:
    print('{}^2 == {}'.format(args.square, answer))
else:
    print(answer)

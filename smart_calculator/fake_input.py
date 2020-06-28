# Simulate user input

import io
import sys


input_str = '''1
a
x c v
/exit
'''

tmp = sys.stdin
sys.stdin = io.StringIO(input_str)

while True:
    input_str = input()
    if input_str == '/exit':
        break
    print(input_str)

sys.stdin = tmp

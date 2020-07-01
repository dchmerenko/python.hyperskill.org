from collections import deque

from test_case import test_case_run

import infix_to_posfix
import brackets
import lib


def calculate(expr):
    '''Calculate expression in infix_to_postfix notation
    Example:

        '''
    if brackets.bracket_check(expr):
        expr = infix_to_posfix.infix_to_postfix(expr)
    else:
        raise NameError('Invalid expression')

    s = deque()

    for c in expr.split():
        if lib.is_number(c):
            s.append(int(c))
        elif lib.is_operator(c):
            s.append(lib.evaluate(s.pop(), s.pop(), c))

    return s.pop()


if __name__ == '__main__':

    test_case = {
        '( 1 + 2 ) * 3': '9',
        '1 + 22': '23',
        '( 1 + 2 ) * ( 3 + 4 )': '21',
        '2 ^ ( ( 1 + 2 ) )': '8',
        '2 - 1': '1',
    }

    test_case_run(calculate, test_case)
